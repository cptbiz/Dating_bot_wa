#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для работы с базой данных
Хранение и управление лидами
"""

import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = "leads.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Создание таблицы лидов
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS leads (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        phone_number TEXT NOT NULL,
                        name TEXT,
                        age INTEGER,
                        country TEXT,
                        relationship_goal TEXT,
                        children TEXT,
                        language TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        status TEXT DEFAULT 'new',
                        notes TEXT
                    )
                ''')
                
                # Создание таблицы нарушений
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS violations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        phone_number TEXT NOT NULL,
                        violation_type TEXT NOT NULL,
                        message TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Создание таблицы статистики
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS statistics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date DATE NOT NULL,
                        total_leads INTEGER DEFAULT 0,
                        completed_leads INTEGER DEFAULT 0,
                        violations_count INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                logger.info("База данных инициализирована успешно")
                
        except Exception as e:
            logger.error(f"Ошибка инициализации базы данных: {e}")
    
    def save_lead(self, phone_number: str, lead_data: Dict) -> bool:
        """Сохранение нового лида"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO leads (
                        phone_number, name, age, country, 
                        relationship_goal, children, language
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    phone_number,
                    lead_data.get('name'),
                    lead_data.get('age'),
                    lead_data.get('country'),
                    lead_data.get('relationship_goal'),
                    lead_data.get('children'),
                    lead_data.get('language')
                ))
                
                conn.commit()
                logger.info(f"Лид сохранен для {phone_number}")
                return True
                
        except Exception as e:
            logger.error(f"Ошибка сохранения лида: {e}")
            return False
    
    def save_violation(self, phone_number: str, violation_type: str, message: str) -> bool:
        """Сохранение нарушения"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO violations (phone_number, violation_type, message)
                    VALUES (?, ?, ?)
                ''', (phone_number, violation_type, message))
                
                conn.commit()
                logger.info(f"Нарушение сохранено для {phone_number}")
                return True
                
        except Exception as e:
            logger.error(f"Ошибка сохранения нарушения: {e}")
            return False
    
    def get_leads(self, limit: int = 100, status: str = None) -> List[Dict]:
        """Получение списка лидов"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                query = "SELECT * FROM leads"
                params = []
                
                if status:
                    query += " WHERE status = ?"
                    params.append(status)
                
                query += " ORDER BY created_at DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Ошибка получения лидов: {e}")
            return []
    
    def get_lead_by_phone(self, phone_number: str) -> Optional[Dict]:
        """Получение лида по номеру телефона"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM leads WHERE phone_number = ?
                    ORDER BY created_at DESC LIMIT 1
                ''', (phone_number,))
                
                row = cursor.fetchone()
                return dict(row) if row else None
                
        except Exception as e:
            logger.error(f"Ошибка получения лида: {e}")
            return None
    
    def update_lead_status(self, lead_id: int, status: str, notes: str = None) -> bool:
        """Обновление статуса лида"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if notes:
                    cursor.execute('''
                        UPDATE leads SET status = ?, notes = ?
                        WHERE id = ?
                    ''', (status, notes, lead_id))
                else:
                    cursor.execute('''
                        UPDATE leads SET status = ?
                        WHERE id = ?
                    ''', (status, lead_id))
                
                conn.commit()
                logger.info(f"Статус лида {lead_id} обновлен на {status}")
                return True
                
        except Exception as e:
            logger.error(f"Ошибка обновления статуса лида: {e}")
            return False
    
    def get_statistics(self, date: str = None) -> Dict:
        """Получение статистики"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if date:
                    cursor.execute('''
                        SELECT 
                            COUNT(*) as total_leads,
                            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_leads,
                            (SELECT COUNT(*) FROM violations WHERE DATE(created_at) = ?) as violations_count
                        FROM leads 
                        WHERE DATE(created_at) = ?
                    ''', (date, date))
                else:
                    cursor.execute('''
                        SELECT 
                            COUNT(*) as total_leads,
                            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_leads,
                            (SELECT COUNT(*) FROM violations) as violations_count
                        FROM leads
                    ''')
                
                row = cursor.fetchone()
                
                return {
                    'total_leads': row[0] or 0,
                    'completed_leads': row[1] or 0,
                    'violations_count': row[2] or 0,
                    'date': date or 'all_time'
                }
                
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return {
                'total_leads': 0,
                'completed_leads': 0,
                'violations_count': 0,
                'date': date or 'all_time'
            }
    
    def export_leads_to_json(self, filename: str = "leads_export.json") -> bool:
        """Экспорт лидов в JSON файл"""
        try:
            leads = self.get_leads(limit=10000)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(leads, f, ensure_ascii=False, indent=2, default=str)
            
            logger.info(f"Лиды экспортированы в {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка экспорта лидов: {e}")
            return False

# Глобальный экземпляр менеджера базы данных
db_manager = DatabaseManager() 