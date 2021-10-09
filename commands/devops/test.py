"""
./commands/devops/test.py
test 채널

"""
import discord
import log
import database
from commands import general


# test
async def fork(channel, author, message):
    log.call(__name__, fork.__name__, channel_id=channel.id, author_id=author.id)
    if message.content.startswith('!hello'):
        await hello(channel, author)

    elif message.content.startswith('!도움'):
        await help_request(channel, author)

    else:
        await general.fork(channel, author, message)


async def hello(channel, author):
    log.call(__name__, fork.__name__, channel_id=channel.id, author_id=author.id)
    await channel.send("안녕하세요!")


async def help_request(channel, author):
    log.call(__name__, help_request.__name__, channel_id=channel.id, author_id=author.id)
    embed = discord.Embed(title="메인 제목", description="설명", color=0x612371)
    embed.set_footer(text="하단 설명")
    await channel.send(embed=embed)
