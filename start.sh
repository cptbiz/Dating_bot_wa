#!/bin/bash

# 🚀 Скрипт запуска Elena WhatsApp Bot

echo "🤖 Запуск Elena WhatsApp Bot..."
echo "=================================="

# Проверка переменных окружения
echo "📋 Проверка переменных окружения:"
echo "PORT: ${PORT:-5000}"
echo "TWILIO_ACCOUNT_SID: ${TWILIO_ACCOUNT_SID:+SET}"
echo "OPENAI_API_KEY: ${OPENAI_API_KEY:+SET}"

# Запуск приложения
echo "🚀 Запуск Gunicorn..."
exec gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 1 --timeout 120 --keep-alive 5 --log-level info app:app 