from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image
import base64
import io
from io import BytesIO
from infer_triton import InferenceModule

app = FastAPI()

inference_module = InferenceModule()  # Инициализируем модуль инференса

@app.post("/detect/", description="Выполняет детекцию номерных знаков на изображении.")
async def detect(
    file: UploadFile = File(..., description="Изображение для детекции"),
    model_name: str = "detect_onnx"
):
    """
    Выполнить детекцию объектов на изображении.

    Args:
        file (UploadFile): Загружаемое изображение.
        model_name (str): Имя модели тритона для использования

    Returns:
        StreamingResponse: Изображение с обработкой
    """
    try:
        contents = await file.read()
        img_base64 = base64.b64encode(contents).decode("utf-8")

        image_with_boxes = await inference_module.infer_and_blur_plates(img_base64, model_name)

        # Конвертируем изображение в поток
        img_byte_arr = io.BytesIO()
        image_with_boxes.save(img_byte_arr, format=image_with_boxes.format or 'PNG')
        img_byte_arr.seek(0)

        return StreamingResponse(img_byte_arr, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке: {str(e)}")