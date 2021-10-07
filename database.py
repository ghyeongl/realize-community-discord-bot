"""
./database.py
json 이나 DB 에서 값을 불러와 리턴하는 함수의 집합
입력이나 수정 삭제도 수행
./data/. 에 각종 파일 저장
"""
import json
import sqlite3

import log


# server_info.json 에서 데이터 끌어오기, 서버 내 채널의 id 조회에 사용
import time


def get_id_dict():
    with open("data/server_info.json", "r") as server_info:
        value = dict(json.load(server_info))
    return value


# members.json 에서 데이터 끌어오기, 멤버의 id 조회에 사용
def get_members_dict():
    with open("data/members.json", "r") as members:
        value = dict(json.load(members))
    return value


data = get_id_dict()
# info = get_members_dict()


# 채널 이름 조회
def get_name_channel(category_num, channel_num):
    global data
    value = data["name"]["channel"][str(category_num)][str(channel_num)]
    return value


# 카테고리 이름 조회
def get_name_category(category_num):
    global data
    value = data["name"]["category"][str(category_num)]
    return value


# 카테고리 ID 조회
def get_id_category(category_num):
    global data
    value = int(data["id"][str(category_num)]["category_id"])
    return value


# 채널 ID 조회
def get_id_channel(category_num, channel_num):
    global data
    value = int(data["id"][str(category_num)][str(channel_num)])
    return value


# 서버 ID 조회
def get_id_server():
    global data
    value = int(data["server"]["id"])
    return value


# 역할 ID 조회
def get_id_roles(roles_name):
    global data
    value = data["roles"][roles_name]
    return value


# Author instance 반환
def get_instance_author(author_id, client):
    pass


# Channel instance 반환
def get_instance_channel(category_num, channel_num, client):
    pass


# Author 받아 Name + Discriminator 반환
def get_disc_author(author):
    value = str(author.name + "#" + author.discriminator)
    return value


# sqlite3 for author CRUD


def db_initialize():
    pass


# 유저 이름 가져오기
def get_name_author(author_id):
    pass


# 유저 회원가입 컨펌
def add_member(author_id, name, disc, reg_info):
    log.call(__name__, add_member.__name__, author_id=author_id, name=name, disc=disc, info=reg_info)
    con = sqlite3.connect('data/members.db')
    cur = con.cursor()
    try:
        cur.execute("""
        INSERT INTO user_info (id, name, discriminator, real_name, number, auth_key, privacy_policy, signup_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (int(author_id), str(name), int(disc), str(reg_info['Name']), int(reg_info['Number']),
                     str(reg_info['Key']), int(reg_info['Confirm']),
                     str(time.strftime('%y%m%d-%H%M%S', time.localtime()))))
        con.commit()
    except sqlite3.OperationalError as e:
        log.error("sqlite3.OperationalError", __name__, add_member.__name__, content=e)
    con.close()


# 유저 조회
def get_member(author_id):

    pass


# 유저 존재 여부 조회
def in_member(author_id):
    log.call(__name__, in_member.__name__, author_id=author_id)
    con = sqlite3.connect('data/members.db')
    cur = con.cursor()
    cur.execute("SELECT id FROM user_info")
    rows = cur.fetchall()
    con.close()
    for row in rows:
        if author_id in row:
            return True
    return False


# 유저 삭제
def del_member(author_id):
    log.call(__name__, del_member.__name__, author_id=author_id)
    con = sqlite3.connect('data/members.db')
    cur = con.cursor()
    cur.execute(f"DELETE FROM user_info WHERE id = {author_id}")
    con.commit()
    con.close()
