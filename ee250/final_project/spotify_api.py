""" Title: Play spotify songs using Spotipy library
Author: <Arvind Mehairjan>
Date: <12-09-2019>
Availability: <https://bit.ly/3po36yN> """
#spotipy documentation - https://spotipy.readthedocs.io/en/2.16.1/
import os
import sys
import spotipy
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
#client id associated with the app created through spotify for developers
    client_id = '9b907c9f2ad4424792057ba71606f879'
#client secret id associated with the app
#required authorization level
    client_secret = '8429b7ab10e144a0b3fcb9ab00ae90cf'  
    redirect_uri = 'https://www.google.com'
    scope = 'user-read-private user-read-playback-state user-modify-playback-state'
    #workaround to a bug regarding scope in the spotipy library
    #solution found in issues section of github documentation
    try:
        token = util.prompt_for_user_token(
            username, scope, client_id, client_secret, redirect_uri)
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(
            username, scope, client_id, client_secret, redirect_uri)
#create an authorized spotify object using spotipy library
    spotifyObject = spotipy.Spotify(auth=token)
#access list of devices linked to spotify account
#most recent device is most recent logged in - music will be played there
    devices = spotifyObject.devices()
    deviceID = devices['devices'][0]['id']

#searches for artist
def spotify_search(query):
    return spotifyObject.search(query, 10)

#plays the track
def spotify_play(track_id):
    global deviceID
    global spotifyObject
    global tracks
    #returns a single track given the track id
    track = spotifyObject.track(track_id)
    tracks = [track["uri"]]
    #plays track from device
    spotifyObject.start_playback(deviceID, None, tracks)

#sets the volume
def spotify_set_volume(volume):
    global deviceID
    global spotifyObject
    spotifyObject.volume(volume, deviceID)

#resume or pause
def spotify_playpause(playpause):
    global deviceID
    global spotifyObject
    global tracks
    if playpause:
        spotifyObject.start_playback()
    else:
        spotifyObject.pause_playback(deviceID)
