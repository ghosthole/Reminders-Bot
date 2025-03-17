from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime

from app.keyboards import *
from app.database import *

router = Router()


class NewReminder(StatesGroup):
    title = State()
    description = State()
    date = State()


def start_text():
    text = f"""<b>Привет! 👋 Я – твой персональный бот-напоминалка!</b>
Больше никаких забытых встреч, дел и важных дат. Просто скажи мне, что и когда напомнить, и я все возьму на себя.

🕒 <b>Что я умею?</b>

⏰ Создать напоминание на любое время
📋 Показывать активные напоминания
✏️ Удалять или изменять напоминания

🚀 <b>Просто напиши мне, о чем напомнить, и я все запомню!</b>

Чтобы создать напоминание, <b>нажми на кнопку</b> ниже или <b>отправь команду</b>:
👉 <b>/new</b> – создать напоминание"""
    return text


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    username = message.from_user.username
    user_id = message.from_user.id
    await state.clear()
    if not await check_user(user_id):
        await message.answer("🌍 <b>Выбери свой часовой пояс</b>\n\nЭто нужно, чтобы напоминания и другие события приходили точно по твоему времени. Если вдруг ошибёшься, не переживай — в настройках всегда можно всё изменить. 😉", reply_markup=get_timezone_keyboard(), parse_mode="HTML")
        await add_user(user_id, username)
    else:
        
        await message.answer_photo(
        photo="https://media.wired.com/photos/653bddf62692abf70732f95b/master/pass/Google-Calendar-Appointments-Gear-GettyImages-1385868923.jpg",
        caption=start_text(),
        reply_markup=menu_keyboard,
        parse_mode="HTML"
    )


time_zones_list = [f"{i:+}" for i in range(-12, 15)]
@router.callback_query(F.data.startswith("utc"))
async def choose_time_zone(callback: CallbackQuery):
    if callback.data[3:] in time_zones_list:
        await callback.message.edit_text(f"✅ Вы выбрали часовой пояс: UTC{callback.data[3:]}")
        await callback.answer()
        await callback.message.answer_photo(
            photo="https://media.wired.com/photos/653bddf62692abf70732f95b/master/pass/Google-Calendar-Appointments-Gear-GettyImages-1385868923.jpg",
            caption=start_text(),
            reply_markup=menu_keyboard,
            parse_mode="HTML"
        )


@router.message(F.text == "✍️ Добавить напоминание")
async def add_reminder_button(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(NewReminder.title)
    await message.answer(
        "📝 Как будет <b>называться</b> твоё напоминание?", parse_mode="HTML"
    )


@router.message(F.text == "⚙️ Настройки")
async def settings(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        """⚙️ <b>Настройки</b>

Здесь ты можешь изменить параметры бота под себя:

🔔 <b>Уведомления</b> – включить или отключить напоминания
🔕 <b>Тишина</b> – отключить уведомления на определённое время
📅 <b>Формат даты</b> – выбрать, как отображать даты.


Выбери нужный пункт ниже! ⬇️""",
        reply_markup=settings_keyboard,
        parse_mode="HTML",
    )


@router.callback_query(F.data == "date_format")
async def date_format(callback: CallbackQuery):
    user_id = callback.from_user.id
    if await check_date_format(user_id) == 0:
        await callback.message.edit_text(
            """📅 <b>Формат даты</b>

Пожалуйста, выберите, в каком <b>формате вам удобно</b> вводить дату:

1️⃣ <b>дд/мм/гггг ЧЧ:ММ</b> (например, 25/02/2025)
2️⃣ <b>дд.мм.гггг ЧЧ:ММ</b> (например, 25.02.2025)

Нажмите на нужный вариант, и мы запомним ваш выбор! ✅                          
""",
            reply_markup=default_date_format_keyboard,
            parse_mode="HTML",
        )
    elif await check_date_format(user_id) == 1:
        await callback.message.edit_text(
            """📅 <b>Формат даты</b>

Пожалуйста, выберите, в каком <b>формате вам удобно</b> вводить дату:

1️⃣ <b>дд/мм/гггг ЧЧ:ММ</b> (например, 25/02/2025)
2️⃣ <b>дд.мм.гггг ЧЧ:ММ</b> (например, 25.02.2025)

Нажмите на нужный вариант, и мы запомним ваш выбор! ✅                          
""",
            reply_markup=changed_date_format_keyboard,
            parse_mode="HTML",
        )


@router.callback_query(F.data == "leave")
async def leave_first(callback: CallbackQuery):
    await callback.message.edit_text(
        """📅 <b>Формат даты</b>

Упс...Этот формат уже был выбран.""",
        reply_markup=back_to_date_format,
        parse_mode="HTML",
    )


@router.callback_query(F.data == "back_to_date_format")
async def back_to_date(callback: CallbackQuery):
    await date_format(callback)


@router.callback_query(F.data == "change_to_second")
async def change_to_second(callback: CallbackQuery):
    user_id = callback.from_user.id
    await update_date_format(user_id)
    await callback.message.edit_text(
        """📅 <b>Формат даты</b>
                                     
Отлично! Формат 2️⃣<b>дд.мм.гггг ЧЧ:ММ</b> выбран.
                                     
👇 Нажми на кнопку, чтобы вернуться в меню.""",
        reply_markup=back_to_menu_keyboard,
        parse_mode="HTML",
    )


@router.callback_query(F.data == "change_to_first")
async def change_to_first(callback: CallbackQuery):
    user_id = callback.from_user.id
    await update_date_format(user_id)
    await callback.message.edit_text(
        """📅 <b>Формат даты</b>
                                     
Отлично! Формат 1️⃣<b>дд/мм/гггг ЧЧ:ММ</b> выбран.
                                     
👇 Нажми на кнопку, чтобы вернуться в меню.""",
        reply_markup=back_to_menu_keyboard,
        parse_mode="HTML",
    )


@router.message(Command("new"))
async def title_step(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(NewReminder.title)
    await message.answer(
        "📝 Как будет <b>называться</b> твоё напоминание?", parse_mode="HTML"
    )


@router.message(NewReminder.title)
async def description_step(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(NewReminder.description)
    await message.answer(
        "💬 Теперь напиши <b>описание</b> твоего напоминания.",
        reply_markup=skip_step_keyboard,
        parse_mode="HTML",
    )


@router.message(NewReminder.description)
async def date_step(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(NewReminder.date)
    await message.answer(
        f"📅 Отлично, {message.from_user.first_name}! Напиши <b>дату и время</b>, когда я должен буду уведомить тебя.\nдд/мм/гггг ЧЧ:ММ (По умолчанию). Формат можно изменить в настройках.\nПример: 24/02/2025 18:13",
        parse_mode="HTML",
    )


@router.message(NewReminder.date)
async def end_step(message: Message, state: FSMContext):
    user_date = None
    user_id = message.from_user.id
    try:
        user_date_format = await check_date_format(user_id)
        today_date = datetime.now().strftime("%d/%m/%Y %H:%M") if user_date_format == 0 else datetime.now().strftime("%d.%m.%Y %H:%M")
        today_formated_date = datetime.strptime(today_date, "%d/%m/%Y %H:%M") if user_date_format == 0 else datetime.strptime(today_date, "%d.%m.%Y %H:%M")

        try:
            user_date = datetime.strptime(message.text, "%d/%m/%Y %H:%M") if user_date_format == 0 else datetime.strptime(message.text, "%d.%m.%Y %H:%M")
            print(f"Введенная дата: {message.text}")

            if user_date <= today_formated_date:
                await message.answer(
                    "❌ Эта дата теперь в прошлом :(\n"
                    f"Напиши дату и время в формате {'дд/мм/гггг ЧЧ:ММ' if user_date_format == 0 else 'дд.мм.гггг ЧЧ:ММ'}. "
                    "Формат можно изменить в настройках.\n"
                    f"Пример: {'24/02/2025 18:13' if user_date_format == 0 else '24.02.2025 18:13'}"
                )
                await state.set_state(NewReminder.date)
                print("Пользователь ввел дату, которая уже прошла.")
                return

        except ValueError:
            print("Ошибка: пользователь ввел дату в неправильном формате.")
            await message.answer(
                "❌ Ты ввел некорректную дату! Необходимо написать дату и время в формате "
                f"{'дд/мм/гггг ЧЧ:ММ' if user_date_format == 0 else 'дд.мм.гггг ЧЧ:ММ'}. "
                "Формат можно изменить в настройках.\n"
                f"Пример: {'24/02/2025 18:13' if user_date_format == 0 else '24.02.2025 18:13'}"
            )
            await state.set_state(NewReminder.date)
            return

    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        return
    if user_date is not None:
        await state.update_data(date=user_date.strftime("%d/%m/%Y %H:%M"))
    else:
        print("Ошибка: user_date остался None после обработки.")
    data = await state.get_data()

    if data["description"] != " ":
        await message.answer(
            f"""🎉 Ура, мы почти закончили! Проверь, корректно ли указаны данные.
                             
▫️ <b>Название</b>\n📌 {data["title"]}

▫️ <b>Описание</b>\n📝 {data["description"]}

▫️ <b>Дата</b>\n🗓️ {data["date"]}

Если ты увидел ошибку в заполненных данных, нажми на кнопку <b>"Заполнить заново"</b>""",
            reply_markup=check_data_keyboard,
            parse_mode="HTML",
        )
    else:
        await message.answer(
            f"""🎉 Ура, мы почти закончили! Проверь, корректно ли указаны данные.
                             
▫️ <b>Название</b>\n📌 {data["title"]}

▫️ <b>Дата</b>\n🗓️ {data["date"]}

Если ты увидел ошибку в заполненных данных, нажми на кнопку <b>"Заполнить заново"</b>""",
            reply_markup=check_data_keyboard,
            parse_mode="HTML",
        )


@router.callback_query(F.data == "skip")
async def skip_description(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.update_data(description=" ")
    await state.set_state(NewReminder.date)
    await callback.message.edit_text(
        f"📅 Отлично, {callback.from_user.first_name}! Напиши <b>дату и время</b>, когда я должен буду уведомить тебя.\nдд/мм/гггг ЧЧ:ММ (По умолчанию). Формат можно изменить в настройках.\nПример: 24/02/2025 18:13",
        parse_mode="HTML",
    )


@router.callback_query(F.data == "again")
async def again_data(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(NewReminder.title)
    await callback.message.edit_text(
        "📝 Как будет <b>называться</b> твоё напоминание?", parse_mode="HTML"
    )


@router.callback_query(F.data == "true")
async def true_data(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    data = await state.get_data()
    await add_reminder(user_id, data["title"], data["description"], data["date"])
    await callback.message.edit_text(
        "✅ Напоминание добавлено!", reply_markup=back_to_menu_keyboard
    )
    await state.clear()


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.clear()
    await callback.answer()
    await update_fun_fact(user_id)
    await callback.message.answer_photo(
        photo="https://img.freepik.com/premium-photo/calendar-with-marked-date-3d-render-illustration-purple-floating-organizer-with-rings-check-points-noted-with-mark-day_75114-1071.jpg",
        caption=f"""<b>📍 Меню</b>

<b>📚 А ты знал, что {await get_fun_fact(user_id)}</b>
Знаешь, напоминания — это помощники от забывчивости!
🤯 Они помогают не откладывать дела в долгий ящик и держать всё под контролем.

Сегодня — отличный день, чтобы сделать хотя бы одно важное дело, которое ты давно планировал. 💪 Может, записаться к врачу, купить подарок другу или просто напомнить себе выпить больше воды? 💧

Давай сделаем этот день продуктивнее! 🚀 Ты сам удивишься, как много можно успеть с небольшими напоминаниями.

Чтобы создать новое напоминание, <b>нажми на кнопку</b> ниже или <b>отправь команду</b>:
👉 <b>/new</b> – создать напоминание""",
        reply_markup=menu_keyboard,
        parse_mode="HTML",
    )


@router.message(F.text == "📖 Список напоминаний")
async def check_reminders(message: Message):
    user_id = message.from_user.id
    reminders_list = await get_reminders(user_id)
    caption = ""
    for title, description, creation_date, completion_date in reminders_list:
        if title:
            user_date_format = await check_date_format(user_id)
            today_date = datetime.now().strftime("%d/%m/%Y %H:%M") if user_date_format == 0 else datetime.now().strftime("%d.%m.%Y %H:%M")
            today_formated_date = datetime.strptime(today_date, "%d/%m/%Y %H:%M") if user_date_format == 0 else datetime.strptime(today_date, "%d.%m.%Y %H:%M")
            
            if description != " ":
                caption += f"""

Название: <b>{title}</b>
Описание: {description}
Дата создания: <b>{creation_date}</b>
Дата уведомления: <b>{completion_date}</b>
"""
            else:
                caption += f"""
                
Название: <b>{title}</b>
Дата создания: <b>{creation_date}</b>
Дата уведомления: <b>{completion_date}</b>
"""
    await message.answer_photo(photo="https://us.123rf.com/450wm/mbezvodinskikh/mbezvodinskikh2106/mbezvodinskikh210600012/170725861-bloc-de-notas-vac%C3%ADo-violeta-sobre-fondo-pastel-ilustraci%C3%B3n-de-procesamiento-3d-simple.jpg?ver=6",
                               caption="📖 <b>Список напоминаний</b>" + caption, parse_mode="HTML")


@router.callback_query(F.data == "one_minute")
async def add_one_minute(callback: CallbackQuery):
    users = await get_all_users()
    for user_id in users:
        user_date_format = await check_date_format(user_id)
        reminders = await get_reminders(user_id)
        for title, description, creation_date, completion_date in reminders:
            pass