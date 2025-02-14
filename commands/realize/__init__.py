"""
./commands/realize/__init__.py
리얼라이즈 오리지널 카테고리

"""
import log
import database
from commands import general


async def fork(channel, author, message):
    log.call(__name__, fork.__name__, channel_id=channel.id, author_id=author.id)

    # 리얼라이즈 오리지널
    category_num = 6

    await general.fork(channel, author, message)
