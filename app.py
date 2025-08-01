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
from datetime import datetime
from flask import Flask, request, jsonify
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import openai
import requests
from pydub import AudioSegment
import speech_recognition as sr

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Конфигурация Twilio
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Конфигурация OpenAI GPT-4 Turbo
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Инициализация клиентов
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) if TWILIO_ACCOUNT_SID else None
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

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

    def transcribe_audio(self, audio_url):
        """Транскрипция голосового сообщения"""
        try:
            # Скачиваем аудио файл
            response = requests.get(audio_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
            
            if response.status_code != 200:
                logger.error(f"Failed to download audio: {response.status_code}")
                return None
            
            # Сохраняем во временный файл
            with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name
            
            # Конвертируем в WAV
            audio = AudioSegment.from_ogg(temp_file_path)
            wav_path = temp_file_path.replace('.ogg', '.wav')
            audio.export(wav_path, format="wav")
            
            # Распознаем речь
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
            
            # Очищаем временные файлы
            os.unlink(temp_file_path)
            os.unlink(wav_path)
            
            logger.info(f"Transcribed audio: {text}")
            return text
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return None

    def get_gpt_response(self, user_message, conversation_history):
        """Получение ответа от GPT-4 Turbo"""
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
                max_tokens=150,
                temperature=0.8,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error getting GPT response: {e}")
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
        # Обработка голосового сообщения
        if media_url and media_url.endswith('.ogg'):
            transcribed_text = self.transcribe_audio(media_url)
            if transcribed_text:
                message = transcribed_text
            else:
                return "I'm sorry, I couldn't understand your voice message. Could you please type your message? 😊"
        
        # Проверка на нарушения
        violations = self.check_violations(message)
        if violations:
            return self.handle_violation(violations)
        
        # Получение истории диалога
        state = user_states.get(user_id, {})
        conversation_history = state.get('conversation_history', [])
        
        # Добавляем сообщение пользователя в историю
        conversation_history.append(f"User: {message}")
        
        # Получаем ответ от GPT-4 Turbo
        response = self.get_gpt_response(message, "\n".join(conversation_history[-5:]))  # Последние 5 сообщений
        
        # Добавляем ответ в историю
        conversation_history.append(f"Elena: {response}")
        
        # Обновляем состояние пользователя
        user_states[user_id] = {
            'conversation_history': conversation_history[-10:],  # Храним последние 10 сообщений
            'last_interaction': datetime.now().isoformat()
        }
        
        return response

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
        
        # Создание ответа
        resp = MessagingResponse()
        resp.message(response_text)
        
        return str(resp)
        
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
        'bot_country': bot.country
    })

@app.route('/', methods=['GET'])
def index():
    """Главная страница"""
    return jsonify({
        'message': f'WhatsApp Bot для BeHappy2Day - {bot.name}',
        'version': '2.0.0',
        'features': [
            'GPT-4 Turbo integration',
            'Voice message transcription',
            'Natural conversation flow',
            'American men 40+ targeting'
        ],
        'endpoints': {
            'webhook': '/webhook',
            'health': '/health'
        }
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 