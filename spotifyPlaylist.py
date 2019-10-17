import os
import spotipy.util as util

class Playlist:
    monday = 'Monday - Good Music'
    tuesday = 'Tuesday - Basis'
    wednesday = 'Wednesday - The Beginning'
    thursday = 'Thursday - Zeros'
    friday = 'Friday - Out The Oven'
    saturday = 'Saturday - Sound of the Present'
    sunday = 'Sunday - Favourites'

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
    
    def edit_playlist(self, spotifyObject, day, track_list):
        # Get playlists and all the details. playlists is of type 'dict'
        playlists = spotifyObject.user_playlists(self.username)

        # Keep playlists and discard some redundant information.
        items = playlists['items']
        # track_list will be used to store what is listed in next line
        
        for item in items:    
            # find 'item' with the playlist-name we are interested in.
            day_fullname = self.get_fullname_day(day)
            if item['name'] == day_fullname:
                playlistID = item['id']
                uri_list = []
                for track in track_list:
                    uri_list.append(track[2])
                spotifyObject.user_playlist_replace_tracks(user=self.username, playlist_id=playlistID, tracks=uri_list)
    
    def get_fullname_day(self, day):
        if day == 'Monday':
            d = self.monday
        if day == 'Tuesday':
            d = self.tuesday
        if day == 'Wednesday':
            d = self.wednesday
        if day == 'Thursday':
            d = self.thursday
        if day == 'Friday':
            d = self.friday
        if day == 'Saturday':
            d = self.saturday
        if day == 'Sunday':
            d = self.sunday
        if not d:
            raise Exception('Specify one of the names of the week with a capital first letter.')
        return d


