import requests
from requests import ConnectionError
import ErrorHandler
from conf.Config import spotify_auth_url, spotify_auth_header, spotify_auth_params, spotify_browse_url, \
    rabbitMq_url, rabbitMq_pw
from FaceMood import FaceMood
import json
import pika

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    from argparse import Namespace

class SpotifyConnector:
    authToken = ""

    def __init__(self):
        self.get_auth_token()

    def get_auth_token(self):
        try:
            r = requests.post(spotify_auth_url,
                              headers=spotify_auth_header,
                              params=spotify_auth_params)
            if r.status_code == 200:
                self.authToken = r.json()['access_token']
            else:
                ErrorHandler.handle_error_response(r, "Spotify Authorization")
        except ConnectionError:
            print("error connecting to spotify auth")

    def browse_for_mood(self, mood):
        """

        :type mood: FaceMood
        """
        try:
            if self.authToken == "":
                self.get_auth_token()
            header = {"Authorization": "Bearer " + self.authToken}
            r = requests.get(spotify_browse_url,
                             headers=header,
                             params=mood.get_spotify_targets())

            if r.status_code == 200:
                results = json.loads(r.text, object_hook=lambda d: Namespace(**d))
                print
                print("received songs:")
                for track in results.tracks:
                    #print(results)
                    print(track.name)
                    self.send_to_rabbit(track.uri)
                    print(track.uri)
                    print(track.external_urls)
                    print
        except ConnectionError:
            print("error connecting to spotify")

    def send_to_rabbit(self, uri):
        try:
            connection = pika.BlockingConnection(pika.URLParameters(rabbitMq_url))
            channel = connection.channel()
            channel.exchange_declare(exchange='songExchange', exchange_type='direct')
            channel.queue_declare(queue='songs')
            channel.queue_bind(exchange='songExchange', queue='songs')
            channel.basic_publish(exchange='songExchange', routing_key='songs', body=uri)
            connection.close()
            print("sent song to rabbit")
        except ConnectionError:
            print("error connecting to rabbitMQ")

