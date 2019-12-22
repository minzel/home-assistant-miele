from custom_components.miele import DOMAIN as DOMAIN, MieleDevice, DEVICES, API

async def async_setup_entry(hass, config_entry, async_add_entities):

    def get_sensors():
        devices = hass.data[DOMAIN][DEVICES]
        return [
            MieleSensor(device, key, value, hass)
            for device in devices
                for key, value in device.state
                if not isinstance(value.state, bool)
        ]

    async_add_entities(await hass.async_add_executor_job(get_sensors), True)

class MieleSensor(MieleDevice):

    @property
    def state(self):
        return self.value.state

    @property
    def device_class(self):
        return self.value.device_class

    @property
    def unit_of_measurement(self):
        return self.value.unit_of_measurement

#    def __init__(self, device, prop, value, hass):
#        api = hass.data[DOMAIN][API]
#        super().__init__(device, prop, value, api, hass)

#    async def async_update(self):
#        await super().async_update()
