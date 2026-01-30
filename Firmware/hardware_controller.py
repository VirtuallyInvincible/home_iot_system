import RPi.GPIO as GPIO
import _thread
import requests
import time
import paho.mqtt.client as mqtt
import ssl
import time
import json


PORT = 8883
TOPIC = "device/led/state"

# You won't get my endpoint, or my secret files!
ENDPOINT = "<iot-endpoint>.amazonaws.com"
CA_PATH = "AmazonRootCA1.pem"
CERT_PATH = "device.pem.crt"
KEY_PATH = "private.pem.key"


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)
    
def on_message(client, userdata, msg):
    print(f"Message received: {msg.topic} -> {msg.payload.decode()}")
    message = json.loads(msg.payload.decode("utf-8"))
    isOn = message.get("state")
    print(f"LED state: {'On' if isOn else 'Off'}")
    if isOn:
        GPIO.output(7, True)
    else:
        GPIO.output(7, False)

def _poll_server_periodically(timeSpanInSeconds):
    while True:
        _poll_server()
        time.sleep(timeSpanInSeconds)

# Deprecated - resort to push notifications from AWS
def _poll_server():
    r = requests.get(url = "https://7jg0916m4m.execute-api.us-east-1.amazonaws.com/api/LED")
    data = r.json()
    isOn = data['message']
    print(f"LED state: {'On' if isOn else 'Off'}")
    if isOn:
        GPIO.output(7, True)
    else:
        GPIO.output(7, False)

def _init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    #GPIO.output(7, False)
    _poll_server()

# Deprecated - user input to arrive via push notifications, not the Raspberry Pi's console
def _handle_user_input():
    userInput = ""
    while userInput != "exit":
        userInput = input("Type 'exit' to shutdown: ")
    GPIO.output(7, False)
    GPIO.cleanup()


_init()
#_thread.start_new(_poll_server_periodically, (5,))
#_handle_user_input()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(CA_PATH,
               certfile=CERT_PATH,
               keyfile=KEY_PATH,
               cert_reqs=ssl.CERT_REQUIRED,
               tls_version=ssl.PROTOCOL_TLSv1_2,
               ciphers=None)
print("Connecting to AWS IoT...")
client.connect(ENDPOINT, PORT, keepalive=60)
client.loop_forever()