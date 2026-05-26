# char.py
import random
from .base import AugmentorBase

class CharNoiseAugmentor(AugmentorBase):
    def __init__(self, prob: float = 0.1):
        self.prob = prob

    def __call__(self, text: str) -> str:
        result = []
        for ch in text:
            if random.random() < self.prob:
                result.append(chr(random.randint(1072, 1103)))  # случайная русская буква
            else:
                result.append(ch)
        return "".join(result)
