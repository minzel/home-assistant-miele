"""
Support for Miele Devices.
"""

from custom_components.miele import DOMAIN as DOMAIN, MieleEntity, DEVICES, API

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Miele device platform."""

    def get_sensors():
        devices = hass.data[DOMAIN][DEVICES]
        return [
            MieleSensor(device, prop, value, hass)
            for device in devices
                for prop, value in device.state
                if not isinstance(value, bool)
        ]

    async_add_entities(await hass.async_add_executor_job(get_sensors), True)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Old way of setting up platform.
    Can only be called when a user accidentally mentions the platform in their
    config. But even in that case it would have been ignored.
    """
    pass

class MieleSensor(MieleEntity):

    def __init__(self, device, prop, value, hass):
        api = hass.data[DOMAIN][API]
        super().__init__(device, prop, value, api, hass)

    async def async_update(self):
        await super().async_update()