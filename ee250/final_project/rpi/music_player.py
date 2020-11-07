import sys
import paho.mqtt.client as mqtt
import spotify_api
from enum import Enum

# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')

import grovepi  # noqa
import grove_rgb_lcd  # noqa

BUTTON = 2
ROTARY = 0

search_text = ""


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    # subscribe to topics of interest here
    client.subscribe('/ee250musicplayer/input')
    client.message_callback_add('/ee250musicplayer/input', on_input)


def on_input(client, userdata, msg):
    global search_text
    if len(msg) == 1:
        search_text += msg
        if len(search_text) == 1:
            grove_rgb_lcd.setText(search_text)
        else:
            grove_rgb_lcd.setText_norefresh(search_text)


def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


grovepi.pinMode(BUTTON, "INPUT")
grovepi.pinMode(ROTARY, "INPUT")

# Initialize screen
grove_rgb_lcd.setText("Start typing\n to search music")

# Initialize Spotify
spotify_api.spotify_init()

# Start MQTT
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
client.loop_start()

button_counter = 0

while True:
    if grovepi.digitalRead(BUTTON):
        button_counter += 1
    else:
        if button_counter != 0:
            if button_counter < 100:
                print(spotify_api.spotify_search("something"))
            else:
                print("long press")
            button_counter = 0
