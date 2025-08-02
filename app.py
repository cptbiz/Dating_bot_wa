#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WhatsApp Bot для BeHappy2Day
Общение как настоящая девушка с американскими мужчинами 40+
"""

import os
import json
import logging
import tempfile
import re
import time
import random
import threading
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import openai
import requests
from pydub import AudioSegment
import speech_recognition as sr

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Отключаем лишние логи
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('werkzeug').setLevel(logging.WARNING)
logging.getLogger('twilio.http_client').setLevel(logging.WARNING)
logging.getLogger('twilio').setLevel(logging.WARNING)

app = Flask(__name__)

# Загружаем переменные окружения
load_dotenv()

# Конфигурация Twilio
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Конфигурация OpenAI GPT-4 Turbo
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Проверка обязательных переменных окружения
if not TWILIO_ACCOUNT_SID:
    logger.warning("TWILIO_ACCOUNT_SID не установлен")
if not TWILIO_AUTH_TOKEN:
    logger.warning("TWILIO_AUTH_TOKEN не установлен")
if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY не установлен")

# Инициализация клиентов
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) if TWILIO_ACCOUNT_SID else None

# Инициализация OpenAI клиента с обработкой ошибок
try:
    openai_client = openai.OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
    logger.info("OpenAI клиент успешно инициализирован")
except Exception as e:
    logger.error(f"Ошибка инициализации OpenAI клиента: {e}")
    openai_client = None

# Состояния пользователей
user_states = {}

class DatingGirlBot:
    def __init__(self):
        self.name = "Elena"  # Имя девушки
        self.age = 28
        self.country = "Ukraine"
        self.city = "Kyiv"
        self.profession = "Marketing Manager"
        self.interests = ["traveling", "cooking", "reading", "yoga", "photography"]
        self.languages = ["English", "Ukrainian", "Russian"]
        
        # Персональность девушки
        self.personality = {
            'style': 'warm, caring, intelligent, independent',
            'communication': 'flirty but respectful, asks questions, shows interest',
            'values': 'family, honesty, mutual respect, shared interests'
        }
        
        # Системный промпт для GPT-4 Turbo - КОРОТКИЕ ОТВЕТЫ
        self.system_prompt = f"""
You are {self.name}, a {self.age}-year-old woman from {self.country}. You are intelligent, caring, and looking for a serious relationship with an American man aged 40+.

IMPORTANT: Keep responses SHORT and NATURAL (1-2 sentences max). Like a real person typing on WhatsApp.

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
- Keep responses SHORT (1-2 sentences)
- Be authentic and genuine
- Sometimes ask follow-up questions
- Show interest in his responses

RESPONSE RULES:
- MAXIMUM 2 sentences per response
- Keep it casual and natural
- Use simple, everyday language
- Add 1-2 emojis naturally
- Sometimes just acknowledge and ask a question
- Be conversational, not formal

IMPORTANT RULES:
- NEVER ask for money, gifts, or financial help
- NEVER share personal contact information (phone, email, social media)
- NEVER discuss politics or controversial topics
- ALWAYS redirect to the website for serious conversations
- Be patient and understanding with language barriers
- Focus on building emotional connection
- Ask about his interests, work, family, hobbies
- Share your own interests and experiences naturally

Current conversation context: You're chatting with an American man on a dating website. Keep responses SHORT and NATURAL like a real person.
"""

    def validate_audio_url(self, audio_url):
        """Валидация URL аудио файла"""
        if not audio_url:
            return False
        
        # Проверяем, что это URL от Twilio
        if not audio_url.startswith('https://'):
            return False
        
        # Проверяем, что это аудио файл
        audio_extensions = ['.ogg', '.wav', '.mp3', '.m4a']
        if not any(ext in audio_url.lower() for ext in audio_extensions):
            return False
        
        return True

    def transcribe_audio(self, audio_url):
        """Транскрипция голосового сообщения"""
        try:
            # Валидация URL
            if not self.validate_audio_url(audio_url):
                logger.error(f"Invalid audio URL: {audio_url}")
                return None
            
            # Скачиваем аудио файл
            response = requests.get(audio_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN), timeout=30)
            
            if response.status_code != 200:
                logger.error(f"Failed to download audio: {response.status_code}")
                return None
            
            # Сохраняем во временный файл
            with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name
            
            try:
                # Конвертируем в WAV
                audio = AudioSegment.from_ogg(temp_file_path)
                wav_path = temp_file_path.replace('.ogg', '.wav')
                audio.export(wav_path, format="wav")
                
                # Распознаем речь
                recognizer = sr.Recognizer()
                with sr.AudioFile(wav_path) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language='en-US')
                
                logger.info(f"Transcribed audio: {text}")
                return text
                
            except Exception as e:
                logger.error(f"Error processing audio: {e}")
                return None
            finally:
                # Очищаем временные файлы
                try:
                    os.unlink(temp_file_path)
                    if 'wav_path' in locals():
                        os.unlink(wav_path)
                except:
                    pass
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return None

    def get_gpt_response(self, user_message, conversation_history):
        """Получение ответа от GPT-4 Turbo - КОРОТКИЙ"""
        try:
            if not openai_client:
                return self.get_fallback_response(user_message)
            
            # Формируем историю диалога
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Previous conversation context: {conversation_history}"},
                {"role": "user", "content": user_message}
            ]
            
            response = openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                max_tokens=80,  # Уменьшил для коротких ответов
                temperature=0.9,  # Увеличил для более естественных ответов
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error getting GPT response: {e}")
            return self.get_fallback_response(user_message)

    def get_fallback_response(self, user_message):
        """Резервные ответы если GPT недоступен - КОРОТКИЕ"""
        fallback_responses = [
            "That's really interesting! Tell me more about yourself 💕",
            "I love hearing about your experiences! What else do you enjoy doing? 😊",
            "You seem like such a wonderful person! What are you looking for in a relationship? 🌹",
            "I'm really enjoying our conversation! What makes you happy? 💕",
            "You sound amazing! I'd love to know more about your life and interests 😊",
            "That's so nice to hear! What do you like to do for fun? 🌹",
            "I love that! Tell me more about yourself 💕",
            "You sound wonderful! What brings you joy? 😊",
            "That's really sweet! What are your hobbies? 🌹",
            "I'm enjoying our chat! What's your favorite thing to do? 💕"
        ]
        
        import random
        return random.choice(fallback_responses)

    def check_violations(self, message):
        """Проверка на нарушения правил"""
        message_lower = message.lower()
        violations = []
        
        # Расширенный список нарушений
        violation_patterns = {
            'contact_info': r'\b(?:phone|email|@|whatsapp|telegram|instagram|facebook|snapchat|twitter|linkedin)\b',
            'money_requests': r'\b(?:money|gift|pay|send|bank|card|transfer|cash|dollar|euro|bitcoin|crypto)\b',
            'political': r'\b(?:politics|government|election|trump|biden|democrat|republican|liberal|conservative)\b',
            'inappropriate': r'\b(?:fuck|shit|ass|bitch|slut|whore|dick|pussy|cock|penis|vagina)\b',
            'spam': r'\b(?:buy|sell|investment|profit|earn|rich|million|billion|lottery|prize)\b'
        }
        
        for violation_type, pattern in violation_patterns.items():
            if re.search(pattern, message_lower):
                violations.append(violation_type)
        
        return violations

    def handle_violation(self, violations):
        """Обработка нарушений - КОРОТКИЕ ОТВЕТЫ"""
        violation_responses = {
            'contact_info': "I'd love to chat more here for now! Maybe we can meet in person someday? 😊",
            'money_requests': "I'm looking for a genuine connection, not money or gifts! 💕",
            'political': "I prefer to keep our conversation light and positive! 😊",
            'inappropriate': "I prefer to keep our conversation respectful and classy! 😊",
            'spam': "I'm here for genuine conversations, not business opportunities! 💕"
        }
        
        for violation in violations:
            if violation in violation_responses:
                return violation_responses[violation]
        
        return "I'd love to keep our conversation positive and respectful! 😊"

    def get_random_delay(self):
        """Получение случайной задержки 20-40 секунд"""
        return random.randint(20, 40)

    def get_response(self, user_id, message, media_url=None):
        """Получение ответа бота - КОРОТКИЙ И ЕСТЕСТВЕННЫЙ"""
        try:
            # Обработка голосового сообщения
            if media_url and self.validate_audio_url(media_url):
                transcribed_text = self.transcribe_audio(media_url)
                if transcribed_text:
                    message = transcribed_text
                    logger.info(f"Voice message transcribed: {transcribed_text}")
                else:
                    return "I'm sorry, I couldn't understand your voice message. Could you please type your message? 😊"
            
            # Проверка на нарушения
            violations = self.check_violations(message)
            if violations:
                logger.warning(f"Violation detected for user {user_id}: {violations}")
                return self.handle_violation(violations)
            
            # Получение истории диалога
            state = user_states.get(user_id, {})
            conversation_history = state.get('conversation_history', [])
            last_response_type = state.get('last_response_type', 'none')
            
            # Добавляем сообщение пользователя в историю
            conversation_history.append(f"User: {message}")
            
            # Определяем тип ответа
            if last_response_type == 'question' and '?' in message.lower():
                # Пользователь ответил на вопрос - даем личную историю
                response = self.get_personal_story()
                response_type = 'story'
            elif last_response_type == 'story':
                # После истории задаем вопрос
                response = self.get_question_response(message)
                response_type = 'question'
            else:
                # Обычный ответ на сообщение
                response = self.get_greeting_response(message)
                response_type = 'greeting'
            
            # Добавляем ответ в историю
            conversation_history.append(f"Elena: {response}")
            
            # Обновляем состояние пользователя
            user_states[user_id] = {
                'conversation_history': conversation_history[-10:],
                'last_interaction': datetime.now().isoformat(),
                'last_user_message_time': datetime.now().isoformat(),
                'last_response_type': response_type
            }
            
            # Планируем авто-сообщение через час
            self.schedule_auto_message(user_id)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in get_response: {e}")
            return "I'm having trouble processing your message right now. Could you try again? 😊"

    def get_greeting_response(self, message):
        """Получение приветственного ответа"""
        message_lower = message.lower().strip()
        
        # Простые приветствия
        if message_lower in ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']:
            return "Hi! 😊"
        elif message_lower in ['how are you', 'how are you doing', 'how do you do']:
            return "I'm doing great, thanks! 😊"
        elif message_lower in ['what\'s up', 'sup', 'wassup']:
            return "Hey! Not much, just here 😊"
        else:
            # Для других сообщений используем GPT
            return self.get_gpt_response(message, "")

    def get_personal_story(self):
        """Получение личной истории"""
        personal_stories = [
            "Today was such a great day! I went for a walk in the park with my friends 💕",
            "I had an amazing day! I was cooking my favorite Ukrainian dish - borscht 😊",
            "It's been a wonderful day! I was reading a book in my favorite coffee shop 🌹",
            "Today was perfect! I went to yoga class and then met my sister for lunch 💕",
            "I had such a nice day! I was taking photos in the city center 😊",
            "Today was lovely! I was practicing my English and watching movies 🌹",
            "It's been a beautiful day! I was walking by the river and enjoying the sunset 💕",
            "Today was fantastic! I was cooking and listening to music 😊",
            "I had a wonderful day! I was shopping and then had coffee with friends 🌹",
            "Today was amazing! I was working from home and then went for a walk 💕"
        ]
        return random.choice(personal_stories)

    def get_question_response(self, user_message):
        """Получение ответа с вопросом после истории"""
        question_responses = [
            "How about you? How was your day? 😊",
            "What about you? What did you do today? 💕",
            "Tell me about your day! How was it? 🌹",
            "What's your story? How was your day? 😊",
            "I'd love to hear about your day! What did you do? 💕",
            "How was your day? Tell me something interesting! 🌹",
            "What about your day? I'm curious to hear! 😊",
            "How are you doing? What's new with you? 💕",
            "What's happening in your life? Tell me! 🌹",
            "How are things with you? What's your day like? 😊"
        ]
        return random.choice(question_responses)

    def should_send_follow_up(self):
        """Определяет, нужно ли отправить второе сообщение (50% вероятность для приветствий)"""
        return random.random() < 0.5

    def get_follow_up_message(self):
        """Получение второго сообщения"""
        follow_up_messages = [
            "How are you doing today? 😊",
            "What's new with you? 💕",
            "How was your day? 🌹",
            "What are you up to? 😊",
            "How are things going? 💕",
            "What's happening in your life? 🌹",
            "How are you feeling today? 😊",
            "What's your day been like? 💕"
        ]
        return random.choice(follow_up_messages)

    def get_auto_message(self):
        """Получение авто-сообщения через час"""
        auto_messages = [
            "Hey! I was thinking about our conversation earlier 💕",
            "Hi! How's your day going? 😊",
            "Hello! I hope you're having a wonderful day 🌹",
            "Hey there! Just wanted to say hi 💕",
            "Hi! What's new with you? 😊",
            "Hello! I'm curious how your day is going 🌹",
            "Hey! I enjoyed our chat earlier 💕",
            "Hi! How are things with you? 😊"
        ]
        return random.choice(auto_messages)

    def send_delayed_message(self, user_id, message, delay_seconds):
        """Отправка сообщения с задержкой"""
        def send_message():
            time.sleep(delay_seconds)
            try:
                if twilio_client:
                    twilio_client.messages.create(
                        body=message,
                        from_=TWILIO_PHONE_NUMBER,
                        to=user_id
                    )
                    logger.info(f"Отправлено отложенное сообщение пользователю {user_id}: {message}")
            except Exception as e:
                logger.error(f"Ошибка отправки отложенного сообщения: {e}")
        
        # Запускаем в отдельном потоке
        thread = threading.Thread(target=send_message)
        thread.daemon = True
        thread.start()

    def schedule_auto_message(self, user_id):
        """Планирование авто-сообщения через час"""
        def send_auto_message():
            time.sleep(3600)  # 1 час
            try:
                # Проверяем, не писал ли пользователь за последний час
                state = user_states.get(user_id, {})
                last_user_message = state.get('last_user_message_time')
                
                if last_user_message:
                    last_time = datetime.fromisoformat(last_user_message)
                    if datetime.now() - last_time < timedelta(hours=1):
                        return  # Пользователь писал недавно
                
                # Проверяем ограничение 24 часа
                if last_user_message:
                    last_time = datetime.fromisoformat(last_user_message)
                    if datetime.now() - last_time > timedelta(hours=24):
                        return  # Прошло больше 24 часов
                
                auto_message = self.get_auto_message()
                if twilio_client:
                    twilio_client.messages.create(
                        body=auto_message,
                        from_=TWILIO_PHONE_NUMBER,
                        to=user_id
                    )
                    logger.info(f"Отправлено авто-сообщение пользователю {user_id}: {auto_message}")
            except Exception as e:
                logger.error(f"Ошибка отправки авто-сообщения: {e}")
        
        # Запускаем в отдельном потоке
        thread = threading.Thread(target=send_auto_message)
        thread.daemon = True
        thread.start()

# Инициализация бота
bot = DatingGirlBot()

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook для получения сообщений от Twilio"""
    try:
        # Получение данных от Twilio
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '')
        media_url = request.values.get('MediaUrl0', '')  # URL голосового сообщения
        
        logger.info(f"Получено сообщение от {sender}: {incoming_msg}")
        if media_url:
            logger.info(f"Голосовое сообщение: {media_url}")
        
        # Получение ответа от бота
        response_text = bot.get_response(sender, incoming_msg, media_url)
        
        # Получаем случайную задержку
        delay = bot.get_random_delay()
        logger.info(f"Задержка ответа: {delay} секунд")
        
        # Отправляем основной ответ с задержкой через Twilio API
        bot.send_delayed_message(sender, response_text, delay)
        
        # Отправляем второе сообщение с дополнительной задержкой если нужно
        if bot.should_send_follow_up():
            follow_up_message = bot.get_follow_up_message()
            follow_up_delay = delay + random.randint(10, 20)
            bot.send_delayed_message(sender, follow_up_message, follow_up_delay)
            logger.info(f"Запланировано второе сообщение через {follow_up_delay} секунд")
        
        # Возвращаем пустой ответ (Twilio получит 200 OK)
        return '', 200
        
    except Exception as e:
        logger.error(f"Ошибка в webhook: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка здоровья приложения"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'twilio_configured': bool(TWILIO_ACCOUNT_SID),
        'openai_configured': bool(OPENAI_API_KEY),
        'bot_name': bot.name,
        'bot_age': bot.age,
        'bot_country': bot.country,
        'active_users': len(user_states),
        'environment': os.getenv('RAILWAY_ENVIRONMENT', 'development')
    })

@app.route('/', methods=['GET'])
def index():
    """Главная страница"""
    return jsonify({
        'message': f'WhatsApp Bot для BeHappy2Day - {bot.name}',
        'version': '2.3.0',
        'features': [
            'GPT-4 Turbo integration',
            'Voice message transcription',
            'Natural conversation flow',
            'American men 40+ targeting',
            'Enhanced security validation',
            'Short human-like responses',
            'Natural delays (20-40 seconds)',
            'Follow-up messages',
            'Auto-messages after 1 hour'
        ],
        'endpoints': {
            'webhook': '/webhook',
            'health': '/health'
        },
        'status': 'running'
    })

@app.route('/test', methods=['GET'])
def test():
    """Тестовая страница"""
    return jsonify({
        'status': 'ok',
        'message': 'Elena WhatsApp Bot is running!',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting Elena WhatsApp Bot on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 