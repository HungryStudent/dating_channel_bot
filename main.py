from aiogram.utils import executor
from create_bot import dp, scheduler, bot
from utils import db
from handlers import users
from handlers import admin


async def on_startup(_):
    db.start()
    await bot.send_photo(796644977, "https://sun9-82.userapi.com/impg/gNTRJuRvRRtEl5Ehu4peXtt0WQxysXupcoXRoA/i9lMsJZa7tk.jpg?size=510x510&quality=95&sign=146f2eb1adc2ef5c79d5c4bb248547c0&c_uniq_tag=LwxfGu1jo9iecxhFxaC2YmYsDPrWqWHV3kt0uXZXzZw&type=album")


if __name__ == "__main__":
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
