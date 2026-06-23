from .synonym import SynonymAugmentor

text = "Кредит и деньги — важный ресурс"

for p in [0.1, 0.5, 1.0]:
    aug = SynonymAugmentor(prob=p)
    print(f"\nprob={p}")
    for _ in range(5):
        print(" →", aug(text))