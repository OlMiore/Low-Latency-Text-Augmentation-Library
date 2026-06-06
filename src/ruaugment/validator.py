class ConfigValidator:
    FORBIDDEN = [
        ("RandomDeletionAugmentor", "SynonymAugmentor"),
    ]

    def validate(self, augmentors):
        names = [a.__class__.__name__ for a in augmentors]
        for bad_first, bad_second in self.FORBIDDEN:
            if bad_first in names and bad_second in names:
                print(f"⚠️ Предупреждение: нежелательная последовательность {bad_first} → {bad_second}")
