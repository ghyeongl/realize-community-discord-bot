import database
import time


cache = []


def call(module_name, func_name, **info):
    global cache
    content = f"[{module_name}][{func_name}] {info} | {time.strftime('%x %X', time.localtime())}"
    print(content)
    cache.append(content)


def division_line():
    global cache
    content = '-' * 30
    print(content)
    cache.append(content)


def error(content, **info):
    pass
