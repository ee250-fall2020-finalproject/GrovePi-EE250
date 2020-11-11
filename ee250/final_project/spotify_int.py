# Import libraries
import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from pprint import pprint
import paho.mqtt.client as mqtt
from json.decoder import JSONDecodeError


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
    client.message_callback_add('/ee250musicplayer/playpausee', on_playpausee)


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


client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
client.loop_start()


username = 'm8p86s9tyv0wxt4izw49c3i79'  # placeholder value here
client_id = '9b907c9f2ad4424792057ba71606f879'  # placeholder value here
client_secret = '8429b7ab10e144a0b3fcb9ab00ae90cf'  # placeholder value here
redirect_uri = 'https://www.google.com'
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

token = util.prompt_for_user_token(
    username, scope, client_id, client_secret, redirect_uri)

sp = spotipy.Spotify(auth=token)

devices = sp.devices()
#print(json.dumps(devices, sort_keys=True, indent=4))
deviceID = devices['devices'][0]['id']

# Get track information
#track = sp.current_user_playing_track()
#print(json.dumps(track, sort_keys=True, indent=4))
# print()
#artist = track['item']['artists'][0]['name']
#track = track['item']['name']

# if artist !="":
#print("Currently playing " + artist + " - " + track)

# User information
user = sp.current_user()
displayName = user['display_name']

while True:
    print()
    print("Welcome to Spotify " + displayName)
    print()
    print("Enter 0 to search for an artist")
    print("Enter 1 to exit")
    print()
    choice = input("Enter your choice: ")

    if choice == "0":
        print()
        searchQuery = input("Ok, what's their name?:")
        print()
        # Get search results
        searchResults = sp.search(searchQuery, 1, 0, "artist")
        # Print artist details
        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(artist['genres'][0])
        print()
        #webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']
        # Album details
        trackURIs = []
        trackArt = []
        z = 0

        # Extract data from album
        albumResults = sp.artist_albums(artistID)
        albumResults = albumResults['items']

        for item in albumResults:
            print("ALBUM: " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            # Extract track data
            trackResults = sp.album_tracks(albumID)
            trackResults = trackResults['items']

            for item in trackResults:
                print(str(z) + ": " + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z += 1
            print()
        while True:
            songSelection = input("Enter a song number to see the album art: ")
            if songSelection == "x":
                break
            trackSelectionList = []
            trackSelectionList.append(trackURIs[int(songSelection)])
            sp.start_playback(deviceID, None, trackSelectionList)
            webbrowser.open(trackArt[int(songSelection)])
    # End program
    if choice == "1":
        break
