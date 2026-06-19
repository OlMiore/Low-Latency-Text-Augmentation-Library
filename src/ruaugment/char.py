import random
from .base import AugmentorBase

WRONG_LAYOUT_MAP = {
    'й': 'q', 'ц': 'w', 'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u',
    'ш': 'i', 'щ': 'o', 'з': 'p', 'х': '[', 'ъ': ']',
    'ф': 'a', 'ы': 's', 'в': 'd', 'а': 'f', 'п': 'g', 'р': 'h', 'о': 'j',
    'л': 'k', 'д': 'l', 'ж': ';', 'э': "'",
    'я': 'z', 'ч': 'x', 'с': 'c', 'м': 'v', 'и': 'b', 'т': 'n', 'ь': 'm',
    'б': ',', 'ю': '.'
}

RUS_NEIGHBORS = {
    'й': ['ц'], 'ц': ['й', 'у', 'ф'], 'у': ['ц', 'к'], 'к': ['у', 'е'],
    'е': ['к', 'н'], 'н': ['е', 'г'], 'г': ['н', 'ш'], 'ш': ['г', 'щ'],
    'щ': ['ш', 'з'], 'з': ['щ', 'х'], 'х': ['з', 'ъ'], 'ъ': ['х'],
    'ф': ['ц', 'ы', 'в'], 'ы': ['ф', 'в', 'а'], 'в': ['ы', 'а', 'п'],
    'а': ['в', 'п', 'р'], 'п': ['а', 'р', 'о'], 'р': ['п', 'о', 'л'],
    'о': ['р', 'л', 'д'], 'л': ['о', 'д', 'ж'], 'д': ['л', 'ж', 'э'],
    'ж': ['д', 'э'], 'э': ['ж'],
    'я': ['ч', 'с'], 'ч': ['я', 'с', 'м'], 'с': ['ч', 'м', 'и'],
    'м': ['с', 'и', 'т'], 'и': ['м', 'т', 'ь'], 'т': ['и', 'ь', 'б'],
    'ь': ['т', 'б', 'ю'], 'б': ['ь', 'ю'], 'ю': ['б']
}


class CharNoiseAugmentor(AugmentorBase):
    def __init__(self, mode: str = "mild"):
        if mode not in ("mild", "medium", "chaos"):
            raise ValueError("mode must be 'mild', 'medium' or 'chaos'")
        self.mode = mode

        if mode == "mild":
            self.prob_neighbor = 0.03
            self.prob_layout = 0.01
            self.prob_drop = 0.01
            self.prob_double = 0.01
            self.prob_caps = 0.005
            self.prob_insert = 0.005
            self.prob_sticky = 0.002
            self.prob_space_drop = 0.005
            self.prob_space_insert = 0.005
            self.prob_space_replace = 0.002
            self.prob_swap = 0.01
            self.max_errors_per_word = 1

        elif mode == "medium":
            self.prob_neighbor = 0.06
            self.prob_layout = 0.03
            self.prob_drop = 0.02
            self.prob_double = 0.02
            self.prob_caps = 0.01
            self.prob_insert = 0.01
            self.prob_sticky = 0.005
            self.prob_space_drop = 0.01
            self.prob_space_insert = 0.01
            self.prob_space_replace = 0.005
            self.prob_swap = 0.03
            self.max_errors_per_word = 2

        else:  # chaos
            self.prob_neighbor = 0.1
            self.prob_layout = 0.08
            self.prob_drop = 0.05
            self.prob_double = 0.05
            self.prob_caps = 0.03
            self.prob_insert = 0.03
            self.prob_sticky = 0.02
            self.prob_space_drop = 0.03
            self.prob_space_insert = 0.03
            self.prob_space_replace = 0.02
            self.prob_swap = 0.08
            self.max_errors_per_word = 5

    def _apply_char_error(self, ch: str):
        """Применяет не более ОДНОЙ ошибки к символу."""
        lower = ch.lower()

        # раскладка
        if lower in WRONG_LAYOUT_MAP and random.random() < self.prob_layout:
            rep = WRONG_LAYOUT_MAP[lower]
            return rep.upper() if ch.isupper() else rep

        # соседняя клавиша
        if lower in RUS_NEIGHBORS and random.random() < self.prob_neighbor:
            rep = random.choice(RUS_NEIGHBORS[lower])
            return rep.upper() if ch.isupper() else rep

        # пропуск
        if ch.isalpha() and random.random() < self.prob_drop:
            return ""  # удаляем символ

        # залипание
        if ch.isalpha() and random.random() < self.prob_sticky:
            return ch * random.randint(3, 5)

        # двойное нажатие
        if ch.isalpha() and random.random() < self.prob_double:
            return ch * 2

        # CapsLock
        if ch.isalpha() and random.random() < self.prob_caps:
            return ch.upper() if ch.islower() else ch.lower()

        # вставка символа рядом
        if random.random() < self.prob_insert:
            return random.choice(".,!?*-+=") + ch

        return ch

    def _apply_space_error(self, space: str):
        """Управляемые ошибки пробелов."""
        # удалить пробел
        if random.random() < self.prob_space_drop:
            return ""

        # заменить пробел на символ
        if random.random() < self.prob_space_replace:
            return random.choice(".,!?*-+=")

        # вставить дополнительный пробел
        if random.random() < self.prob_space_insert:
            return "  "

        return " "

    def __call__(self, text: str) -> str:
        words = text.split(" ")
        out_words = []

        for word in words:
            if not word:
                out_words.append("")
                continue

            chars = list(word)

            # перестановка букв внутри слова
            if len(chars) > 2 and random.random() < self.prob_swap:
                i = random.randint(0, len(chars) - 2)
                chars[i], chars[i + 1] = chars[i + 1], chars[i]

            errors_left = self.max_errors_per_word
            new_chars = []

            for ch in chars:
                if errors_left > 0:
                    new_ch = self._apply_char_error(ch)
                    if new_ch != ch:
                        errors_left -= 1
                    new_chars.append(new_ch)
                else:
                    new_chars.append(ch)

            out_words.append("".join(new_chars))

        # обработка пробелов между словами
        result = out_words[0] if out_words else ""
        for w in out_words[1:]:
            space = self._apply_space_error(" ")
            result += space + w

        return result