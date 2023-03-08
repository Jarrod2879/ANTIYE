from flask import Flask
from flask import render_template

import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

os.environ["SPOTIPY_CLIENT_ID"] = 'c38014d9f1a84743adb0cbbf626407aa'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'dee60e2250444c599bbae39268ccbccd'
os.environ["SPOTIPY_REDIRECT_URI"] = 'https://localhost:8888/callback/'

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', name=None)

@app.route("/ANTIYE/")
def ANTIYE():
    # Authenticate the app
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public"))

    # Get the user's playlists
    playlists = sp.current_user_playlists()

    # Loop through each playlist
    for playlist in playlists["items"]:
        # Get the tracks in the playlist
        results = sp.playlist_tracks(playlist["id"])
        print(playlist["name"])
        tracks = results["items"]
        while results["next"]:
            results = sp.next(results)
            tracks.extend(results["items"])
        
        # Loop through each track
        for track in tracks:
            # Get the track's details
            if track["track"]["id"] is not None:
                track_details = sp.track(track["track"]["id"])
            # Check if the artist is Kanye West
            if "Kanye West" in [artist["name"] for artist in track_details["artists"]]:
                # Remove the track from the playlist
                sp.playlist_remove_all_occurrences_of_items(playlist["id"], [track["track"]["id"]])

    return "<p>Removing Kanye</p>"