#!/bin/bash

# 🚀 Скрипт развертывания Elena WhatsApp Bot на Railway

echo "🤖 Развертывание Elena WhatsApp Bot на Railway"
echo "================================================"

# Проверка наличия Railway CLI
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI не установлен"
    echo "📦 Установка Railway CLI..."
    npm install -g @railway/cli
fi

# Проверка авторизации в Railway
if ! railway whoami &> /dev/null; then
    echo "🔐 Авторизация в Railway..."
    railway login
fi

# Создание нового проекта Railway
echo "🏗️ Создание проекта Railway..."
railway init

# Настройка переменных окружения
echo "⚙️ Настройка переменных окружения..."
railway variables set TWILIO_ACCOUNT_SID="$TWILIO_ACCOUNT_SID"
railway variables set TWILIO_AUTH_TOKEN="$TWILIO_AUTH_TOKEN"
railway variables set TWILIO_PHONE_NUMBER="$TWILIO_PHONE_NUMBER"
railway variables set OPENAI_API_KEY="$OPENAI_API_KEY"

# Развертывание
echo "🚀 Развертывание приложения..."
railway up

# Получение URL приложения
echo "🌐 Получение URL приложения..."
APP_URL=$(railway status --json | jq -r '.url')

echo "✅ Развертывание завершено!"
echo "🌐 URL приложения: $APP_URL"
echo "🔗 Webhook URL: $APP_URL/webhook"
echo ""
echo "📋 Следующие шаги:"
echo "1. Настройте webhook в Twilio Console: $APP_URL/webhook"
echo "2. Протестируйте бота: $APP_URL/health"
echo "3. Проверьте логи: railway logs" 