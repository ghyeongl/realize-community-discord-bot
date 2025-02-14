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
async def fork(channel, author, message, client):
    log.call(__name__, fork.__name__, author_id=author.id, channel_id=channel.id)

    # DB에 등록되지 않은 새 사용자일 경우
    if not database.in_member(author.id):
        await signup.fork(channel, author, message, client)

    # 명령어 !도움
    elif message.content.startswith("!도움"):
        await help_request(channel, author, message)
        pass

    # 명령어 !대나무숲
    elif message.content.startswith("!대나무숲"):
        await bamboo(channel, author, message)
        pass

    # 명령어 !확인
    elif message.content.startswith("!확인"):
        await check(channel, author, message)
        pass

    # 등록된 사용자일 경우
    elif database.in_member(author.id):
        await default(channel, author, message)


# 명령어 !도움 에 대한 함수
async def help_request(channel, author, message):
    log.call(__name__, help_request.__name__, author_id=author.id, channel_id=channel.id)
    embed = discord.Embed(title="봇 이용방법", description="리얼라이즈 커뮤니티의 디스코드 봇 캡챠", color=0x612371)

    embed.set_footer(text="하단 설명")
    await channel.send(embed=embed)


# 명령어 !대나무숲 에 대한 함수
async def bamboo(channel, author, message):
    log.call(__name__, bamboo.__name__, author_id=author.id, channel_id=channel.id)
    pass


# 명령어 !확인 에 대한 함수
async def check(channel, author, message):
    log.call(__name__, check.__name__, author_id=author.id, channel_id=channel.id)
    pass


# 등록된 사용자의 경우
async def default(channel, author, message):
    log.call(__name__, default.__name__, author_id=author.id, channel_id=channel.id)
    await channel.send("안녕하세요! '!도움' 을 입력해 명령어를 알아보세요.")
