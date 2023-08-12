"""Binary sensor platform for Benq Serial."""
from homeassistant.components.binary_sensor import (BinarySensorEntity,
                                                    BinarySensorDeviceClass)

from .const import BINARY_SENSOR
from .const import DEFAULT_NAME
from .const import DOMAIN
from .entity import BenqSerialEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    # async_add_devices([BenqSerialBinarySensor(coordinator, entry, 'pow')])


class BenqSerialBinarySensor(BenqSerialEntity, BinarySensorEntity):
    """benq_serial binary_sensor class."""

    @property
    def name(self):
        """Return the name of the binary_sensor."""
        return f"{DEFAULT_NAME}_{self._key}_{BINARY_SENSOR}"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return BinarySensorDeviceClass.POWER

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return self.coordinator.data.get(self._key, "") in ["on", True, 1]
