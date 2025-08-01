#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WhatsApp Bot для BeHappy2Day
Обработка лидов и квалификация пользователей
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import openai

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

# Конфигурация OpenAI (опционально для умных ответов)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Инициализация клиентов
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) if TWILIO_ACCOUNT_SID else None
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# Состояния пользователей (в продакшене использовать Redis или базу данных)
user_states = {}

# Класс для управления диалогом
class DatingBot:
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
        state = user_states.get(user_id, {})
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
        user_states[user_id] = {
            'step': 'name',
            'data': {}
        }
        return self.questions['name']

    def handle_name(self, user_id, message):
        """Обработка имени"""
        user_states[user_id]['data']['name'] = message
        user_states[user_id]['step'] = 'age'
        return self.questions['age']

    def handle_age(self, user_id, message):
        """Обработка возраста"""
        try:
            age = int(message)
            if age < 18:
                return "Извини, но тебе должно быть 18+ для регистрации! 😊"
            user_states[user_id]['data']['age'] = age
            user_states[user_id]['step'] = 'country'
            return self.questions['country']
        except ValueError:
            return "Пожалуйста, напиши свой возраст цифрами! 😊"

    def handle_country(self, user_id, message):
        """Обработка страны"""
        user_states[user_id]['data']['country'] = message
        user_states[user_id]['step'] = 'relationship_goal'
        return self.questions['relationship_goal']

    def handle_relationship_goal(self, user_id, message):
        """Обработка целей отношений"""
        user_states[user_id]['data']['relationship_goal'] = message
        user_states[user_id]['step'] = 'children'
        return self.questions['children']

    def handle_children(self, user_id, message):
        """Обработка информации о детях"""
        user_states[user_id]['data']['children'] = message
        user_states[user_id]['step'] = 'language'
        return self.questions['language']

    def handle_language(self, user_id, message):
        """Обработка языка общения"""
        user_states[user_id]['data']['language'] = message
        user_states[user_id]['step'] = 'completed'
        return self.handle_completion(user_id, message)

    def handle_completion(self, user_id, message):
        """Завершение регистрации"""
        user_data = user_states[user_id]['data']
        
        # Сохранение лида (в продакшене - в базу данных)
        self.save_lead(user_data)
        
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
        if user_id in user_states:
            del user_states[user_id]
        
        return completion_message.strip()

    def save_lead(self, user_data):
        """Сохранение лида"""
        lead_data = {
            'timestamp': datetime.now().isoformat(),
            'source': 'whatsapp_bot',
            'data': user_data
        }
        
        # В продакшене сохранять в базу данных или CRM
        logger.info(f"Новый лид: {json.dumps(lead_data, ensure_ascii=False)}")
        
        # Можно добавить сохранение в файл или отправку на email
        try:
            with open('leads.json', 'a', encoding='utf-8') as f:
                f.write(json.dumps(lead_data, ensure_ascii=False) + '\n')
        except Exception as e:
            logger.error(f"Ошибка сохранения лида: {e}")

# Инициализация бота
bot = DatingBot()

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook для получения сообщений от Twilio"""
    try:
        # Получение данных от Twilio
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '')
        
        logger.info(f"Получено сообщение от {sender}: {incoming_msg}")
        
        # Получение ответа от бота
        response_text = bot.get_response(sender, incoming_msg)
        
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
        'openai_configured': bool(OPENAI_API_KEY)
    })

@app.route('/', methods=['GET'])
def index():
    """Главная страница"""
    return jsonify({
        'message': 'WhatsApp Bot для BeHappy2Day',
        'version': '1.0.0',
        'endpoints': {
            'webhook': '/webhook',
            'health': '/health'
        }
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 