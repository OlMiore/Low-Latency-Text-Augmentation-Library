import logging
from .char_pipeline import CharNoisePipeline

logging.basicConfig(level=logging.DEBUG)

def main():
    text = "Кредит и деньги были важны для клиента в новом проекте"

    print("\n=== mild ===")
    pipe = CharNoisePipeline(mode="mild")
    print(pipe(text))

    print("\n=== medium ===")
    pipe = CharNoisePipeline(mode="medium")
    print(pipe(text))

    print("\n=== chaos ===")
    pipe = CharNoisePipeline(mode="chaos")
    print(pipe(text))

if __name__ == "__main__":
    main()