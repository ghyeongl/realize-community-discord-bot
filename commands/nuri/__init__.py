"""
./commands/nuri/__init__.py
나누리랩 카테고리

"""
import log
import database
from commands import general


async def fork(channel, author, message):
    log.call(__name__, fork.__name__, channel_id=channel.id, author_id=author.id)

    # 나누리랩
    category_num = 3

    await general.fork(channel, author, message)
