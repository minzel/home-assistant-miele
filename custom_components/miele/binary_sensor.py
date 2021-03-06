from homeassistant.components.binary_sensor import BinarySensorEntity
from custom_components.miele import DOMAIN, MieleEntity, DEVICES, API

async def async_setup_entry(hass, config_entry, async_add_entities):

    def get_sensors():
        devices = hass.data[DOMAIN][DEVICES]
        return [
            MieleBinarySensor(device, key, value, hass)
            for device in devices
                for key, value in device.state
                if isinstance(value.state, bool)
        ]

    async_add_entities(await hass.async_add_executor_job(get_sensors), True)

class MieleBinarySensor(MieleEntity, BinarySensorEntity):

    @property
    def state(self):
        return ("off", "on")[self._sensor.state]

    @property
    def unit_of_measurement(self):
        return self._sensor.unit_of_measurement

    @property
    def device_class(self):
        return self._sensor.device_class

    async def async_update(self):
        await super().async_update()