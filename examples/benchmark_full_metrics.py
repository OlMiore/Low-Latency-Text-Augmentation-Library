import time
import csv
import sys
import os
from statistics import median

# Добавляем путь к src, чтобы импортировать ruaugment
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from ruaugment import (
    Pipeline,
    CharNoiseAugmentor,
    SynonymAugmentor,
    RandomDeletionAugmentor,
    RandomSwapAugmentor,
    MorphAugmentor,
)

# ---------- Вспомогательные функции ----------

def measure_latency(augmentor, text, runs=200):
    times = []
    for _ in range(runs):
        t0 = time.time()
        augmentor(text)
        times.append((time.time() - t0) * 1000)  # ms
    times_sorted = sorted(times)
    return {
        "p50": median(times_sorted),
        "p95": times_sorted[int(0.95 * runs) - 1],
        "p99": times_sorted[int(0.99 * runs) - 1],
    }


def measure_throughput(augmentor, texts, batch_size):
    """
    Простейшая модель throughput: обрабатываем тексты по batch_size подряд,
    считаем, сколько образцов в секунду проходит через пайплайн.
    """
    n = len(texts)
    t0 = time.time()
    i = 0
    while i < n:
        batch = texts[i:i + batch_size]
        for t in batch:
            augmentor(t)
        i += batch_size
    total_time = time.time() - t0
    samples_per_sec = n / total_time if total_time > 0 else 0.0
    return samples_per_sec


def generate_text(token, length):
    # Очень простой генератор "текстов" нужной длины
    return " ".join([token] * length)


# ---------- Конфигурация пайплайна ----------

pipeline = Pipeline([
    CharNoiseAugmentor(prob=0.05),
    SynonymAugmentor(),
    MorphAugmentor(),
    RandomSwapAugmentor(swaps=1),
    RandomDeletionAugmentor(prob=0.1),
])

# ---------- 1. Latency для разных длин текстов ----------

latency_lengths = [
    ("short_20_50", 30),    # условно 20–50 токенов
    ("medium_100_200", 150),
    ("long_300_500", 400),
]

latency_results = []

print("=== LATENCY BENCHMARK ===")

for label, length in latency_lengths:
    text = generate_text("кредит", length)
    metrics = measure_latency(pipeline, text, runs=200)
    print(f"[{label}] len={length} tokens -> p50={metrics['p50']:.2f} ms, "
          f"p95={metrics['p95']:.2f} ms, p99={metrics['p99']:.2f} ms")
    latency_results.append({
        "scenario": label,
        "length_tokens": length,
        "p50_ms": round(metrics["p50"], 2),
        "p95_ms": round(metrics["p95"], 2),
        "p99_ms": round(metrics["p99"], 2),
    })

# ---------- 2. Throughput для разных batch size ----------

batch_sizes = [8, 16, 32, 64]
throughput_results = []

# Возьмём, например, 1024 текстов средней длины
texts_for_throughput = [
    generate_text("деньги", 100) for _ in range(1024)
]

print("\n=== THROUGHPUT BENCHMARK ===")

for bs in batch_sizes:
    thr = measure_throughput(pipeline, texts_for_throughput, batch_size=bs)
    print(f"batch_size={bs} -> throughput={thr:.2f} samples/sec")
    throughput_results.append({
        "batch_size": bs,
        "samples": len(texts_for_throughput),
        "throughput_samples_per_sec": round(thr, 2),
    })

# ---------- 3. Сохраняем результаты в CSV ----------

root_dir = os.path.join(os.path.dirname(__file__), "..")

latency_csv = os.path.join(root_dir, "metrics_latency.csv")
throughput_csv = os.path.join(root_dir, "metrics_throughput.csv")

with open(latency_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=latency_results[0].keys())
    writer.writeheader()
    writer.writerows(latency_results)

with open(throughput_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=throughput_results[0].keys())
    writer.writeheader()
    writer.writerows(throughput_results)

print(f"\nLatency metrics saved to {latency_csv}")
print(f"Throughput metrics saved to {throughput_csv}")