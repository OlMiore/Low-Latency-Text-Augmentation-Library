import random
from .base import AugmentorBase

MORPH_RULES = {
    "важны": ["важен", "важна", "важно"],
    "деньги": ["средства", "капитал"],
    "кредит": ["займ", "ссуда"]
}

class MorphAugmentor(AugmentorBase):
    def __call__(self, text: str) -> str:
        words = text.split()
        new_words = []
        for w in words:
            if w.lower() in MORPH_RULES and random.random() < 0.3:
                new_words.append(random.choice(MORPH_RULES[w.lower()]))
            else:
                new_words.append(w)
        return " ".join(new_words)
