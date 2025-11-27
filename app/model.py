import random

def load_model():
    """Симуляция загрузки модели для классификации изображений."""
    print("Загрузка модели распознавания...")
    return {"version": "1.0-images"}

def predict(model: dict, image_bytes: bytes) -> dict:
    """Симуляция предсказания по изображению."""
    if len(image_bytes) < 100:  # Простая проверка, что данные не пустые
        raise ValueError("Invalid image data provided")
    
    prediction = random.choice(["cat", "dog"])
    confidence = random.uniform(0.75, 0.99)
    
    return {
        "prediction": prediction, 
        "confidence": round(confidence, 4)
    }