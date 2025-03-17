import aiosqlite as sql
from datetime import datetime, timedelta
import random


async def create():
    async with sql.connect("reminders.db") as con:
        await con.execute(
            """CREATE TABLE IF NOT EXISTS users (
                          user_id INTEGER,
                          username TEXT NOT NULL,
                          date_format INTEGER NOT NULL DEFAULT 0,
                          fun_fact TEXT)"""
        )

        await con.execute(
            # is_completed take 0/1 (False/True)
            """CREATE TABLE IF NOT EXISTS reminders (
            user_id INTEGER,
            is_completed INTEGER NOT NULL DEFAULT 0,
            title TEXT NOT NULL,
            description TEXT,
            creation_date TEXT,
            completion_date TEXT)"""
        )
        await con.commit()


async def add_user(user_id, username):
    async with sql.connect("reminders.db") as con:
        await con.execute("""INSERT INTO users (user_id, username, date_format, fun_fact) VALUES (?, ?, ?, ?)""", (user_id, username, 0, "-"))
        await con.commit()


async def add_reminder(user_id, title, description, completion_date):
    async with sql.connect("reminders.db") as con:
        now_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        await con.execute(
            """INSERT INTO reminders (user_id,  title,
            description, creation_date, completion_date) VALUES (?, ?, ?, ?, ?)""",
            (user_id, title, description, now_date, completion_date)
        )
        await con.commit()


async def check_date_format(user_id):
    async with sql.connect("reminders.db") as con:
        cursor = await con.execute("""SELECT date_format FROM users WHERE user_id = ?""", (user_id,))
        date_format = await cursor.fetchone()
        return date_format[0]


async def update_date_format(user_id):
    async with sql.connect("reminders.db") as con:
        date_format = await check_date_format(user_id)
        if date_format == 0:
            date = 1
        else:
            date = 0
        await con.execute(
                """UPDATE users SET date_format = ? WHERE user_id = ?""", (date, user_id)
                )
        await con.commit()


async def update_fun_fact(user_id):
    async with sql.connect("reminders.db") as con:
        with open("interesting_facts.txt", "r+", encoding="utf-8") as file:
            facts_list = []
            for fact in file:
                parts = fact.rsplit(".", 1)
                ready_fact = "?".join(parts)[4:]
                facts_list.append(ready_fact[:1].casefold() + ready_fact[1:])
        await con.execute(
            """UPDATE users SET fun_fact = ? WHERE user_id = ?""", (random.choice(facts_list), user_id))
        await con.commit()

async def get_fun_fact(user_id):
    async with sql.connect("reminders.db") as con:
        cursor = await con.execute("SELECT fun_fact FROM users WHERE user_id = ?", (user_id,))
        user_fact = await cursor.fetchone()
        return user_fact[0]


async def get_reminders(user_id):
    async with sql.connect("reminders.db") as con:
        cursor = await con.execute("SELECT title, description, creation_date, completion_date FROM reminders WHERE user_id = ? AND is_completed = 0", (user_id,))
        reminder_info = await cursor.fetchall()
        return reminder_info


async def get_all_users():
    async with sql.connect("reminders.db") as con:
        cursor = await con.execute("SELECT user_id FROM users")
        user_ids = await cursor.fetchall()
        return [row[0] for row in user_ids]
    

async def check_user(user_id):
    async with sql.connect("reminders.db") as con:
        cursor = await con.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        user = await cursor.fetchone()
        return user


async def mark_reminder_as_completed(user_id, completion_date):
    async with sql.connect("reminders.db") as con:
        await con.execute("UPDATE reminders SET is_completed = 1 WHERE user_id = ? AND completion_date = ?", (user_id, completion_date.strftime("%d/%m/%Y %H:%M")))
        await con.commit()


async def update_one_minute(user_id, creation_date):
    async with sql.connect("reminders.db") as con:
        now = datetime.now()
        new_time = now + timedelta(minutes=1)
        await con.execute("UPDATE reminders SET completion_date = ? AND is_completed = 0 WHERE user_id = ? AND creation_date = ?", (new_time, user_id, creation_date))
        await con.commit()