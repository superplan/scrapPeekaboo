# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd #pip install pandas
import hashlib

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

        ### Helfer

        
    def close(self):
        self.db.close()
        
    def create_table_file(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE File(
              FileId        INT PRIMARY KEY NOT NULL,
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
            
    def gen_id(self, str):   
        val = hashlib.sha1(str.encode('utf8'))          
        return int(val.hexdigest()[:10],base=16)     
            
    def add_file(self, fileObject):
        (fotoValue, videoValue) = (0,1)
        if (fileObject.is_foto):
            (fotoValue, videoValue) = (1,0)
        
        cursor = self.db.cursor()
        try:            
            cursor.execute('''
            INSERT INTO File(FileId, SrcOnline, Date, Foto, Video, Caption)
            VALUES(?,?,?,?,?,?)''', 
            (self.gen_id(fileObject.src),
             fileObject.src,
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

        except sqlite3.IntegrityError as e:
            print("WARNUNG: Die Datenbank kennt dieses Foto/Video bereits: " + str(self.gen_id(fileObject.src)))
            print(e)
        finally:
            self.db.commit()
        
    def select(self):
        print(pd.read_sql_query('''SELECT * FROM File''', self.db))
        
            
    def drop_table(self, name):
        cursor = self.db.cursor()
        cursor.execute("DROP TABLE "+name)
        self.db.commit()
    
    def show_tables(self):        
        cursor = self.db.cursor()
        res = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for name in res:
            print(name[0])
            
    def reset(self):
        self.drop_table("File")
        self.drop_table("Comment")
        self.create_table_file()
        self.create_table_comment()

if __name__ == "__main__":
    
    man = dbManager()
#     man.show_tables()
#     print(FileClass().example_data())
    man.add_file(FileClass().example_data())
    man.select()

    
#     test = "http://alihk.peekaboocdn.com/hk/pictures/original/201804/537296975/430397421240478d91b06eb64b39187fd42b1869ec6a01e09ff99bbbec0834dc.jpg"
    
#     print(man.gen_id(test))
    
#     530448612306362800257013452669206305184754401186
#     399065182187
    
    
    
    
    
    
    
    man.close() 
    
    
    