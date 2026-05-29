from .validator import ConfigValidator

class Pipeline:
    def __init__(self, augmentors):
        self.augmentors = augmentors
        ConfigValidator().validate(augmentors)

    def __call__(self, text: str) -> str:
        print("=== Запуск пайплайна ===")
        print("Исходный текст:", text)

        for aug in self.augmentors:
            print(f"→ {aug.__class__.__name__}")
            text = aug(text)
            print("   ", text)

        print("=== Пайплайн завершён ===")
        return text
