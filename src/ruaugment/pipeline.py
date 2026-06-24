import logging
from typing import List, Union
from .validator import ConfigValidator

logger = logging.getLogger(__name__)

class Pipeline:
    def __init__(self, augmentors: List):
        self.augmentors = augmentors
        ConfigValidator().validate(augmentors)

        # Рекомендуемый порядок: сначала семантика, потом шум
        self.augmentors = sorted(
            augmentors,
            key=lambda a: a.order if hasattr(a, "order") else 100
        )

    def augment(self, text: str) -> str:
        """Аугментация одной строки."""
        if not isinstance(text, str):
            raise TypeError("Pipeline.augment expects a string")

        for aug in self.augmentors:
            logger.debug(f"Applying {aug.__class__.__name__}")
            text = aug(text)

        return text

    def augment_batch(self, texts: List[str]) -> List[str]:
        """Аугментация списка строк."""
        if not isinstance(texts, list):
            raise TypeError("Pipeline.augment_batch expects a list[str]")

        result = []
        for t in texts:
            result.append(self.augment(t))
        return result

    def __call__(self, x: Union[str, List[str]]):
        """Универсальный интерфейс."""
        if isinstance(x, str):
            return self.augment(x)
        elif isinstance(x, list):
            return self.augment_batch(x)
        else:
            raise TypeError("Pipeline input must be str or list[str]")