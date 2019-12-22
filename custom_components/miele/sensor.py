from custom_components.miele import DOMAIN as DOMAIN, MieleEntity, DEVICES, API

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

class MieleSensor(MieleEntity):

    @property
    def state(self):
        return self.sensor.state

    @property
    def unit_of_measurement(self):
        return self.sensor.unit_of_measurement

    @property
    def device_class(self):
        return self.sensor.device_class

    async def async_update(self):
        await super().async_update()
