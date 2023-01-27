from aiogram.types import MediaGroup
from vkbottle.bot import Bot
from vkbottle import GroupEventType, GroupTypes

from config import VK_TOKEN, channel_id
from create_bot import bot

import logging

from keyboards import admin

vk_bot = Bot(VK_TOKEN)
logging.getLogger("vkbottle").setLevel(logging.INFO)
logging.getLogger("aiogram").setLevel(logging.INFO)


@vk_bot.on.raw_event(GroupEventType.WALL_POST_NEW, dataclass=GroupTypes.WallPostNew)
async def new_post(event: GroupTypes.WallPostNew):
    if event.object.post_type.value != "post":
        return
    user = await vk_bot.api.users.get(event.object.signer_id, fields=["domain"])
    if not event.object.attachments:
        await bot.send_message(channel_id, event.object.text + "\nhttps://vk.com/" + user[0].domain,
                               reply_markup=admin.bot_url)
    elif len(event.object.attachments) == 1:
        await bot.send_photo(channel_id, event.object.attachments[0].photo.sizes[-1].url,
                             caption=event.object.text + "\nhttps://vk.com/" + user[0].domain,
                             reply_markup=admin.bot_url)
    else:
        media = MediaGroup()
        media.attach_photo(event.object.attachments[0].photo.sizes[-1].url,
                           caption=event.object.text + "\nhttps://vk.com/" + user[0].domain)
        event.object.attachments.pop(0)
        for photo in event.object.attachments:
            media.attach_photo(photo.photo.sizes[-1].url)
        await bot.send_media_group(channel_id, media)


vk_bot.run_forever()
