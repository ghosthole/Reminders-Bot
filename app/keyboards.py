from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


back_to_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️ Вернуться в меню", callback_data="back_to_menu")]
])

skip_step_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Пропустить", callback_data="skip")]
])

check_data_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔄 Заполнить заново", callback_data="again"), InlineKeyboardButton(text="✅ Данные верны", callback_data="true")]
])

menu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="✍️ Добавить напоминание")],
    [KeyboardButton(text="📖 Список напоминаний"), KeyboardButton(text="⚙️ Настройки")],
], resize_keyboard=True)

settings_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔔 Уведомления", callback_data="notifications"), InlineKeyboardButton(text="🔕 Тишина", callback_data="mute")],
    [InlineKeyboardButton(text="📅 Формат даты", callback_data="date_format")]
])

default_date_format_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ дд/мм/гггг ЧЧ:ММ", callback_data="leave"), InlineKeyboardButton(text="дд.мм.гггг ЧЧ:ММ", callback_data="change_to_second")]
])
changed_date_format_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="дд/мм/гггг ЧЧ:ММ", callback_data="change_to_first"), InlineKeyboardButton(text="✅ дд.мм.гггг ЧЧ:ММ", callback_data="leave")]
])

back_to_date_format = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📅 Вернуться к выбору формата даты", callback_data="back_to_date_format")]
])

set_new_date = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="3️⃣ минуты", callback_data="three_minute"), InlineKeyboardButton(text="5️⃣ минут", callback_data="five_minutes"), InlineKeyboardButton(text="🔟 минут", callback_data="ten_minutes")],
    [InlineKeyboardButton(text="⬅️ Вернуться в меню", callback_data="back_to_menu"), InlineKeyboardButton(text="🕐 Ввести своё время", callback_data="set_any_time")]
])



def get_timezone_keyboard():
    time_zones_list = [f"{i:+}" for i in range(-12, 15)]
    buttons = [InlineKeyboardButton(text=f"UTC {i}", callback_data=f"utc{i}") for i in time_zones_list]
    other_button = InlineKeyboardButton(text="Другие", callback_data="other")
    buttons.append(other_button)
    rows = [buttons[i:i+4] for i in range(0, len(buttons), 4)]
    return InlineKeyboardMarkup(inline_keyboard=rows)

[InlineKeyboardButton(text="UTC -9:30", callback_data="utc-9:30"), InlineKeyboardButton(text="UTC -4:30", callback_data="utc-4:30"), InlineKeyboardButton(text="UTC -3:30", callback_data="utc-3:30"),
 InlineKeyboardButton(text="UTC +3:30", callback_data="utc+3:30"), InlineKeyboardButton(text="UTC +4:30", callback_data="utc+4:30"), InlineKeyboardButton(text="UTC +5:30", callback_data="utc+5:30"),
 InlineKeyboardButton(text="UTC +5:45", callback_data="utc+5:45"), InlineKeyboardButton(text="UTC +6:30", callback_data="utc+6:30"), InlineKeyboardButton(text="UTC +8:45", callback_data="utc+8:45"),
 InlineKeyboardButton(text="UTC +9:30", callback_data="utc+9:30"), InlineKeyboardButton(text="UTC +10:30", callback_data="utc+10:30"), InlineKeyboardButton(text="UTC +12:45", callback_data="utc+12:45")]