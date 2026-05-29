import random
from .base import AugmentorBase

class RandomDeletionAugmentor(AugmentorBase):
    def __init__(self, prob=0.1):
        self.prob = prob

    def __call__(self, text: str) -> str:
        return " ".join(
            w for w in text.split() if random.random() > self.prob
        )