"""
Support for Miele Devices.
"""

from homeassistant.components.cover import CoverDevice

from custom_components.miele import DOMAIN as DOMAIN, MieleEntity, DEVICES, API

from .base import MieleDevice

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Miele device platform."""

    def get_covers():
        devices = hass.data[DOMAIN][DEVICES]
        return [
            MieleCover(cover, hass.data[DOMAIN][API])
            for cover in devices
        ]

    async_add_entities(await hass.async_add_executor_job(get_covers), True)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Old way of setting up platform.
    Can only be called when a user accidentally mentions the platform in their
    config. But even in that case it would have been ignored.
    """
    pass


class MieleCover(MieleEntity, CoverDevice):
    """Representation of a Miele cover device."""

    def __init__(self, device, api):
        """Initialize the Miele device."""
        super().__init__(device, api)
        self.cover = MieleDevice(self.device, self.api)
 
    async def async_update(self):
        """Update the device with the latest data."""
        await super().async_update()
        self.cover = MieleDevice(self.device, self.api)