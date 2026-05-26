# base.py
from abc import ABC, abstractmethod
import random

class AugmentorBase(ABC):
    @abstractmethod
    def __call__(self, text: str) -> str:
        pass
