import random
from .base import AugmentorBase

class RandomDeletionAugmentor(AugmentorBase):
    def __init__(self, prob=0.1, min_tokens_left=1):
        self.prob = prob
        self.min_tokens_left = min_tokens_left

        # Небольшой список служебных слов
        self.stopwords = {
            "и", "в", "на", "по", "с", "к", "у", "о",
            "что", "как", "но", "а"
        }

    def __call__(self, text: str) -> str:
        tokens = text.split()
        new_tokens = []

        for w in tokens:
            # Базовая вероятность удаления
            p = self.prob

            # Если слово служебное — чуть повышаем вероятность
            if w.lower() in self.stopwords:
                p = min(self.prob * 1.2, 0.9)

            # Удаляем с вероятностью p
            if random.random() > p:
                new_tokens.append(w)

        # Страховка: не удаляем весь текст
        if len(new_tokens) < self.min_tokens_left:
            new_tokens = tokens[:self.min_tokens_left]

        return " ".join(new_tokens)