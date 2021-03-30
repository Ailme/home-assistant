"""Adds Support for Electrolux Convector"""
import asyncio
import logging

from aiohttp import ClientSession

from .const import API_LOGIN, API_SET_DEVICE_PARAMS, LANG

_LOGGER = logging.getLogger(__name__)


class RusclimatApi:
    """ Wrapper class to the Rusclimat API """

    def __init__(self, host: str, username: str, password: str, appcode: str):
        self._host = host
        self._username = username
        self._password = password
        self._appcode = appcode
        self._token = None
        self._data = {}
        self.session = None

    def __del__(self):
        _LOGGER.debug('Destructor called.')
        self.session.close()

    def create_session(self):
        self.session = ClientSession()

    async def request(self, url: str, payload: dict):
        if self.session is None or self.session.closed:
            self.create_session()

        headers = {
            "lang": LANG,
            "Content-Type": "application/json; charset=UTF-8",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.3.1",
        }

        resp = await self.session.post(f"{self._host}/{url}", json=payload, headers=headers)
        json = await resp.json()

        _LOGGER.debug(json)

        if json is None:
            _LOGGER.error(f"Request error: json is None")
            return {}

        return json

    async def login(self):
        """Login"""

        payload = {
            "login": self._username,
            "password": self._password,
            "appcode": self._appcode
        }

        json = await self.request(API_LOGIN, payload)

        self._token = json["result"]["token"]
        self._data = json["result"]["device"]

        return json

    async def update_device_params(self, params: dict):
        if self._token is None:
            await self.login()

        payload = {
            "token": self._token,
            "device": [params]
        }

        json = await self.request(API_SET_DEVICE_PARAMS, payload)

        return json

    async def set_preset_mode(self, uid: str, mode: int) -> bool:
        payload = {
            "uid": uid,
            "params": {
                "mode": mode
            }
        }

        json = await self.update_device_params(payload)

        return json["result"] == "1"

    async def set_temperature(self, uid: str, temp: int) -> bool:
        payload = {
            "uid": uid,
            "params": {
                "temp_comfort": temp
            }
        }

        json = await self.update_device_params(payload)

        return self._check_result(json)

    async def set_state(self, uid: str, state: int) -> bool:
        payload = {
            "uid": uid,
            "params": {
                "state": state
            }
        }

        json = await self.update_device_params(payload)

        return self._check_result(json)

    @staticmethod
    def _check_result(json) -> bool:
        return json["result"] == "1"
