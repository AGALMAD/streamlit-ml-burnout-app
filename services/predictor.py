from pathlib import Path
import joblib
from services.vectorizer import TextVectorizer

class TextPredictor:
    def __init__(self, model_filename="svm_calibrated_model.joblib",
                 vectorizer_filename="tfidf_vectorizer.joblib"):

        model_path = Path(__file__).resolve().parent.parent / "models" / model_filename

        if not model_path.exists():
            raise FileNotFoundError(f"No se encontró el modelo en {model_path}")

        self.model = joblib.load(model_path)
        self.vectorizer = TextVectorizer(vectorizer_filename)

    def predict(self, text):
        X_input = self.vectorizer.vectorize(text)

        pred_class = self.model.predict(X_input)[0]
        pred_proba = self.model.predict_proba(X_input).max()

        return {
            "prediction": str(pred_class),
            "probability": float(pred_proba)
        }
