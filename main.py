"""
디스코드 봇 캡챠 v1.0
메인 스크립트
제작자: 류관형
"""
import discord
import commands
import verify
import auth
import database
import log

client = discord.Client()


@client.event
async def on_ready():
    log.call(__name__, on_ready.__name__, user=f"{client.user}")


"""
on_message 함수에서 fork 시 필요한 객체


"""
@client.event
async def on_message(message):
    # 발신자 동일 체크
    if message.author == client.user:
        if isinstance(message.channel, discord.channel.DMChannel):
            log.call(__name__, on_message.__name__, author=message.author.name, channel=message.author.name,
                     content=message.content)
        else:
            log.call(__name__, on_message.__name__, author=message.author.name, channel=message.channel.name,
                     content=message.content)
        return

    # 로깅
    log.division_line()
    log.call(__name__, on_message.__name__, author=message.author.name, content=message.content)

    # DM 채널인 경우 commands.fork_dm
    if isinstance(message.channel, discord.channel.DMChannel):
        log.call(__name__, on_message.__name__, is_DM=True, channel=message.author.name)
        channel = message.channel
        await commands.fork_dm(channel, message)

    # 일반 채널인 경우 commands.fork. -> fork
    else:
        log.call(__name__, on_message.__name__, is_DM=False, channel=message.channel.name)
        category = message.channel.category
        channel = message.channel
        await commands.fork(category, channel, message)

    # 로그 전송
    debug_ch = client.get_channel(database.get_id_channel(8, 3))
    try:
        await debug_ch.send('\n'.join(log.cache))
    except discord.errors.HTTPException:
        await debug_ch.send('400: [discord.errors.HTTPException]')
    log.cache.clear()


client.run('ODgyMTc1NTk5MTM1ODE3NzQ4.YS3kDA.t6Q7jLRBY8r5-t97NsCoCzeEq4w')
