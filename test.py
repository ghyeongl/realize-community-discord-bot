import sqlite3
conn = sqlite3.connect('my_database.sqlite')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE SCHOOL
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         AGE            INT     NOT NULL,
         ADDRESS        CHAR(50),
         MARKS          INT);''')
print("Opened database successfully")