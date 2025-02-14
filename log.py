"""
./log.py
로그 기록 및 전송 시스템
"""
import csv
import os
import time
import datetime
import asyncio
import threading
import schedule


# 글로벌 변수 초기화
cache = []
remain = []
cur_path = ''


# (기능) 어제 로그를 추가
def _prev_path(folder):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    prev = f"{folder}/{yesterday.strftime('%y%m%d')}.txt"
    if os.path.exists(prev):
        remain.append(prev)


# (기능) 파일 이름 정하기
def log_path():
    date = time.strftime('%y%m%d', time.localtime())
    folder = "./data/log"
    path = f"{folder}/{date}.txt"
    if not os.path.exists(path):
        fp = open(path, "w")
        content = f"[log][log_path] New log | path: {path}" \
                  f" | {time.strftime('%x %X', time.localtime())}"
        fp.write(content + "\n")
        print(content)
        fp.close()
        _prev_path(folder)
    return path


# (기능) 로그 경로 바꾸기
def log_path_change():
    global cur_path
    cur_path = log_path()


# (기능) 로그 파일에 내용 추가
def append_log(path, content):
    fp = open(path, "a")
    fp.write(content + "\n")
    fp.close()


# 스케줄러 스레드
class Schedule(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.stat = True

    def run(self):
        call(__name__, Schedule.run.__name__)
        asyncio.run(self.scheduler())

    def stop(self):
        call(__name__, Schedule.stop.__name__)
        self.stat = False

    async def scheduler(self):
        m = 60 - time.time() % 60
        await asyncio.sleep(m)
        call(__name__, Schedule.scheduler.__name__, precision=round(time.time() % 1, 5))
        while self.stat:
            schedule.run_pending()
            await asyncio.sleep(60)


# 처음 실행할 때
def first_call():
    content = "="*30 + "\n" + f"[log][first_call] {time.strftime('%x %X', time.localtime())}"
    print(content)
    append_log(cur_path, content)


# 로깅
def call(module_name, func_name, **info):
    content = f"[{module_name}][{func_name}] {str(info)[1:-1]} | {time.strftime('%x %X', time.localtime())}"
    content = content.replace("'", "")
    print(content)
    append_log(cur_path, content)


# 결과 로깅
def result(module_name, func_name, **info):
    content = f"[result][{module_name}][{func_name}] {str(info)[1:-1]} | {time.strftime('%x %X', time.localtime())}"
    content = content.replace("'", "")
    print(content)
    append_log(cur_path, content)


# 구분선
def division_line():
    content = '-' * 30
    print(content)
    append_log(cur_path, content)


# 에러
def error(content, module_name, func_name, **info):
    global cache
    content = f"[error][{content}][{module_name}][{func_name}] {str(info)[1:-1]}" \
              f" | {time.strftime('%x %X', time.localtime())}"
    content = content.replace("'", "")
    append_log(cur_path, content)
    print("\033[31m" + content + "\033[0m")
    cache.append(content)


# 채팅 기록
def chats(channel_id, author_id, contents):
    ti = time.strftime("%y%m%d", time.localtime())
    dire = "./data/chats"
    path = f"{dire}/{ti}.csv"
    f = open(path, "a", encoding='utf-8', newline='')
    wr = csv.writer(f)
    cur_time = time.strftime("%H%M%S", time.localtime())
    wr.writerow([channel_id, author_id, cur_time, contents.replace('\n', "/n")])
    f.close()


# 처음 실행시
log_path_change()
first_call()
schedule.every().day.at("00:00").do(log_path_change)
t = Schedule("log thread")
t.start()
