"""
./commands/direct/__init__.py
DM을 건 유저를 DB 에서 읽어오고, 요청에 따라 관련 기능을 보여줌
* 추후 필요한 경우 회원가입 등 장문 파일을 나눌 것
"""

import discord
import log
member_info = {}
member_id = []
name = {}
number = {}


async def first_greet(channel, message):
    global member_info, member_id, name, number
    log.call(__name__, first_greet.__name__, member_info=member_info, member_id=member_id, name=name, number=number)
    author_id_str = str(message.author.id)

    if author_id_str in member_id:

        if message.content.startswith('초기화'):
            del member_info[author_id_str]
            member_id.remove(author_id_str)
            await channel.send("초기화되었습니다. 언제든 제게 메시지를 보내 다시 진행할 수 있어요!")

        if member_info[author_id_str]["agree"] == "":
            if message.content.startswith('예'):
                member_info[author_id_str]["agree"] = True
                await channel.send('진행을 시작합니다. 이름을 입력해주세요! (실명을 입력하지 않을 경우, 등록 요청이 기각될 수 있어요.)')
            elif message.content.startswith('아니'):
                del member_info[author_id_str]
                member_id.remove(author_id_str)
                await channel.send('등록을 취소합니다. 언제든 제게 메시지를 보내 다시 진행할 수 있어요!')
            else:
                await channel.send('제대로 입력해주세요!')

        elif member_info[author_id_str]["name"] == "":

            if name.get(author_id_str) is None:
                name[author_id_str] = message.content
                await channel.send(f'{message.content}님! 만나서 반가워요. 제가 옳게 부르고 있나요? (예/아니오)')
            else:
                if message.content.startswith('예'):
                    member_info[author_id_str]["name"] = name[author_id_str]
                    del name[author_id_str]
                    await channel.send('이름이 추가되었어요! 몇 기인가요? (숫자만 입력해주세요!)')
                elif message.content.startswith('아니'):
                    del name[author_id_str]
                    await channel.send(f'이름이 제거되었어요. 다시 입력해주세요!')
                else:
                    await channel.send(f'제대로 대답해주세요!')

        elif member_info[author_id_str]["number"] == "":

            if number.get(author_id_str) is None:
                if message.content.isdigit():
                    number[author_id_str] = message.content
                    await channel.send(f"{number[author_id_str]}기로 입력되었어요. 맞나요? (예/아니오)")

                elif message.content.split('기')[0].isdigit():
                    number[author_id_str] = message.content.split('기')[0]
                    await channel.send(f"{number[author_id_str]}기로 입력되었어요. 맞나요? (예/아니오)")

                else:
                    await channel.send("제대로 입력해주세요!")

            else:
                if message.content.startswith('예'):
                    member_info[author_id_str]["number"] = number[author_id_str]
                    del number[author_id_str]
                    await channel.send('기수가 추가되었어요! 리얼라이즈 동아리에 소속되어있나요? (예/아니오)')

                elif message.content.startswith('아니'):
                    del number[author_id_str]
                    await channel.send('입력값이 제거되었어요. 몇 기인가요? (숫자만 입력해주세요)')

                else:
                    await channel.send('제대로 대답해주세요!')

        elif member_info[author_id_str]["realize"] == "":
            if message.content.startswith('예'):
                member_info[author_id_str]["realize"] = True
                await channel.send(f'입력된 값이예요: {member_info[author_id_str]}. 등록 요청을 전송할까요? (예/아니오)')

            elif message.content.startswith('아니'):
                member_info[author_id_str]["realize"] = False
                await channel.send(f'입력된 값이예요: {member_info[author_id_str]}. 등록 요청을 전송할까요? (예/아니오)')

            else:
                await channel.send('제대로 대답해주세요!')

        elif member_info[author_id_str]["realize"] != "":
            if message.content.startswith('예'):
                await admin(member_info[author_id_str], message.author)
                member_id.remove(author_id_str)
                await channel.send('전송했습니다. 감사합니다.')

            elif message.content.startswith('아니'):
                del member_info[author_id_str]
                member_id.remove(author_id_str)
                await channel.send('초기화 되었어요. 아무거나 입력하면 다시 진행합니다.')

            else:
                await channel.send('제대로 대답해주세요!')

        else:
            del member_info[author_id_str]
            member_id.remove(author_id_str)
            await channel.send('알 수 없는 에러 발생. 초기화됩니다. 아무거나 입력하면 다시 진행합니다.')

    elif author_id_str in member_info:
        await channel.send('승인을 기다리고 있어요. 잠시만 기다려주세요! \n초기화를 통해 승인 목록에서 제거할 수 있어요.')

        if message.content.startswith('초기화'):
            del member_info[author_id_str]
            await channel.send('초기화 되었어요. 아무거나 입력하면 다시 진행합니다.')

    else:
        member_id.append(author_id_str)
        member_info[author_id_str] = {"name": "", "number": "", "realize": "", "agree": ""}
        await channel.send("처음뵙겠습니다! 저는 리얼라이즈 커뮤니티의 봇 '캡챠' 라고 해요!\n"
                           "이제부터 등록 절차를 진행할거예요! 등록시 개인정보 처리방침에 동의하는 것으로 간주됩니다.\n"
                           "(개인정보 처리방침은 서버 내 공지-및-문화에서 확인할 수 있어요!)\n"
                           "진행하시겠습니까? (예/아니오)  (문제가 생기면 '초기화' 를 입력하세요.)")


async def admin(information, author):
    log.call(__name__, admin.__name__, author=author, information=information)
    print(f"{information} | {author} | {author.id}")


async def help_request(channel, message):
    embed = discord.Embed(title="봇 이용방법", description="리얼라이즈 커뮤니티의 디스코드 봇 캡챠", color=0x612371)

    embed.set_footer(text="하단 설명")
    await channel.send(embed=embed)
