"""
./commands/devops/management.py
커뮤니티 운영을 위한 다양한 커맨드 제공
새 유저 DB 추가 등
"""
import database

confirm_pending = []
member_info = {}
security_status = 1
keys = ['Samplekey']
names = {}


# 새 등록 요청이 왔을 때 알림
async def new_request(message, author_id, client):
    channel = client.get_channel(database.get_id_channel(7, 4))
    author_name = message.author.name + "#" + message.author.discriminator
    details = member_info[author_id]
    await channel.send(f"[New Request] Name: {author_name} | Details: {details} | ID: {author_id}")
    await channel.send(f"[Confirm_pending List] {confirm_pending}")


# management 채널 커맨드에 대해 fork
async def fork(channel, message):
    # 명령어 !도움
    if message.content.startswith("!도움"):
        await help_request(channel, message)

    # 명령어 !모두
    elif message.content.startswith("!모두"):
        await accept_all(channel, message)


# 명령어 !도움 에 대한 함수
async def help_request(channel, message):
    pass


# 명령어 !모두 에 대한 함수
async def accept_all(channel, message):
    for i in confirm_pending:
        database.add_author(i, member_info[i])
