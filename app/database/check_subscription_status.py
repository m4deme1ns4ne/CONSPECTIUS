import mysql.connector
from mysql.connector import Error
from logger import logger
from database.config import db_config
from datetime import datetime

@logger.catch
def check_subscription_status(telegram_id):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()
            check_query = """SELECT subscription_status, subscription_end_date FROM user_payments 
                             WHERE telegram_id = %s ORDER BY payment_date DESC LIMIT 1"""
            cursor.execute(check_query, (telegram_id,))
            result = cursor.fetchone()
            if result:
                subscription_status, subscription_end_date = result
                if subscription_status and subscription_end_date < datetime.now():
                    # Обновляем статус подписки, если срок действия истек
                    update_query = """UPDATE user_payments 
                                      SET subscription_status = 0 
                                      WHERE telegram_id = %s AND subscription_status = 1"""
                    cursor.execute(update_query, (telegram_id,))
                    connection.commit()
                    return False
                return subscription_status
            return False
    except Error as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            logger.info("Соединение с MySQL закрыто")
