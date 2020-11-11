import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

spotifyObject = None
deviceID = None
tracks = []


def spotify_init():
    global spotifyObject
    global deviceID

    # Get the username from terminal
    username = sys.argv[1]

    client_id = '9b907c9f2ad4424792057ba71606f879'  # placeholder value here
    client_secret = '8429b7ab10e144a0b3fcb9ab00ae90cf'  # placeholder value here
    redirect_uri = 'https://www.google.com'
    scope = 'user-read-private user-read-playback-state user-modify-playback-state'

    try:
        token = util.prompt_for_user_token(
            username, scope, client_id, client_secret, redirect_uri)
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(
            username, scope, client_id, client_secret, redirect_uri)

    spotifyObject = spotipy.Spotify(auth=token)

    devices = spotifyObject.devices()
    deviceID = devices['devices'][0]['id']


def spotify_search(query):
    return spotifyObject.search(query, 5)


def spotify_play(track_id):
    global deviceID
    global spotifyObject
    global tracks
    track = spotifyObject.track(track_id)
    tracks = [track]
    spotifyObject.start_playback(deviceID, None, tracks)


def spotify_set_volume(volume):
    global deviceID
    global spotifyObject
    spotifyObject.volume(volume, deviceID)


def spotify_playpause(playpause):
    global deviceID
    global spotifyObject
    global tracks
    if playpause:
        spotifyObject.start_playback(deviceID, None, tracks)
    else:
        spotifyObject.pause_playback(deviceID)
