import requests
import ErrorHandler
from conf.Config import spotify_auth_url, spotify_auth_header, spotify_auth_params, spotify_browse_url
from FaceMood import FaceMood
import json
try:
    from types import SimpleNamespace as Namespace
except ImportError:
    from argparse import Namespace

class SpotifyConnector:
    authToken = ""

    def __init__(self):
        self.get_auth_token()

    def get_auth_token(self):
        r = requests.post(spotify_auth_url,
                          headers=spotify_auth_header,
                          params=spotify_auth_params)
        if r.status_code == 200:
            self.authToken = r.json()['access_token']
        else:
            ErrorHandler.handle_error_response(r, "Spotify Authorization")

    def browse_for_mood(self, mood):
        """

        :type mood: FaceMood
        """
        header = {"Authorization": "Bearer " + self.authToken}
        r = requests.get(spotify_browse_url,
                         headers=header,
                         params=mood.get_spotify_targets())

        if r.status_code == 200:
            results = json.loads(r.text, object_hook=lambda d: Namespace(**d))
            for track in results.tracks:
                print(track.name)
                print(track.uri)
                print(track.external_urls)
                print
