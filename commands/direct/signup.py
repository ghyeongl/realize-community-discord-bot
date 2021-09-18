"""
./commands/direct/signup.py
회원가입 전용(DB에 등록되지 않은 사용자 대상) 회원가입 로직
유저 데이터는 ./commands/devops/management 에 저장
"""
import log
from commands.devops.management import confirm_pending, member_info
from commands.devops.management import new_request


# DB에 등록되지 않은 사용자를 대상으로 한 fork
async def fork(channel, message, client):
    log.call(__name__, fork.__name__)
    author_id = message.author.id

    # 유저가 저장한 정보를 모두 날림
    if message.content.startswith('초기화'):
        await reset(channel, message, author_id)

    # 새 멤버 캐시에 등록되지 않은 사용자의 경우
    elif author_id not in member_info:
        await meet(channel, message, author_id)

    # 첫 번째 입력
    elif member_info[author_id]["동의여부"] == "":
        await person_agree(channel, message, author_id)

    # 두 번째 입력
    elif member_info[author_id]["이름"] == "":
        await person_name(channel, message, author_id)

    # 세 번째 입력
    elif member_info[author_id]["기수"] == "":
        await person_number(channel, message, author_id)

    # 네 번째 입력
    elif member_info[author_id]["리얼라이즈"] == "":
        await person_realize(channel, message, author_id)

    # 작성 완료 목록에 포함되지 않은 경우
    elif author_id not in confirm_pending:
        await person_confirm(channel, message, author_id, client)

    # 그 외 (새 멤버 캐시와, 작성 완료 목록에 모두 있는 사용자)
    else:
        await confirmation(channel, message, author_id)


# confirm_pending 상태 구문 추가하기
async def reset(channel, message, author_id):
    try:
        del member_info[author_id]
        await channel.send("초기화 되었습니다. 언제든 제게 메시지를 보내 다시 진행할 수 있어요!")
    except KeyError:
        await channel.send("정보가 이미 지워져 있어요. 다시 가입하고 싶으면 아무 메시지나 보내주세요!")


# 새 사용자
async def meet(channel, message, author_id):
    member_info[author_id] = {"이름": "", "기수": "", "리얼라이즈": "", "동의여부": ""}
    await channel.send("안녕하세요! 저는 리얼라이즈 커뮤니티의 봇 '캡챠' 라고 해요!\n"
                       "이제부터 등록 절차를 진행할거예요! 등록시 개인정보 처리방침에 동의하는 것으로 간주됩니다.\n"
                       "(개인정보 처리방침은 서버 내 공지-및-문화에서 확인할 수 있어요!)\n"
                       "진행하시겠습니까? (예/아니오)  (문제가 생기면 '초기화' 를 입력하세요.)")


# 새 사용자로 등록된 유저
async def person_agree(channel, message, author_id):
    if message.content.startswith('예'):
        member_info[author_id]["동의여부"] = True
        await channel.send('진행을 시작합니다.')
        await channel.send('이름을 입력해주세요! (실명을 입력하지 않을 경우, 등록 요청이 기각될 수 있어요.)')
    elif message.content.startswith('아니'):
        del member_info[author_id]
        await channel.send('등록을 취소합니다. 언제든 제게 메시지를 보내 다시 진행할 수 있어요!')
    else:
        await channel.send('제대로 입력해주세요!')


# 새 사용자 등록 및 개인정보 동의를 한 유저 대상 이름 묻기
async def person_name(channel, message, author_id):
    member_info[author_id]["이름"] = message.content
    await channel.send(f"{message.content}님! 만나서 반가워요. (아닐 시 '초기화' 입력)")
    await channel.send("몇 기인가요? (이 커뮤니티는 세종과고생만 가입할 수 있어요!)")


# 개인정보 동의, 이름 등록을 마친 유저 대상 기수 묻기
async def person_number(channel, message, author_id):
    if message.content.isdigit():
        member_info[author_id]["기수"] = message.content
        await channel.send(f"{member_info[author_id]['기수']}기로 입력되었어요. (아닐 시 '초기화' 입력)")
        await channel.send('리얼라이즈 동아리에 소속되어있나요? (예/아니오)')

    elif message.content.split('기')[0].isdigit():
        member_info[author_id]["기수"] = message.content.split('기')[0]
        await channel.send(f"{member_info[author_id]['기수']}기로 입력되었어요. (아닐 시 '초기화' 입력)")
        await channel.send('리얼라이즈 동아리에 소속되어있나요? (예/아니오)')

    else:
        await channel.send("제대로 입력해주세요!")


# 리얼라이즈 회원인지
async def person_realize(channel, message, author_id):
    if message.content.startswith('예'):
        member_info[author_id]["리얼라이즈"] = True
        value = str(member_info[author_id]).replace("'", "")
        await channel.send(f'입력된 값이예요: {value[1:-1]}. 등록 요청을 전송할까요? (예/아니오)')

    elif message.content.startswith('아니'):
        member_info[author_id]["리얼라이즈"] = False
        value = str(member_info[author_id]).replace("'", "")
        await channel.send(f"입력된 값이예요: {value[1:-1]}. 등록 요청을 전송할까요? (예/아니오)")

    else:
        await channel.send("제대로 입력해주세요!")


# 전송여부 판단
async def person_confirm(channel, message, author_id, client):
    if message.content.startswith('예'):
        confirm_pending.append(author_id)
        await new_request(message, author_id, client)
        await channel.send('전송되었어요. 커뮤니티에서 만나요!')

    elif message.content.startswith('아니'):
        del member_info[author_id]
        await channel.send('초기화 되었어요. 아무거나 입력하면 다시 진행합니다.')

    else:
        await channel.send('제대로 입력해주세요!')


# 승인 대기시
async def confirmation(channel, message, author_id):
    await channel.send('승인을 기다리고 있어요. 잠시만 기다려주세요! \n초기화를 통해 승인 요청 목록에서 제거할 수 있어요.')
