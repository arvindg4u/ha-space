import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .const import CONF_SPACE_ID, DOMAIN, UPDATER_NAME

STEP_USER_DATA_SCHEMA = vol.Schema({vol.Required(CONF_SPACE_ID): str})

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    async def async_step_user(self, user_input=None) -> FlowResult:
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors={})
        space_id = user_input[CONF_SPACE_ID]
        if "/" not in space_id:
            return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors={"base": "invalid_space_id"})
        await self.async_set_unique_id(f"ha_space_updater_{space_id}")
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title=f"HA Space ({space_id})", data=user_input)
