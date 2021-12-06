import spotipy
from spotipy.oauth2 import SpotifyOAuth

class Spotify:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="",
                                               client_secret="",
                                               redirect_uri="http://localhost:3000/",
                                               scope="user-library-read user-modify-playback-state app-remote-control streaming user-read-playback-state"))
    def savedTracks(self):
        results = self.sp.current_user_saved_tracks()
        ids = []
        for idx, item in enumerate(results['items']):
            ids.append(item['track']['uri'])
    
    def playSong(self,ids=None):
        if ids: self.sp.start_playback(uris=ids)
        else: self.sp.start_playback(uris=self.savedTracks())
    
    def getCurrentlyPlaying(self):
        try:
            info = self.sp.current_user_playing_track()
            song = info['item']['name']
            artist = info['item']['album']['artists'][0]['name']
            return f"{song} - {artist}"
        except:
            return "None"
    
    def search(self, q):
        ret = []
        results = self.sp.search(q='track:' + q, type='track')
        for idx, item in enumerate(results['tracks']['items']):
            ret.append([item['name'],item['uri']])
        return ret

    def qSong(self, id):
        print(id)
        self.sp.add_to_queue(uri=id)

    def pause(self):
        self.sp.pause_playback()
    def play(self):
        self.sp.start_playback()
    def skip(self):
        self.sp.next_track()

if __name__ == "__main__":
    spot = Spotify()
    spot.qSong("id")