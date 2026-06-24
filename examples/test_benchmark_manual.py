import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from ruaugment.base import set_seed
from examples.benchmark_full_metrics import measure_latency, measure_throughput, pipeline

set_seed(42)

def test_latency():
    text = "Банк одобрил кредит клиенту."
    metrics = measure_latency(pipeline, text, runs=50)
    print("Latency test:", metrics)

def test_throughput():
    texts = ["Тестовый текст"] * 128
    thr = measure_throughput(pipeline, texts, batch_size=16)
    print("Throughput test:", thr)

if __name__ == "__main__":
    test_latency()
    test_throughput()