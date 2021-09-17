import discord


async def fork(channel, message):
    if message.content.startswith('!hello'):
        await hello(channel)

    if message.content.startswith('!도움'):
        await request_help(channel)


async def hello(channel):
    await channel.send("안녕하세요!")


async def request_help(channel):
    embed = discord.Embed(title="메인 제목", description="설명", color=0x612371)
    embed.set_footer(text="하단 설명")
    await channel.send(embed=embed)