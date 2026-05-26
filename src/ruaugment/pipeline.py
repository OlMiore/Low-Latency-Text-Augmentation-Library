# pipeline.py
from .validator import ConfigValidator

class Pipeline:
    def __init__(self, augmentors):
        self.augmentors = augmentors
        ConfigValidator().validate(augmentors)

    def __call__(self, text: str) -> str:
        for aug in self.augmentors:
            text = aug(text)
        return text

  # validator.py
class ConfigValidator:
    FORBIDDEN = [
        ("CharNoiseAugmentor", "SynonymAugmentor"),
        ("CharNoiseAugmentor", "MorphAugmentor"),
    ]

    def validate(self, augmentors):
        names = [a.__class__.__name__ for a in augmentors]
        for bad_first, bad_second in self.FORBIDDEN:
            if bad_first in names and bad_second in names:
                raise ValueError(
                    f"Недопустимая последовательность: {bad_first} → {bad_second}"
                )
