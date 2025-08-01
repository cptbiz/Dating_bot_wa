#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упрощенный тест WhatsApp бота без внешних зависимостей
"""

class SimpleDatingBot:
    def __init__(self):
        self.welcome_messages = [
            "Привет, красавчик! 😊 Я помогу тебе найти любовь на BeHappy2Day! Расскажи, как тебя зовут?",
            "Ой, привет! 💕 Готова помочь тебе познакомиться с прекрасными девушками! Как тебя зовут?",
            "Привет, милый! 🌹 Хочешь найти свою вторую половинку? Начнем с твоего имени!"
        ]
        
        self.questions = {
            'name': "Отлично! А сколько тебе лет?",
            'age': "Круто! Из какой ты страны?",
            'country': "Что ты ищешь в отношениях? Серьезные или просто общение?",
            'relationship_goal': "Понятно! У тебя есть дети?",
            'children': "Отлично! Последний вопрос - на каком языке ты предпочитаешь общаться?",
            'language': "Супер! Сейчас я создам твой профиль на BeHappy2Day! 💕"
        }
        
        self.violations = [
            'phone', 'email', '@', 'whatsapp', 'telegram', 'instagram', 'facebook',
            'girl', 'minor', 'child', 'teen', 'money', 'gift', 'pay', 'send',
            'politics', 'government', 'election', 'rude', 'fuck', 'shit'
        ]
        
        self.user_states = {}

    def check_violations(self, message):
        """Проверка на нарушения правил"""
        message_lower = message.lower()
        violations = []
        
        for violation in self.violations:
            if violation in message_lower:
                violations.append(violation)
        
        return violations

    def get_response(self, user_id, message):
        """Получение ответа бота"""
        # Проверка на нарушения
        violations = self.check_violations(message)
        if violations:
            return self.handle_violation(violations)
        
        # Получение состояния пользователя
        state = self.user_states.get(user_id, {})
        current_step = state.get('step', 'welcome')
        
        if current_step == 'welcome':
            return self.handle_welcome(user_id, message)
        elif current_step == 'name':
            return self.handle_name(user_id, message)
        elif current_step == 'age':
            return self.handle_age(user_id, message)
        elif current_step == 'country':
            return self.handle_country(user_id, message)
        elif current_step == 'relationship_goal':
            return self.handle_relationship_goal(user_id, message)
        elif current_step == 'children':
            return self.handle_children(user_id, message)
        elif current_step == 'language':
            return self.handle_language(user_id, message)
        else:
            return self.handle_completion(user_id, message)

    def handle_violation(self, violations):
        """Обработка нарушений"""
        violation_messages = {
            'phone': "Извини, но я не могу передавать контактные данные. Это правила сайта! 😊",
            'email': "Контактные данные можно передавать только при личной встрече! 💕",
            'money': "Я не прошу денег и подарков! Давай общаться честно! 😘",
            'minor': "Обсуждение несовершеннолетних запрещено! Давай вернемся к знакомствам! 💕",
            'gift': "Я не прошу подарков! Давай общаться честно! 😘",
            'pay': "Я не прошу денег! Давай общаться честно! 😘",
            'fuck': "Пожалуйста, общайся вежливо! 😊",
            'shit': "Пожалуйста, общайся вежливо! 😊"
        }
        
        for violation in violations:
            if violation in violation_messages:
                return violation_messages[violation]
        
        return "Извини, но это нарушает правила сайта! Давай общаться вежливо! 😊"

    def handle_welcome(self, user_id, message):
        """Обработка приветствия"""
        self.user_states[user_id] = {
            'step': 'name',
            'data': {}
        }
        return self.questions['name']

    def handle_name(self, user_id, message):
        """Обработка имени"""
        self.user_states[user_id]['data']['name'] = message
        self.user_states[user_id]['step'] = 'age'
        return self.questions['age']

    def handle_age(self, user_id, message):
        """Обработка возраста"""
        try:
            age = int(message)
            if age < 18:
                return "Извини, но тебе должно быть 18+ для регистрации! 😊"
            self.user_states[user_id]['data']['age'] = age
            self.user_states[user_id]['step'] = 'country'
            return self.questions['country']
        except ValueError:
            return "Пожалуйста, напиши свой возраст цифрами! 😊"

    def handle_country(self, user_id, message):
        """Обработка страны"""
        self.user_states[user_id]['data']['country'] = message
        self.user_states[user_id]['step'] = 'relationship_goal'
        return self.questions['relationship_goal']

    def handle_relationship_goal(self, user_id, message):
        """Обработка целей отношений"""
        self.user_states[user_id]['data']['relationship_goal'] = message
        self.user_states[user_id]['step'] = 'children'
        return self.questions['children']

    def handle_children(self, user_id, message):
        """Обработка информации о детях"""
        self.user_states[user_id]['data']['children'] = message
        self.user_states[user_id]['step'] = 'language'
        return self.questions['language']

    def handle_language(self, user_id, message):
        """Обработка языка общения"""
        self.user_states[user_id]['data']['language'] = message
        self.user_states[user_id]['step'] = 'completed'
        return self.handle_completion(user_id, message)

    def handle_completion(self, user_id, message):
        """Завершение регистрации"""
        user_data = self.user_states[user_id]['data']
        
        completion_message = f"""
Отлично, {user_data.get('name', 'милый')}! 💕

Твой профиль создан! Вот твои данные:
• Имя: {user_data.get('name')}
• Возраст: {user_data.get('age')}
• Страна: {user_data.get('country')}
• Цель: {user_data.get('relationship_goal')}
• Дети: {user_data.get('children')}
• Язык: {user_data.get('language')}

Скоро с тобой свяжется наш менеджер для завершения регистрации на BeHappy2Day! 

Сайт: https://behappy2day.com
Поддержка: polovinka@behappy2day.com

Удачи в поисках любви! 💋
        """
        
        # Очистка состояния
        if user_id in self.user_states:
            del self.user_states[user_id]
        
        return completion_message.strip()

def test_bot():
    """Тестирование бота"""
    print("🤖 Тестирование WhatsApp бота для BeHappy2Day")
    print("=" * 50)
    
    bot = SimpleDatingBot()
    
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
        
        user_id = f"test_user_{conversation['name'].replace(' ', '_').lower()}"
        
        for i, message in enumerate(conversation['messages']):
            print(f"👤 Пользователь: {message}")
            
            response = bot.get_response(user_id, message)
            print(f"🤖 Бот: {response}")
            print()
            
            # Если бот обнаружил нарушение, прерываем диалог
            if any(violation in response.lower() for violation in ['нарушает', 'запрещено', 'не могу', 'правила сайта']):
                print("🚫 Диалог прерван из-за нарушения правил")
                break

def test_violations():
    """Тестирование проверки нарушений"""
    print("\n🛡️ Тестирование проверки нарушений")
    print("=" * 50)
    
    bot = SimpleDatingBot()
    
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

if __name__ == "__main__":
    print("🚀 Запуск тестов WhatsApp бота")
    print("=" * 50)
    
    # Тестирование основного функционала
    test_bot()
    
    # Тестирование проверки нарушений
    test_violations()
    
    print("\n✅ Тестирование завершено!")
    print("\n💡 Для запуска бота с Twilio:")
    print("   1. pip install -r requirements.txt")
    print("   2. python app.py")
    print("   3. Настройте Twilio webhook") 