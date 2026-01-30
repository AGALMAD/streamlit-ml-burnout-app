import joblib
import os
import json
import numpy as np
from services.vectorizer import TextVectorizer

class TextPredictor:
    def __init__(self, model_path="svm_calibrated_model.joblib"):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"No se encontró el modelo en {model_path}")
        
        self.model = joblib.load(model_path)
        self.vectorizer = TextVectorizer()
    
    def predict(self, text):

        # Transformar texto
        X_input = self.vectorizer.vectorize(text)

        # Predicción
        pred_class = self.model.predict(X_input)[0]
        pred_proba = self.model.predict_proba(X_input).max()

        # Crear JSON
        result = {
            "prediction": str(pred_class),
            "probability": float(pred_proba) if pred_proba is not None else None
        }
        return json.dumps(result)
