"""
API for Miele bound to HASS OAuth.
"""

from asyncio import run_coroutine_threadsafe
from typing import Dict, Union

from . import miele_api

from homeassistant import core, config_entries
from homeassistant.helpers import config_entry_oauth2_flow

class ConfigEntryMieleApi(miele_api.MieleApi):
    """Provide a Miele API tied into an OAuth2 based config entry."""

    def __init__(
        self,
        hass: core.HomeAssistant,
        config_entry: config_entries.ConfigEntry,
        implementation: config_entry_oauth2_flow.AbstractOAuth2Implementation,
    ):
        """Initialize the Config Entry Miele API."""
        self.hass = hass
        self.config_entry = config_entry
        self.session = config_entry_oauth2_flow.OAuth2Session(
            hass, config_entry, implementation
        )
        super().__init__(None, None, token=self.session.token)

    def refresh_tokens(self,) -> Dict[str, Union[str, int]]:
        """Refresh and return new Miele tokens using Home Assistant OAuth2 session."""
        run_coroutine_threadsafe(
            self.session.async_ensure_token_valid(), self.hass.loop
        ).result()

        return self.session.token
