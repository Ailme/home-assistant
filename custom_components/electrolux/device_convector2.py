"""Convector2 class"""

from .const import *


class Convector2:

    def __init__(self):
        self.state = STATE_OFF
        self.child_lock = STATE_OFF
        self.sensor_fault = STATE_OFF
        self.window_open = STATE_OFF
        self.mute = STATE_OFF
        self.window_opened = STATE_OFF
        self.calendar_on = STATE_OFF
        self.brightness = BRIGHTNESS_MODE_FULL
        self.led_off_auto = LED_MODE_AUTO
        self.temp_comfort = TEMP_COMFORT_MIN
        self.delta_eco = DELTA_ECO_DEFAULT
        self.temp_antifrost = TEMP_ANTIFROST_DEFAULT
        self.mode = MODE_COMFORT
        self.mode_temp_1 = 0
        self.mode_temp_2 = 0
        self.mode_temp_3 = 0
        self.hours = 0
        self.minutes = 0
        self.timer = STATE_OFF
        self.current_temp = 0
        self.heat_mode = HEAT_MODE_AUTO
        self.power = POWER_0
        self.code = 0
        self.lcd_on = STATE_ON
        self.time_seconds = 0
        self.time_minutes = 0
        self.time_hour = 0
        self.time_day = 0
        self.time_month = 0
        self.time_year = 0
        self.time_weekday = 0
        self.preset_monday = PRESET_0
        self.preset_tuesday = PRESET_0
        self.preset_wednesday = PRESET_0
        self.preset_thursday = PRESET_0
        self.preset_friday = PRESET_0
        self.preset_saturday = PRESET_0
        self.preset_sunday = PRESET_0
        self.preset_day_1 = MODE_OFF
        self.preset_day_2 = MODE_OFF
        self.preset_day_3 = MODE_OFF
        self.preset_day_4 = MODE_OFF
        self.preset_day_5 = MODE_OFF
        self.preset_day_6 = MODE_OFF
        self.preset_day_7 = MODE_OFF
        self.preset_day_8 = MODE_OFF
        self.preset_day_9 = MODE_OFF
        self.preset_day_10 = MODE_OFF
        self.preset_day_11 = MODE_OFF
        self.preset_day_12 = MODE_OFF
        self.preset_day_13 = MODE_OFF
        self.preset_day_14 = MODE_OFF
        self.preset_day_15 = MODE_OFF
        self.preset_day_16 = MODE_OFF
        self.preset_day_17 = MODE_OFF
        self.preset_day_18 = MODE_OFF
        self.preset_day_19 = MODE_OFF
        self.preset_day_20 = MODE_OFF
        self.preset_day_21 = MODE_OFF
        self.preset_day_22 = MODE_OFF
        self.preset_day_23 = MODE_OFF
        self.preset_day_24 = MODE_OFF
        self.tempid = None
        self.uid = None
        self.mac = None
        self.room = None
        self.sort = 0
        self.type = TYPE_CONVECTOR_2
        self.curr_slot = None
        self.active_slot = None
        self.slop = None
        self.curr_scene = None
        self.curr_scene_id = None
        self.wait_slot = None
        self.curr_slot_dropped = None
        self.curr_scene_dropped = None
        self.online = STATE_OFF
        self.lock = STATE_OFF

    def from_json(self, data: dict):
        """Fill self from json data"""
        for key in data:
            setattr(self, key, data[key])

    @property
    def state(self) -> int:
        return int(self._state)

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def current_temp(self) -> int:
        return int(self._current_temp)

    @current_temp.setter
    def current_temp(self, value):
        self._current_temp = value

    @property
    def mode(self) -> int:
        return int(self._mode)

    @mode.setter
    def mode(self, value):
        self._mode = value

    @property
    def temp_comfort(self) -> int:
        return int(self._temp_comfort)

    @temp_comfort.setter
    def temp_comfort(self, value):
        self._temp_comfort = value

    @property
    def delta_eco(self) -> int:
        return int(self._delta_eco)

    @delta_eco.setter
    def delta_eco(self, value):
        self._delta_eco = value

    @property
    def temp_antifrost(self) -> int:
        return int(self._temp_antifrost)

    @temp_antifrost.setter
    def temp_antifrost(self, value):
        self._temp_antifrost = value
