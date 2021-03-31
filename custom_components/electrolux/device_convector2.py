"""Convector2 class"""

import logging

from .device_base import Device
from .rusclimatapi import RusclimatApi
from .const import *

_LOGGER = logging.getLogger(__name__)


class Convector2(Device):

    def __init__(self, uid: str, api: RusclimatApi, data: dict = None):
        super().__init__(uid)

        self._api = api
        self._state = STATE_OFF
        self._child_lock = STATE_OFF
        self._sensor_fault = STATE_OFF
        self._window_open = STATE_OFF
        self._mute = STATE_OFF
        self._window_opened = STATE_OFF
        self._calendar_on = STATE_OFF
        self._brightness = BRIGHTNESS_MODE_FULL
        self._led_off_auto = LED_MODE_PERMANENT
        self._temp_comfort = TEMP_COMFORT_MIN
        self._delta_eco = DELTA_ECO_DEFAULT
        self._temp_antifrost = TEMP_ANTIFROST_DEFAULT
        self._mode = MODE_COMFORT
        self._mode_temp_1 = 0
        self._mode_temp_2 = 0
        self._mode_temp_3 = 0
        self._hours = 0
        self._minutes = 0
        self._timer = STATE_OFF
        self._current_temp = 0
        self._heat_mode = HEAT_MODE_AUTO
        self._power = POWER_0
        self._code = 0
        self._lcd_on = STATE_ON
        self._time_seconds = 0
        self._time_minutes = 0
        self._time_hour = 0
        self._time_day = 0
        self._time_month = 0
        self._time_year = 0
        self._time_weekday = 0
        self._preset_monday = PRESET_0
        self._preset_tuesday = PRESET_0
        self._preset_wednesday = PRESET_0
        self._preset_thursday = PRESET_0
        self._preset_friday = PRESET_0
        self._preset_saturday = PRESET_0
        self._preset_sunday = PRESET_0
        self._preset_day_1 = MODE_OFF
        self._preset_day_2 = MODE_OFF
        self._preset_day_3 = MODE_OFF
        self._preset_day_4 = MODE_OFF
        self._preset_day_5 = MODE_OFF
        self._preset_day_6 = MODE_OFF
        self._preset_day_7 = MODE_OFF
        self._preset_day_8 = MODE_OFF
        self._preset_day_9 = MODE_OFF
        self._preset_day_10 = MODE_OFF
        self._preset_day_11 = MODE_OFF
        self._preset_day_12 = MODE_OFF
        self._preset_day_13 = MODE_OFF
        self._preset_day_14 = MODE_OFF
        self._preset_day_15 = MODE_OFF
        self._preset_day_16 = MODE_OFF
        self._preset_day_17 = MODE_OFF
        self._preset_day_18 = MODE_OFF
        self._preset_day_19 = MODE_OFF
        self._preset_day_20 = MODE_OFF
        self._preset_day_21 = MODE_OFF
        self._preset_day_22 = MODE_OFF
        self._preset_day_23 = MODE_OFF
        self._preset_day_24 = MODE_OFF
        self._tempid = None
        self._mac = None
        self._room = None
        self._sort = 0
        self._type = TYPE_CONVECTOR_2
        self._curr_slot = None
        self._active_slot = None
        self._slop = None
        self._curr_scene = None
        self._curr_scene_id = None
        self._wait_slot = None
        self._curr_slot_dropped = 0
        self._curr_scene_dropped = 0
        self._online = STATE_OFF
        self._lock = STATE_OFF

        self._from_json(data)

    async def set_state(self, value):
        _LOGGER.debug(f"set_state: {value}")

        status = await self._api.set_state(self.uid, value)

        if status:
            await self.update()

    # todo
    async def set_child_lock(self, value):
        _LOGGER.debug(f"set_child_lock: {value}")

    # todo
    async def set_window_open(self, value):
        _LOGGER.debug(f"set_window_open: {value}")

    # todo
    async def set_mute(self, value):
        _LOGGER.debug(f"set_mute: {value}")

    # todo
    async def set_brightness(self, value):
        _LOGGER.debug(f"set_brightness: {value}")

    # todo
    async def set_led_off_auto(self, value):
        _LOGGER.debug(f"set_led_off_auto: {value}")

    # todo
    async def set_delta_eco(self, value):
        _LOGGER.debug(f"set_delta_eco: {value}")

    # todo
    async def set_temp_antifrost(self, value):
        _LOGGER.debug(f"set_temp_antifrost: {value}")

    # todo
    async def set_heat_mode(self, value):
        _LOGGER.debug(f"set_heat_mode: {value}")

    # todo
    async def set_power(self, value):
        _LOGGER.debug(f"set_power: {value}")

    # todo
    async def set_room(self, value):
        _LOGGER.debug(f"set_room: {value}")

    # todo
    async def set_lock(self, value):
        _LOGGER.debug(f"set_lock: {value}")

    async def set_mode(self, value):
        _LOGGER.debug(f"set_mode: {value}")

        status = await self._api.set_preset_mode(self.uid, value)

        if status:
            await self.update()

    async def set_temp_comfort(self, value):
        _LOGGER.debug(f"set_temp_comfort: {value}")

        status = await self._api.set_temperature(self.uid, value)

        if status:
            await self.update()

    @property
    def state(self) -> int:
        return int(self._state)

    @property
    def child_lock(self) -> int:
        return int(self._child_lock)

    @property
    def window_open(self) -> int:
        return int(self._window_open)

    @property
    def window_opened(self) -> int:
        return int(self._window_opened)

    @property
    def mute(self) -> int:
        return int(self._mute)

    @property
    def calendar_on(self) -> int:
        return int(self._calendar_on)

    @property
    def brightness(self) -> int:
        return int(self._brightness)

    @property
    def led_off_auto(self) -> int:
        return int(self._led_off_auto)

    @property
    def current_temp(self) -> float:
        return float(self._current_temp)

    @property
    def mode(self) -> int:
        return int(self._mode)

    @property
    def temp_comfort(self) -> float:
        return float(self._temp_comfort)

    @property
    def delta_eco(self) -> int:
        return int(self._delta_eco)

    @property
    def temp_antifrost(self) -> int:
        return int(self._temp_antifrost)

    @property
    def hours(self) -> int:
        return int(self._hours)

    @property
    def minutes(self) -> int:
        return int(self._minutes)

    @property
    def timer(self) -> int:
        return int(self._timer)

    @property
    def heat_mode(self) -> int:
        return int(self._heat_mode)

    @property
    def power(self) -> int:
        return int(self._power)

    @property
    def time_seconds(self) -> int:
        return int(self._time_seconds)

    @property
    def time_minutes(self) -> int:
        return int(self._time_minutes)

    @property
    def time_hour(self) -> int:
        return int(self._time_hour)

    @property
    def time_day(self) -> int:
        return int(self._time_day)

    @property
    def time_month(self) -> int:
        return int(self._time_month)

    @property
    def time_year(self) -> int:
        return int(self._time_year)

    @property
    def time_weekday(self) -> int:
        return int(self._time_weekday)

    @property
    def code(self) -> int:
        return int(self._code)

    @property
    def curr_scene_dropped(self) -> int:
        return int(self._curr_scene_dropped)

    @property
    def curr_slot_dropped(self) -> int:
        return int(self._curr_slot_dropped)

    @property
    def curr_scene(self) -> str:
        return self._curr_scene

    @property
    def curr_slot(self) -> int:
        return int(self._curr_slot)

    @property
    def mac(self) -> str:
        return self._mac

    @property
    def online(self) -> int:
        return int(self._online)

    @property
    def sort(self) -> int:
        return int(self._sort)

    @property
    def lock(self) -> int:
        return int(self._lock)

    async def update(self):
        for device in await self._api.get_device_params(self.uid):
            if device["uid"] == self.uid:
                self._from_json(device)

    def _from_json(self, data: dict):
        """Fill self from json data"""
        for key in data:
            setattr(self, f"_{key}", data[key])

