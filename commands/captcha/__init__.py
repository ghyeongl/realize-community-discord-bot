"""
./commands/captcha/__init__.py
첫 번째 카테고리 CAPTCHA 에서 채널별로 분류하는 역할
"""
import database
import log
from ..captcha import entrance, not_a_robot


async def fork(channel, author, message):
    log.call(__name__, fork.__name__, channel_id=channel.id, author_id=author.id)

    # CAPTCHA
    category_num = 1

    # 입국-수속
    if channel.id == database.get_id_channel(category_num, 1):
        await entrance.fork(channel, author, message)

    # 로봇이-아닙니다
    elif channel.id == database.get_id_channel(category_num, 2):
        await not_a_robot.fork(channel, author, message)
