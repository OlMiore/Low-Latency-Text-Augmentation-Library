import logging
from .pipeline import Pipeline
from .char import CharNoiseAugmentor

logger = logging.getLogger(__name__)

class CharNoisePipeline(Pipeline):
    """
    Специализированный пайплайн, который применяет только CharNoiseAugmentor.
    Удобен для демонстрации шумовых ошибок и тестирования.
    """

    def __init__(self, mode="mild"):
        augmentors = [CharNoiseAugmentor(mode=mode)]
        super().__init__(augmentors)