import sqlite3
import os
import time

class MyDatabase():
    def __init__(self, dbname: str) -> None:
        abs = os.path.abspath(__file__)
        ROOT = os.path.dirname(abs) + "/"
        self.dbname = dbname
        self.connect = sqlite3.connect(ROOT + dbname)

    def get_cursor(self) -> sqlite3.Cursor:
        return self.connect.cursor()
    
    # def get_max_uid(self) -> int:
    #     c = self.get_cursor()
    #     c.execute("select max(uid) from user;")
    #     return c.fetchone()
    
    # def get_uids(self) -> list:
    #     c = self.get_cursor()
    #     c.execute("select uid from user;")
    #     return [i[0] for i in c.fetchall()]
    
    # def get_data_for_csv(self, date=False) -> list:
    #     c = self.get_cursor()
    #     if date:
    #         c.execute("select uid, name, date from user order by uid;")
    #     else:
    #         c.execute("select uid, name from user order by uid;")
    #     return c.fetchall()
    
    def get_data(self, sql) -> list:
        c = self.get_cursor()
        c.execute(sql)
        return c.fetchall()
    
    def write_data(self, sql, data) -> list:
        c = self.get_cursor()
        c.execute(sql, data)
        return

    # def insert_data(self, uid: int, name: str, autoDate:bool = True, date:str = 0) -> None:
    #     c = self.get_cursor()
    #     if autoDate:
    #         c.execute(f"insert into user(uid, name, date) values(?, ?, {int(time.time())})", (uid, name))
    #     else:
    #         c.execute(f"insert into user(uid, name, date) values(?, ?, \"{date}\")", (uid, name))
    #     print(f"@{self.dbname} active: insert user {type(uid)}{uid} {type(name)}{name}")
    
    # def delete_data(self) -> None:
    #     c1 = self.get_cursor()
    #     c1.execute("delete from sqlite_sequence where name='user';")
    #     c2 = self.get_cursor()
    #     c2.execute("delete from user;")
    #     print(f"@{self.dbname} active: delete data")

    def close(self) -> None:
        self.connect.commit()
        self.connect.close()
