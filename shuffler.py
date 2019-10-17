import spotipy
from json.decoder import JSONDecodeError

import os, random
import credentials
import shuffler_funs
import spotifyPlaylist


username = 'manoskaterboi'
day = input('Enter day name (with the first letter to be capital): ')
# https://open.spotify.com/user/manoskaterboi?si=IRJJQT4vSz2Pmj-UH-d_bQ
myClientID = credentials.SPOTIPY_CLIENT_ID
mySecretKey = credentials.SPOTIPY_CLIENT_SECRET
myRedirect = credentials.SPOTIPY_REDIRECT_URI

shuffler = shuffler_funs.EditPlaylist(username=username, myClientID=myClientID, mySecretKey=mySecretKey, myRedirect=myRedirect)
playlistManager = spotifyPlaylist.Playlist(username=username, myClientID=myClientID, mySecretKey=mySecretKey, myRedirect=myRedirect)

# Create spotify Object
spotifyObject = spotipy.Spotify(auth=shuffler.token)

new_songs = shuffler.get_random_tracklist(spotifyObject, day, username)

for song in new_songs:
    print(song)

spotifyObject2 = spotipy.Spotify(auth=playlistManager.token)
"""
playlist_name = 'Test'
playlistManager.create_playlist(spotifyObject2, username, new_songs, playlist_name)
"""
playlistManager.edit_playlist(spotifyObject2, day, new_songs)
