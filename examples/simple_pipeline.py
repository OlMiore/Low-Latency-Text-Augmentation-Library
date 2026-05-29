import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from ruaugment.char import CharNoiseAugmentor
from ruaugment.synonym import SynonymAugmentor
from ruaugment.deletion import RandomDeletionAugmentor
from ruaugment.pipeline import Pipeline

pipeline = Pipeline([
    CharNoiseAugmentor(prob=0.05),
    SynonymAugmentor(),
    RandomDeletionAugmentor(prob=0.1),
])

if __name__ == "__main__":
    text = "кредит и деньги важны"
    print("Исходный текст:", text)
    print("Аугментированный:", pipeline(text))
