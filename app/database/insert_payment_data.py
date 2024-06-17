import mysql.connector
from mysql.connector import Error
from logger import logger

from database.config import db_config


@logger.catch
def insert_payment_data(telegram_id, payment_date, subscription_end_date, subscription_status=True):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()
            insert_query = """INSERT INTO user_payments (telegram_id, payment_date, subscription_end_date, subscription_status)
                              VALUES (%s, %s, %s, %s)"""
            cursor.execute(insert_query, (telegram_id, payment_date, subscription_end_date, subscription_status))
            connection.commit()
            logger.info("Запись успешно вставлена в таблицу user_payments")

    except Error as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            logger.info("Соединение с MySQL закрыто")
