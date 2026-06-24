from .base import set_seed
from .deletion import RandomDeletionAugmentor

# Устанавливаем сид для детерминизма
set_seed(42)

text = "кредит и деньги важны"

for p in [0.1, 0.5, 1.0]:
    aug = RandomDeletionAugmentor(prob=p, min_tokens_left=1)
    print(f"\nprob={p}")
    for _ in range(5):
        print(" →", aug(text))