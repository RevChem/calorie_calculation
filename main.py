from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from PIL import Image
from ultralytics import YOLO
import os
from fastapi.responses import StreamingResponse
import io


# Загружаем обученную модель
model = YOLO("weights/best1.pt") 
app = FastAPI()


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    image = Image.open(file_path)
    results = model(image)

    # Рисуем bounding boxes на изображении
    plotted_img = results[0].plot()

    os.remove(file_path)

    # Конвертируем изображение в байты для ответа
    img_bytes = io.BytesIO()
    Image.fromarray(plotted_img[..., ::-1].copy()).save(img_bytes, format="JPEG")  # BGR -> RGB


    return StreamingResponse(io.BytesIO(img_bytes.getvalue()), media_type="image/jpeg")