"""
./commands/lily/__init__.py
이루리랩 카테고리 명령어
"""
import log
import database
from commands import general


async def fork(channel, author, message):
    log.call(__name__, fork.__name__, channel_id=channel.id, author_id=author.id)

    # 이루리랩
    category_num = 2

    await general.fork(channel, author, message)
