"""
./commands/direct/signup.py
회원가입 전용(DB에 등록되지 않은 사용자 대상) 회원가입 로직
유저 데이터는 ./commands/devops/management 에 저장
"""
import discord.errors

import log
import database
from commands.devops.management import confirm_pending, member_info
from commands.devops.management import new_request, accept
from commands.devops.management import keys, names


# DB에 등록되지 않은 사용자를 대상으로 한 fork
async def fork(channel, author, message, client):
    log.call(__name__, fork.__name__, author_id=author.id, channel_id=channel.id)

    # 유저가 저장한 정보를 모두 날림
    if message.content.startswith('초기화'):
        await reset(channel, author.id)

    # 새 멤버 캐시에 등록되지 않은 사용자의 경우
    elif author.id not in member_info:
        await meet(channel, author.id)

    # 첫 번째 입력
    elif member_info[author.id]["Confirm"] == "":
        await person_agree(channel, author, message)

    # 두 번째 입력
    elif member_info[author.id]["Name"] == "":
        await person_name(channel, author, message)

    # 세 번째 입력
    elif member_info[author.id]["Number"] == "":
        await person_number(channel, author, message)

    # 네 번째 입력
    elif member_info[author.id]["Key"] == "":
        await person_key(channel, author, message)

    # 작성 완료 목록에 포함되지 않은 경우
    elif author.id not in confirm_pending:
        await person_confirm(channel, author, message, client)

    # 그 외 (새 멤버 캐시와, 작성 완료 목록에 모두 있는 사용자)
    else:
        await confirmation(channel, author)


# confirm_pending 상태 구문 추가하기
async def reset(channel, author_id):
    log.call(__name__, reset.__name__, author_id=author_id, channel_id=channel.id)
    try:
        del member_info[author_id]
        if author_id in confirm_pending:
            confirm_pending.remove(author_id)
        await channel.send("초기화 되었습니다. 언제든 제게 메시지를 보내 다시 진행할 수 있어요!")
    except KeyError:
        await channel.send("정보가 이미 지워져 있어요. 다시 가입하고 싶으면 아무 메시지나 보내주세요!")


# 새 사용자
async def meet(channel, author_id):
    log.call(__name__, meet.__name__, author_id=author_id, channel_id=channel.id)
    member_info[author_id] = {"Confirm": "", "Name": "", "Number": "", "Key": "", "Tag": ""}
    await channel.send("안녕하세요! 저는 리얼라이즈 커뮤니티의 봇 '캡챠' 라고 해요!\n"
                       "이제부터 등록 절차를 진행할거예요! 등록시 개인정보 처리방침에 동의하는 것으로 간주됩니다.\n"
                       "(개인정보 처리방침은 서버 내 공지-및-문화에서 확인할 수 있어요!)\n"
                       "진행하시겠습니까? (예/아니오)  (문제가 생기면 '초기화' 를 입력하세요.)")


# 새 사용자로 등록된 유저
async def person_agree(channel, author, message):
    log.call(__name__, person_agree.__name__, author_id=author.id, channel_id=channel.id)
    if message.content.startswith('예'):
        member_info[author.id]["Confirm"] = True
        member_info[author.id]["Tag"] = author.name + '#' + author.discriminator
        await channel.send('진행을 시작합니다.')
        await channel.send('이름을 입력해주세요! (실명을 입력하지 않을 경우, 등록 요청이 기각될 수 있어요.)')
    elif message.content.startswith('아니'):
        del member_info[author.id]
        await channel.send('등록을 취소합니다. 언제든 제게 메시지를 보내 다시 진행할 수 있어요!')
    else:
        await channel.send('제대로 입력해주세요!')


# 새 사용자 등록 및 개인정보 동의를 한 유저 대상 이름 묻기
async def person_name(channel, author, message):
    log.call(__name__, person_name.__name__, author_id=author.id, channel_id=channel.id)
    if len(message.content) <= 6:
        member_info[author.id]["Name"] = message.content
        await channel.send(f"{message.content}님! 만나서 반가워요. (아닐 시 '초기화' 입력)")
        await channel.send("몇 기인가요? (이 커뮤니티는 세종과고생만 가입할 수 있어요!)")

    else:
        await channel.send(f"앗! 이름은 6자를 넘을 수 없어요.")
        await reset(channel, author.id)


# 개인정보 동의, 이름 등록을 마친 유저 대상 기수 묻기
async def person_number(channel, author, message):
    log.call(__name__, person_number.__name__, author_id=author.id, channel_id=channel.id)
    if message.content.isdigit():
        member_info[author.id]["Number"] = int(message.content)
        await channel.send(f"{member_info[author.id]['Number']}기로 입력되었어요. (아닐 시 '초기화' 입력)")
        await channel.send('제공받은 인증키를 입력해주세요! (없다면 "없음" 입력)')

    elif message.content.split('기')[0].isdigit():
        member_info[author.id]["Number"] = int(message.content.split('기')[0])
        await channel.send(f"{member_info[author.id]['Number']}기로 입력되었어요. (아닐 시 '초기화' 입력)")
        await channel.send('제공받은 인증키를 입력해주세요! (없다면 "없음" 입력)')

    else:
        await channel.send("제대로 입력해주세요!")


# 인증키를 작성했는지
async def person_key(channel, author, message):
    log.call(__name__, person_key.__name__, author_id=author.id, channel_id=channel.id)
    if message.content.startswith('없음'):
        member_info[author.id]["Key"] = False
    elif len(message.content) <= 20:
        member_info[author.id]["Key"] = message.content
    else:
        await channel.send("앗! 인증키는 20자를 넘을 수 없어요.")
        await reset(channel, author.id)

    value = f"동의여부: {member_info[author.id]['Confirm']}, 이름: {member_info[author.id]['Name']}, " \
            f"기수: {member_info[author.id]['Number']}, 인증키: {member_info[author.id]['Key']}"
    await channel.send(f'입력된 값이예요: {value}. 등록 요청을 전송할까요? (예/아니오)')


# 전송여부 판단
async def person_confirm(channel, author, message, client):
    log.call(__name__, person_confirm.__name__, author_id=author.id, channel_id=channel.id)
    if message.content.startswith('예'):
        if member_info[author.id]['Key']:
            await reg_confirm(channel, author, client, member_info[author.id])
        else:
            await new_request(author, client)
            await channel.send('대기명단에 추가되었어요. 조금만 기다리면 결과를 알려드릴게요!')

    elif message.content.startswith('아니'):
        await reset(channel, author.id)

    else:
        await channel.send('제대로 입력해주세요!')


# 인증키 일치 여부 확인
async def reg_confirm(channel, author, client, reg_info):
    log.call(__name__, reg_confirm.__name__, author_id=author.id, channel_id=channel.id)
    from commands.devops.management import security_status
    if security_status == 0:
        if reg_info['Number'] >= 15:
            await channel.send('신입생이시군요! 세종과고에 오신걸 환영해요. 입학 축하해요!')
            await reg_confirmed(channel, author, client)
        elif reg_info['Key'] in keys:
            await reg_confirmed(channel, author, client)
        else:
            await reg_rejected(channel, author)

    elif security_status == 1:
        if reg_info['Number'] >= 15:
            await reg_rejected(channel, author)
        elif reg_info['Key'] in keys:
            await reg_confirmed(channel, author, client)
        else:
            await reg_rejected(channel, author)

    elif security_status == 2:
        if reg_info['Number'] >= 15:
            await reg_rejected(channel, author)
        elif reg_info['Key'] in keys:
            if reg_info['Number'] is names[reg_info['Name']]:
                await reg_confirmed(channel, author, client)
            else:
                await reg_rejected(channel, author)
        else:
            await reg_rejected(channel, author)

    elif security_status == 3:
        await channel.send('현재 자동 회원가입이 잠시 중단된 상태예요.'
                           '대기명단에 넣었으니 조금 기다려주세요.')
        await new_request(author, client)


# 승인시 권한 해제 절차
async def reg_confirmed(channel, author, client):
    log.call(__name__, reg_confirmed.__name__, author_id=author.id, channel_id=channel.id)
    await accept(author.id, client)


# 승인 거부시 초기화
async def reg_rejected(channel, author):
    log.call(__name__, reg_rejected.__name__, author_id=author.id, channel_id=channel.id)
    await channel.send('앗! 세종과고생이 아니신가요? 아쉽게도, 잘못 찾아오셨어요.')
    await reset(channel, author.id)


# 승인 대기시
async def confirmation(channel, author):
    log.call(__name__, confirmation.__name__, author_id=author.id, channel_id=channel.id)
    await channel.send('승인을 기다리고 있어요. 잠시만 기다려주세요! \n초기화를 통해 승인 요청 목록에서 제거할 수 있어요.')
