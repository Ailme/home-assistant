"""Adds Support for Electrolux Convector"""

import logging

from datetime import datetime, timedelta
import voluptuous as vol
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from time import mktime, strptime
from http.client import HTTPException

from socket import AF_INET, SOCK_DGRAM, SO_REUSEADDR, SOL_SOCKET, socket, timeout

_LOGGER = logging.getLogger(__name__)


class RusclimatApi(object):
    """ Wrapper class to the Rusclimat API """

    def __init__(self, username, passwotd, host, appcode):
        self._username = username
        self._passwotd = passwotd
        self._host = host
        self._appcode = appcode

    def _send_request(self, request_path, json_payload):
        """Send the request to the server"""

        for i in range(3):
            try:
                req = Request(
                    self._host + request_path,
                    data=str.encode(json_payload),
                )
                with urlopen(req, timeout=60) as result:
                    resp = json.loads(result.read().decode("utf-8"))
                    return resp

            except HTTPError as http_err:
                if http_err.code == 404:
                    _LOGGER.info("Rusclimat not found: %s Trying to find...", self._host)
                else:
                    _LOGGER.error("Rusclimat api error")
                    continue
            except HTTPException as http_ex:
                _LOGGER.info("Rusclimat disconnected %s", str(http_ex))
            except URLError as url_ex:
                _LOGGER.info("Rusclimat timeout %s", str(url_ex))
            except ConnectionResetError as cr_ex:
                _LOGGER.info("Rusclimat connection reset %s", str(cr_ex))
            except ConnectionAbortedError as ca_ex:
                _LOGGER.info("Rusclimat connection abort %s", str(ca_ex))

        return None

    def update(self):
        """Get unit attributes."""

        return 1

    @property
    def preset(self):
        return 0
