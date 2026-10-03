import joblib

from app.core.config import MODEL_PATH


model = joblib.load(MODEL_PATH)


def predict(text: str) -> tuple[str, float]:
    probabilities = model.predict_proba([text])[0]
    best_index = probabilities.argmax()

    intent = str(model.classes_[best_index])
    confidence = float(probabilities[best_index])

    return intent, confidence