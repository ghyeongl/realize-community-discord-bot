"""
./commands/captcha/not_a_robot.py
로봇이-아닙니다

"""
import log
import database
from commands import general


# 로봇이-아닙니다 채널의 명령어에 대한 모음
async def fork(channel, author, message):
    log.call(__name__, fork.__name__, channel_id=channel.id, author_id=author.id)

    if False:
        pass
    else:
        await general.fork(channel, author, message)
