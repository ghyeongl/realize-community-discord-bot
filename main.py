"""
디스코드 봇 캡챠 v1.0
메인 스크립트
commands, data, auth, database, log, main, verify
제작자: 류관형
"""
import discord
import commands
import verify
import auth
import database
import log

intents = discord.Intents().all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    log.call(__name__, on_ready.__name__, user=f"{client.user}")
    await client.change_presence(activity=discord.Game(name="일단 '!도움' 쳐봐 / 일"))


@client.event
async def on_message(message):
    # 변수 간소화
    channel = message.channel
    author = message.author
    name_tag = database.get_disc_author(author)

    # 디버그 채널인 경우 모두 무시
    if channel.id == database.get_id_channel(7, 3):
        return

    # 로그 정보 생성
    log_content = message.content
    if isinstance(channel, discord.channel.DMChannel):
        log_author = name_tag
        log_channel = channel.recipient.name + "#" + channel.recipient.discriminator
        log_etc = None
    else:
        log_author = name_tag
        log_channel = channel.name
        log_etc = {"Nick": author.nick}

    # 로깅
    log.division_line()
    log.call(__name__, on_message.__name__, author=log_author, channel=log_channel, content=log_content,
             author_id=author.id, channel_id=channel.id, note=log_etc)

    # 발신자가 봇인 경우 아래 내용 실행 안함
    if author == client.user:
        return

    # DM인 경우 fork_dm, 아닌경우 fork 호출
    if isinstance(channel, discord.channel.DMChannel):
        await commands.direct.fork(channel, message, author, client)
    elif message.content.startswith("!"):
        await commands.fork(channel, message, author, client)

    # 디버그 채널에 로그 전송
    debug_ch = client.get_channel(database.get_id_channel(7, 3))
    if log.remain:
        await debug_ch.send(file=discord.File(log.remain.pop()))
    if log.cache:
        await debug_ch.send('\n'.join(log.cache))
        log.cache.clear()


client.run('ODgyMTc1NTk5MTM1ODE3NzQ4.YS3kDA.t6Q7jLRBY8r5-t97NsCoCzeEq4w')
