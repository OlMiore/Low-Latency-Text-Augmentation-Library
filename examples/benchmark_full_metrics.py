import time
import csv
import sys
import os
import numpy as np

# Добавляем путь к src
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from ruaugment import (
    Pipeline,
    CharNoiseAugmentor,
    SynonymAugmentor,
    RandomDeletionAugmentor,
    RandomSwapAugmentor,
    MorphAugmentor,
)
from ruaugment.base import set_seed

# ------------------ Детерминизм ------------------

set_seed(42)

# ------------------ Репрезентативные тексты ------------------

REAL_TEXTS = [
    "Банк одобрил кредит клиенту после проверки документов.",
    "Финансовые операции требуют строгого соблюдения регуляторных норм.",
    "Клиент обратился в службу поддержки для уточнения условий договора.",
    "Компания сообщила о росте прибыли за последний квартал.",
    "Система автоматически обработала транзакцию без задержек.",
]

def generate_dataset(n, base_texts):
    """Создаёт датасет из реальных текстов, а не повторяющихся токенов."""
    out = []
    for i in range(n):
        out.append(base_texts[i % len(base_texts)])
    return out

# ------------------ Метрики ------------------

def measure_latency(pipeline, text, runs=200):
    latencies = []
    for _ in range(runs):
        t0 = time.perf_counter()
        pipeline(text)
        latencies.append((time.perf_counter() - t0) * 1000)

    return {
        "p50": float(np.percentile(latencies, 50)),
        "p95": float(np.percentile(latencies, 95)),
        "p99": float(np.percentile(latencies, 99)),
    }


def measure_throughput(pipeline, texts, batch_size):
    """Корректный throughput: обрабатываем батчами."""
    batches = [texts[i:i + batch_size] for i in range(0, len(texts), batch_size)]

    t0 = time.perf_counter()
    for batch in batches:
        pipeline(batch)  # batch-mode
    total_time = time.perf_counter() - t0

    return len(texts) / total_time if total_time > 0 else 0.0

# ------------------ Пайплайн ------------------

pipeline = Pipeline([
    SynonymAugmentor(prob=0.5),
    MorphAugmentor(prob=0.5),
    CharNoiseAugmentor(mode="medium"),
    RandomSwapAugmentor(prob=0.1),
    RandomDeletionAugmentor(prob=0.1),
])

# ------------------ 1. Latency ------------------

print("=== LATENCY BENCHMARK ===")

latency_results = []
for label, text in [
    ("short", REAL_TEXTS[0]),
    ("medium", REAL_TEXTS[1] + " " + REAL_TEXTS[2]),
    ("long", " ".join(REAL_TEXTS * 5)),
]:
    metrics = measure_latency(pipeline, text, runs=200)
    print(f"[{label}] p50={metrics['p50']:.2f} ms, p95={metrics['p95']:.2f} ms, p99={metrics['p99']:.2f} ms")
    latency_results.append({
        "scenario": label,
        "p50_ms": round(metrics["p50"], 2),
        "p95_ms": round(metrics["p95"], 2),
        "p99_ms": round(metrics["p99"], 2),
    })

# ------------------ 2. Throughput ------------------

print("\n=== THROUGHPUT BENCHMARK ===")

texts_for_throughput = generate_dataset(1024, REAL_TEXTS)
batch_sizes = [8, 16, 32, 64]

throughput_results = []
for bs in batch_sizes:
    thr = measure_throughput(pipeline, texts_for_throughput, batch_size=bs)
    print(f"batch_size={bs} -> throughput={thr:.2f} samples/sec")
    throughput_results.append({
        "batch_size": bs,
        "samples": len(texts_for_throughput),
        "throughput_samples_per_sec": round(thr, 2),
    })

# ------------------ 3. Сохранение ------------------

root_dir = os.path.join(os.path.dirname(__file__), "..")

with open(os.path.join(root_dir, "metrics_latency.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=latency_results[0].keys())
    writer.writeheader()
    writer.writerows(latency_results)

with open(os.path.join(root_dir, "metrics_throughput.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=throughput_results[0].keys())
    writer.writeheader()
    writer.writerows(throughput_results)

print("\nMetrics saved.")