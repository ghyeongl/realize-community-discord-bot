"""
./commands/captcha/entrance.py
명령어에 따라 실행할 함수를 담고 있음.
- 처음 들어온 사람에게 답장
- 테스트 구문
- 채널 내 도움말 임베드 실행
"""
import discord

import database
import log
from commands import general


# 하위 패키지로 fork
async def fork(channel, author, message):
    log.call(__name__, fork.__name__, channel_id=channel.id, author_id=author.id, type=message.type)

    # 새 멤버 알림
    if message.type == discord.MessageType.new_member:
        await nice_to_meet_you(channel, author, message)

    else:
        await general.fork(channel, author, message)


# 새 멤버 알림이 왔을 때 실행하는 함수
async def nice_to_meet_you(channel, author, message):
    log.call(__name__, nice_to_meet_you.__name__, channel_id=channel.id, author_id=author.id, name=author.name)
    await channel.send(f"안녕하세요, {author.name}님! 만나서 반가워요.\n"
                       f"입회 절차를 완료하기 위해, 저(캡챠)에게 개인 메시지를 보내주세요!")
