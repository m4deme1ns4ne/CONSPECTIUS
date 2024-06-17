import mysql.connector
from mysql.connector import Error
from logger import logger
from database.config import db_config


@logger.catch
def check_subscription_status(telegram_id):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()
            check_query = """SELECT subscription_status FROM user_payments WHERE telegram_id = %s ORDER BY payment_date DESC LIMIT 1"""
            cursor.execute(check_query, (telegram_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return False
    except Error as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            logger.info("Соединение с MySQL закрыто")
