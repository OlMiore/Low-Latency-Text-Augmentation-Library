import random

def set_seed(seed: int):
    random.seed(seed)

class AugmentorBase:
    def __call__(self, text: str) -> str:
        raise NotImplementedError