from pathlib import Path
import joblib

class TextVectorizer:
    def __init__(self, filename="tfidf_vectorizer.joblib"):
        path = Path(__file__).resolve().parent.parent / "models" / filename

        if not path.exists():
            raise FileNotFoundError(f"No se encontró el vectorizador en {path}")

        self.vectorizer = joblib.load(path)

    def vectorize(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        return self.vectorizer.transform(texts)
