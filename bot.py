import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Бот запущен. Уведомления о выходах включены.")

@dp.chat_member()
async def member_update(event: types.ChatMemberUpdated):
    if event.old_chat_member.status in ("member", "restricted") and event.new_chat_member.status == "left":
        user = event.old_chat_member.user
        time = datetime.now().strftime("%d.%m.%Y %H:%M")

        text = (
            "🚪 Участник покинул группу\n"
            f"👤 Имя: {user.full_name}\n"
            f"🔗 @{user.username if user.username else 'нет username'}\n"
            f"🆔 ID: {user.id}\n"
            f"🕒 {time}"
        )

        await bot.send_message(ADMIN_ID, text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
