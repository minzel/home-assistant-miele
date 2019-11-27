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
CONF_OBJECT_ID_PREFIX = 'id_prefix'

DEFAULT_OBJECT_ID_PREFIX = 'miele'

MIELE_CONFIG = 'miele_cfg'

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_CLIENT_ID): cv.string,
                vol.Required(CONF_CLIENT_SECRET): cv.string,
                vol.Optional(CONF_OBJECT_ID_PREFIX, default=DEFAULT_OBJECT_ID_PREFIX): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

MIELE_COMPONENTS = ["sensor"]

async def async_setup(hass, config):
    hass.data[DOMAIN] = {}
    hass.data[MIELE_CONFIG] = config.get(DOMAIN, {})

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
    return True

async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
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
    
    # create sensors
    for component in MIELE_COMPONENTS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True

async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry):
    hass.data[DOMAIN].pop(API, None)

    await asyncio.gather(
        *[
            hass.config_entries.async_forward_entry_unload(entry, component)
            for component in MIELE_COMPONENTS
        ]
    )
    return True

@Throttle(SCAN_INTERVAL)
async def update_all_devices(hass):
    """Update all the devices."""
    try:
        data = hass.data[DOMAIN]
        data[DEVICES] = await hass.async_add_executor_job(data[API].get_devices)
    except HTTPError as err:
        _LOGGER.warning("Cannot update devices: %s", err.response.status_code)

class MieleEntity(Entity):
    def __init__(self, device, miele_api, hass):
        self.device = device
        self.api = miele_api

        config = hass.data[MIELE_CONFIG]

        prefix = config.get(CONF_OBJECT_ID_PREFIX)
        self.unqiue_id = prefix + "_" + self.device.getType() + "_" + self.device.getId()

    @property
    def unique_id(self):
        return self.unqiue_id

    @property
    def name(self):
        return self.device.getName()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": self.name,
            "model": self.device.ident.deviceIdentLabel.techType,
            "manufacturer": "Miele"
        }

    @property
    def device_state_attributes(self):
        attrs = {
            'model': self.device.ident.deviceIdentLabel.techType,
            'serial_number': self.device.getId(),
            'gateway_type': self.device.ident.xkmIdentLabel.techType,
            'gateway_version' : self.device.ident.xkmIdentLabel.releaseVersion
        }

        for key, value in self.device.state:
            attrs[key] = value

        return attrs

    async def async_update(self):
        await update_all_devices(self.hass)
        devices = self.hass.data[DOMAIN][DEVICES]
        self.device = next((d for d in devices if d.getId() == self.device.getId()), self.device)

class MieleDevice:
    def __init__(self, device, api):
        self.device = device
        self.api = api
