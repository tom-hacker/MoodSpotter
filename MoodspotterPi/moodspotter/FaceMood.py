import random
from conf.Config import spotify_happy_seeds, spotify_annoyed_seeds, spotify_calm_seeds, spotify_neutral_seeds, spotify_sad_seeds


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
                 'target_valence': 1.0,             # positiveness of track
                 'seed_tracks': [],
                 'limit': 5
                 }


def reset_target_values():
    target_values['seed_tracks'] = []
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
    sadness = 0.0

    def divide_all_by(self, divisor):
        self.anger /= divisor
        self.contempt /= divisor
        self.disgust /= divisor
        self.fear /= divisor
        self.happiness /= divisor
        self.neutral /= divisor
        self.sadness /= divisor

    def get_spotify_targets(self):
        reset_target_values()
        self.add_seeds()

        print(target_values)
        return target_values

    def add_seeds(self):
        if self.happiness > .25:        #play positive, happy songs
            seed = random.choice(spotify_happy_seeds)
            target_values['seed_tracks'].append(seed)
            target_values['target_energy'] *= max(self.happiness, self.anger)
            target_values['target_danceability'] *= self.happiness
            target_values['target_liveness'] *= self.happiness
            target_values['target_valence'] *= self.happiness
            target_values['target_instrumentalness'] *= 1 - self.happiness

        if self.sadness > .25:           #play sad songs
            seed = random.choice(spotify_sad_seeds)
            target_values['seed_tracks'].append(seed)
            target_values['target_energy'] *= 1 - self.sadness
            target_values['target_danceability'] *= 1 - self.sadness
            target_values['target_instrumentalness'] *= 1 - self.happiness

        if self.contempt > .25 or self.disgust > .25:  #play negative songs, with higher energy
            seed = random.choice(spotify_annoyed_seeds)
            target_values['seed_tracks'].append(seed)
            target_values['target_energy'] *= max(self.happiness, self.anger)
            target_values['target_valence'] *= 1 - max(self.contempt, self.disgust)
            target_values.pop('target_liveness')

        if self.anger > .25 or self.fear > .25:    #play calming, slow songs
            seed = random.choice(spotify_calm_seeds)
            target_values['seed_tracks'].append(seed)
            target_values['target_energy'] *= 1 - max(self.anger, self.fear)
            target_values['target_danceability'] *= 1 - max(self.anger, self.fear)
            target_values['target_valence'] *= max(self.anger, self.fear)


        if self.neutral > .25:
            seed = random.choice(spotify_neutral_seeds)
            target_values['seed_tracks'].append(seed)

        if self.neutral > .60:
            target_values['target_energy'] = .7
            target_values.pop('target_instrumentalness')
            target_values.pop('target_acousticness')
            target_values.pop('target_liveness')

        if self.sadness > 60:
            target_values.pop('target_valence')
            target_values.pop('target_liveness')

        if len(target_values['seed_tracks']) <= 0:
            seed = random.choice(spotify_neutral_seeds)
            target_values['seed_tracks'].append(seed)


