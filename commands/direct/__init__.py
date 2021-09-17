"""
./commands/direct/__init__.py
DM을 건 유저를 DB 에서 읽어오고, 요청에 따라 관련 기능을 보여줌
* 추후 필요한 경우 회원가입 등 장문 파일을 나눌 것
"""

import discord
import database
import log
import commands.direct.signup


# fork
async def fork(channel, message, client):
    log.call(__name__, fork.__name__)

    # DB에 등록되지 않은 새 사용자일 경우
    if not database.find_author_id(message.author.id):
        await signup.fork(channel, message, client)

    # 명령어 !도움
    elif message.content.startswith("!도움"):
        await help_request(channel, message)
        pass

    # 명령어 !대나무숲
    elif message.content.startswith("!대나무숲"):
        await bamboo(channel, message)
        pass

    # 명령어 !확인
    elif message.content.startswith("!확인"):
        await check(channel, message)
        pass


# 명령어 !도움 에 대한 함수
async def help_request(channel, message):
    embed = discord.Embed(title="봇 이용방법", description="리얼라이즈 커뮤니티의 디스코드 봇 캡챠", color=0x612371)

    embed.set_footer(text="하단 설명")
    await channel.send(embed=embed)


# 명령어 !대나무숲 에 대한 함수
async def bamboo(channel, message):
    pass


# 명령어 !확인 에 대한 함수
async def check(channel, message):
    pass
