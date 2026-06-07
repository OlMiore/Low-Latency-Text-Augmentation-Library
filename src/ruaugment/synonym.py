import random
from .base import AugmentorBase

SYN_DICT = {
    "кредит": ["займ", "ссуда"],
    "деньги": ["средства", "финансы"],
}

class SynonymAugmentor(AugmentorBase):
    def __call__(self, text: str) -> str:
        words = text.split()
        new_words = []
        for w in words:
            if w.lower() in SYN_DICT:
                new_words.append(random.choice(SYN_DICT[w.lower()]))
            else:
                new_words.append(w)
        return " ".join(new_words)