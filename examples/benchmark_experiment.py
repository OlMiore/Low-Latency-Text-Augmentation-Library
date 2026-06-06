import time
import csv
import sys
import os

# Добавляем путь к src, чтобы можно было импортировать ruaugment
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from ruaugment import (
    Pipeline,
    CharNoiseAugmentor,
    SynonymAugmentor,
    RandomDeletionAugmentor,
    RandomSwapAugmentor,
    MorphAugmentor,
)

texts = [
    "кредит и деньги важны",
    "финансы играют ключевую роль",
    "важно понимать экономику",
    "деньги решают многое",
    "кредит помогает бизнесу",
]

pipeline = Pipeline([
    CharNoiseAugmentor(prob=0.05),
    SynonymAugmentor(),
    MorphAugmentor(),
    RandomSwapAugmentor(swaps=1),
    RandomDeletionAugmentor(prob=0.1),
])

results = []
latencies = []

print("=== Запуск эксперимента ===")

for i, text in enumerate(texts, start=1):
    start = time.time()
    augmented = pipeline(text)
    latency = (time.time() - start) * 1000
    latencies.append(latency)
    results.append({
        "iteration": i,
        "input_text": text,
        "output_text": augmented,
        "latency_ms": round(latency, 2),
    })
    print(f"[{i}] {text} → {augmented} ({latency:.2f} ms)")

# Запись метрик в CSV в корень проекта
csv_path = os.path.join(os.path.dirname(__file__), "..", "metrics.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

avg_latency = sum(latencies) / len(latencies)
print(f"\nСредняя задержка: {avg_latency:.2f} ms")
print(f"Метрики сохранены в {csv_path}")