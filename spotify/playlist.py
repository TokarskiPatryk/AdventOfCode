# pip install spotipy
import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth


class Spotify:

    def __init__(self, scope_sp='user-library-read'):
        self.scope_sp = scope_sp
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope_sp))

    def export_saved_tracks(self):
        results = self.sp.current_user_saved_tracks(limit=50)
        self.exporting_songs_to_json(results, 'tracks.json')

    def export_playlist(self, playlist_id):
        results = self.sp.playlist_items(playlist_id)
        filename = self.playlist_name(playlist_id) + '.json'
        self.exporting_songs_to_json(results, filename)

    def exporting_songs_to_json(self, results, filename):
        new_songs = list()
        items = self.full_list_of(results)

        for item in items:
            song_id = item['track']['id']
            artist = item['track']['artists'][0]['name']
            song = item['track']['name']
            new_songs.append([artist, song, song_id])

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(new_songs, f, ensure_ascii=False, indent=2)
        # print(len(new_songs))

    @staticmethod
    def list_songs_in_json(filename_without_extension):
        filename_without_extension += '.json'
        with open(filename_without_extension, encoding='utf-8') as f:
            data = json.load(f)
            print(json.dumps(data, ensure_ascii=False, indent=2))

    def list_user_playlists(self):
        for playlist in self.list_of_playlists():
            print(playlist['name'], ' - ', playlist['id'])

    def playlist_name_to_id(self, name):
        for playlist in self.list_of_playlists():
            if playlist['name'] == name:
                return playlist['id']
        return -1

    def list_of_playlists(self):
        results = self.sp.current_user_playlists()
        items = self.full_list_of(results)
        return items

    def full_list_of(self, results):
        items: list = results['items']

        while results['next']:
            results = self.sp.next(results)
            items.extend(results['items'])
        return items

    def playlist_name(self, playlist_id):
        playlist = self.sp.playlist(playlist_id, fields='name')
        return playlist['name']


# Spotify.list_user_playlists()
sp_user = Spotify()

# export_playlist(playlist_name_to_id('neon'))
# list_user_playlists()

from ytmusicapi import YTMusic
ytmusic = YTMusic('headers_auth.json')

# playlistId = ytmusic.create_playlist("test", "test description")
# search_results = ytmusic.search("Oasis Wonderwall")
# ytmusic.add_playlist_items(playlistId, [search_results[0]['videoId']])

#request = ytmusic.get_library_playlists()
#print(json.dumps(request, indent=2))


def yt_list_user_playlists():
    requests = ytmusic.get_library_playlists()
    for playlist in requests:
        print(playlist['title'], ' - ', playlist['playlistId'])


def add_playlist_from_json_file(filename):
    with open(filename + '.json', encoding='utf-8') as file:
        data = json.load(file)
    playlist_id = ytmusic.create_playlist(filename, 'spotify playlist')
    list_of_songs = list()
    inc = 0
    for song in data:
        name = song[1]
        artist = song[0]

        video_id = get_song_id(name, artist)
        list_of_songs.append(video_id)
        inc += 1
        if inc == 20:
            ytmusic.add_playlist_items(playlist_id, list_of_songs)
            list_of_songs = list()
            inc = 0

    ytmusic.add_playlist_items(playlist_id, list_of_songs)


def get_song_id(name, artist):
    result = search_song(name, artist, 'songs')
    try:
        return result[0]['videoId']
    except IndexError:
        print(f'{name} - {artist}')
        result = search_song(name, artist, 'videos')
        try:
            return result[0]['videoId']
        except IndexError:
            print(f'Song ({name} - {artist}) does not exist.')


def search_song(name, artist, search_type):
    return ytmusic.search(f'{name} {artist}', filter=search_type, limit=1, ignore_spelling=True)


# with open('INDIE NIGHT.json', encoding='utf-8') as f:
#     data = json.load(f)
#     print(len(data))


add_playlist_from_json_file('TECHNO TECHNO TECHNOOO')