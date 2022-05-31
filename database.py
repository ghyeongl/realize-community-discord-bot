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


def get_tk_dict():
    with open("data/token.json", "r") as token:
        value = dict(json.load(token))
    return value


data = get_id_dict()
token = get_tk_dict()


# 채널 이름 조회
def get_name_channel(category_num, channel_num):
    value = data["name"]["channel"][str(category_num)][str(channel_num)]
    return value


# 카테고리 이름 조회
def get_name_category(category_num):
    value = data["name"]["category"][str(category_num)]
    return value


# 카테고리 ID 조회
def get_id_category(category_num):
    value = int(data["id"][str(category_num)]["category_id"])
    return value


# 채널 ID 조회
def get_id_channel(category_num, channel_num):
    value = int(data["id"][str(category_num)][str(channel_num)])
    return value


# 서버 ID 조회
def get_id_server():
    value = int(data["server"]["id"])
    return value


# 봇 토큰 조회
def get_token_bot():
    value = str(token["token"])
    return value


# 역할 ID 조회
def get_id_roles(roles_name):
    value = data["roles"][roles_name]
    return value


# Author 받아 Name + Discriminator 반환
def get_disc_author(author):
    value = str(author.name + "#" + author.discriminator)
    return value


# 유저 회원가입 컨펌
def add_member(user_id, name, disc, reg_info):
    log.call(__name__, add_member.__name__, user_id=user_id, name=name, disc=disc, info=reg_info)
    con = sqlite3.connect('data/members.db')
    cur = con.cursor()
    try:
        cur.execute("""
        INSERT INTO user_info (id, name, discriminator, real_name, number, auth_key, privacy_policy, signup_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (int(user_id), str(name), int(disc), str(reg_info['Name']), int(reg_info['Number']),
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
def in_member(user_id):
    log.call(__name__, in_member.__name__, user_id=user_id)
    con = sqlite3.connect('data/members.db')
    cur = con.cursor()
    cur.execute("SELECT id FROM user_info")
    rows = cur.fetchall()
    con.close()
    for row in rows:
        if user_id in row:
            return True
    return False


# 유저 삭제
def del_member(user_id):
    log.call(__name__, del_member.__name__, user_id=user_id)
    con = sqlite3.connect('data/members.db')
    cur = con.cursor()
    cur.execute(f"DELETE FROM user_info WHERE id = {user_id}")
    con.commit()
    con.close()
