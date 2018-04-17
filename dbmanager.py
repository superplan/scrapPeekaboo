# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd #pip install pandas
import hashlib

from os.path import expanduser


class DBManager:
    
    def __init__(self, database = ""):
        
        self.database_name = "peekaboo.db"
        if len(database) > 0:
            self.database_name = database
            
        ### Wo bin ich hier?
        home = expanduser("~")
        if home == r'C:\Users\michaelk':
            self.db = sqlite3.connect('C:/Users/michaelk/dev/python/scrapPeekaboo/' + self.database_name)
        else:
            self.db = sqlite3.connect('/home/michael/dev/python/scrapPeekaboo/' + self.database_name)

        self.db.execute("PRAGMA foreign_keys = ON")
        ### Helfer

        
    def close(self):
        self.db.close()

    def create_table_album(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE if not exists Album(
              AlbumId       INT PRIMARY KEY NOT NULL,
              Src           TEXT NOT NULL,
              Date          DATETIME,
              Caption       TEXT
            );
        ''')

    def create_table_file(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE if not exists File(
              FileId        INT PRIMARY KEY NOT NULL,
              SrcOnline     TEXT NOT NULL,
              SrcLocal      TEXT,
              Access        INT,
              Date          DATETIME,
              Type          INT,
              Caption       TEXT,
              AlbumId       INTEGER NOT NULL,
              FOREIGN KEY(AlbumId) REFERENCES Album(AlbumId) ON DELETE CASCADE
            );
        ''')

    def create_table_comment(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE if not exists Comment(
              CommentId     INTEGER PRIMARY KEY,
              UserName      TEXT NOT NULL,
              Date          DATETIME,
              Like          INT,
              Text          TEXT,
              FileId        INTEGER NOT NULL,
              FOREIGN KEY(FileId) REFERENCES File(FileId) ON DELETE CASCADE
            );
        ''')
            
    def gen_id(self, long_string):   
        val = hashlib.sha1(long_string.encode('utf8'))          
        return int(val.hexdigest()[:10],base=16)

    def persist_album(self, albumObject):

        unique_id = self.gen_id(albumObject.src)
        cursor = self.db.cursor()

        try:
            cursor.execute('''
            INSERT INTO Album(AlbumId, Src, Date, Caption)
            VALUES(?,?,?,?)''',
                           (unique_id,
                            albumObject.src,
                            albumObject.date,
                            albumObject.caption))

            for file in albumObject.file_list:
                self.persist_file(file, unique_id)

        except sqlite3.IntegrityError as e:
            print(e)
            print("WARNUNG: Möglicherweise kennt die Datenbank kennt dieses Album bereits: " + str(
                self.gen_id(albumObject.src)))
        finally:
            self.db.commit()

    def persist_file(self, fileObject, album_id, commit = False):
        
        unique_id = self.gen_id(fileObject.src)
        cursor = self.db.cursor()
        
        try:
            cursor.execute('''
            INSERT INTO File(FileId, SrcOnline, Access, Date, Type, Caption, AlbumId)
            VALUES(?,?,?,?,?,?,?)''',
            (unique_id,
             fileObject.src,
             fileObject.access.value,
             fileObject.date,
             fileObject.type.value,
             fileObject.caption,
             album_id))

            for comment in fileObject.comment_list:
                self.persist_comment(comment, unique_id)

        except sqlite3.IntegrityError as e:
            print(e)
            print("WARNUNG: Möglicherweise kennt die Datenbank kennt dieses Foto/Video bereits: " + str(self.gen_id(fileObject.src)))
            print("         Oder es fehlt eine eindeutige Zuordnung zu einem Album.")
        finally:
            if (commit):
                self.db.commit()
                    
    def persist_comment(self, comm, file_id, commit = False):
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO Comment(UserName, Date, Like, Text, FileId)
            VALUES(?,?,?,?,?)''', 
            (comm.who, 
             comm.date, 
             comm.is_like, 
             comm.text,
             file_id))
        
        if(commit):
            self.db.commit()

    def select(self):
        pd.options.display.max_colwidth = 200
        pd.set_option('display.width', 200)
        print(pd.read_sql_query('''SELECT * FROM Album''', self.db))
        print(pd.read_sql_query('''SELECT * FROM File''', self.db))
        print(pd.read_sql_query('''SELECT * FROM Comment''', self.db))
        
    def sel(self, string):
        pd.options.display.max_colwidth = 200
        pd.set_option('display.width', 200)
        print(pd.read_sql_query(string, self.db))
        
    def get_album_links(self):
        self.db.row_factory = lambda cursor, row: row[0]
        cursor = self.db.cursor()
        return cursor.execute('SELECT Src FROM Album').fetchall()

    def delete(self):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM File WHERE FileId<>'42'")
        self.db.commit()
        
    def drop_table(self, name):
        cursor = self.db.cursor()
        cursor.execute("DROP TABLE if exists "+name)
        self.db.commit()
    
    def show_tables(self):        
        cursor = self.db.cursor()
        res = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for name in res:
            print(name[0])
            
    def reset(self):
        self.drop_table("Album")
        self.drop_table("File")
        self.drop_table("Comment")
        self.create_table_album()
        self.create_table_file()
        self.create_table_comment()

if __name__ == "__main__":

        
    from fileclass import FileClass
    from albumclass import AlbumClass
#    test = "http://alihk.peekaboocdn.com/hk/pictures/original/201804/537296975/430397421240478d91b06eb64b39187fd42b1869ec6a01e09ff99bbbec0834dc.jpg"

    
    import sqlite3 as db

    
    conn3 = db.connect('C:/Users/michaelk/dev/python/scrapPeekaboo/peekaboo.db' )
    conn3.row_factory = lambda cursor, row: row[0]
    c3 = conn3.cursor()
    list_4444 = c3.execute('SELECT Date FROM Album').fetchall()  

    
#     print(sorted(set(list_4444) - set(list_444)))
   
#     man = DBManager("peekaboo.db")
#     man.sel("SELECT * FROM Album where Date = '31.07.2015'")
    
    