"""
./commands/devops/__init__.py
관리화면에 관한 모든 것을 다루는 곳
"""
import database
import log
from ..devops import moderator, test


async def fork(channel, message):
    log.call(__name__, fork.__name__)
    # DEVOPS
    category_num = 8

    # moderator-only
    if channel.id == database.get_id_channel(category_num, 1):
        await moderator.fork(channel, message)

    # test
    if channel.id == database.get_id_channel(category_num, 2):
        await test.fork(channel, message)