FROM python:3.12-slim

WORKDIR /CONSPECTIUS

ENV PYTHONUNBUFFERED=1

# В Dockerfile conspectius (после установки Poetry)
RUN apt-get update && apt-get install -y ffmpeg

# Установка Poetry
RUN pip install poetry==1.8.2
    
# Копируем только файлы конфигурации Poetry перед установкой зависимостей
COPY pyproject.toml poetry.lock ./
    
# Установка зависимостей
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi
    
# Копируем остальные файлы проекта
COPY . .

CMD ["poetry", "run", "python3.12", "main.py"]
