"""Adds Support for Electrolux Convector"""

import logging
from aiohttp import ClientSession

from homeassistant import exceptions
from .const import API_LOGIN, LANG

_LOGGER = logging.getLogger(__name__)


class RusclimatApi:
    """ Wrapper class to the Rusclimat API """

    _key = None
    _token = None
    _server = None

    def __init__(self, session: ClientSession, host):
        self.session = session
        self.baseUrl = host

    async def login(self, username: str, password: str, appcode: str) -> bool:
        """Login"""
        _LOGGER.debug("login")

        payload = {
            "login": username,
            "password": password,
            "appcode": appcode
        }

        headers = {
            "lang": LANG,
            "tcp": "y",
            "debug": "new'",
            "Content-Type": "application/json; charset=UTF-8",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.3.1",
        }

        try:
            resp = await self.session.post(f"{self.baseUrl}/{API_LOGIN}", json=payload, headers=headers)
            json = await resp.json()
        except (Exception, RuntimeError) as e:
            _LOGGER.exception(f"Login error: {e}")
            return False

        _LOGGER.debug(json)

        if json is None:
            _LOGGER.error(f"Login error: {json}")
            return False

        if json["error_code"] != "0":
            _LOGGER.error(f"Login error: {json['error_message']}")
            return False

        self._key = json["result"]['enc_key']
        self._token = json["result"]["token"]
        self._server = json["result"]["server"]

        _LOGGER.debug(json["result"])

        return json

    async def _connect(self, fails: int = 0):
        """Permanent connection loop to Cloud Servers."""

    def update(self):
        """Get unit attributes."""

        return 1

    @property
    def preset(self):
        return 0


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""
