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