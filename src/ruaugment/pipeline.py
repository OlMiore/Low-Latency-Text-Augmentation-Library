<<<<<<< HEAD
import time
=======
# pipeline.py
>>>>>>> 7952769343f788334f394c9dbaeb962b5f7c9fca
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

<<<<<<< HEAD
        latency = (time.time() - start) * 1000
        print(f"=== Пайплайн завершён за {latency:.2f} ms ===")
        return text
=======
        print("=== Пайплайн завершён ===")
        return text
>>>>>>> 7952769343f788334f394c9dbaeb962b5f7c9fca
