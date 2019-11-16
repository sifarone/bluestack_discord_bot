import os
import sqlite3

import config

class DatabaseHandlerSQLite():
    def __init__(self):
        try:
            self.conn = sqlite3.connect(config.DB_NAME)
            self.cur = self.conn.cursor()

            #Create Table if not already created
            self.cur.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='usersearchhistory' ''')
            if self.cur.fetchone()[0] == 1:
                print('Table already exists.')
            else:
                print('Creating <usersearchhistory> table.')
                self.cur.execute("""CREATE TABLE usersearchhistory (
                    username text NOT NULL,
                    searchterm text NOT NULL
                )""")
                self.conn.commit()
        except Exception as e:
            print('Database Connection Error : ', e)        

    def storeUserSearchHistory(self, userName, searchTerm):
        dbSearchString = "SELECT * FROM '%s' WHERE username='%s' AND searchterm='%s'" % (config.USER_HISTORY_TABLE_NAME, userName, searchTerm)
        try:
            self.cur.execute(dbSearchString)
            if len(self.cur.fetchall()):
                print('Data already exists in Database')
            else:
                dbInsertString = "INSERT INTO '%s' VALUES ('%s', '%s')" % (config.USER_HISTORY_TABLE_NAME, userName, searchTerm)
                self.cur.execute(dbInsertString)
            self.conn.commit()
        except Exception as e:
            print('Database Insert Error : ', e)

    def getUserSearchHistory(self, userName):
        result = []
        dbSearchString = "SELECT * FROM '%s' WHERE username='%s'" % (config.USER_HISTORY_TABLE_NAME, userName)
        print('DB Search String :',dbSearchString)
        try:
            self.cur.execute(dbSearchString)
            for i in self.cur.fetchall():
                result.append(i[1])
            return result
        except Exception as e:
            print('Database Read Error : ', e)
            return result

    def __del__(self):
        self.conn.close()
