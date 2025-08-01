#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для тестирования WhatsApp бота
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import bot

def test_bot():
    """Тестирование бота"""
    print("🤖 Тестирование WhatsApp бота для BeHappy2Day")
    print("=" * 50)
    
    # Тестовые диалоги
    test_conversations = [
        {
            "name": "Нормальный диалог",
            "messages": [
                "Привет",
                "Михаил",
                "25",
                "Россия",
                "Серьезные отношения",
                "Нет",
                "Русский"
            ]
        },
        {
            "name": "Нарушение - передача контактов",
            "messages": [
                "Привет",
                "Михаил",
                "25",
                "Мой телефон +7-999-123-45-67"
            ]
        },
        {
            "name": "Нарушение - несовершеннолетние",
            "messages": [
                "Привет",
                "Анна",
                "16",
                "Россия"
            ]
        },
        {
            "name": "Нарушение - просьба денег",
            "messages": [
                "Привет",
                "Иван",
                "30",
                "Можешь отправить мне деньги?"
            ]
        }
    ]
    
    for conversation in test_conversations:
        print(f"\n📱 Тест: {conversation['name']}")
        print("-" * 30)
        
        user_id = "test_user_123"
        
        for i, message in enumerate(conversation['messages']):
            print(f"👤 Пользователь: {message}")
            
            response = bot.get_response(user_id, message)
            print(f"🤖 Бот: {response}")
            print()
            
            # Если бот обнаружил нарушение, прерываем диалог
            if any(violation in response.lower() for violation in ['нарушает', 'запрещено', 'не могу']):
                print("🚫 Диалог прерван из-за нарушения правил")
                break

def test_violations():
    """Тестирование проверки нарушений"""
    print("\n🛡️ Тестирование проверки нарушений")
    print("=" * 50)
    
    test_messages = [
        ("Привет, мой email: test@example.com", "email"),
        ("Мой телефон: +7-999-123-45-67", "phone"),
        ("Хочу познакомиться с девочкой 15 лет", "minor"),
        ("Можешь отправить мне подарок?", "gift"),
        ("Отправь деньги на карту", "money"),
        ("Политика - это важно", "politics"),
        ("Fuck you!", "rude"),
        ("Обычное сообщение без нарушений", None)
    ]
    
    for message, expected_violation in test_messages:
        violations = bot.check_violations(message)
        print(f"📝 Сообщение: {message}")
        print(f"🔍 Найденные нарушения: {violations}")
        print(f"✅ Ожидаемое нарушение: {expected_violation}")
        print()

def test_database():
    """Тестирование базы данных"""
    print("\n💾 Тестирование базы данных")
    print("=" * 50)
    
    try:
        from database import db_manager
        
        # Тестовые данные
        test_lead = {
            'name': 'Тестовый Пользователь',
            'age': 25,
            'country': 'Россия',
            'relationship_goal': 'Серьезные отношения',
            'children': 'Нет',
            'language': 'Русский'
        }
        
        # Сохранение тестового лида
        success = db_manager.save_lead("+7-999-123-45-67", test_lead)
        print(f"💾 Сохранение лида: {'✅ Успешно' if success else '❌ Ошибка'}")
        
        # Получение статистики
        stats = db_manager.get_statistics()
        print(f"📊 Статистика: {stats}")
        
        # Получение лидов
        leads = db_manager.get_leads(limit=5)
        print(f"📋 Количество лидов: {len(leads)}")
        
    except ImportError:
        print("❌ Модуль database не найден")
    except Exception as e:
        print(f"❌ Ошибка тестирования БД: {e}")

if __name__ == "__main__":
    print("🚀 Запуск тестов WhatsApp бота")
    print("=" * 50)
    
    # Тестирование основного функционала
    test_bot()
    
    # Тестирование проверки нарушений
    test_violations()
    
    # Тестирование базы данных
    test_database()
    
    print("\n✅ Тестирование завершено!")
    print("\n💡 Для запуска бота выполните:")
    print("   python app.py")
    print("\n💡 Для настройки Twilio:")
    print("   1. Зарегистрируйтесь на console.twilio.com")
    print("   2. Получите Account SID и Auth Token")
    print("   3. Настройте webhook URL") 