#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Проверка формата TWILIO_PHONE_NUMBER
"""

import re
import os
from dotenv import load_dotenv

def check_phone_format(phone_number):
    """Проверка правильности формата номера телефона"""
    
    # Паттерн для проверки
    pattern = r'^whatsapp:\+[1-9]\d{1,14}$'
    
    if re.match(pattern, phone_number):
        return True, "✅ Правильный формат"
    else:
        return False, "❌ Неправильный формат"

def validate_phone_number(phone_number):
    """Подробная валидация номера"""
    
    errors = []
    
    # Проверка префикса
    if not phone_number.startswith('whatsapp:'):
        errors.append("❌ Отсутствует префикс 'whatsapp:'")
    
    # Проверка наличия +
    if not phone_number.startswith('whatsapp:+'):
        errors.append("❌ Отсутствует '+' после whatsapp:")
    
    # Проверка длины номера
    number_part = phone_number.replace('whatsapp:', '')
    if len(number_part) < 7 or len(number_part) > 15:
        errors.append("❌ Неправильная длина номера (должно быть 7-15 цифр)")
    
    # Проверка на цифры
    if not number_part[1:].isdigit():
        errors.append("❌ Номер должен содержать только цифры после '+'")
    
    # Проверка кода страны
    country_code = number_part[1:3]  # Первые 2 цифры после +
    valid_country_codes = ['1', '7', '33', '44', '49', '380', '375', '48']
    
    if not any(number_part.startswith('+' + code) for code in valid_country_codes):
        errors.append("⚠️ Возможно неправильный код страны")
    
    return errors

def main():
    """Основная функция"""
    print("📞 Проверка формата TWILIO_PHONE_NUMBER")
    print("=" * 50)
    
    # Загружаем переменные окружения
    load_dotenv()
    
    # Получаем номер из переменных окружения
    phone_number = os.getenv('TWILIO_PHONE_NUMBER', '')
    
    if not phone_number:
        print("❌ TWILIO_PHONE_NUMBER не найден в переменных окружения")
        print("\n💡 Добавьте в .env файл:")
        print("TWILIO_PHONE_NUMBER=whatsapp:+1234567890")
        return
    
    print(f"📱 Проверяем номер: {phone_number}")
    print()
    
    # Проверяем формат
    is_valid, message = check_phone_format(phone_number)
    print(message)
    
    # Подробная валидация
    errors = validate_phone_number(phone_number)
    
    if errors:
        print("\n🔍 Детальная проверка:")
        for error in errors:
            print(error)
    else:
        print("\n✅ Номер прошел все проверки!")
    
    print("\n📋 Примеры правильных форматов:")
    print("TWILIO_PHONE_NUMBER=whatsapp:+1234567890    # США")
    print("TWILIO_PHONE_NUMBER=whatsapp:+380501234567  # Украина")
    print("TWILIO_PHONE_NUMBER=whatsapp:+79051234567   # Россия")
    print("TWILIO_PHONE_NUMBER=whatsapp:+49123456789   # Германия")
    print("TWILIO_PHONE_NUMBER=whatsapp:+447911123456  # Великобритания")

if __name__ == "__main__":
    main() 