from .base import set_seed
from .synonym import SynonymAugmentor

# Устанавливаем сид для детерминизма
set_seed(42)

text = "Кредит и деньги — важный ресурс"

for p in [0.1, 0.5, 1.0]:
    aug = SynonymAugmentor(prob=p)
    print(f"\nprob={p}")
    for _ in range(5):
        print(" →", aug(text))