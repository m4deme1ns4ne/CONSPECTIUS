import os

import aiomysql
from dotenv import load_dotenv


class DatabaseConfig:
    """Хранит конфигурацию базы данных."""

    def __init__(self) -> None:
        load_dotenv()
        self._user = os.getenv("DB_USER", "root")
        self._db = os.getenv("DB_NAME", "conspectius")
        self._host = os.getenv("DB_HOST", "localhost")
        self._port = os.getenv("DB_PORT", 3306)

        # Бросаем исключение, если конфигурация отсутствует
        if not any([self._user, self._db, self._host, self._port]):
            raise ValueError(
                "Отсутствие конфигурации базы данных в переменных окружения."
            )

    @property
    def user(self):
        return self._user

    @property
    def db(self):
        return self._db

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port


class DatabaseConnection:
    """Управляет подключением к базе данных."""

    def __init__(self, config: DatabaseConfig) -> None:
        self.config = config
        self._connection = None

    async def get_connection(self):
        """Получение соединения с базой данных."""
        if not self._connection or self._connection.closed:
            self._connection = await aiomysql.connect(
                user=self.config.user,
                db=self.config.db,
                host=self.config.host,
                port=self.config.port,
                autocommit=True,  # Убедитесь, что транзакции выполняются автоматически
            )
        return self._connection


class UserManagement:
    """Управляет операциями с пользователями."""

    def __init__(self, connection: DatabaseConnection):
        self.connection = connection

    async def user_exists(self, telegram_id: int) -> bool:
        """Проверка существования пользователя в таблице users."""
        async with await self.connection.get_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    SELECT 1 FROM users WHERE telegram_id = %s
                """,
                    (telegram_id,),
                )
                result = await cur.fetchone()
                return result is not None

    async def add_user(self, telegram_id: int) -> None:
        """Добавление нового пользователя в таблицы users и usage_conspectius."""
        async with await self.connection.get_connection() as conn:
            async with conn.cursor() as cur:
                # Добавляем пользователя в таблицу users, если он ещё не существует
                await cur.execute(
                    "INSERT IGNORE INTO users (telegram_id) VALUES (%s)",
                    (telegram_id,),
                )

                # Добавляем запись в таблицу usage_conspectius, если её нет
                await cur.execute(
                    "INSERT IGNORE INTO usage_conspectius (telegram_id) VALUES (%s)",
                    (telegram_id,),
                )

    async def update_users_call_data(
        self, telegram_id: int, count: int
    ) -> None:
        """
        Обновление данных пользователя в таблице usage_conspectius.

        :param telegram_id: Уникальный идентификатор пользователя в Телеграмм.
        :param count: Количество вызовов модели.
        """

        async with await self.connection.get_connection() as conn:
            async with conn.cursor() as cur:
                # Здесь нужно жестко указать название столбца, который вы хотите обновить.
                # Например, если столбец называется 'call_count', то запрос будет таким:
                query = "UPDATE usage_conspectius SET call_count = %s WHERE telegram_id = %s"
                await cur.execute(query, (count, telegram_id))
