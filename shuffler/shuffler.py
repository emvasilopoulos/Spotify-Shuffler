import spotipy
from json.decoder import JSONDecodeError

import os
import credentials
import shuffler_funs
import spotifyPlaylist

username = input('Enter your Spotify username: ')
in_playlist = input('Enter your playlist that you want to take tracks from: ')
out_playlist = input('Enter your playlist that you want to be renewed: ')

# https://open.spotify.com/user/manoskaterboi?si=IRJJQT4vSz2Pmj-UH-d_bQ
myClientID = credentials.SPOTIPY_CLIENT_ID
mySecretKey = credentials.SPOTIPY_CLIENT_SECRET
myRedirect = credentials.SPOTIPY_REDIRECT_URI

shuffler = shuffler_funs.EditPlaylist(username=username, myClientID=myClientID, mySecretKey=mySecretKey, myRedirect=myRedirect)
playlistManager = spotifyPlaylist.Playlist(username=username, myClientID=myClientID, mySecretKey=mySecretKey, myRedirect=myRedirect)

# Create spotify Object
spotifyObject = spotipy.Spotify(auth=shuffler.token)

new_songs = shuffler.get_random_tracklist(spotifyObject, in_playlist, username)
if len(new_songs) == 0:
    raise Exception('something went wrong')

for song in new_songs:
    print(song)

spotifyObject2 = spotipy.Spotify(auth=playlistManager.token)

playlistManager.edit_playlist(spotifyObject2, out_playlist, new_songs)
