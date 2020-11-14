# Team Members -- Jaylen Jackson and Haowen Liu
# Repo Link -- https://github.com/ee250-fall2020-finalproject/GrovePi-EE250

import sys
import threading
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


class State(Enum):
    START = 0
    INPUT = 1
    RESULT = 2
    PLAYER = 3


state = State.START
lock = threading.Lock()

BUTTON = 2
ROTARY = 0

search_text = ""

search_results = []


def on_connect(client, userdata, flags, rc):
    """ Handle MQTT connection """
    print("Connected to server (i.e., broker) with result code "+str(rc))

    # subscribe to keyboard input
    client.subscribe('/ee250musicplayer/input')
    client.message_callback_add('/ee250musicplayer/input', on_input)


def on_input(client, userdata, msg):
    """ Handle keyboard input when in INPUT state """
    global search_text
    global state
    if state == State.RESULT or state == State.PLAYER:
        return
    if len(str(msg.payload, 'utf-8')) != 1:
        return
    if state == State.START:
        state = State.INPUT
    lock.acquire()
    if str(msg.payload, 'utf-8') == '\n':
        # Message ended, search and switch to RESULT state
        global cursor_location
        global search_results
        state = state.RESULT
        results = spotify_api.spotify_search(search_text)
        for result in results["tracks"]["items"]:
            search_results.append(
                {"name": result["name"], "id": result["id"]})
        search_text = ""
        cursor_location = 0
        grove_rgb_lcd.setText(search_results[cursor_location]["name"])
    else:
        # Part of the message, print and keep listening
        search_text += str(msg.payload, 'utf-8')
        if len(search_text) == 1:
            grove_rgb_lcd.setText(search_text)
        else:
            grove_rgb_lcd.setText_norefresh(search_text)
    lock.release()


def on_message(client, userdata, msg):
    """ Generic messag handle """
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


def update_player_display(name, playing, volume):
    """ Update player display
    name: name of song
    playing: True or False
    volume: 0-100
    """
    display = name[0:16] + "\n"
    if playing:
        display += "playing      "
    else:
        display += "paused       "

    display += (str)(volume)
    grove_rgb_lcd.setText(display)

    # Configure pins
grovepi.pinMode(BUTTON, "INPUT")
grovepi.pinMode(ROTARY, "INPUT")

# Initialize screen
grove_rgb_lcd.setText("Start typing\nto search music")

# Initialize Spotify
spotify_api.spotify_init()

# Start MQTT
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
client.loop_start()

button_counter = 0
cursor_location = 0
play = True
volume = 50
currently_playing = ""

while True:
    lock.acquire()
    # Check button
    if state == state.RESULT:
        button_reading = grovepi.digitalRead(BUTTON)
        if button_reading:
            button_counter += 1
        else:
            # Press to select songs
            if button_counter != 0:
                client.publish("/ee250musicplayer/song",
                               search_results[cursor_location]["id"])
                state = State.PLAYER
                rotary = grovepi.analogRead(ROTARY)
                volume = (int)(rotary / 50.9) * 5
                client.publish("/ee250musicplayer/volume", (str)(volume))
                currently_playing = search_results[cursor_location]["name"]
                update_player_display(
                    currently_playing, play, volume)
                search_results = []
                button_counter = 0

    elif state == State.PLAYER:
        button_reading = grovepi.digitalRead(BUTTON)
        if button_reading:
            button_counter += 1
        else:
            if button_counter != 0:
                if button_counter < 100:
                    # Short press for play and pause
                    play = not play
                    client.publish("/ee250musicplayer/playpause",
                                   "Play" if play else "Pause")
                    update_player_display(
                        currently_playing, play, volume)
                else:
                    # Long press to go back to home page
                    state = State.START
                    grove_rgb_lcd.setText("Start typing\nto search music")
                    play = True
                    volume = 50
                    currently_playing = ""
                    client.publish("/ee250musicplayer/playpause", "Pause")
                button_counter = 0

    # Check rotary encoder
    if state == State.RESULT:
        # Scroll throw results in RESULT state
        rotary = grovepi.analogRead(ROTARY)
        new_cursor_location = (int)(rotary / 103)
        if new_cursor_location != cursor_location:
            cursor_location = new_cursor_location
            grove_rgb_lcd.setText(search_results[cursor_location]["name"])
    elif state == State.PLAYER:
        # Adjust volume in PLAYER mode
        rotary = grovepi.analogRead(ROTARY)
        new_volume = (int)(rotary / 50.9) * 5
        if new_volume != volume:
            update_player_display(
                currently_playing, play, volume)
            client.publish("/ee250musicplayer/volume", (str)(volume))
            volume = new_volume
    lock.release()
