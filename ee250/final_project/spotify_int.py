# Import libraries
import paho.mqtt.client as mqtt
import spotify_api
from pynput import keyboard


def on_connect(client, userdata, flags, rc):
    """ Handle MQTT connection """
    print("Connected to server (i.e., broker) with result code "+str(rc))

    # subscribe to song id
    client.subscribe('/ee250musicplayer/song')
    client.message_callback_add('/ee250musicplayer/song', on_song)

    # subscribe to volume
    client.subscribe('/ee250musicplayer/volume')
    client.message_callback_add('/ee250musicplayer/volume', on_volume)

    # subscribe to palypause
    client.subscribe('/ee250musicplayer/volume')
    client.message_callback_add('/ee250musicplayer/playpause', on_playpausee)


def on_message(client, userdata, msg):
    """ Generic messag handle """
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


def on_song(client, userdata, msg):
    """ Player song with song id 'msg'"""
    pass


def on_volume(client, userdata, msg):
    """ Adjust volume """
    pass


def on_playpausee(client, userdata, msg):
    """ Play or pause """
    pass


def on_press(key):
    try:
        k = key.char
    except:
        return

    client.publish('/ee250musicplayer/input', k)


spotify_api.spotify_init()

client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
client.loop_start()

lis = keyboard.Listener(on_press=on_press)
lis.start()
