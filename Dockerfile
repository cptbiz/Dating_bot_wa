FROM python:3.9-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование файла зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Создание пользователя для безопасности
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Открытие порта
EXPOSE 5000

# Делаем скрипт запуска исполняемым
RUN chmod +x start.sh

# Запуск приложения через скрипт
CMD ["./start.sh"] 