"""
./commands/__init__.py
main 스크립트에서 호출되어 각종 채널에 따라 분류하는 역할
DM 채널의 경우도 수행
"""
import database
import log
import commands.direct
import commands.captcha
import commands.lily
import commands.nuri
import commands.mandry
import commands.realize
import commands.infinity
import commands.devops
import commands.general


# 서버 내 채널의 카테고리별 fork
async def fork(channel, author, message, client):
    category = channel.category
    log.call(__name__, fork.__name__, channel_id=channel.id, author_id=author.id)

    # CAPTCHA
    if category.id == database.get_id_category(1):
        await captcha.fork(channel, author, message)

    elif message.content.startswith("!"):
        # 이루리랩
        if category.id == database.get_id_category(2):
            await lily.fork(channel, author, message)

        # 나누리랩
        elif category.id == database.get_id_category(3):
            await nuri.fork(channel, author, message)

        # 맨드리랩
        elif category.id == database.get_id_category(4):
            await mandry.fork(channel, author, message)

        # 무한확장 대화채널
        elif category.id == database.get_id_category(5):
            await infinity.fork(channel, author, message)

        # 리얼라이즈 오리지널
        elif category.id == database.get_id_category(6):
            await realize.fork(channel, author, message)

        # DEVOPS
        elif category.id == database.get_id_category(7):
            await devops.fork(channel, author, message, client)

        # General
        else:
            await general.fork(channel, author, message)
