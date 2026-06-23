import random
from .base import AugmentorBase

# Расширяемый словарь синонимов
SYN_DICT = {
    "кредит": ["займ", "ссуда"],
    "деньги": ["средства", "финансы"],
    "банк": ["финучреждение", "кредитная организация"],
    "клиент": ["пользователь", "заказчик"],
    "платёж": ["оплата", "транзакция"],
    "ошибка": ["сбой", "неполадка"],
    "задача": ["вопрос", "проблема"],
    "важный": ["значимый", "существенный"],
}

class SynonymAugmentor(AugmentorBase):
    def __init__(self, prob=0.3):
        self.prob = prob

    def _preserve_case(self, original: str, synonym: str) -> str:
        """Сохраняем заглавную букву, если она была."""
        if original.istitle():
            return synonym.capitalize()
        return synonym

    def __call__(self, text: str) -> str:
        words = text.split()
        new_words = []

        for w in words:
            key = w.lower()

            # Если слово есть в словаре и выпала вероятность замены
            if key in SYN_DICT and random.random() < self.prob:
                synonym = random.choice(SYN_DICT[key])
                synonym = self._preserve_case(w, synonym)
                new_words.append(synonym)
            else:
                new_words.append(w)

        return " ".join(new_words)