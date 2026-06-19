from .char import CharNoiseAugmentor

text = "кредит и деньги важны"

for mode in ("mild", "medium", "chaos"):
    print(f"\n=== Режим: {mode} ===")
    aug = CharNoiseAugmentor(mode=mode)
    for i in range(5):
        print(f"{i+1:02d}. {aug(text)}")