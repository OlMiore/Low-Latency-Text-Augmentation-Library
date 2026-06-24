import warnings

class ConfigValidator:
    # Семантический порядок аугментаций
    ORDER = {
        "SynonymAugmentor": 1,          # семантика
        "MorphAugmentor": 2,            # грамматика
        "CharNoiseAugmentor": 3,        # символы
        "RandomSwapAugmentor": 4,       # перестановки
        "RandomDeletionAugmentor": 5,   # удаление
    }

    # Несовместимые пары (строгие ошибки)
    FORBIDDEN = [
        ("CharNoiseAugmentor", "MorphAugmentor"),  # Morph не сможет обработать испорченные слова
    ]

    @classmethod
    def validate(cls, augmentors):
        names = [a.__class__.__name__ for a in augmentors]

        # 1. Проверка порядка
        order_values = [cls.ORDER.get(name, 999) for name in names]
        if order_values != sorted(order_values):
            raise ValueError(
                f"Некорректный порядок аугментаторов: {names}. "
                f"Ожидается порядок по уровням семантики: "
                f"Synonym → Morph → Char → Swap → Deletion."
            )

        # 2. Проверка дубликатов
        if len(names) != len(set(names)):
            warnings.warn(f"Обнаружены дубликаты аугментаторов: {names}")

        # 3. Проверка несовместимостей
        for bad_first, bad_second in cls.FORBIDDEN:
            if bad_first in names and bad_second in names:
                idx1 = names.index(bad_first)
                idx2 = names.index(bad_second)
                if idx1 < idx2:
                    raise ValueError(
                        f"Недопустимая последовательность: {bad_first} → {bad_second}. "
                        f"Эти аугментаторы несовместимы."
                    )

        return True