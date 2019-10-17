import os
import spotipy.util as util

class Playlist:
    
    def __init__(self, username, myClientID, mySecretKey, myRedirect):
        # Get token || if scope=None then only public playlists will be returned
        self.username = username
        try:
            self.token = util.prompt_for_user_token(username=username, scope='playlist-modify-public', client_id=myClientID, client_secret=mySecretKey, redirect_uri=myRedirect)
        except:
            os.remove(f".cache-{username}")
            self.token = util.prompt_for_user_token(username=username, scope='playlist-modify-public', client_id=myClientID, client_secret=mySecretKey, redirect_uri=myRedirect)

    def create_playlist(self, spotifyObject, track_list, playlist_name):
        desc = 'This playlist was created using the Spotify API.'
        rets = spotifyObject.user_playlist_create(user=self.username, name=playlist_name, public=True)
        #rets is a dictionary
        self.id = rets['id']
        self.owner = rets['owner']
        self.uri = rets['uri']

        uri_list = []
        for track in track_list:
            uri_list.append(track[2])
        spotifyObject.user_playlist_add_tracks(user=username, playlist_id=self.id, tracks=uri_list)
    
    def edit_playlist(self, spotifyObject, out_playlist, track_list):
        # Get playlists and all the details. playlists is of type 'dict'
        playlists = spotifyObject.user_playlists(self.username)

        # Keep playlists and discard some redundant information.
        items = playlists['items']
        # track_list will be used to store what is listed in next line
        
        for item in items:    
            # find 'item' with the playlist-name we are interested in.
            if item['name'] == out_playlist:
                playlistID = item['id']
                uri_list = []
                for track in track_list:
                    uri_list.append(track[2])
                spotifyObject.user_playlist_replace_tracks(user=self.username, playlist_id=playlistID, tracks=uri_list)
    


