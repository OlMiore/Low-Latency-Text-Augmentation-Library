from .swap import RandomSwapAugmentor

text = "кредит и деньги важны"

for p in [0.1, 0.5, 1.0]:
    aug = RandomSwapAugmentor(prob=p)
    print(f"\nprob={p}")
    for _ in range(5):
        print(" →", aug(text))