"""
./commands/general.py
기본적인 커맨드들

"""

import discord

import log


async def fork(channel, author, message):
    log.call(__name__, fork.__name__, channel_id=channel.id, author_id=author.id)

    if message.content.startswith("!도움"):
        await help_request(channel, author)


# !도움
async def help_request(channel, author):
    log.call(__name__, help_request.__name__, channel_id=channel.id, author_id=author.id)
    embed = discord.Embed(title="Realize Community 도움말",
                          description="커뮤니티에 오신 여러분들을 모두 환영해요! 카테고리는 모두 4개로 이루어져 있어요.", color=0xd63864)
    embed.add_field(name="CAPTCHA", value="커뮤니티의 입구와도 같은 곳이에요. 새로 들어오는 분들의 가입을 돕고 있어요.\n.", inline=False)
    embed.add_field(name="이루리랩", value="커뮤니티의 광장이예요. 자유롭게 대화를 나누고, 협업할 친구를 찾아요. "
                                       "어제만든 메이킹 작품을 자랑하거나, 익명 게시글을 올려요."
                                       "(대나무숲 기능은 10/25 출시예정)\n.", inline=False)
    embed.add_field(name="나누리랩", value="커뮤니티의 시장이예요. 나눌 수 있는 모든걸 나누고, 모르는건 자유롭게 질문해봐요! "
                                       "재능기부에 썼던 아두이노가 남는다구요? 나누리랩에 올려보세요!\n.", inline=False)
    embed.add_field(name="맨드리랩", value="학교에는 생각보다 많은 부품과 기자재들이 있지만, 많은 사람들이 잘 몰라요. "
                                       "3D 프린터가 필요한가요? 학교에 투명망토가 있나요? 맨드리랩에 물어보세요!\n.", inline=False)
    embed.add_field(name="무한확장 대화채널", value="친구와 대화할 공간이 필요하면 여기로 오세요! (무한확장 기능은 11월중 출시예정)")
    embed.set_footer(text="챗봇 캡챠는 세종과고 리얼라이즈에서 ♡을 담아 만듭니다.")
    await channel.send(embed=embed)
