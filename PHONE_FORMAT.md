# 📞 Формат TWILIO_PHONE_NUMBER

## ✅ Правильный формат

```env
TWILIO_PHONE_NUMBER=whatsapp:+1234567890
```

## 🔍 Структура

```
whatsapp:+[код страны][номер телефона]
```

### Обязательные элементы:
- **`whatsapp:`** - префикс для WhatsApp Business API
- **`+`** - международный символ
- **`[код страны]`** - 1-3 цифры кода страны
- **`[номер телефона]`** - 7-15 цифр номера

## 🌍 Примеры для разных стран

```env
# США
TWILIO_PHONE_NUMBER=whatsapp:+1234567890

# Украина
TWILIO_PHONE_NUMBER=whatsapp:+380501234567

# Россия
TWILIO_PHONE_NUMBER=whatsapp:+79051234567

# Германия
TWILIO_PHONE_NUMBER=whatsapp:+49123456789

# Великобритания
TWILIO_PHONE_NUMBER=whatsapp:+447911123456

# Канада
TWILIO_PHONE_NUMBER=whatsapp:+14161234567

# Австралия
TWILIO_PHONE_NUMBER=whatsapp:+61412345678
```

## ❌ Неправильные форматы

```env
# ❌ Без префикса whatsapp:
TWILIO_PHONE_NUMBER=+1234567890

# ❌ Без +
TWILIO_PHONE_NUMBER=whatsapp:1234567890

# ❌ С пробелами
TWILIO_PHONE_NUMBER=whatsapp: +1234567890

# ❌ С дополнительными символами
TWILIO_PHONE_NUMBER=whatsapp:+1-234-567-8900
```

## 🔧 Проверка формата

Запустите скрипт проверки:
```bash
python3 check_phone_format.py
```

## 📋 Для Railway Variables

В Railway Dashboard добавьте:
```env
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=whatsapp:+1234567890
OPENAI_API_KEY=your_openai_api_key_here
```

## ⚠️ Важные моменты

1. **Номер должен быть зарегистрирован в Twilio**
2. **Используйте международный формат**
3. **Префикс `whatsapp:` обязателен**
4. **Без пробелов и дополнительных символов**
5. **Только цифры после `+`**

## 🆘 Получение номера в Twilio

1. Войдите в [Twilio Console](https://console.twilio.com)
2. Перейдите в "Phone Numbers" → "Manage" → "Active numbers"
3. Купите номер или используйте тестовый из WhatsApp Sandbox
4. Скопируйте номер в формате `whatsapp:+1234567890`

---

**💡 Запомните: всегда используйте префикс `whatsapp:` и международный формат!** 