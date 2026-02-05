"""Restricted Media Player entity implementation."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.const import (
    ATTR_ENTITY_ID,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)

from .const import (
    CONF_ALLOWED_SOURCES,
    CONF_BASE_ENTITY,
    CONF_NAME,
    TECHNICIAN_MODE_SOURCE,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Restricted Media Player from a config entry."""
    base_entity_id = config_entry.data[CONF_BASE_ENTITY]
    allowed_sources = config_entry.data[CONF_ALLOWED_SOURCES]
    name = config_entry.data[CONF_NAME]

    async_add_entities(
        [RestrictedMediaPlayer(hass, config_entry, base_entity_id, allowed_sources, name)],
        True,
    )


class RestrictedMediaPlayer(MediaPlayerEntity):
    """Representation of a Restricted Media Player."""

    _attr_should_poll = False

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        base_entity_id: str,
        allowed_sources: list[str],
        name: str,
    ) -> None:
        """Initialize the Restricted Media Player."""
        self.hass = hass
        self._config_entry = config_entry
        self._base_entity_id = base_entity_id
        self._allowed_sources = allowed_sources
        self._attr_name = name
        self._attr_unique_id = f"{config_entry.entry_id}"

        # Generate entity_id based on name
        entity_id_suffix = name.lower().replace(" ", "_")
        self.entity_id = f"media_player.{entity_id_suffix}"

    @property
    def available(self) -> bool:
        """Return True if base entity is available."""
        state = self.hass.states.get(self._base_entity_id)
        if state is None:
            return False
        return state.state not in (STATE_UNAVAILABLE, STATE_UNKNOWN)

    @property
    def state(self) -> MediaPlayerState | None:
        """Return the state of the player."""
        state = self.hass.states.get(self._base_entity_id)
        if state is None:
            return None

        # Map string states to MediaPlayerState enum
        state_str = state.state
        try:
            return MediaPlayerState(state_str)
        except ValueError:
            # If state is not a valid MediaPlayerState, return as-is
            return state_str

    @property
    def source_list(self) -> list[str] | None:
        """Return the list of available sources."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None

        current_source = base_state.attributes.get("source")

        # If current source is not in allowed list, prepend Technician Mode
        if current_source and current_source not in self._allowed_sources:
            return [TECHNICIAN_MODE_SOURCE] + self._allowed_sources

        # Otherwise, just return allowed sources
        return self._allowed_sources

    @property
    def source(self) -> str | None:
        """Return the current input source."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None

        current_source = base_state.attributes.get("source")

        # If current source is not in allowed list, show Technician Mode
        if current_source and current_source not in self._allowed_sources:
            return TECHNICIAN_MODE_SOURCE

        return current_source

    @property
    def volume_level(self) -> float | None:
        """Volume level of the media player (0..1)."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("volume_level")

    @property
    def is_volume_muted(self) -> bool | None:
        """Boolean if volume is currently muted."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("is_volume_muted")

    @property
    def media_content_id(self) -> str | None:
        """Content ID of current playing media."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("media_content_id")

    @property
    def media_content_type(self) -> str | None:
        """Content type of current playing media."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("media_content_type")

    @property
    def media_duration(self) -> int | None:
        """Duration of current playing media in seconds."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("media_duration")

    @property
    def media_position(self) -> int | None:
        """Position of current playing media in seconds."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("media_position")

    @property
    def media_position_updated_at(self) -> Any:
        """When was the position of the current playing media valid."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("media_position_updated_at")

    @property
    def media_title(self) -> str | None:
        """Title of current playing media."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("media_title")

    @property
    def media_artist(self) -> str | None:
        """Artist of current playing media, music track only."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("media_artist")

    @property
    def media_album_name(self) -> str | None:
        """Album name of current playing media, music track only."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("media_album_name")

    @property
    def media_album_artist(self) -> str | None:
        """Album artist of current playing media, music track only."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("media_album_artist")

    @property
    def media_track(self) -> int | None:
        """Track number of current playing media, music track only."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("media_track")

    @property
    def media_series_title(self) -> str | None:
        """Title of series of current playing media, TV show only."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("media_series_title")

    @property
    def media_season(self) -> str | None:
        """Season of current playing media, TV show only."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("media_season")

    @property
    def media_episode(self) -> str | None:
        """Episode of current playing media, TV show only."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("media_episode")

    @property
    def media_channel(self) -> str | None:
        """Channel currently playing."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("media_channel")

    @property
    def media_playlist(self) -> str | None:
        """Title of Playlist currently playing."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("media_playlist")

    @property
    def app_id(self) -> str | None:
        """ID of the current running app."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("app_id")

    @property
    def app_name(self) -> str | None:
        """Name of the current running app."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return None
        return base_state.attributes.get("app_name")

    @property
    def supported_features(self) -> MediaPlayerEntityFeature:
        """Flag media player features that are supported."""
        base_state = self.hass.states.get(self._base_entity_id)
        if not base_state:
            return MediaPlayerEntityFeature(0)

        base_features = base_state.attributes.get("supported_features", 0)

        # Ensure SELECT_SOURCE is included if base supports it
        if base_features & MediaPlayerEntityFeature.SELECT_SOURCE:
            return MediaPlayerEntityFeature(base_features)

        return MediaPlayerEntityFeature(base_features)

    @property
    def device_info(self):
        """Return device info for this virtual wrapper entity."""
        return {
            "identifiers": {(self._config_entry.domain, self._config_entry.entry_id)},
            "name": self._attr_name,
            "manufacturer": "Restricted Media Player",
            "model": "Restricted Wrapper",
        }

    async def async_select_source(self, source: str) -> None:
        """Select input source."""
        if source == TECHNICIAN_MODE_SOURCE:
            # Technician Mode is informational only, don't do anything
            _LOGGER.debug(
                "Technician Mode selected on %s - this is informational only",
                self.entity_id,
            )
            return

        # Pass through to base entity
        await self.hass.services.async_call(
            "media_player",
            "select_source",
            {
                ATTR_ENTITY_ID: self._base_entity_id,
                "source": source,
            },
            blocking=True,
        )

    async def async_volume_up(self) -> None:
        """Volume up the media player."""
        await self.hass.services.async_call(
            "media_player",
            "volume_up",
            {ATTR_ENTITY_ID: self._base_entity_id},
            blocking=True,
        )

    async def async_volume_down(self) -> None:
        """Volume down the media player."""
        await self.hass.services.async_call(
            "media_player",
            "volume_down",
            {ATTR_ENTITY_ID: self._base_entity_id},
            blocking=True,
        )

    async def async_set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""
        await self.hass.services.async_call(
            "media_player",
            "volume_set",
            {
                ATTR_ENTITY_ID: self._base_entity_id,
                "volume_level": volume,
            },
            blocking=True,
        )

    async def async_mute_volume(self, mute: bool) -> None:
        """Mute the volume."""
        await self.hass.services.async_call(
            "media_player",
            "volume_mute",
            {
                ATTR_ENTITY_ID: self._base_entity_id,
                "is_volume_muted": mute,
            },
            blocking=True,
        )

    async def async_media_play(self) -> None:
        """Send play command."""
        await self.hass.services.async_call(
            "media_player",
            "media_play",
            {ATTR_ENTITY_ID: self._base_entity_id},
            blocking=True,
        )

    async def async_media_pause(self) -> None:
        """Send pause command."""
        await self.hass.services.async_call(
            "media_player",
            "media_pause",
            {ATTR_ENTITY_ID: self._base_entity_id},
            blocking=True,
        )

    async def async_media_stop(self) -> None:
        """Send stop command."""
        await self.hass.services.async_call(
            "media_player",
            "media_stop",
            {ATTR_ENTITY_ID: self._base_entity_id},
            blocking=True,
        )

    async def async_media_next_track(self) -> None:
        """Send next track command."""
        await self.hass.services.async_call(
            "media_player",
            "media_next_track",
            {ATTR_ENTITY_ID: self._base_entity_id},
            blocking=True,
        )

    async def async_media_previous_track(self) -> None:
        """Send previous track command."""
        await self.hass.services.async_call(
            "media_player",
            "media_previous_track",
            {ATTR_ENTITY_ID: self._base_entity_id},
            blocking=True,
        )

    async def async_media_seek(self, position: float) -> None:
        """Send seek command."""
        await self.hass.services.async_call(
            "media_player",
            "media_seek",
            {
                ATTR_ENTITY_ID: self._base_entity_id,
                "seek_position": position,
            },
            blocking=True,
        )

    async def async_play_media(
        self, media_type: str, media_id: str, **kwargs: Any
    ) -> None:
        """Play a piece of media."""
        await self.hass.services.async_call(
            "media_player",
            "play_media",
            {
                ATTR_ENTITY_ID: self._base_entity_id,
                "media_content_type": media_type,
                "media_content_id": media_id,
                **kwargs,
            },
            blocking=True,
        )

    async def async_turn_on(self) -> None:
        """Turn the media player on."""
        await self.hass.services.async_call(
            "media_player",
            "turn_on",
            {ATTR_ENTITY_ID: self._base_entity_id},
            blocking=True,
        )

    async def async_turn_off(self) -> None:
        """Turn the media player off."""
        await self.hass.services.async_call(
            "media_player",
            "turn_off",
            {ATTR_ENTITY_ID: self._base_entity_id},
            blocking=True,
        )

    async def async_toggle(self) -> None:
        """Toggle the media player."""
        await self.hass.services.async_call(
            "media_player",
            "toggle",
            {ATTR_ENTITY_ID: self._base_entity_id},
            blocking=True,
        )

    async def async_added_to_hass(self) -> None:
        """Register callbacks when entity is added."""
        # Track state changes of the base entity
        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                self._base_entity_id,
                self._async_base_entity_state_changed,
            )
        )

    @callback
    def _async_base_entity_state_changed(self, event) -> None:
        """Handle base entity state changes."""
        self.async_write_ha_state()
