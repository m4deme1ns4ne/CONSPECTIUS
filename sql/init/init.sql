-- Создаем базу, если не существует
CREATE DATABASE IF NOT EXISTS conspectius;
USE conspectius;

-- Создание таблицы usage_conspectius
CREATE TABLE IF NOT EXISTS usage_conspectius (
    telegram_id BIGINT NOT NULL,
    count_conspect INT DEFAULT 0,
    PRIMARY KEY (telegram_id)
);

-- Создание таблицы users
CREATE TABLE IF NOT EXISTS users (
    telegram_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (telegram_id)
);
