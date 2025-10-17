"""Менеджер веб-чата с поддержкой Normal и Admin режимов."""

import logging
from datetime import datetime
from enum import Enum
from typing import Any

from .database import Database
from .llm_client import LLMClient

logger = logging.getLogger(__name__)


class ChatMode(str, Enum):
    """Режимы работы чата."""

    NORMAL = "normal"
    ADMIN = "admin"


class ChatManager:
    """Менеджер веб-чата для администратора."""

    def __init__(self, database: Database, llm_client: LLMClient):
        """Инициализация менеджера чата.

        Args:
            database: Экземпляр Database для работы с БД
            llm_client: Клиент для работы с LLM
        """
        self.database = database
        self.llm_client = llm_client
        logger.info("ChatManager initialized")

    async def send_message(
        self, session_id: str, message: str, mode: ChatMode = ChatMode.NORMAL
    ) -> tuple[str, str | None]:
        """Отправка сообщения в чат и получение ответа.

        Args:
            session_id: ID сессии пользователя
            message: Сообщение от пользователя
            mode: Режим работы чата (normal/admin)

        Returns:
            Tuple[response, sql_query]: Ответ от LLM и SQL запрос (если admin режим)
        """
        logger.info(f"Processing message for session {session_id}, mode: {mode}")

        # Сохраняем сообщение пользователя
        await self._save_message(session_id, "user", message)

        # Получаем историю для контекста
        history = await self.get_history(session_id, limit=10)

        # Обрабатываем в зависимости от режима
        if mode == ChatMode.ADMIN:
            response, sql_query = await self._handle_admin_mode(message)
        else:
            response = await self._handle_normal_mode(history)
            sql_query = None

        # Сохраняем ответ ассистента
        await self._save_message(session_id, "assistant", response, sql_query)

        return response, sql_query

    async def _handle_normal_mode(
        self, history: list[dict[str, str]]
    ) -> str:
        """Обработка сообщения в Normal режиме.

        Args:
            history: История диалога

        Returns:
            Ответ от LLM
        """
        system_prompt = (
            "Ты AI-ассистент для администратора Telegram бота. "
            "Помогай администратору с вопросами по управлению ботом, "
            "объясняй функциональность и давай полезные советы."
        )

        return await self.llm_client.get_response(
            messages=history, system_prompt=system_prompt
        )

    async def _handle_admin_mode(self, message: str) -> tuple[str, str]:
        """Обработка сообщения в Admin режиме с Text2Postgre.

        Args:
            message: Вопрос пользователя

        Returns:
            Tuple[response, sql_query]: Ответ и сгенерированный SQL запрос
        """
        # Шаг 1: Генерируем SQL запрос
        sql_query = await self._generate_sql(message)

        # Шаг 2: Выполняем SQL запрос
        try:
            query_results = await self._execute_sql(sql_query)
        except Exception as e:
            logger.error(f"SQL execution error: {e}")
            return (
                f"Ошибка выполнения SQL запроса: {str(e)}",
                sql_query,
            )

        # Шаг 3: Формируем ответ через LLM
        response = await self._format_results(message, query_results, sql_query)

        return response, sql_query

    async def _generate_sql(self, question: str) -> str:
        """Генерация SQL запроса из вопроса на естественном языке.

        Args:
            question: Вопрос пользователя

        Returns:
            SQL запрос
        """
        text2postgre_prompt = """Ты эксперт по PostgreSQL.
Переведи вопрос пользователя в SQL запрос.

База данных PostgreSQL с таблицами:

**users:**
- user_id (BIGINT) - ID пользователя Telegram
- username (VARCHAR) - username пользователя
- first_name (VARCHAR) - имя пользователя
- last_name (VARCHAR) - фамилия пользователя
- language_code (VARCHAR) - код языка (ru, en, de, etc.)
- is_premium (BOOLEAN) - Premium статус
- is_bot (BOOLEAN) - является ли ботом
- created_at (TIMESTAMP) - дата регистрации

**messages:**
- id (SERIAL) - ID сообщения
- user_id (BIGINT) - ID пользователя
- chat_id (BIGINT) - ID чата
- role (VARCHAR) - роль (user, assistant, system)
- content (TEXT) - текст сообщения
- character_count (INT) - количество символов
- created_at (TIMESTAMP) - дата создания
- deleted_at (TIMESTAMP) - дата удаления (NULL если не удалено)

Важно:
- Используй ТОЛЬКО SELECT запросы
- Учитывай поле deleted_at (WHERE deleted_at IS NULL для неудаленных)
- Исключай ботов (WHERE is_bot = FALSE) при запросах по users
- Используй агрегации и GROUP BY где уместно
- Форматируй даты с помощью to_char() для читабельности

Верни ТОЛЬКО SQL запрос, без объяснений, без markdown кода."""

        messages = [{"role": "user", "content": f"Вопрос: {question}"}]

        sql_query = await self.llm_client.get_response(
            messages=messages, system_prompt=text2postgre_prompt
        )

        # Очистка от markdown и лишних символов
        sql_query = sql_query.strip()
        if sql_query.startswith("```sql"):
            sql_query = sql_query[6:]
        if sql_query.startswith("```"):
            sql_query = sql_query[3:]
        if sql_query.endswith("```"):
            sql_query = sql_query[:-3]

        sql_query = sql_query.strip()

        logger.info(f"Generated SQL: {sql_query}")
        return sql_query

    async def _execute_sql(self, sql_query: str) -> list[dict[str, Any]]:
        """Выполнение SQL запроса.

        Args:
            sql_query: SQL запрос

        Returns:
            Результаты запроса
        """
        # Проверка безопасности: только SELECT запросы
        if not sql_query.strip().upper().startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed")

        conn = self.database._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql_query)
                results = cur.fetchall()
                logger.info(f"SQL returned {len(results)} rows")
                return results
        finally:
            conn.close()

    async def _format_results(
        self, question: str, results: list[dict[str, Any]], sql_query: str
    ) -> str:
        """Форматирование результатов SQL через LLM.

        Args:
            question: Оригинальный вопрос
            results: Результаты SQL запроса
            sql_query: Выполненный SQL запрос

        Returns:
            Человекочитаемый ответ
        """
        format_prompt = """Ты AI-ассистент для администратора.
Пользователь задал вопрос о статистике бота, был выполнен SQL запрос.
Сформируй понятный ответ на основе результатов.

Требования:
- Ответ должен быть коротким и по делу
- Используй форматирование (списки, выделения)
- Если результатов нет, скажи об этом
- Добавь краткий вывод или инсайт если уместно"""

        results_text = self._format_results_as_text(results)

        messages = [
            {
                "role": "user",
                "content": f"""Вопрос: {question}

SQL запрос:
{sql_query}

Результаты:
{results_text}

Сформируй ответ для администратора.""",
            }
        ]

        return await self.llm_client.get_response(
            messages=messages, system_prompt=format_prompt
        )

    def _format_results_as_text(self, results: list[dict[str, Any]]) -> str:
        """Форматирование результатов SQL в текст.

        Args:
            results: Результаты запроса

        Returns:
            Текстовое представление
        """
        if not results:
            return "Пусто (0 строк)"

        if len(results) == 1 and len(results[0]) == 1:
            # Если один результат с одним полем, просто выводим значение
            value = list(results[0].values())[0]
            return str(value)

        # Форматируем как таблицу
        lines = []
        for row in results[:50]:  # Лимит 50 строк
            row_str = ", ".join(f"{k}: {v}" for k, v in row.items())
            lines.append(row_str)

        if len(results) > 50:
            lines.append(f"... (еще {len(results) - 50} строк)")

        return "\n".join(lines)

    async def get_history(
        self, session_id: str, limit: int = 10
    ) -> list[dict[str, str]]:
        """Получение истории чата для сессии.

        Args:
            session_id: ID сессии
            limit: Лимит сообщений

        Returns:
            История в формате OpenAI API
        """
        conn = self.database._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT role, content
                    FROM chat_messages
                    WHERE session_id = %s
                    ORDER BY created_at DESC
                    LIMIT %s
                    """,
                    (session_id, limit),
                )
                messages = cur.fetchall()

                # Reverse to get chronological order
                history = [
                    {"role": msg["role"], "content": msg["content"]}
                    for msg in reversed(messages)
                ]

                logger.debug(f"Retrieved {len(history)} messages for session {session_id}")
                return history
        finally:
            conn.close()

    async def clear_history(self, session_id: str) -> None:
        """Очистка истории чата для сессии.

        Args:
            session_id: ID сессии
        """
        conn = self.database._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM chat_messages WHERE session_id = %s",
                    (session_id,),
                )
                conn.commit()
                logger.info(f"History cleared for session {session_id}")
        finally:
            conn.close()

    async def _save_message(
        self, session_id: str, role: str, content: str, sql_query: str | None = None
    ) -> None:
        """Сохранение сообщения в БД.

        Args:
            session_id: ID сессии
            role: Роль (user/assistant/system)
            content: Содержимое сообщения
            sql_query: SQL запрос (опционально, для admin режима)
        """
        conn = self.database._get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO chat_messages (session_id, role, content, sql_query, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (session_id, role, content, sql_query, datetime.now()),
                )
                conn.commit()
        finally:
            conn.close()

