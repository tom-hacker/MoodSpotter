try:
    from SecretConfig import ms_cognitive_key, spotify_id, spotify_secret
except ImportError:
    print("The config file \"SecretConfig.py\" is missing.")
    ms_cognitive_key, spotify_id, spotify_secret = "err"

ms_cognitive_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"
ms_cognitive_client_key = ms_cognitive_key

ms_cognitive_headers_byteimg = {'Content-Type': "application/octet-stream",
                                'Ocp-Apim-Subscription-Key': ms_cognitive_key}
ms_cognitive_params = {'returnFaceId': 'true',
                       'returnFaceAttributes': 'age,gender,smile,facialHair,glasses,emotion,hair,makeup,accessories'}

spotify_client_id = spotify_id
spotify_client_secret = spotify_secret

