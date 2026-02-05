"""Config flow for Restricted Media Player integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.media_player import DOMAIN as MEDIA_PLAYER_DOMAIN
from homeassistant.const import CONF_ENTITY_ID
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.helpers import entity_registry as er

from .const import (
    CONF_ALLOWED_SOURCES,
    CONF_BASE_ENTITY,
    CONF_NAME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class RestrictedMediaPlayerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Restricted Media Player."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._base_entity_id: str | None = None
        self._base_entity_name: str | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle the initial step - select base media player."""
        errors: dict[str, str] = {}

        if user_input is not None:
            self._base_entity_id = user_input[CONF_BASE_ENTITY]

            # Get the base entity to extract its name
            state = self.hass.states.get(self._base_entity_id)
            if state:
                self._base_entity_name = state.attributes.get("friendly_name", self._base_entity_id)
            else:
                self._base_entity_name = self._base_entity_id

            # Check if already configured
            await self.async_set_unique_id(self._base_entity_id)
            self._abort_if_unique_id_configured()

            return await self.async_step_sources()

        data_schema = vol.Schema(
            {
                vol.Required(CONF_BASE_ENTITY): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain=MEDIA_PLAYER_DOMAIN),
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_sources(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle the sources selection step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Merge the data from both steps
            data = {
                CONF_BASE_ENTITY: self._base_entity_id,
                CONF_ALLOWED_SOURCES: user_input[CONF_ALLOWED_SOURCES],
                CONF_NAME: user_input.get(CONF_NAME, f"Restricted {self._base_entity_name}"),
            }

            return self.async_create_entry(
                title=data[CONF_NAME],
                data=data,
            )

        # Get source list from base entity
        state = self.hass.states.get(self._base_entity_id)
        if not state:
            return self.async_abort(reason="cannot_connect")

        source_list = state.attributes.get("source_list", [])

        if not source_list:
            return self.async_abort(reason="no_sources")

        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_NAME,
                    default=f"Restricted {self._base_entity_name}",
                ): selector.TextSelector(),
                vol.Required(CONF_ALLOWED_SOURCES): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=source_list,
                        multiple=True,
                        mode=selector.SelectSelectorMode.LIST,
                    ),
                ),
            }
        )

        return self.async_show_form(
            step_id="sources",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "base_entity": self._base_entity_name,
            },
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Restricted Media Player."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Update the config entry with new allowed sources
            new_data = {**self.config_entry.data}
            new_data[CONF_ALLOWED_SOURCES] = user_input[CONF_ALLOWED_SOURCES]

            self.hass.config_entries.async_update_entry(
                self.config_entry,
                data=new_data,
            )

            return self.async_create_entry(title="", data={})

        # Get source list from base entity
        base_entity_id = self.config_entry.data[CONF_BASE_ENTITY]
        state = self.hass.states.get(base_entity_id)

        if not state:
            return self.async_abort(reason="cannot_connect")

        source_list = state.attributes.get("source_list", [])

        if not source_list:
            return self.async_abort(reason="no_sources")

        current_sources = self.config_entry.data.get(CONF_ALLOWED_SOURCES, [])

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_ALLOWED_SOURCES,
                    default=current_sources,
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=source_list,
                        multiple=True,
                        mode=selector.SelectSelectorMode.LIST,
                    ),
                ),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            errors=errors,
        )
