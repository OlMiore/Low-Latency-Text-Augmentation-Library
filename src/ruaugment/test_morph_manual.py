from .morph import MorphAugmentor

text = "Кредит и деньги были важны для клиента в новом проекте"

for p in [0.1, 0.5, 1.0]:
    print(f"\nprob={p}")
    aug = MorphAugmentor(prob=p)
    for _ in range(5):
        print(" →", aug(text))