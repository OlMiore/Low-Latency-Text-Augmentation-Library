from .base import set_seed
from .validator import ConfigValidator
from .synonym import SynonymAugmentor
from .morph import MorphAugmentor
from .char import CharNoiseAugmentor
from .deletion import RandomDeletionAugmentor

set_seed(42)

def ok_pipeline():
    augms = [
        SynonymAugmentor(prob=0.5),
        MorphAugmentor(prob=0.5),
        CharNoiseAugmentor(mode="medium"),
        RandomDeletionAugmentor(prob=0.3),
    ]
    ConfigValidator.validate(augms)
    print("✅ Корректный пайплайн прошёл валидацию")

def bad_order():
    augms = [
        CharNoiseAugmentor(mode="medium"),
        SynonymAugmentor(prob=0.5),
    ]
    ConfigValidator.validate(augms)

if __name__ == "__main__":
    ok_pipeline()
    try:
        bad_order()
    except ValueError as e:
        print("❌ Ожидаемая ошибка порядка:", e)