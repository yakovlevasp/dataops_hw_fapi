import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Тест проверки статуса сервиса."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_success():
    """Happy Path: тест успешного предсказания."""
    # Создаем тестовое изображение (минимальный валидный JPEG)
    test_image = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00' + b'0' * 100
    
    files = {"file": ("test.jpg", test_image, "image/jpeg")}
    response = client.post("/predict", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
    assert "status" in data
    assert data["status"] == "success"
    assert data["prediction"] in ["cat", "dog"]
    assert 0.75 <= data["confidence"] <= 1.0

def test_predict_invalid_file_type():
    """Bad Input: тест с неверным типом файла."""
    files = {"file": ("test.txt", b"invalid file content", "text/plain")}
    response = client.post("/predict", files=files)
    
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]

def test_predict_empty_file():
    """Bad Input: тест с пустым файлом."""
    files = {"file": ("empty.jpg", b"", "image/jpeg")}
    response = client.post("/predict", files=files)
    
    assert response.status_code == 500
    assert "Error processing image" in response.json()["detail"]