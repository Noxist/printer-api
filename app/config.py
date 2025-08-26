import os
from zoneinfo import ZoneInfo

def getenv_prefer(old_key: str, new_key: str, default=None):
    # Versucht erst alte Variablenname, sonst neuen
    value = os.getenv(old_key)
    if value is None:
        value = os.getenv(new_key, default)
    return value

APP_API_KEY = getenv_prefer("API_KEY", "API_KEY", "change_me")

MQTT_HOST = getenv_prefer("MQTT_HOST", "MQTT_HOST")
MQTT_PORT = int(getenv_prefer("MQTT_PORT", "MQTT_PORT", "8883"))
MQTT_USER = getenv_prefer("MQTT_USERNAME", "MQTT_USER")
MQTT_PASS = getenv_prefer("MQTT_PASSWORD", "MQTT_PASS")
MQTT_TLS = getenv_prefer("MQTT_TLS", "MQTT_TLS", "true").lower() == "true"

TOPIC = getenv_prefer("PRINT_TOPIC", "PRINT_TOPIC", "print/tickets")
PUBLISH_QOS = int(getenv_prefer("PRINT_QOS", "PUBLISH_QOS", "2"))

UI_PASS = getenv_prefer("UI_PASS", "UI_PASS", "set_me")
COOKIE_NAME = "ui_token"
UI_REMEMBER_DAYS = int(getenv_prefer("UI_REMEMBER_DAYS", "UI_REMEMBER_DAYS", "30"))
TZ = ZoneInfo(os.getenv("TIMEZONE", "Europe/Zurich"))

PRINT_WIDTH_PX = int(getenv_prefer("PRINT_WIDTH_PX", "PRINT_WIDTH_PX", "576"))
FONT_TITLE = getenv_prefer("FONT_FILE_TITLE", "FONT_FILE_TITLE", "ttf/DejaVuSans-Bold.ttf")
FONT_BODY = getenv_prefer("FONT_FILE_BODY", "FONT_FILE_BODY", "ttf/DejaVuSans.ttf")
SIZE_TITLE = int(getenv_prefer("FONT_SIZE_TITLE", "FONT_SIZE_TITLE", "32"))
SIZE_BODY = int(getenv_prefer("FONT_SIZE_BODY", "FONT_SIZE_BODY", "28"))
MARGIN_X = int(getenv_prefer("MARGIN_X", "MARGIN_X", "20"))
MARGIN_Y = int(getenv_prefer("MARGIN_Y", "MARGIN_Y", "20"))
EXTRA_BOTTOM = int(getenv_prefer("EXTRA_BOTTOM", "EXTRA_BOTTOM", "30"))
