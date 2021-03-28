"""Adds Support for Electrolux Thermostat"""


class RusclimatApi(object):
    """ Wrapper class to the Rusclimat API """

    def __init__(self, username, passwotd, host, appcode):
        self._username = username
        self._passwotd = passwotd
        self._host = host
        self._appcode = appcode