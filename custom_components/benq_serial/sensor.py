"""Sensor platform for Benq Serial."""
from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import ICON
from .const import SENSOR
from .entity import BenqSerialEntity
from homeassistant.components.sensor.const import SensorDeviceClass
from homeassistant.const import UnitOfTemperature


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([
        BenqSerialTemperatureSensor(coordinator, entry, 'tmp1'),
        BenqSerialIntSensor(coordinator, entry, 'fan1'),
        BenqSerialIntSensor(coordinator, entry, 'fan2'),
        BenqSerialIntSensor(coordinator, entry, 'fan3'),
    ])


class BenqSerialIntSensor(BenqSerialEntity):
    """benq_serial Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self._key}_{SENSOR}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._key, '')

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:fan"

    @property
    def device_class(self):
        """Return de device class of the sensor."""
        return "benq_serial__custom_device_class"


class BenqSerialTemperatureSensor(BenqSerialEntity):
    """benq_serial Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self._key}_{SENSOR}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._key, '') / 10

    @property
    def native_unit_of_measurement(self):
        return UnitOfTemperature.CELSIUS

    @property
    def device_class(self):
        """Return de device class of the sensor."""
        return SensorDeviceClass.TEMPERATURE


class BenqSerialBinSensor(BenqSerialEntity):
    """benq_serial Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self._key}_{SENSOR}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._key, '') == 'on'

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def device_class(self):
        """Return de device class of the sensor."""
        return "benq_serial__custom_device_class"
