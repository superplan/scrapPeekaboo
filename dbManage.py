# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd #pip install pandas

from fileclass import FileClass
from os.path import expanduser
    

class dbManager:
    
    def __init__(self):
        
        ### Wo bin ich hier?
        home = expanduser("~")
        if home == r'C:\Users\michaelk':
            self.db = sqlite3.connect('C:/Users/michaelk/dev/python/scrapPeekaboo/peekaboo.db')
        else:
            self.db = sqlite3.connect('/home/michael/dev/python/scrapPeekaboo/peekaboo.db')

    def close(self):
        self.db.close()
        
    def create_table_file(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE File(
              FileId        INTEGER PRIMARY KEY,
              SrcOnline     TEXT NOT NULL,
              SrcLocal      TEXT,
              Date          DATETIME,
              Foto          INTEGER NOT NULL,
              Video         INTEGER NOT NULL,
              Caption       TEXT
            );
        ''')
            
    def create_table_comment(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE Comment(
              CommentId     INTEGER PRIMARY KEY,
              UserName      TEXT NOT NULL,
              Date          DATETIME,
              Like          INTEGER,
              Text          TEXT,              
              FileId        INTEGER NOT NULL,
              FOREIGN KEY(FileId) REFERENCES File(FileId)
            );
        ''')
            
    def add_file(self, fileObject):
        (fotoValue, videoValue) = (0,1)
        if (fileObject.is_foto):
            (fotoValue, videoValue) = (1,0)
        
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO File(SrcOnline, Date, Foto, Video, Caption)
            VALUES(?,?,?,?,?)''', 
            (fileObject.src, 
             fileObject.date, 
             fotoValue, 
             videoValue,
             fileObject.caption))
#         cursor.execute('''
#             INSERT INTO Comment(UserName, Date, Like, Text, FileId)
#             VALUES(?,?,?,?,?)''', 
#             (fileObject.src, 
#              fileObject.date, 
#              fotoValue, 
#              videoValue,
#              fileObject.caption))
        self.db.commit()
        
    def select(self):
        print(pd.read_sql_query('''SELECT * FROM Comment''', self.db))
        
            
    def drop_table(self, name):
        cursor = self.db.cursor()
        cursor.execute("DROP TABLE "+name)
        self.db.commit()
    
    def show_tables(self):        
        cursor = self.db.cursor()
        res = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for name in res:
            print(name[0])

if __name__ == "__main__":
    
    dbm = dbManager()
    dbm.show_tables()

    pic = FileClass()
    print(pic.example_data())
     
    dbm.add_file(pic.example_data())
    dbm.select()