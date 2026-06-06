import random
from .base import AugmentorBase

class CharNoiseAugmentor(AugmentorBase):
    def __init__(self, prob=0.05):
        self.prob = prob

    def __call__(self, text: str) -> str:
        new_chars = []
        for ch in text:
            if random.random() < self.prob:
                new_chars.append(chr(ord(ch) + 1))
            else:
                new_chars.append(ch)
<<<<<<< HEAD
        return "".join(new_chars)
=======
        return "".join(new_chars)
>>>>>>> 7952769343f788334f394c9dbaeb962b5f7c9fca
