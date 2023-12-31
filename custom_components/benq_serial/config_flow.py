"""Adds config flow for Benq Serial."""
import voluptuous as vol
import logging
from homeassistant import config_entries
from homeassistant.core import callback

from .api import BenqSerialApiClient
from .const import CONF_PORT
from .const import CONF_HOSTNAME
from .const import DOMAIN
from .const import PLATFORMS


class BenqSerialFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for benq_serial."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            valid = await self._test_connection(
                user_input[CONF_HOSTNAME], user_input[CONF_PORT]
            )
            if valid:
                return self.async_create_entry(
                    title=user_input[CONF_HOSTNAME], data=user_input
                )
            else:
                self._errors["base"] = "auth"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return BenqSerialOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_HOSTNAME): str, vol.Required(CONF_PORT): int}
            ),
            errors=self._errors,
        )

    async def _test_connection(self, hostname, port):
        """Return true if credentials is valid."""
        try:
            api = BenqSerialApiClient(hostname, port, None)
            data = await api.async_get_data('pow')
            logging.getLogger(__package__).warn(f"data: {data}")
            return len(data) > 0
        except Exception:  # pylint: disable=broad-except
            pass
        return False


class BenqSerialOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for benq_serial."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_HOSTNAME), data=self.options
        )
