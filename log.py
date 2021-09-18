"""
./log.py
로그 기록 및 전송 시스템
"""

import os
import time
import database


# 파일 열기
def find_log_file():
    i = 0
    while True:
        path = f"./data/log/log_{i}.txt"
        if os.path.exists(path):
            i += 1
        else:
            return i


cache = []
num = find_log_file()
f = f"./data/log/log_{num}.txt"


def append_log(path, content):
    fp = open(path, "a")
    fp.write(content + "\n")
    fp.close()


# 로깅
def call(module_name, func_name, **info):
    global cache

    content = f"[{module_name}][{func_name}] {str(info)[1:-1]} | {time.strftime('%x %X', time.localtime())}"
    content = content.replace("'", "")
    print(content)
    append_log(f, content)
    cache.append(content)


# 구분선
def division_line():
    global cache
    content = '-' * 30
    print(content)
    append_log(f, content)
    cache.append(content)


# 에러
def error(content, **info):
    global cache

    content = f"[{content}] {str(info)[1:-1]} | {time.strftime('%x %X', time.localtime())}"
    content = content.replace("'", "")
    append_log(f, content)
    print("\033[31m" + content + "\033[0m")
