import random
from pymorphy3 import MorphAnalyzer
from .base import AugmentorBase

class MorphAugmentor(AugmentorBase):
    def __init__(self, prob=0.3):
        self.prob = prob
        self.morph = MorphAnalyzer()

        # Набор граммем, которые дают заметные изменения
        self.targets = [
            {"gent"},  # родительный падеж
            {"datv"},  # дательный
            {"accs"},  # винительный
            {"ablt"},  # творительный
            {"loct"},  # предложный
            {"plur"},  # множественное число
            {"sing"},  # единственное число
            {"femn"},  # женский род
            {"masc"},  # мужской род
            {"neut"},  # средний род
            {"past"},  # прошедшее время
            {"pres"},  # настоящее время
        ]

    def _preserve_case(self, original: str, new: str) -> str:
        if original.istitle():
            return new.capitalize()
        return new

    def _try_inflect(self, word, parsed):
        random.shuffle(self.targets)

        for grammemes in self.targets:
            form = parsed.inflect(grammemes)
            if form and form.word != word:
                return form.word

        return None

    def __call__(self, text: str) -> str:
        words = text.split()
        new_words = []

        for w in words:
            if random.random() >= self.prob:
                new_words.append(w)
                continue

            parsed = self.morph.parse(w)[0]

            # Меняем только существительные, прилагательные, глаголы
            if not any(tag in parsed.tag for tag in ["NOUN", "ADJF", "VERB", "INFN", "PRTF"]):
                new_words.append(w)
                continue

            new_form = self._try_inflect(w, parsed)

            if new_form:
                new_words.append(self._preserve_case(w, new_form))
            else:
                new_words.append(w)

        return " ".join(new_words)