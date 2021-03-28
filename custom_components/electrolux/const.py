"""Constants for the Electrolux integration."""

DOMAIN = "electrolux"

APPCODE_ELECTROLUX = "electrolux"
HOST_RUSKLIMAT = "http://dongle.rusklimat.ru"
LANG = "ru"

DEFAULT_NAME = "Electrolux Convector"
DEFAULT_MIN_TEMP = 4
DEFAULT_MAX_TEMP = 27

PLATFORMS = ["climate"]

API_CHANGE_PASSWORD = "api/userChangePassword"
API_CREATE_CALENDAR = "api/setTimeSlot"
API_DELETE_DEVICE = "api/deleteDevice"
API_DELETE_DEVICE_BY_TEMP_ID = "api/deleteDeviceByTempID"
API_LOGIN = "api/userAuth"
API_REGISTRATION = "api/userRegister"
API_REMIND_PASSWORD = "api/userRemindPassword"
API_SEND_CODE = "api/userRegister"
API_UPDATE_CALENDAR_SLOTS = "api/setTimeSlot"
