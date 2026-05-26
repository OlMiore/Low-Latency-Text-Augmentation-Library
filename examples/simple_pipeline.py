from ruaugment.char import CharNoiseAugmentor
from ruaugment.deletion import RandomDeletionAugmentor
from ruaugment.synonym import SynonymAugmentor
from ruaugment.pipeline import Pipeline

pipeline = Pipeline([
    SynonymAugmentor(),
    RandomDeletionAugmentor(prob=0.1),
    CharNoiseAugmentor(prob=0.05),
])

text = "кредит одобрен"
print(pipeline(text))
