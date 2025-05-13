import paho.mqtt.client as mqtt
import json

class MQTTHandler:
    def __init__(self, broker="localhost", port=1883, username=None, password=None):
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.received_messages = []

        # Set authentication if provided
        if username and password:
            self.client.username_pw_set(username, password)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            message = json.loads(msg.payload.decode())
            self.received_messages.append({
                'topic': msg.topic,
                'payload': message
            })
        except Exception as e:
            print(f"Error processing message: {str(e)}")

    def connect(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
        except Exception as e:
            raise Exception(f"Failed to connect to MQTT broker: {str(e)}")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic, payload):
        try:
            self.client.publish(topic, json.dumps(payload))
        except Exception as e:
            raise Exception(f"Failed to publish message: {str(e)}")

    def subscribe(self, topic):
        self.client.subscribe(topic)