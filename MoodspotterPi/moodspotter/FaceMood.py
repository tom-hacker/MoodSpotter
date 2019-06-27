target_values = {'target_acousticness': 1.0,
                 'target_danceability': 1.0,
                 'target_energy': 1.0,
                 'target_instrumentalness': 1.0,
                 #'target_key': 4,                  # key - integer maps to pitches
                 'target_liveness': 1.0,            # probability that track is live
                 #'target_loudness': -30,           # relative loudness (strength) in dB, -60 to 0
                 #'target_mode': 0,                 # major (1) or minor (0)
                 #'target_popularity': 50,          # 0 to 100 value, 100 being highest
                 #'target_speechiness': 25,         # is target text or song? < .33 music; .33 -> .66 mixed music and speech; > .66 speech only
                 #'target_tempo': 100,              # bpm
                 'target_valence': 1.0,              # positiveness of track
                 'seed_tracks': ['7JJmb5XwzOO8jgpou264Ml'],
                 'limit': 5
                 }


def reset_target_values():
    target_values['target_acousticness'] = 1.0
    target_values['target_danceability'] = 1.0
    target_values['target_energy'] = 1.0
    target_values['target_instrumentalness'] = 1.0
    target_values['target_liveness'] = 1.0
    target_values['target_valence'] = 1.0
    #target_values['target_key'] = 4
    #target_values['target_loudness'] = -30
    #target_values['target_mode'] = 0
    #target_values['target_popularity'] = 50
    #target_values['target_speechiness'] = 25
    #target_values['target_tempo'] = 100


class FaceMood:
    def __init__(self):
        pass

    anger = 0.0
    contempt = 0.0
    disgust = 0.0
    fear = 0.0
    happiness = 0.0
    neutral = 0.0

    def divide_all_by(self, divisor):
        self.anger /= divisor
        self.contempt /= divisor
        self.disgust /= divisor
        self.fear /= divisor
        self.happiness /= divisor
        self.neutral /= divisor

    def get_spotify_targets(self):
        reset_target_values()
        target_values['target_energy'] *= self.happiness
        target_values['target_danceability'] *= self.happiness
        target_values['target_liveness'] *= self.happiness
        return target_values