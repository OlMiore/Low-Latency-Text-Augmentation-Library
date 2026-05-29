# benchmark_basic.py
import time
from statistics import median

def benchmark(augmentor, text, runs=1000):
    times = []
    for _ in range(runs):
        t0 = time.time()
        augmentor(text)
        times.append((time.time() - t0) * 1000)
    return {
        "p50": median(times),
        "p95": sorted(times)[int(0.95 * runs)],
        "p99": sorted(times)[int(0.99 * runs)],
    }
