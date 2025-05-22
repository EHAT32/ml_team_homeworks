FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y build-essential libgl1 && \
    rm -rf /var/lib/apt/lists/*

COPY web-service/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY web-service /app/

# Команда запуска
CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0"]