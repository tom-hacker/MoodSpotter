import requests
import ErrorHandler
from conf.Config import spotify_auth_url, spotify_auth_header, spotify_auth_params


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
