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
def get_id_dict():
    log.call(__name__, get_id_dict.__name__)
    with open("data/server_info.json", "r") as server_info:
        value = dict(json.load(server_info))
    return value


# members.json 에서 데이터 끌어오기, 멤버의 id 조회에 사용
def get_members_dict():
    log.call(__name__, get_members_dict.__name__)
    with open("data/members.json", "r") as members:
        value = dict(json.load(members))
    return value


data = get_id_dict()
# info = get_members_dict()


# 채널 이름 조회
def get_name_channel(category_num, channel_num):
    log.call(__name__, get_name_channel.__name__, input=(category_num, channel_num))
    global data
    value = data["name"]["channel"][str(category_num)][str(channel_num)]
    return value


# 카테고리 이름 조회
def get_name_category(category_num):
    log.call(__name__, get_name_category.__name__, input=category_num)
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


# Author instance 반환
def get_instance_author(author_id, client):
    log.call(__name__, get_instance_author.__name__)
    pass


# Channel instance 반환
def get_instance_channel(category_num, channel_num, client):
    log.call(__name__, get_instance_channel.__name__)
    pass


# sqlite3 for author CRUD
con = sqlite3.connect('data/author.db')
cur = con.cursor()


def db_initialize():
    pass


# 유저 이름 가져오기
def get_name_author(author_id):
    log.call(__name__, get_name_author.__name__)
    pass


# DB에 정보 추가
def add_author(author_id, author_info):
    log.call(__name__, add_author.__name__)
    pass


# DB 정보 업데이트
def update_author_info(author_id, type_of_update, contents):
    log.call(__name__, update_author_info.__name__)
    pass


# 유저가 DB에 등록되어 있는지 조회
def find_author_id(author_id):
    log.call(__name__, find_author_id.__name__)
    return False


# 유저 삭제
def del_author(author_id):
    log.call(__name__, del_author.__name__)
    pass
