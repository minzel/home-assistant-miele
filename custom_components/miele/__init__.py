"""
Support for Miele@home
"""

import asyncio
import logging
from datetime import timedelta

import voluptuous as vol
from requests import HTTPError

from homeassistant.helpers import config_validation as cv, config_entry_oauth2_flow
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.util import Throttle

from . import api, miele_api, config_flow

from .const import (
    ATTR_STATUS,
    DOMAIN,
)

API = "api"

DEVICES = "devices"

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=60)

CONF_CLIENT_ID = "client_id"
CONF_CLIENT_SECRET = "client_secret"
CONF_LANGUAGE = "language"
CONF_OBJECT_PREFIX = 'prefix'

DEFAULT_LANGUAGE = 'en'
DEFAULT_OBJECT_PREFIX = 'miele'

MIELE_CONFIG = 'miele_cfg'

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_CLIENT_ID): cv.string,
                vol.Required(CONF_CLIENT_SECRET): cv.string,
                vol.Optional(CONF_LANGUAGE, default=DEFAULT_LANGUAGE): cv.string,
                vol.Optional(CONF_OBJECT_PREFIX, default=DEFAULT_OBJECT_PREFIX): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

MIELE_COMPONENTS = ["sensor", "binary_sensor"]

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

    hass.data[DOMAIN][API] = api.ConfigEntryMieleApi(
        hass, entry, implementation)

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
        config = hass.data[MIELE_CONFIG]
        data[DEVICES] = await hass.async_add_executor_job(data[API].get_devices, config.get(CONF_LANGUAGE))
    except HTTPError as err:
        _LOGGER.warning("Cannot update devices: %s", err.response.status_code)



class MieleEntity(Entity):

    def __init__(self, device, prop, sensor, hass):
        self._device = device
        self._prop = prop
        self._sensor = sensor
        self._hass = hass
        self._sensor_id = f"{self._device.type}_{self._device.id}"
        if(self._prop != ATTR_STATUS):
            self._sensor_id += f"_{self._prop}"

    @property
    def name(self):
        return self._sensor_id

    @property
    def unique_id(self):
        return self._sensor_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device.id)},
            "name": self._device.ident.type.value_localized,
            "model": self._device.ident.deviceIdentLabel.techType,
            "manufacturer": "Miele"
        }

    @property
    def device_state_attributes(self):
        return self._sensor.attributes;

    async def async_update(self):
        await update_all_devices(self._hass)
        devices = self._hass.data[DOMAIN][DEVICES]

        for device in devices:
            if device.id == self._device.id:
                self._device = device
                for k, v in device.state:
                    if k == self._prop:
                        self._sensor = v
                        break
