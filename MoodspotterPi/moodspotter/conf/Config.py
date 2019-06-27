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

#waves - dean lewis;
spotify_sad_seeds = ["0BfVKJALJjpzNYIQiEgF2G"]

#Mellomaniac - dj shaw; Strawberry seeds - coldplay;
spotify_calm_seeds = ["7gEky4JRrXUQdImEldIUlT", "4NmcfahJGawtwaMATGgP0L"]

#Grace Kelly - mika
spotify_neutral_seeds = ["2SDx0PooHZI1SQKR0y44bs"]
spotify_party_seeds = []
#down in the past - Mando Diao; Without me - Eminem;
spotify_annoyed_seeds = ["2vx5Dc3Zxtd5yGDlh2pAAz", "7lQ8MOhq6IN2w8EYcFNSUk"]
