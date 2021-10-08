"""
./commands/devops/__init__.py
management -> 서버 관리용 커맨드 로직
test -> 새 기능 시험용 로직
moderator -> 디스코드 팀 알림 받는 로직
"""
import database
import log
from ..devops import moderator, test, management


# Devops 카테고리 대상 fork
async def fork(channel, message, client):
    log.call(__name__, fork.__name__)
    # DEVOPS
    category_num = 7

    # moderator-only
    if channel.id == database.get_id_channel(category_num, 1):
        pass

    # test
    if channel.id == database.get_id_channel(category_num, 2):
        await test.fork(channel, message)

    # management
    if channel.id == database.get_id_channel(category_num, 4):
        await management.fork(channel, message, client)


