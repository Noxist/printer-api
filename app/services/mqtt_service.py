import ssl
import json
import time
import uuid
import paho.mqtt.client as mqtt
from app.config import MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASS, MQTT_TLS, TOPIC, PUBLISH_QOS
from app.utils.helpers import log

class MQTTService:
    def __init__(self):
        self.client = mqtt.Client()
        self._setup_client()
        self._connect()

    def _setup_client(self):
        if MQTT_TLS:
            self.client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
        if MQTT_USER or MQTT_PASS:
            self.client.username_pw_set(MQTT_USER, MQTT_PASS)

    def _connect(self):
        self.client.connect(MQTT_HOST, MQTT_PORT, 60)
        self.client.loop_start()

    def publish_image(self, b64_png: str, cut_paper: int = 1, paper_width_mm: int = 0, paper_height_mm: int = 0):
        payload = {
            "ticket_id": f"web-{int(time.time()*1000)}-{uuid.uuid4().hex[:6]}",
            "data_type": "png",
            "data_base64": b64_png,
            "paper_type": 0,
            "paper_width_mm": paper_width_mm,
            "paper_height_mm": paper_height_mm,
            "cut_paper": cut_paper
        }
        try:
            log(f"MQTT publish → topic={TOPIC} qos={PUBLISH_QOS} bytes={len(b64_png)}")
            self.client.publish(TOPIC, json.dumps(payload), qos=PUBLISH_QOS, retain=False)
        except Exception as e:
            log("MQTT publish error:", repr(e))
            raise

mqtt_service = MQTTService()

