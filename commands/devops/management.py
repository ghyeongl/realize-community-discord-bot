"""
./commands/devops/management.py
커뮤니티 운영을 위한 다양한 커맨드 제공
새 유저 DB 추가 등
"""
import discord
from discord import errors, File
import sys
import database
import log

confirm_pending = []
member_info = {}
security_status = 1
keys = ['Samplekey']
names = {}


# 새 등록 요청이 왔을 때 알림
async def new_request(author, client):
    confirm_pending.append(author.id)
    channel = client.get_channel(database.get_id_channel(7, 4))
    author_name = author.name + "#" + author.discriminator
    details = member_info[author.id]
    await channel.send(f"[New Request] Name: {author_name} | Details: {details} | ID: {author.id}")
    await channel.send(f"[Confirm_pending List] {confirm_pending}")


# management 채널 커맨드에 대해 fork
async def fork(channel, message, client):
    # 명령어 !도움
    if message.content.startswith("!도움"):
        await help_request(channel, message)

    # 대기자 모두 가입
    elif message.content.startswith("!가입 모두"):
        await request_accept_all(channel, message, client)

    # 대기자 가입 제외
    elif message.content.startswith("!가입 제외"):
        await request_reject(channel, message, client)

    # 특정 대기자 가입
    elif message.content.startswith("!가입 일부"):
        await request_accept(channel, message, client)

    # 가입 조회
    elif message.content.startswith("!가입 조회"):
        await request_list(channel)

    # 인증키 추가
    elif message.content.startswith("!인증키 추가"):
        await key_add(channel, message)

    # 인증키 제거
    elif message.content.startswith("!인증키 제거"):
        await key_del(channel, message)

    # 인증키 조회
    elif message.content.startswith("!인증키 조회"):
        await key_get(channel, message)

    # 보안 레벨 설정
    elif message.content.startswith("!보안 레벨"):
        await security_modify(channel, message)

    # 보안 조회
    elif message.content.startswith("!보안 조회"):
        await security_check(channel)

    # 대나무숲 유저 차단
    elif message.content.startswith("!대나무숲 차단"):
        await bamboo_restrict(channel, message)

    # 로그 파일 보내기
    elif message.content.startswith("!로그 전송"):
        await log_send(channel, message)

    # 봇 재시작
    elif message.content.startswith("!봇 재시작"):
        await bot_restart(channel, message)

    # 봇 종료
    elif message.content.startswith("!봇 종료"):
        await bot_shutdown(channel, message, client)


# 초기화
async def _reset(channel, author_id):
    log.call(__name__, _reset.__name__, author_id=author_id, channel_id=channel.id)
    try:
        del member_info[author_id]
        if author_id in confirm_pending:
            confirm_pending.remove(author_id)
        await channel.send("초기화 되었습니다. 언제든 제게 메시지를 보내 다시 진행할 수 있어요!")
    except KeyError:
        await channel.send("정보가 이미 지워져 있어요. 다시 가입하고 싶으면 아무 메시지나 보내주세요!")


# 수락
async def accept(author_id, client):
    guild = client.get_guild(database.get_id_server())
    member = guild.get_member(author_id)
    author = client.get_user(author_id)
    reg_info = member_info[author_id]

    try:
        if member is not None:
            database.add_member(member.id, member.name, member.discriminator, reg_info)
            await member.add_roles(guild.get_role(database.get_id_roles("Makers")),
                                   reason="캡챠가 부여함")
            await member.edit(nick=reg_info["Name"])
            await member.dm_channel.send('등록이 완료되었어요. 커뮤니티를 확인해보세요!')
            del member_info[member.id]
            return True
        elif author is not None:
            log.error("member is None", __name__, accept.__name__, member=member)
            await author.dm_channel.send('앗! 서버에 존재하지 않는 유저예요. 이 증상이 지속되면, 관리자에게 연락하세요.')
            await _reset(author.dm_channel, author.id)
            return False
        else:
            log.error("Unexpected", __name__, accept.__name__)
            return False

    except errors.Forbidden:
        log.error("discord.errors.Forbidden", __name__, accept.__name__)
        await author.dm_channel.send('알 수 없는 에러가 발생했어요. 그러면 당신은 혹시 신적인 존재..?')
        database.del_member(author.id)
        await _reset(author.dm_channel, author.id)
        return False


# 메시지 내 유저 네임태그를 member_info 에서 찾아 author 를 반환
def _find(message, client):
    user = message.content.split()[2]
    print(user)
    for i in confirm_pending:
        print(i)
        if user == member_info[i]['Tag']:
            author = i
            return author
    return None


# 명령어 !도움 에 대한 함수
async def help_request(channel, message):
    embed = discord.Embed(title="관리페이지 명령어 목록", description="명령어와 {값} 간 띄어쓰기 필수", color=0x612371)
    embed.add_field(name="가입 관리", value="!가입 모두, !가입 제외 {아이디}, !가입 일부 {아이디}, !가입 조회", inline=False)
    embed.add_field(name="인증키 관리", value="!인증키 추가 {인증키}, !인증키 제거 {인증키}, !인증키 조회", inline=False)
    embed.add_field(name="보안 관리", value="!보안 레벨 {숫자}, !보안 조회", inline=False)
    embed.add_field(name="시스템 관리", value="!로그 전송, !봇 종료", inline=False)
    embed.set_footer(text="세종과고 리얼라이즈에서 ♡을 담아 만듭니다.")
    await channel.send(embed=embed)


# 명령어 !가입 모두 에 대한 함수
async def request_accept_all(channel, message, client):
    success = True
    for author_id in confirm_pending:
        success &= await accept(author_id, client)
    if success:
        await channel.send('등록이 모두 완료되었습니다.')
    else:
        await channel.send('일부 등록에 실패하였습니다.')


# !가입 제외 {아이디}
async def request_reject(channel, message, client):
    user_id = _find(message, client)
    user = client.get_guild(database.get_id_server()).get_member(user_id)
    await user.dm_channel.send('가입 요청이 거부되었어요.')
    await _reset(user.dm_channel, user_id)
    await channel.send('요청 거부에 성공하였습니다.')


# !가입 일부 {아이디}
async def request_accept(channel, message, client):
    user_id = _find(message, client)
    success = await accept(client, user_id)
    if success:
        await channel.send('등록에 성공하였습니다.')
    else:
        await channel.send('등록에 실패하였습니다.')


# !가입 조회
async def request_list(channel):
    for i in confirm_pending:
        await channel.send(member_info[i])
    await channel.send("[confirm_pending]" + str(confirm_pending))


# !인증키 추가
async def key_add(channel, message):
    new_key = message.content.split()[2]
    keys.append(new_key)
    await channel.send('키 추가가 완료되었습니다: ' + str(keys))


# !인증키 제거
async def key_del(channel, message):
    key = message.content.split()[2]
    keys.remove(key)
    await channel.send('키 제거가 완료되었습니다: ' + str(keys))


# !인증키 조회
async def key_get(channel, message):
    await channel.send('현재 키 목록: ' + str(keys))


# !보안 레벨
async def security_modify(channel, message):
    global security_status
    level = int(message.content.split()[2])
    security_status = level
    await security_check(channel)


# !보안 조회
async def security_check(channel):
    global security_status
    await channel.send('현재 보안 레벨은 ' + str(security_status) + ' 입니다.')


# !대나무숲 차단
async def bamboo_restrict(channel, message):
    pass


# !로그 전송
async def log_send(channel, message):
    path = log.log_path()
    await channel.send(file=File(path))


# !봇 재시작
async def bot_restart(channel, message):
    pass


# !봇 종료
async def bot_shutdown(channel, message, client):
    await channel.send('봇을 종료합니다.')
    log.t.stop()
    client.loop.stop()
    if client.loop.is_closed():
        exit()
