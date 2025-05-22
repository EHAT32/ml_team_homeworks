FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей для OpenCV
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        curl \
        software-properties-common \
        libgl1 \
        libglib2.0-0 \
        ffmpeg \
        && rm -rf /var/lib/apt/lists/*

# Сначала копируем только requirements.txt и устанавливаем зависимости
COPY ./api-service/requirements.txt /app
RUN pip3 install -r requirements.txt

# Затем копируем остальной код
COPY ./api-service /app

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000"]