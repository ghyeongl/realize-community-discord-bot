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
import commands.lily_circle
import commands.nuri
import commands.mandry
import commands.realize
import commands.infinity
import commands.devops


# 서버 내 채널의 카테고리별 fork
async def fork(channel, message, author, client):
    category = channel.category
    log.call(__name__, fork.__name__, author=database.get_disc_author(author), content=message.content)

    # CAPTCHA
    if category.id == database.get_id_category(1):
        await captcha.fork(channel, message)

    # 이루리랩
    elif category.id == database.get_id_category(2):
        await lily.fork(channel, message)

    # 이루리랩 써클
    elif category.id == database.get_id_category(3):
        await lily_circle.fork(channel, message)

    # 나누리랩
    elif category.id == database.get_id_category(4):
        await nuri.fork(channel, message)

    # 맨드리랩
    elif category.id == database.get_id_category(5):
        await mandry.fork(channel, message)

    # 리얼라이즈 오리지널
    elif category.id == database.get_id_category(6):
        await realize.fork(channel, message)

    # 무한확장 대화채널
    elif category.id == database.get_id_category(7):
        await infinity.fork(channel, message)

    # DEVOPS
    elif category.id == database.get_id_category(8):
        await devops.fork(channel, message)
