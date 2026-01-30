import joblib
import os


class TextVectorizer:
    def __init__(self, path="tfidf_vectorizer.joblib"):
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el vectorizador en {path}")
        self.vectorizer = joblib.load(path)

    def vectorize(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        return self.vectorizer.transform(texts)
