# 🤖 Elena - WhatsApp Dating Bot для BeHappy2Day

**Elena** - это интеллектуальный WhatsApp бот, который общается как настоящая девушка с американскими мужчинами 40+ на сайте знакомств BeHappy2Day.

## 🌟 Особенности

* 🤖 **GPT-4 Turbo интеграция** - естественное общение с ИИ
* 🎤 **Голосовые сообщения** - распознавание и транскрипция речи
* 👩‍🦰 **Персонализация** - Elena, 28 лет, из Украины, Marketing Manager
* 💬 **Английский язык** - общение с американскими мужчинами 40+
* 🛡️ **Безопасность** - проверка на нарушения правил сайта
* 📊 **Аналитика** - отслеживание диалогов и лидов
* 🚀 **Railway** - готов к развертыванию в облаке

## 👩‍🦰 О Elena

**Elena** - это виртуальная девушка, которая общается с американскими мужчинами 40+:

* **Возраст**: 28 лет
* **Страна**: Украина, Киев
* **Профессия**: Marketing Manager
* **Интересы**: путешествия, кулинария, чтение, йога, фотография
* **Языки**: английский, украинский, русский
* **Характер**: теплая, заботливая, умная, независимая

## 📋 Требования

* Python 3.8+
* Twilio Account (WhatsApp Business API)
* OpenAI API Key (GPT-4 Turbo)
* Railway Account (для развертывания)

## 🚀 Быстрая установка

### 1. Клонирование репозитория

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
```

Отредактируйте `.env` файл:

```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=whatsapp:+1234567890

# OpenAI GPT-4 Turbo Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Railway Configuration
RAILWAY_STATIC_URL=your_railway_app_url_here
```

### 4. Тестирование

```bash
python3 test_girl_bot.py
```

### 5. Запуск

```bash
python3 app.py
```

## 🎤 Голосовые сообщения

Бот поддерживает распознавание голосовых сообщений:

* 📱 Получает голосовые сообщения через Twilio
* 🎵 Конвертирует аудио в текст
* 💬 Обрабатывает транскрипцию как обычное сообщение
* 🔄 Отвечает естественным образом

## 🤖 GPT-4 Turbo интеграция

Elena использует GPT-4 Turbo для естественного общения:

* 🧠 **Системный промпт** - определяет личность Elena
* 💭 **История диалога** - помнит предыдущие сообщения
* 🎯 **Целевая аудитория** - американские мужчины 40+
* 💕 **Эмодзи** - естественное использование смайликов
* 🛡️ **Правила** - соблюдение политики сайта

## 🛡️ Проверка нарушений

Бот автоматически проверяет сообщения на:

* ❌ Передачу контактов (телефон, email, соцсети)
* ❌ Просьбы о деньгах/подарках
* ❌ Грубость и нецензурную лексику
* ❌ Политические темы
* ❌ Спам и рекламу

## 🚀 Развертывание на Railway

### 1. Подключение к Railway

1. Зарегистрируйтесь на [railway.app](https://railway.app)
2. Подключите GitHub репозиторий
3. Выберите репозиторий `Dating_bot_wa`

### 2. Настройка переменных окружения

В Railway Dashboard добавьте:

```env
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=whatsapp:+1234567890
OPENAI_API_KEY=your_openai_api_key
```

### 3. Развертывание

Railway автоматически:

* Установит зависимости из `requirements.txt`
* Запустит приложение с Gunicorn
* Настроит HTTPS и домен

### 4. Настройка Twilio Webhook

В Twilio Console установите webhook URL:

```
https://your-app.railway.app/webhook
```

## 📱 Примеры диалогов

### Нормальный диалог

```
👤 User: Hi Elena, I'm John from California. I'm 45 and work as an engineer.
💕 Elena: Hi there! I'm Elena from Ukraine. I'm 28 and I work as a Marketing Manager. I love traveling and cooking! What about you? 💕

👤 User: I work in software development. I enjoy hiking and cooking in my free time.
💕 Elena: That sounds wonderful! I really enjoy meeting new people and learning about different cultures. What do you do for work? 😊
```

### Голосовое сообщение

```
🎤 User: [Voice message] "Hi Elena, this is Mike from Texas. I'm 48."
💕 Elena: Hi there! I'm Elena from Ukraine. I'm 28 and I work as a Marketing Manager. I love traveling and cooking! What about you? 💕
```

### Нарушение правил

```
👤 User: Can I get your phone number?
💕 Elena: I'd love to chat more, but I prefer to keep our conversation here for now! Maybe we can meet in person someday? 😊
```

## 📊 Мониторинг

### Проверка здоровья

```bash
curl https://your-app.railway.app/health
```

### Логи Railway

* Откройте Railway Dashboard
* Перейдите в раздел "Deployments"
* Просмотрите логи в реальном времени

### Аналитика

* Диалоги сохраняются в памяти (в продакшене - Redis/БД)
* Статистика доступна через `/health` endpoint
* Логи в Railway Dashboard

## 🔧 Настройка для BeHappy2Day

### Правила сайта

Elena соблюдает все правила BeHappy2Day:

* ✅ Не передает контакты вне платформы
* ✅ Не просит деньги или подарки
* ✅ Общается вежливо и уважительно
* ✅ Фокусируется на серьезных отношениях
* ✅ Перенаправляет на сайт для продолжения

### Интеграция с CRM

Для полной интеграции добавьте:

1. **База данных**: PostgreSQL для хранения диалогов
2. **Email уведомления**: Новые лиды на email
3. **API интеграция**: Подключение к CRM системе
4. **Аналитика**: Отслеживание конверсии

## 🐛 Устранение неполадок

### Проблемы с Twilio

1. Проверьте правильность Account SID и Auth Token
2. Убедитесь, что webhook URL доступен из интернета
3. Проверьте логи в Twilio Console

### Проблемы с OpenAI

1. Проверьте правильность API Key
2. Убедитесь, что есть кредиты для GPT-4 Turbo
3. Проверьте лимиты API

### Проблемы с Railway

1. Проверьте переменные окружения
2. Убедитесь, что все зависимости установлены
3. Проверьте логи в Railway Dashboard

### Проблемы с голосовыми сообщениями

1. Убедитесь, что установлен ffmpeg
2. Проверьте права доступа к временным файлам
3. Проверьте подключение к Google Speech API

## 📞 Поддержка

* 📧 Email: polovinka@behappy2day.com
* 🌐 Сайт: https://behappy2day.com
* 📱 WhatsApp: Настройте через Twilio

## 📄 Лицензия

MIT License - см. файл LICENSE для подробностей.

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения
4. Создайте Pull Request

---

**Создано с ❤️ для BeHappy2Day - Elena готова к общению! 💕** 