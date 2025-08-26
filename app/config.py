import os
from zoneinfo import ZoneInfo

APP_API_KEY = os.getenv("API_KEY", "change_me")

MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))
MQTT_USER = os.getenv("MQTT_USERNAME")
MQTT_PASS = os.getenv("MQTT_PASSWORD")
MQTT_TLS = os.getenv("MQTT_TLS", "true").lower() == "true"

TOPIC = os.getenv("PRINT_TOPIC", "print/tickets")
PUBLISH_QOS = int(os.getenv("PRINT_QOS", "2"))

UI_PASS = os.getenv("UI_PASS", "set_me")
COOKIE_NAME = "ui_token"
UI_REMEMBER_DAYS = int(os.getenv("UI_REMEMBER_DAYS", "30"))
TZ = ZoneInfo(os.getenv("TIMEZONE", "Europe/Zurich"))

PRINT_WIDTH_PX = int(os.getenv("PRINT_WIDTH_PX", "576"))

FONT_TITLE = os.getenv("FONT_FILE_TITLE", "ttf/DejaVuSans-Bold.ttf")
FONT_BODY = os.getenv("FONT_FILE_BODY", "ttf/DejaVuSans.ttf")
SIZE_TITLE = int(os.getenv("FONT_SIZE_TITLE", "32"))
SIZE_BODY = int(os.getenv("FONT_SIZE_BODY", "28"))

MARGIN_X = int(os.getenv("MARGIN_X", "20"))
MARGIN_Y = int(os.getenv("MARGIN_Y", "20"))
EXTRA_BOTTOM = int(os.getenv("EXTRA_BOTTOM", "30"))

