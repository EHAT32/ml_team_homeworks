# Переводчик на базе LLM

![Анимация](gifs/llm-demo.gif)

## Установка и запуск

Сперва потребуется [Docker](https://www.docker.com/)

Клонируем исходный репозиторий

```
git clone https://github.com/EHAT32/ml_team_homeworks.git
```

Заходим в репозиторий проекта:
```
cd translator
```
В корневой папке создаем файл .env и добавляем токен с сайта [openrouter](https://bothub.chat/en/profile/for-developers)

Содержание файла backend/.env:
```
API_KEY=KEY
API_URL=https://bothub.chat/api/v2/openai/v1/chat/completions
MODEL_NAME=gpt-4o
```
Вводим далее команду:
```
docker compose up -d 
```

Сервис разворачивается локально, для его тестирования перейдите по следующему адресу в браузере

```
http://127.0.0.1:5001/
```
