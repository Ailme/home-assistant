"""
Adds Support for Electrolux Convector

Configuration for this platform:
climate:
  - platform: electrolux
    name: Electrolux Convector
    username: phone
    password: 123456
"""

import logging
import voluptuous as vol

from .device_convector2 import Convector2
from .rusclimatapi import RusclimatApi

import homeassistant.helpers.config_validation as cv

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from homeassistant.components.climate import ClimateEntity, PLATFORM_SCHEMA
from homeassistant.components.climate.const import (
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_PRESET_MODE,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE,
    PRESET_COMFORT,
    PRESET_ECO,
)
from homeassistant.const import (
    ATTR_TEMPERATURE,
    CONF_USERNAME,
    CONF_PASSWORD,
    TEMP_CELSIUS,
)

from .const import (
    DEFAULT_MIN_TEMP,
    DEFAULT_MAX_TEMP,
    TYPE_CONVECTOR_2,
    MODE_COMFORT,
    MODE_NO_FROST,
    MODE_ECO,
    STATE_ON,
    STATE_OFF
)

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})

SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE

PRESET_NO_FROST = "no_frost"

HA_PRESET_TO_CONVECTOR = {PRESET_COMFORT: MODE_COMFORT, PRESET_ECO: MODE_ECO, PRESET_NO_FROST: MODE_NO_FROST}
CONVECTOR_PRESET_TO_HA = {v: k for k, v in HA_PRESET_TO_CONVECTOR.items()}


async def async_setup_platform(hass: HomeAssistant, config: dict, async_add_entities, discovery_info=None):
    _LOGGER.debug("climate.async_setup_platform")
    _LOGGER.debug("climate.async_setup_platform.config")
    _LOGGER.debug(config)

    # session = async_get_clientsession(hass)
    # api = RusclimatApi(session, HOST_RUSKLIMAT)
    #
    # await async_setup_reload_service(hass, DOMAIN, 'climate')
    # async_add_entities([Convector(api)])

    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_devices):
    if config_entry.options != {}:
        data = config_entry.options
    else:
        data = config_entry.data
    _LOGGER.info("setup entity-config_entry_data=%s", data)

    api = RusclimatApi(data["host"], data["username"], data["password"], data["appcode"])
    json = await api.login()

    devices = []
    for device in json["result"]["device"]:
        print(device)

        if device["type"] == TYPE_CONVECTOR_2:
            entity = Convector2Climate(device["uid"], api, device)
            entity.update()
            devices.append(entity)

    async_add_devices(devices)


class Convector2Climate(ClimateEntity):
    """Representation of an Climate."""

    def __init__(self, uid: str, api: RusclimatApi, data: dict = None):
        """Initialize"""
        self._api = api

        self._icon = "mdi:radiator"
        self._name = "convector_" + uid
        self._uid = uid
        self._min_temp = DEFAULT_MIN_TEMP
        self._max_temp = DEFAULT_MAX_TEMP
        self._current_temp = None
        self._current_setpoint = None
        self._paired = False
        self._heating = False
        self._preset = None
        self._current_state = -1
        self._current_operation = ""

        self.update_from_json(data)

    def update(self):
        """Update unit attributes."""
        # self._api.update()
        # self.data.update()
        # self._current_setpoint = self.data.current_setpoint
        # self._current_operation = self.data.current_operation
        # self._current_temp = self.data.current_temp
        # self._preset = CONVECTOR_PRESET_TO_HA.get(self.data.preset)
        # self._heating = self.data.heating

    def update_from_json(self, data: dict):
        """Update unit attributes."""
        device = Convector2()
        device.from_json(data)

        self._current_temp = device.temp_comfort
        self._heating = device.state

        if device.mode == MODE_COMFORT:
            self._target_temperature = device.temp_comfort
        elif device.mode == MODE_ECO:
            self._target_temperature = device.temp_comfort - device.delta_eco
        elif device.mode == MODE_NO_FROST:
            self._target_temperature = device.temp_antifrost
        else:
            self._target_temperature = 0

    @staticmethod
    def _get_float(value, default=None):
        if value is not None:
            return float(value)
        return default

    @property
    def hvac_mode(self):
        """Return hvac operation """
        if self._heating:
            return HVAC_MODE_HEAT
        return HVAC_MODE_OFF

    @property
    def hvac_modes(self):
        """Return the list of available hvac operation modes. Need to be a subset of HVAC_MODES. """
        return [HVAC_MODE_HEAT]

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""

        status = await self._api.set_state(self._uid, STATE_OFF if self._heating else STATE_ON)

        if status:
            self._heating = not self._heating

    @property
    def hvac_action(self):
        """Return the current running hvac operation if supported.  Need to be one of CURRENT_HVAC_*.  """
        if self._heating:
            return CURRENT_HVAC_HEAT
        return CURRENT_HVAC_IDLE

    @property
    def name(self):
        """Return the name of the climate device."""
        return self._name

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def unique_id(self):
        """Return the unique ID of the binary sensor."""
        return self._uid

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._current_temp

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        if self._min_temp:
            return self._min_temp

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        if self._max_temp:
            return self._max_temp

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._current_setpoint

    @property
    def preset_mode(self):
        """Return the current preset mode, e.g., home, away, temp."""
        return CONVECTOR_PRESET_TO_HA.get(self._preset)

    @property
    def preset_modes(self):
        """Return a list of available preset modes."""
        return [PRESET_COMFORT, PRESET_ECO, PRESET_NO_FROST]

    async def async_set_preset_mode(self, preset_mode):
        """Set a new preset mode. If preset_mode is None, then revert to auto."""

        if self._preset == preset_mode:
            return

        convector_preset = HA_PRESET_TO_CONVECTOR.get(preset_mode, PRESET_COMFORT)
        status = await self._api.set_preset_mode(self._uid, convector_preset)

        if status:
            self._preset = preset_mode

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""

        target_temp = kwargs.get(ATTR_TEMPERATURE)
        if target_temp is None:
            return
        else:
            status = await self._api.set_temperature(self._uid, target_temp)

        if status:
            self._target_temperature = target_temp

    @property
    def precision(self):
        return 0
