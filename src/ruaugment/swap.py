import random
from .base import AugmentorBase

class RandomSwapAugmentor(AugmentorBase):
    def __init__(self, prob=0.1):
        self.prob = prob

    def __call__(self, text: str) -> str:
        tokens = text.split()
        n = len(tokens)

        # Если меньше двух слов — свап невозможен
        if n < 2:
            return text

        i = 0
        while i < n - 1:
            # С вероятностью prob меняем местами токен i и i+1
            if random.random() < self.prob:
                tokens[i], tokens[i + 1] = tokens[i + 1], tokens[i]
                i += 2  # пропускаем следующий, чтобы не свапать его дважды
            else:
                i += 1

        return " ".join(tokens)