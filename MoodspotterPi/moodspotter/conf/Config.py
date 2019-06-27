import base64
try:
    from SecretConfig import ms_cognitive_key, spotify_id, spotify_secret, rabbitMq_Password
except ImportError:
    print("The config file \"SecretConfig.py\" is missing.")
    ms_cognitive_key, spotify_id, spotify_secret = "err"

ms_cognitive_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"
ms_cognitive_client_key = ms_cognitive_key

ms_cognitive_headers_byteimg = {'Content-Type': "application/octet-stream",
                                'Ocp-Apim-Subscription-Key': ms_cognitive_key}
ms_cognitive_params = {'returnFaceId': 'true',
                       'returnFaceAttributes': 'age,gender,smile,facialHair,glasses,emotion,hair,makeup,accessories'}


spotify_auth_url = "https://accounts.spotify.com/api/token"
spotify_auth_header = {"Content-Type": "application/x-www-form-urlencoded",
                       "Authorization": "Basic " + base64.b64encode(spotify_id + ":" + spotify_secret)}
spotify_auth_params = {"grant_type": "client_credentials"}
spotify_browse_url = "https://api.spotify.com/v1/recommendations"

rabbitMq_url = "amqp://luanalcf:ov_QK7fqHJXeptQpQul_a9dvGMrlsZYf@macaw.rmq.cloudamqp.com/luanalcf"
rabbitMq_pw = rabbitMq_Password

#happy - pharrell; over the rainbow - israel kamika...; Hey Ya! OutKast; walking on Sunshin - Katrina & the Waves
spotify_happy_seeds = ["5b88tNINg4Q4nrRbrCXUmg", "2K0FpmAfvyqW4sHjBGpIQn", "2PpruBYCo4H7WOBJ7Q2EwM", "05wIrZSwuaVWhcv5FfqeH0",
#dont worry be happy - bobby mcferrin, viva la vida - coldplay;
                       "5YbgcwHjQhdT1BYQ4rxWlD", "3Fcfwhm8oRrBvBZ8KGhtea"]

#waves - dean lewis; someone you loved - lewis capaldi; tears in heaven - eric clapton; everybody hurts - R.E.M;
spotify_sad_seeds = ["0BfVKJALJjpzNYIQiEgF2G", "7qEHsqek33rTcFNT9PFqLf", "7utRJ4BeYx85khzP3lKoBX", "6PypGyiu0Y2lCDBN1XZEnP",
#sounds of silence - simon & garfunkel;
                     "5jZVO2BKMYigxIGVgfRvs3"]

#Mellomaniac - dj shaw; Strawberry seeds - coldplay; jazz; Please dont go - barcelona; mozart
spotify_calm_seeds = ["7gEky4JRrXUQdImEldIUlT", "4NmcfahJGawtwaMATGgP0L", "3HfPHK9gTHDtaeJHEH1x2n", "0lRnbYaPtv0A5OezVahO8e", "3k4S8Nya2OdCHpkG9sSNDM"]

#Grace Kelly - mika; paint it, black - stones; sympath. for the devil - stones; black hole sun - soundgarden;
spotify_neutral_seeds = ["2SDx0PooHZI1SQKR0y44bs", "63T7DJ1AFDD6Bn8VzG6JE8", "1Ud6moTC0KyXMq1Oxfien0", "2EoOZnxNgtmZaD8uUmz2nD",
#Under the Bridge - RHChili peppers; jazz; Aisha - outlandish
                         "3d9DChrdc6BOeFsbrZ3Is0", "2QLoxnf8H9MVHdlJt6l3Pe", "7mze3mJmu79AJu8SnS37pS"]

#Sweet but psycho - ava max; Summer Jam - Underdog project
#spotify_party_seeds = ["25sgk305KZfyuqVBQIahim", "6L54wM12STr1kS8nPjPIaS"]
#down in the past - Mando Diao; Without me - Eminem; nobody speak - dj shadow; billy talent - red flag;
spotify_annoyed_seeds = ["2vx5Dc3Zxtd5yGDlh2pAAz", "7lQ8MOhq6IN2w8EYcFNSUk", "2A9rFFPwsnhusCh8ZMBvYY", "2RZWdE8kYPlCAcRUYDeuLC"]
