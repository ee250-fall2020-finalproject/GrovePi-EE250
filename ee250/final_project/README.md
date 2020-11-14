# RPi Music Controller

## Team members

Jaylen Jackson, Haowen Liu

## Demo link

https://drive.google.com/file/d/1crtEzESvJiiXI2PsabZVZq4FXK8Jt79b/view?usp=sharing

Note: the above link requires USC login to access.

## Nodes:

- RPi
- Computer
- Spotify API

## Environment requirements

- RPi
  - paho
  - spotipy
- Computer
  - paho
  - pynput
  - spotipy

## Setup guide:

- RPi (connection to display / VNC required):

  - `cd` into the directory containing the source codes
  - Execute `python3 ./music_player.py [your Spotify account]`
  - Then sign-in in the opened browser window
  - Copy the redirected URL to the command line and hit enter

- Computer
  - Prepare a device running Spotify, logged in with the same account supplied above (this device can either be the same computer or any other device)
  - `cd` into the directory containing the source codes
  - Execute `python3 ./spotify_int.py [your Spotify account]`
  - Sign-in the same way as above

## Usage guide:

- RPi: You will be greeted with a startup message
- Computer: Enter the keyword you want to search with (max 32 characters)
- RPi: Press the button to search
- RPi: Use the rotary encoder to scroll through your top 10 results
- RPi: Press on the button to select
- Computer: The song you selected will play
- RPi: Short press the button to play/pause; adjust the rotary encoder to adjust the volume
- RPi: Long press the button to pause playback and go back to the initial state
