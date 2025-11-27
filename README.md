# Animal Classifier API

API для распознавания кошек и собак на изображениях с использованием FastAPI.

## Клиентский путь

Пользователи могут загружать фотографии животных и получать автоматическое определение, кошка или собака изображена на фото. Сервис полезен для сортировки фотогалерей, организации медиафайлов и образовательных целей.

## Требования

- Python 3.8+
- uv (современный менеджер пакетов Python)
- Поддерживаемые форматы: JPEG, PNG
- Максимальный размер файла: 5 МБ

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yakovlevasp/dataops_hw_fapi
cd animal_classifier
```

2. Установите зависимости
```bash
uv pip install -r requirements.txt
```
3. Запустите сервер:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API Endpoints

#### GET /
Информация о API и доступных эндпоинтах.

#### GET /health
Проверка статуса сервиса.

#### POST /predict
Загрузка изображения для классификации.

Тело запроса: form-data с файлом изображения

Успешный ответ (200):
```
{
  "prediction": "cat",
  "confidence": 0.8543,
  "status": "success",
  "image_format": "jpeg"
}
```
Пример запроса с curl:
```
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@image.jpg"
```

### Документация
После запуска сервера документация доступна по адресу:

Swagger UI: http://localhost:8000/docs


### Тестирование
Запуск тестов:
```bash
uv run pytest tests/
```


