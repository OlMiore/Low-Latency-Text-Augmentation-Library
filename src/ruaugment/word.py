# deletion.py
import random
from .base import AugmentorBase

class RandomDeletionAugmentor(AugmentorBase):
    def __init__(self, prob: float = 0.1):
        self.prob = prob

    def __call__(self, text: str) -> str:
        words = text.split()
        kept = [w for w in words if random.random() > self.prob]
        return " ".join(kept) if kept else text

# swap.py
import random
from .base import AugmentorBase

class RandomSwapAugmentor(AugmentorBase):
    def __init__(self, swaps: int = 1):
        self.swaps = swaps

    def __call__(self, text: str) -> str:
        words = text.split()
        for _ in range(self.swaps):
            if len(words) < 2:
                break
            i, j = random.sample(range(len(words)), 2)
            words[i], words[j] = words[j], words[i]
        return " ".join(words)
