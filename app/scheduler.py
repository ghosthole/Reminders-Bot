from app.database import (
    check_date_format,
    get_reminders,
    get_all_users,
    mark_reminder_as_completed
)
from app.keyboards import (set_new_date)
from datetime import datetime
from aiogram import Bot
import logging



async def send_reminders(bot: Bot):
    """Функция для проверки и отправки напоминаний пользователям."""
    logging.info("Функция send_reminders запустилась!")  # Логирование
    users = await get_all_users()
    logging.info(f"Получены пользователи: {users}")  # Проверяем, есть ли пользователи

    for user_id in users:
        logging.info(f"Обрабатываем пользователя: {user_id}")  # Лог для каждого пользователя
        user_date_format = await check_date_format(user_id)

        # Получаем текущее время БЕЗ секунд и микросекунд
        now = datetime.now().replace(second=0, microsecond=0)
        logging.info(f"Текущее время (без секунд): {now}")

        reminders = await get_reminders(user_id)
        logging.info(f"Напоминания пользователя {user_id}: {reminders}")

        for title, description, creation_date, completion_date in reminders:
            # Если completion_date хранится как строка в БД, преобразуем её
            if isinstance(completion_date, str):
                completion_date = datetime.strftime(
                    completion_date, "%d/%m/%Y %H:%M" if user_date_format == 0 else "%d.%m.%Y %H:%M"
                )

            # Убираем секунды у даты завершения
            completion_date = completion_date.replace(second=0, microsecond=0)

            logging.info(f"Время пользователя (без секунд): {completion_date}")

            # Проверяем, если разница не больше минуты (в случае мелких рассинхронов)
            if abs((now - completion_date).total_seconds()) < 60:
                text = f"⏰ <b>Напоминание!</b>\n\n📌 {title}\n\n🚀 <b>Нужно немного больше времени?</b> Просто выбери удобный вариант из предложенных или введи своё время."
                if description and description.strip():
                    text += f"\n💬 {description}"
                logging.info(f"Отправка напоминания пользователю {user_id}: {text}")
                await bot.send_message(user_id, text, parse_mode="HTML", reply_markup=set_new_date)

                # Помечаем напоминание, как отправленное
                await mark_reminder_as_completed(user_id, completion_date)