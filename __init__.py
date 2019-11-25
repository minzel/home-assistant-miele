"""
Support for Miele@home
"""

import asyncio
import logging
from datetime import timedelta

import voluptuous as vol
from requests import HTTPError

from homeassistant.helpers import config_validation as cv, config_entry_oauth2_flow
from . import config_flow
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.util import Throttle
from .const import DOMAIN

from . import api
from . import miele_api

API = "api"

DEVICES = "devices"

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=60)

CONF_CLIENT_ID = "client_id"
CONF_CLIENT_SECRET = "client_secret"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_CLIENT_ID): cv.string,
                vol.Required(CONF_CLIENT_SECRET): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

MIELE_COMPONENTS = ["cover"]

async def async_setup(hass, config):
    print("async_setup :: begin")
    hass.data[DOMAIN] = {}

    if DOMAIN not in config:
        return True

    config_flow.MieleFlowHandler.async_register_implementation(
        hass,
        config_entry_oauth2_flow.LocalOAuth2Implementation(
            hass,
            DOMAIN,
            config[DOMAIN][CONF_CLIENT_ID],
            config[DOMAIN][CONF_CLIENT_SECRET],
            "https://api.mcs3.miele.com/thirdparty/login",
            "https://api.mcs3.miele.com/thirdparty/token",
        ),
    )
    print("async_setup :: end")
    return True

async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Set up Miele from a config entry."""
    print("update_all_devices :: begin")
    # Backwards compat
    if "auth_implementation" not in entry.data:
        hass.config_entries.async_update_entry(
            entry, data={**entry.data, "auth_implementation": DOMAIN}
        )

    implementation = await config_entry_oauth2_flow.async_get_config_entry_implementation(
        hass, entry
    )

    hass.data[DOMAIN][API] = api.ConfigEntryMieleApi(hass, entry, implementation)

    await update_all_devices(hass)

    for component in MIELE_COMPONENTS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )
    print("update_all_devices :: end")
    return True

async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Unload a config entry."""
    print("async_unload_entry :: begin")
    hass.data[DOMAIN].pop(API, None)

    await asyncio.gather(
        *[
            hass.config_entries.async_forward_entry_unload(entry, component)
            for component in MIELE_COMPONENTS
        ]
    )
    print("async_unload_entry  :: end")
    return True

class MieleEntity(Entity):
    """Representation of a generic Miele device."""

    def __init__(self, device, miele_api):
        """Initialize the Miele device."""
        self.device = device
        self.api = miele_api

    @property
    def unique_id(self):
        """Return the unique id base on the id returned by Miele."""
        return self.device.ident.deviceIdentLabel.fabNumber

    @property
    def name(self):
        """Return the name of the device."""
        return self.device.ident.type.value_localized

    @property
    def device_info(self):
        """Return device specific attributes.
        Implemented by platform classes.
        """
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self.name,
            "model": "TODO",
            # For the moment, Miele only returns their own device.
            "manufacturer": "Miele",
        }

    async def async_update(self):
        """Update the device with the latest data."""
        await update_all_devices(self.hass)
        devices = self.hass.data[DOMAIN][DEVICES]
        self.device = next((d for d in devices if d.ident.deviceIdentLabel.fabNumber == self.device.ident.deviceIdentLabel.fabNumber), self.device)

@Throttle(SCAN_INTERVAL)
async def update_all_devices(hass):
    """Update all the devices."""
    try:
        data = hass.data[DOMAIN]
        data[DEVICES] = await hass.async_add_executor_job(data[API].get_devices)
    except HTTPError as err:
        _LOGGER.warning("Cannot update devices: %s", err.response.status_code)