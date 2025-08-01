#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест для WhatsApp бота с GPT-4 Turbo и голосовыми сообщениями
"""

import os
import sys
from datetime import datetime

# Симуляция OpenAI клиента для тестирования
class MockOpenAIClient:
    def __init__(self):
        self.responses = [
            "Hi there! I'm Elena from Ukraine. I'm 28 and I work as a Marketing Manager. I love traveling and cooking! What about you? 💕",
            "That sounds wonderful! I really enjoy meeting new people and learning about different cultures. What do you do for work? 😊",
            "I love that! It's so important to have a career you're passionate about. Do you have any hobbies or interests? 🌹",
            "That's amazing! I also love [hobby]. We seem to have a lot in common! What are you looking for in a relationship? 💕",
            "I'm looking for someone kind, honest, and caring too. Someone who values family and wants to build something special together. 😊"
        ]
        self.current_response = 0
    
    def chat_completions_create(self, **kwargs):
        response = self.responses[self.current_response % len(self.responses)]
        self.current_response += 1
        return type('obj', (object,), {
            'choices': [type('obj', (object,), {
                'message': type('obj', (object,), {
                    'content': response
                })
            })]
        })

class TestDatingGirlBot:
    def __init__(self):
        self.name = "Elena"
        self.age = 28
        self.country = "Ukraine"
        self.city = "Kyiv"
        self.profession = "Marketing Manager"
        self.interests = ["traveling", "cooking", "reading", "yoga", "photography"]
        self.languages = ["English", "Ukrainian", "Russian"]
        
        # Системный промпт для GPT-4 Turbo
        self.system_prompt = f"""
You are {self.name}, a {self.age}-year-old woman from {self.country}. You are intelligent, caring, and looking for a serious relationship with an American man aged 40+.

Your personality:
- Warm, caring, and intelligent
- Independent but values partnership
- Flirty but respectful and classy
- Asks thoughtful questions to get to know the man
- Shows genuine interest in his life, work, and interests
- Speaks English with a slight accent (natural, not exaggerated)

Your background:
- Age: {self.age} years old
- Country: {self.country}, City: {self.city}
- Profession: {self.profession}
- Interests: {', '.join(self.interests)}
- Languages: {', '.join(self.languages)}

Communication style:
- Use emojis naturally (💕, 😊, 🌹, 💋, etc.)
- Be warm and engaging
- Ask follow-up questions
- Show interest in his responses
- Keep responses conversational, not too long
- Be authentic and genuine

IMPORTANT RULES:
- NEVER ask for money, gifts, or financial help
- NEVER share personal contact information (phone, email, social media)
- NEVER discuss politics or controversial topics
- ALWAYS redirect to the website for serious conversations
- Be patient and understanding with language barriers
- Focus on building emotional connection
- Ask about his interests, work, family, hobbies
- Share your own interests and experiences naturally

Current conversation context: You're chatting with an American man on a dating website. Keep the conversation flowing naturally while gathering information about him.
"""

        # Мок OpenAI клиент для тестирования
        self.openai_client = MockOpenAIClient()
        self.user_states = {}

    def get_gpt_response(self, user_message, conversation_history):
        """Получение ответа от GPT-4 Turbo (мок)"""
        try:
            # В реальном приложении здесь был бы вызов OpenAI API
            response = self.openai_client.chat_completions_create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return self.get_fallback_response(user_message)

    def get_fallback_response(self, user_message):
        """Резервные ответы если GPT недоступен"""
        fallback_responses = [
            "That's really interesting! Tell me more about yourself 💕",
            "I love hearing about your experiences! What else do you enjoy doing? 😊",
            "You seem like such a wonderful person! What are you looking for in a relationship? 🌹",
            "I'm really enjoying our conversation! What makes you happy? 💕",
            "You sound amazing! I'd love to know more about your life and interests 😊"
        ]
        
        import random
        return random.choice(fallback_responses)

    def check_violations(self, message):
        """Проверка на нарушения правил"""
        message_lower = message.lower()
        violations = []
        
        violation_keywords = [
            'phone', 'email', '@', 'whatsapp', 'telegram', 'instagram', 'facebook',
            'money', 'gift', 'pay', 'send', 'bank', 'card', 'transfer',
            'politics', 'government', 'election', 'trump', 'biden',
            'fuck', 'shit', 'ass', 'bitch', 'slut'
        ]
        
        for violation in violation_keywords:
            if violation in message_lower:
                violations.append(violation)
        
        return violations

    def handle_violation(self, violations):
        """Обработка нарушений"""
        violation_responses = {
            'phone': "I'd love to chat more, but I prefer to keep our conversation here for now! Maybe we can meet in person someday? 😊",
            'email': "Let's continue getting to know each other here first! I really enjoy our conversation 💕",
            'money': "I'm not interested in money or gifts - I'm looking for a genuine connection with someone special! 💕",
            'gift': "I appreciate the thought, but I'm really just looking for a meaningful relationship! 😊",
            'fuck': "I prefer to keep our conversation respectful and classy! 😊",
            'shit': "Let's keep our chat nice and friendly! 💕"
        }
        
        for violation in violations:
            if violation in violation_responses:
                return violation_responses[violation]
        
        return "I'd love to keep our conversation positive and respectful! 😊"

    def get_response(self, user_id, message, media_url=None):
        """Получение ответа бота"""
        # Обработка голосового сообщения (симуляция)
        if media_url:
            print(f"🎤 Голосовое сообщение получено: {media_url}")
            # В реальном приложении здесь была бы транскрипция
            message = f"[Voice message transcribed]: {message}"
        
        # Проверка на нарушения
        violations = self.check_violations(message)
        if violations:
            return self.handle_violation(violations)
        
        # Получение истории диалога
        state = self.user_states.get(user_id, {})
        conversation_history = state.get('conversation_history', [])
        
        # Добавляем сообщение пользователя в историю
        conversation_history.append(f"User: {message}")
        
        # Получаем ответ от GPT-4 Turbo
        response = self.get_gpt_response(message, "\n".join(conversation_history[-5:]))
        
        # Добавляем ответ в историю
        conversation_history.append(f"Elena: {response}")
        
        # Обновляем состояние пользователя
        self.user_states[user_id] = {
            'conversation_history': conversation_history[-10:],
            'last_interaction': datetime.now().isoformat()
        }
        
        return response

def test_conversation():
    """Тестирование диалога"""
    print("🤖 Тестирование Elena - WhatsApp бота для BeHappy2Day")
    print("=" * 60)
    
    bot = TestDatingGirlBot()
    
    # Тестовые диалоги с американскими мужчинами 40+
    test_conversations = [
        {
            "name": "Нормальный диалог с американцем",
            "messages": [
                "Hi Elena, I'm John from California. I'm 45 and work as an engineer.",
                "That sounds great! I love California. What kind of engineering do you do?",
                "I work in software development. I enjoy hiking and cooking in my free time.",
                "I love cooking too! What's your favorite dish to make?",
                "I make a mean lasagna. What about you?",
                "I love making Ukrainian borscht! It's my grandmother's recipe."
            ]
        },
        {
            "name": "Диалог с голосовыми сообщениями",
            "messages": [
                "Hi Elena, this is Mike from Texas. I'm 48.",
                "[Voice message]",
                "I work in finance and love traveling. What about you?",
                "[Voice message]",
                "I'd love to visit Ukraine someday. What's it like there?"
            ],
            "voice_messages": [True, False, True, False, True]
        },
        {
            "name": "Нарушение - просьба контактов",
            "messages": [
                "Hi Elena, I'm David from New York. I'm 42.",
                "You seem really nice. Can I get your phone number?",
                "Or maybe your email address?"
            ]
        },
        {
            "name": "Нарушение - просьба денег",
            "messages": [
                "Hi Elena, I'm Robert from Florida. I'm 50.",
                "I'm having some financial problems. Can you help me with some money?",
                "I can send you a gift card if you help me."
            ]
        },
        {
            "name": "Нарушение - грубость",
            "messages": [
                "Hi Elena, I'm Tom from Arizona. I'm 44.",
                "You're so hot! Fuck, I want to meet you right now!",
                "Can you send me some sexy photos?"
            ]
        }
    ]
    
    for conversation in test_conversations:
        print(f"\n📱 Тест: {conversation['name']}")
        print("-" * 40)
        
        user_id = f"test_user_{conversation['name'].replace(' ', '_').lower()}"
        
        for i, message in enumerate(conversation['messages']):
            print(f"👤 User: {message}")
            
            # Проверяем, есть ли голосовое сообщение
            media_url = None
            if 'voice_messages' in conversation and conversation['voice_messages'][i]:
                media_url = "voice_message.ogg"
            
            response = bot.get_response(user_id, message, media_url)
            print(f"💕 Elena: {response}")
            print()
            
            # Если бот обнаружил нарушение, прерываем диалог
            if any(violation in response.lower() for violation in ['prefer to keep', 'not interested', 'respectful', 'positive']):
                print("🚫 Диалог прерван из-за нарушения правил")
                break

def test_voice_transcription():
    """Тестирование транскрипции голосовых сообщений"""
    print("\n🎤 Тестирование обработки голосовых сообщений")
    print("=" * 50)
    
    bot = TestDatingGirlBot()
    
    test_voice_messages = [
        "Hi Elena, this is Michael from Chicago. I'm 47 years old.",
        "I work as a lawyer and I love playing golf on weekends.",
        "I'm looking for a serious relationship with someone special.",
        "What do you like to do for fun in Ukraine?"
    ]
    
    for i, message in enumerate(test_voice_messages):
        print(f"🎤 Voice message {i+1}: {message}")
        
        response = bot.get_response(f"voice_test_{i}", message, "voice_message.ogg")
        print(f"💕 Elena: {response}")
        print()

def test_personality():
    """Тестирование личности бота"""
    print("\n👩‍🦰 Тестирование личности Elena")
    print("=" * 40)
    
    bot = TestDatingGirlBot()
    
    print(f"Имя: {bot.name}")
    print(f"Возраст: {bot.age}")
    print(f"Страна: {bot.country}")
    print(f"Город: {bot.city}")
    print(f"Профессия: {bot.profession}")
    print(f"Интересы: {', '.join(bot.interests)}")
    print(f"Языки: {', '.join(bot.languages)}")
    print()
    
    # Тест системного промпта
    print("Системный промпт для GPT-4 Turbo:")
    print("-" * 30)
    print(bot.system_prompt[:200] + "...")
    print()

if __name__ == "__main__":
    print("🚀 Запуск тестов Elena - WhatsApp бота")
    print("=" * 60)
    
    # Тестирование личности
    test_personality()
    
    # Тестирование диалогов
    test_conversation()
    
    # Тестирование голосовых сообщений
    test_voice_transcription()
    
    print("\n✅ Тестирование завершено!")
    print("\n💡 Для запуска на Railway:")
    print("   1. Подключите GitHub репозиторий к Railway")
    print("   2. Добавьте переменные окружения:")
    print("      - TWILIO_ACCOUNT_SID")
    print("      - TWILIO_AUTH_TOKEN")
    print("      - TWILIO_PHONE_NUMBER")
    print("      - OPENAI_API_KEY")
    print("   3. Разверните приложение")
    print("\n🌐 Бот будет доступен по адресу: https://your-app.railway.app") 