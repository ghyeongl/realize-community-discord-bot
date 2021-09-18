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


# 하위 패키지로 fork
async def fork(channel, message):
    log.call(__name__, fork.__name__, author=database.get_disc_author(message.author), type=message.type)

    # 새 멤버 알림
    if message.type == discord.MessageType.new_member:
        await nice_to_meet_you(channel, message)

    # 명령어 !hello
    elif message.content.startswith('!hello'):
        await hello(channel)

    # 명령어 !도움
    elif message.content.startswith('!도움'):
        await help_request(channel)

    # 명령어 !ㅁㄹㅇ
    elif message.content.startswith('!ㅁㄹㅇ'):
        pass


# 새 멤버 알림이 왔을 때 실행하는 함수
async def nice_to_meet_you(channel, message):
    await channel.send(f"안녕하세요, {message.author.name}님! 만나서 반가워요.\n"
                       f"입회 절차를 완료하기 위해, 저(캡챠)에게 개인 메시지를 보내주세요!")


# 테스트
async def hello(channel):
    await channel.send("안녕하세요!")


# 명령어 !도움 반응
async def help_request(channel):
    embed = discord.Embed(title="")
    await channel.send()

