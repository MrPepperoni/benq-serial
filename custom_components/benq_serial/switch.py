"""Switch platform for Benq Serial."""
import logging
from homeassistant.components.switch import SwitchEntity

from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import ICON
from .const import SWITCH
from .entity import BenqSerialEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([BenqSerialBinarySwitch(coordinator, entry, 'pow')])


class BenqSerialBinarySwitch(BenqSerialEntity, SwitchEntity):
    """benq_serial switch class."""

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        await self.coordinator.api.async_set_data(self._key, "on")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        await self.coordinator.api.async_set_data(self._key, "off")
        await self.coordinator.async_request_refresh()

    @property
    def name(self):
        """Return the name of the switch."""
        return f"{DEFAULT_NAME}_{self._key}_{SWITCH}"

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self.coordinator.data.get(self._key, "") in ["on", True, 1]
