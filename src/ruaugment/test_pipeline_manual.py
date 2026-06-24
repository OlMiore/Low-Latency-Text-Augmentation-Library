import logging
from .base import set_seed
from .pipeline import Pipeline
from .synonym import SynonymAugmentor
from .morph import MorphAugmentor
from .char import CharNoiseAugmentor
from .deletion import RandomDeletionAugmentor

# Устанавливаем сид для детерминизма
set_seed(42)

logging.basicConfig(level=logging.DEBUG)

def main():
    text = "Кредит и деньги были важны для клиента"

    augmentors = [
        SynonymAugmentor(prob=0.5),
        MorphAugmentor(prob=0.5),
        CharNoiseAugmentor(mode="medium"),
        RandomDeletionAugmentor(prob=0.2),
    ]

    pipeline = Pipeline(augmentors)

    print("\n=== Тест одиночной строки ===")
    print("Исходный текст:", text)
    print("Результат:", pipeline(text))

    print("\n=== Тест батча ===")
    batch = [
        "Клиент запросил кредит",
        "Деньги были перечислены",
        "Проект был завершён успешно"
    ]
    results = pipeline(batch)
    for original, augmented in zip(batch, results):
        print(f"{original}  →  {augmented}")

if __name__ == "__main__":
    main()