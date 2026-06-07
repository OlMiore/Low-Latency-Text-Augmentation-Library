import time
from .validator import ConfigValidator

class Pipeline:
    def __init__(self, augmentors):
        self.augmentors = augmentors
        ConfigValidator().validate(augmentors)

    def __call__(self, text: str) -> str:
        start = time.time()
        print("=== Запуск пайплайна ===")
        print("Исходный текст:", text)

        for aug in self.augmentors:
            print(f"→ {aug.__class__.__name__}")
            text = aug(text)
            print("   ", text)

        latency = (time.time() - start) * 1000
        print(f"=== Пайплайн завершён за {latency:.2f} ms ===")
        return text