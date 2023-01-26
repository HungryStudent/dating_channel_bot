from aiogram.utils import executor
from create_bot import dp, scheduler
from utils import db
from handlers import users
from handlers import admin


async def on_startup(_):
    db.start()


if __name__ == "__main__":
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
