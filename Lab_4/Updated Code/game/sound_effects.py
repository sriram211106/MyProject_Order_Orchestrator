import array
import math

import pygame


class SoundEffects:
    def __init__(self):
        self.jump = self._make_tone(660, 0.09)
        self.score = self._make_tone(880, 0.12)
        self.game_over = self._make_tone(220, 0.3)

    @staticmethod
    def _make_tone(frequency, duration):
        sample_rate = 22050
        sample_count = int(sample_rate * duration)
        samples = array.array("h")

        for index in range(sample_count):
            progress = index / sample_rate
            fade_in = min(1.0, index / (sample_rate * 0.01))
            fade_out = min(1.0, (sample_count - index) / (sample_rate * 0.04))
            envelope = min(fade_in, fade_out)
            sample = int(10000 * envelope * math.sin(2 * math.pi * frequency * progress))
            samples.append(sample)

        return pygame.mixer.Sound(buffer=samples.tobytes())

    def play_jump(self):
        self.jump.play()

    def play_score(self):
        self.score.play()

    def play_game_over(self):
        self.game_over.play()
