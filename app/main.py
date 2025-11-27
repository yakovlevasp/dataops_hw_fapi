from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.model import load_model, predict
import io
from PIL import Image

app = FastAPI(
    title="Animal Classifier API",
    description="API для распознавания кошек и собак на изображениях",
    version="1.0.0"
)

# Глобальная переменная для хранения модели
model = None

@app.on_event("startup")
async def startup_event():
    """Загрузка модели при старте приложения."""
    global model
    model = load_model()

def validate_image_format(image_bytes: bytes) -> str:
    """
    Проверяет формат изображения с помощью PIL.
    Возвращает 'jpeg', 'png' или вызывает исключение.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        format_name = image.format.lower()
        
        if format_name in ['jpeg', 'jpg', 'png']:
            return 'jpeg' if format_name == 'jpg' else format_name
        else:
            raise ValueError(f"Unsupported image format: {format_name}")
    except Exception as e:
        raise ValueError(f"Invalid image file: {str(e)}")

@app.get("/")
async def root():
    """Корневой эндпоинт с информацией о API."""
    return {
        "message": "Animal Classifier API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Проверка статуса сервиса."""
    return {"status": "ok"}

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    """
    Эндпоинт для предсказания класса изображения (кошка/собака).
    
    - **file**: Изображение в формате JPEG или PNG
    """
    # Проверка имени файла
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided"
        )
    
    # Получение содержимого файла
    contents = await file.read()
    
    if len(contents) == 0:
        raise HTTPException(
            status_code=400,
            detail="Empty file provided"
        )
    
    # Проверка размера файла (5 МБ максимум)
    if len(contents) > 5 * 1024 * 1024:  # 5 МБ в байтах
        raise HTTPException(
            status_code=400,
            detail="File size too large. Maximum size is 5MB."
        )
    
    try:
        # Проверка формата изображения с помощью PIL
        image_format = validate_image_format(contents)
        
        # Дополнительная проверка расширения файла
        file_extension = file.filename.lower().split('.')[-1]
        if file_extension not in ['jpg', 'jpeg', 'png']:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file extension. Please upload JPEG or PNG image. Got: .{file_extension}"
            )
            
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error validating image: {str(e)}"
        )
    
    try:
        # Получение предсказания
        result = predict(model, contents)
        return {
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "status": "success",
            "image_format": image_format
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)