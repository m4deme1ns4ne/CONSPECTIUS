import mysql.connector
from mysql.connector import Error
from logger import logger
from datetime import timedelta

from database.config import db_config


@logger.catch
def insert_payment_data(telegram_id, payment_date, subscription_end_date, subscription_status=True):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()

            # Проверка наличия существующей записи
            check_query = """SELECT subscription_end_date FROM user_payments 
                             WHERE telegram_id = %s ORDER BY payment_date DESC LIMIT 1"""
            cursor.execute(check_query, (telegram_id,))
            result = cursor.fetchone()

            if result:
                # Обновляем существующую запись
                existing_end_date = result[0]
                new_end_date = max(existing_end_date, payment_date) + timedelta(days=30)
                update_query = """UPDATE user_payments 
                                  SET subscription_end_date = %s, subscription_status = %s
                                  WHERE telegram_id = %s"""
                cursor.execute(update_query, (new_end_date, subscription_status, telegram_id))
            else:
                # Вставляем новую запись
                insert_query = """INSERT INTO user_payments (telegram_id, payment_date, subscription_end_date, subscription_status)
                                  VALUES (%s, %s, %s, %s)"""
                cursor.execute(insert_query, (telegram_id, payment_date, subscription_end_date, subscription_status))

            connection.commit()
            logger.info("Запись успешно обновлена/вставлена в таблицу user_payments")

    except Error as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            logger.info("Соединение с MySQL закрыто")
