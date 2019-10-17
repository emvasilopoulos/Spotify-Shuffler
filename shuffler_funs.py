import random
import os
import spotipy.util as util

class EditPlaylist:
    def __init__(self, username, myClientID, mySecretKey, myRedirect):
        # Get token || if scope=None then only public playlists will be returned
        try:
            self.token = util.prompt_for_user_token(username=username, scope='playlist-read-private', client_id=myClientID, client_secret=mySecretKey, redirect_uri=myRedirect)
        except:
            os.remove(f".cache-{username}")
            self.token = util.prompt_for_user_token(username=username, scope='playlist-read-private', client_id=myClientID, client_secret=mySecretKey, redirect_uri=myRedirect)

    def get_tracklist(self, spotifyObject, day, username):
        #Get playlists and all the details. playlists is of type 'dict'
        playlists = spotifyObject.user_playlists(username)

        # Keep playlists and discard some redundant information.
        items = playlists['items']
        # track_list will be used to store what is listed in next line
        track_list = []     # list of tuples--> (track_artist, track_name, track_id)
        for item in items:    
            # find 'item' with the playlist-name we are interested in 
            if item['name'] == day + ' - Storage':
                #print(item['id'])
                
                playlist_details = spotifyObject.user_playlist_tracks(user=username, playlist_id=item['id'])
                for detail in playlist_details['items']:
                    track = detail['track']
                    name = track['name']
                    artists = track['artists']
                    artist = artists[0]
                    track_id = track['id']
                    tup = (artist['name'], name, track_id)
                    track_list.append(tup)
                break

        return sorted(track_list, key=self.takeFirstElement)

    def takeFirstElement(self, elem):
        return elem[0]

    def groupByArtist(self, track_list):
        prev_artist = ''
        group_list = []
        artist_songs = []
        for i in range(len(track_list)):
            tup = track_list[i]
            if tup[0] != prev_artist:
                artist_songs = []
                artist_songs.append(tup)
                group_list.append(artist_songs)
            else:
                artist_songs.append(tup)
            prev_artist = tup[0]
        return group_list

    def getOneSongPerArtist(self, group_list):
        new_songs = []
        for artist_songlist in group_list:
            l = len(artist_songlist)
            index = random.randint(0, l-1)
            new_songs.append(artist_songlist[index])

        l = len(new_songs)
        print(l)
        new_songs = random.sample(new_songs, k=l)
        return new_songs

    def get_random_tracklist(self, spotifyObject, day, username):
        track_list = self.get_tracklist(spotifyObject, day, username)
        group_list = self.groupByArtist(track_list)
        new_songs = self.getOneSongPerArtist(group_list)
        return new_songs