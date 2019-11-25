"""
Support for Miele Devices.
"""

from custom_components.miele import DOMAIN as DOMAIN, MieleEntity, DEVICES, API

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Miele device platform."""

    def get_sensors():
        devices = hass.data[DOMAIN][DEVICES]
        return [
            MieleSensor(miele, hass.data[DOMAIN][API])
            for miele in devices
        ]

    async_add_entities(await hass.async_add_executor_job(get_sensors), True)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Old way of setting up platform.
    Can only be called when a user accidentally mentions the platform in their
    config. But even in that case it would have been ignored.
    """
    pass

class MieleDevice:
    __slots__ = "device", "api"

    def __init__(self, device, api):
        self.device = device
        self.api = api

class MieleSensor(MieleEntity):

    def __init__(self, device, api):
        super().__init__(device, api)
        self.miele = MieleDevice(self.device, self.api)
 
    @property
    def state(self):
        return self.device.state.status.value_localized

    async def async_update(self):
        await super().async_update()
        self.miele = MieleDevice(self.device, self.api)