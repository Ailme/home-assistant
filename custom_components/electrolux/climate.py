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

from .rusclimatapi import RusclimatApi

import homeassistant.helpers.config_validation as cv

from homeassistant.helpers.reload import async_setup_reload_service
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.components.climate import ClimateEntity, PLATFORM_SCHEMA
from homeassistant.components.climate.const import (
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_PRESET_MODE,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE,
    PRESET_COMFORT,
    PRESET_SLEEP,
    PRESET_ECO,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_TEMPERATURE,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_NAME,
    TEMP_CELSIUS,
)

from .const import (
    DOMAIN,
    APPCODE_ELECTROLUX,
    HOST_RUSKLIMAT,
    DEFAULT_NAME,
    DEFAULT_MIN_TEMP,
    DEFAULT_MAX_TEMP
)

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})

SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE

HA_PRESET_TO_CONVECTOR = {PRESET_COMFORT: 0, PRESET_SLEEP: 1, PRESET_ECO: 2}
CONVECTOR_PRESET_TO_HA = {v: k for k, v in HA_PRESET_TO_CONVECTOR.items()}

# async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
#     _LOGGER.info(config)
#
#     session = async_get_clientsession(hass)
#     api = RusclimatApi(session, HOST_RUSKLIMAT)
#
#     await async_setup_reload_service(hass, DOMAIN, 'climate')
#     async_add_entities([Convector(api)])
#
#     return True


async def async_setup_entry(hass, config_entry, async_add_devices):
    _LOGGER.debug("async_setup_entry.climate")

    if config_entry.options != {}:
        result = config_entry.options
    else:
        result = config_entry.data
    _LOGGER.info("setup entity-config_entry_data=%s", result)

    session = async_get_clientsession(hass)
    api = RusclimatApi(session, HOST_RUSKLIMAT)

    await async_setup_reload_service(hass, DOMAIN, 'climate')
    async_add_devices([Convector(api)])


class Convector(ClimateEntity):
    """Representation of an Climate."""

    def __init__(self, api):
        """Initialize"""
        self._api = api
        self._icon = "mdi:radiator"
        self._name = DEFAULT_NAME
        self._min_temp = DEFAULT_MIN_TEMP
        self._max_temp = DEFAULT_MAX_TEMP
        self._current_temp = None
        self._current_setpoint = None
        self._paired = False
        self._heating = False
        self._preset = None
        self._current_state = -1
        self._current_operation = ""

    def update(self):
        """Update unit attributes."""

        # self.data.update()
        # self._current_setpoint = self.data.current_setpoint
        # self._current_operation = self.data.current_operation
        # self._current_temp = self.data.current_temp
        # self._preset = CONVECTOR_PRESET_TO_HA.get(self.data.preset)
        # self._heating = self.data.heating

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

    def set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        pass

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
        return self._name

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
        return CONVECTOR_PRESET_TO_HA.get(self._api.preset)

    @property
    def preset_modes(self):
        """Return a list of available preset modes."""
        return [PRESET_COMFORT, PRESET_SLEEP, PRESET_ECO]

    def set_preset_mode(self, preset_mode):
        """Set a new preset mode. If preset_mode is None, then revert to auto."""

        if self._preset == preset_mode:
            return

        convector_preset = HA_PRESET_TO_CONVECTOR.get(preset_mode, PRESET_COMFORT)
        status = self._api.set_preset_mode(convector_preset)
        if status == 2:
            self._preset = preset_mode
            return

        _LOGGER.error("Request Status: %s", status)

    def set_temperature(self, **kwargs):
        """Set new target temperature."""

        target_temp = kwargs.get(ATTR_TEMPERATURE)
        if target_temp is None:
            return
        else:
            status = self._api.set_temperature(target_temp)
            if status != 2:
                _LOGGER.error("Request Status: %s", status)

            self.update()
