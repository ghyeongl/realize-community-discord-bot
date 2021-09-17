"""
./log.py
로그 기록 및 전송 시스템
"""

import database
import time


cache = []


# 로깅
def call(module_name, func_name, **info):
    global cache

    content = f"[{module_name}][{func_name}] {str(info)[1:-1]} | {time.strftime('%x %X', time.localtime())}"
    content = content.replace("'", "")
    print(content)
    cache.append(content)


# 구분선
def division_line():
    global cache
    content = '-' * 30
    print(content)
    cache.append(content)


# 에러
def error(content, **info):
    pass
