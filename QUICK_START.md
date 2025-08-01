# 🚀 Быстрый старт WhatsApp бота

## 📋 Что получилось

Создан полноценный WhatsApp-бот для BeHappy2Day с функциями:

- ✅ Автоматическая квалификация лидов
- ✅ Проверка на нарушения правил сайта
- ✅ Естественные диалоги с эмодзи
- ✅ Сохранение лидов в JSON/БД
- ✅ Готов к развертыванию на Heroku/Railway

## 🔧 Быстрая настройка

### 1. Клонирование
```bash
git clone https://github.com/cptbiz/Dating_bot_wa.git
cd Dating_bot_wa
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка переменных окружения
```bash
cp env.example .env
# Отредактируйте .env файл с вашими данными Twilio
```

### 4. Тестирование
```bash
python3 simple_test.py
```

### 5. Запуск
```bash
python3 app.py
```

## 📱 Настройка Twilio

1. Зарегистрируйтесь на [console.twilio.com](https://console.twilio.com/)
2. Получите Account SID и Auth Token
3. Настройте WhatsApp Sandbox
4. Установите webhook URL: `https://your-domain.com/webhook`

## 🌐 Развертывание

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

### Railway
```bash
# Подключите GitHub репозиторий к Railway
# Добавьте переменные окружения
```

### Docker
```bash
docker-compose up -d
```

## 📊 Мониторинг

- Проверка здоровья: `curl http://localhost:5000/health`
- Лиды сохраняются в `leads.json`
- Логи в консоли

## 🛡️ Безопасность

Бот автоматически проверяет:
- ❌ Передачу контактов
- ❌ Обсуждение несовершеннолетних
- ❌ Просьбы о деньгах/подарках
- ❌ Грубость и нецензурную лексику

## 📞 Поддержка

- 📧 Email: polovinka@behappy2day.com
- 🌐 Сайт: https://behappy2day.com
- 📱 WhatsApp: Настройте через Twilio

---

**Готово! 🎉 Бот успешно загружен в GitHub и готов к использованию!** 