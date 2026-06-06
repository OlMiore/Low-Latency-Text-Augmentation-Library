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
<<<<<<< HEAD
        return " ".join(new_words)
=======
        return " ".join(new_words)
>>>>>>> 7952769343f788334f394c9dbaeb962b5f7c9fca
