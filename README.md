# Conspectius

![изображение](https://github.com/user-attachments/assets/c6cb0aee-0ad8-49ef-bccb-3fe4270065e5)

Conspectius — это программа, предназначенная для создания детализированных и академических конспектов на основе аудио лекций. Она помогает пользователям эффективно обрабатывать и структурировать информацию, полученную из аудио материалов, что особенно полезно для студентов и исследователей.


## Оглавление

- [Conspectius](#conspectius)
  - [Установка](#установка)
  - [Использование](#использование)
  - [Технологии](#технологии)
  - [Лицензия](#лицензия)
  - [Контакты](#контакты)

## Установка

Для установки проекта необходимо использовать [Poetry](https://python-poetry.org/). Убедитесь, что у вас установлен Python версии 3.12 или выше.

1. Клонируйте репозиторий:

  ```bash
  git clone https://github.com/m4deme1ns4ne/CONSPECTIUS.git
  git clone https://github.com/m4deme1ns4ne/site_conspectius.git

  cd CONSPECTIUS
  ```

2. Создайте файл `.env` в корне директории CONSPECTIUS и добавьте необходимые переменные окружения:

   ```
   TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
   OPENAI_API_KEY="your_openai_api_key"
   PROXY="your_proxy_url" (опционально)
   ASSEMBLY_AI_API="your_assembly_ai_token"
   URL=your_URL (для сервера загрузчика, опционально)

   MYSQL_ROOT_PASSWORD=your_MYSQL_ROOT_PASSWORD
   MYSQL_DATABASE=your_MYSQL_DATABASE
   MYSQL_USER=your_MYSQL_USER
   MYSQL_PASSWORD=your_MYSQL_PASSWORD
   MYSQL_PORT=your_MYSQL_PORT
   MYSQL_HOST=your_MYSQL_HOST
   ```

## Использование

Запустите бота с помощью следующей команды:

```bash
docker compose up --build -d
```

После запуска бота вы можете отправить аудиофайл, и он автоматически создаст конспект на основе вашего аудио сообщения. Бот поддерживает различные языки и может создавать конспекты разной длины в зависимости от ваших предпочтений.

## Технологии

Основные технологии и библиотеки использующиеся в проекте:

- **Python 3.12**: Основной язык программирования.
- **Aiogram**: Библиотека для создания Telegram-ботов.
- **AssemblyAI**: API для транскрибации аудио в текст.
- **Poetry**: Инструмент для управления зависимостями и упаковки.
- **OpenAI**: Библиотека предоставляющая доступ к LLM gpt.

## Лицензия

Этот проект лицензирован под лицензией GNU General Public License v3.0. Подробности можно найти в файле [LICENSE](LICENSE).

## Контакты
- **Имя**: Александр Волжанин
- **Email**: alexandervolzhanin2004@gmail.com
- **GitHub**: [m4deme1ns4ne](https://github.com/m4deme1ns4ne)
