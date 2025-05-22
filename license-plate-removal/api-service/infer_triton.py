import os
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import grpc
import cv2

import tritonclient.grpc.aio as grpcclient
from tritonclient.grpc import service_pb2, service_pb2_grpc
from tritonclient.utils import triton_to_np_dtype


class InferenceModule:
    def __init__(self) -> None:
        self.url = os.environ.get("TRITON_SERVER_URL", "127.0.0.1:8001")
        self.triton_client = grpcclient.InferenceServerClient(url=self.url)

    async def infer_and_blur_plates(self, img_b64: str, model_name: str = "detect_onnx") -> Image.Image:
        """
        Выполняет инференс модели детекции и размывает найденные номерные знаки.

        Args:
            img_b64 (str): Base64-кодированное изображение.
            model_name (str): Имя модели на сервере Triton.

        Returns:
            Image.Image: Изображение с размытыми номерными знаками.
        """
        # Декодируем изображение
        pil_img = self.decode_img(img_b64)
        original_size = pil_img.size

        # Получаем параметры модели
        model_meta, _ = self.parse_model_metadata(model_name)
        input_shape = model_meta.inputs[0].shape
        _, c, h, w = input_shape  # например [3, 640, 640]

        # Предобработка
        img_np = self.preprocess_image(img_b64, target_size=(w, h))

        # Подготовка входа для Triton
        dtype = model_meta.inputs[0].datatype
        inputs = [grpcclient.InferInput(model_meta.inputs[0].name, [1, c, h, w], dtype)]
        inputs[0].set_data_from_numpy(img_np.astype(triton_to_np_dtype(dtype)))

        outputs = [grpcclient.InferRequestedOutput(model_meta.outputs[0].name)]

        # Инференс
        results = await self.triton_client.infer(
            model_name=model_name,
            inputs=inputs,
            outputs=outputs
        )

        # Получаем выход
        output = results.as_numpy(model_meta.outputs[0].name)
        detections = np.transpose(output[0], (1, 0))

        # Фильтрация по уверенности
        confidence_threshold = 0.5
        valid_detections = detections[detections[:, 4] > confidence_threshold]

        # Размываем номера
        blurred_img = self.blur_license_plates(pil_img, valid_detections, original_size, (w, h))
        return blurred_img

    def blur_license_plates(self, img: Image.Image, detections: np.ndarray, original_size, model_size) -> Image.Image:
        """
        Размывает области с номерными знаками на изображении с использованием эллипса

        Args:
            img: Оригинальное изображение (PIL.Image)
            detections: Массив [N, 5] с координатами x, y, w, h, conf
            original_size: Размер оригинального изображения (W, H)
            model_size: Размер входа модели

        Returns:
            Image.Image: Изображение с размытыми номерными знаками
        """
        image_np = np.array(img)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        scale_x = original_size[0] / model_size[0]
        scale_y = original_size[1] / model_size[1]

        for det in detections:
            xc, yc, wc, hc, conf = det[:5]
            xc, yc = int(xc * scale_x), int(yc * scale_y)
            wc, hc = int(wc * scale_x), int(hc * scale_y)

            x_min = max(0, xc - wc // 2)
            y_min = max(0, yc - hc // 2)
            x_max = min(original_size[0], xc + wc // 2)
            y_max = min(original_size[1], yc + hc // 2)

            if x_max <= x_min or y_max <= y_min:
                continue

            # Создаем маску в виде эллипса
            mask = np.zeros(image_np.shape[:2], dtype=np.uint8)
            center = (xc, yc)
            axes = (wc // 2, hc // 2)
            cv2.ellipse(mask, center, axes, angle=0, startAngle=0, endAngle=360, color=255, thickness=-1)

            # Размываем изображение
            blurred = cv2.GaussianBlur(image_np, (51, 51), 0)

            # Накладываем размытие только на область эллипса
            mask_inv = cv2.bitwise_not(mask)
            foreground = cv2.bitwise_and(image_np, image_np, mask=mask_inv)
            background = cv2.bitwise_and(blurred, blurred, mask=mask)
            combined = cv2.add(foreground, background)

            image_np = combined

        # Возвращаем обратно в RGB для PIL
        image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        return Image.fromarray(image_np)

    def preprocess_image(self, img_b64: str, target_size=(640, 640)) -> np.ndarray:
        """Предобработка: resize + нормализация"""
        pil_img = self.decode_img(img_b64).convert("RGB")
        pil_img = pil_img.resize(target_size, Image.BILINEAR)
        img_np = np.array(pil_img).astype(np.float32) / 255.0
        img_np = np.transpose(img_np, (2, 0, 1))  # HWC -> CHW
        img_np = np.expand_dims(img_np, axis=0)  # CHW -> BCHW
        return img_np

    @staticmethod
    def decode_img(img_base64: str) -> Image.Image:
        """Декодирует base64-строку в объект PIL.Image"""
        if img_base64.startswith("data:image/"):
            header, encoded = img_base64.split(",", 1)
        else:
            encoded = img_base64
        img_bytes = base64.b64decode(encoded)
        return Image.open(BytesIO(img_bytes)).convert("RGB")

    def parse_model_metadata(self, model_name: str):
        """Получает метаданные модели через gRPC"""
        channel = grpc.insecure_channel(self.url)
        grpc_stub = service_pb2_grpc.GRPCInferenceServiceStub(channel)
        metadata_request = service_pb2.ModelMetadataRequest(name=model_name)
        metadata_response = grpc_stub.ModelMetadata(metadata_request)
        config_request = service_pb2.ModelConfigRequest(name=model_name)
        config_response = grpc_stub.ModelConfig(config_request)
        return metadata_response, config_response