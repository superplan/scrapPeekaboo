# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd  # pip install pandas
import hashlib

from os.path import expanduser


class DBManager:

    def __init__(self, database=""):

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

    @staticmethod
    def gen_id(long_string):
        val = hashlib.sha1(long_string.encode('utf8'))
        return int(val.hexdigest()[:10], base=16)

    def persist_album(self, album_object):

        unique_id = self.gen_id(album_object.src)
        cursor = self.db.cursor()

        try:
            cursor.execute('''
            INSERT INTO Album(AlbumId, Src, Date, Caption)
            VALUES(?,?,?,?)''',
                           (unique_id,
                            album_object.src,
                            album_object.date,
                            album_object.caption))

            for file in album_object.file_list:
                self.persist_file(file, unique_id)

        except sqlite3.IntegrityError as e:
            print(e)
            print("WARNUNG: Möglicherweise kennt die Datenbank kennt dieses Album bereits: " + str(
                self.gen_id(album_object.src)))
        finally:
            self.db.commit()

    def persist_file(self, file_object, album_id, commit=False):

        unique_id = self.gen_id(file_object.src)
        cursor = self.db.cursor()

        try:
            cursor.execute('''
            INSERT INTO File(FileId, SrcOnline, Access, Date, Type, Caption, AlbumId)
            VALUES(?,?,?,?,?,?,?)''',
                           (unique_id,
                            file_object.src,
                            file_object.access.value,
                            file_object.date,
                            file_object.type.value,
                            file_object.caption,
                            album_id))

            for comment in file_object.comment_list:
                self.persist_comment(comment, unique_id)

        except sqlite3.IntegrityError as e:
            print(e)
            print("WARNUNG: Möglicherweise kennt die Datenbank kennt dieses Foto/Video bereits: " + str(
                self.gen_id(file_object.src)))
            print("         Oder es fehlt eine eindeutige Zuordnung zu einem Album.")
        finally:
            if commit:
                self.db.commit()

    def persist_comment(self, comm, file_id, commit=False):
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO Comment(UserName, Date, Like, Text, FileId)
            VALUES(?,?,?,?,?)''',
                       (comm.who,
                        comm.date,
                        comm.is_like,
                        comm.text,
                        file_id))

        if commit:
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

    def get_album_src(self, date = ""):
        c = self.db.cursor()
        t = (date,)
        c.execute('SELECT src FROM Album WHERE Date=? ORDER BY AlbumId', t)
        return c.fetchone()[0]
    
    def file_is_downloaded(self, src = ""):
        c = self.db.cursor()
        t = (src,)
        c.execute('SELECT SrcLocal FROM File WHERE SrcOnline=?', t)
        return c.fetchone() is not None

    def scraped_files_in_album(self, album_src):
        c = self.db.cursor()
        id = (self.gen_id(album_src),)
        c.execute('SELECT Count(FileId) FROM File WHERE AlbumId=?', id)
        return c.fetchone()

    def file_is_scraped(self, file_src):
        c = self.db.cursor()
        c.execute('SELECT Count(FileId) FROM File WHERE SrcOnline=?', [file_src])
        return c.fetchone() > 0

    def get_album_links(self):
        self.db.row_factory = lambda cursor, row: row[0]
        cursor = self.db.cursor()
        # bekannte Alben
        all_links = cursor.execute('SELECT Src FROM Album').fetchall()
        # nocht nicht verarbeitete Alben
        not_progressed = cursor.execute('select Src from Album where AlbumID not in (Select Distinct AlbumId from File)').fetchall()
        # return list(set(all_links) - set(list_1))
        return all_links[-200:]



    def delete(self):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM File WHERE FileId<>'42'")
        self.db.commit()

    def drop_table(self, name):
        cursor = self.db.cursor()
        cursor.execute("DROP TABLE if exists " + name)
        self.db.commit()

    def show_tables(self):
        cursor = self.db.cursor()
        result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for name in result:
            print(name[0])

    def reset(self):
        self.drop_table("Album")
        self.drop_table("File")
        self.drop_table("Comment")
        self.create_table_album()
        self.create_table_file()
        self.create_table_comment()

    def stats(self):
        c = self.db.cursor()
        c.execute('SELECT Count(FileId) FROM File WHERE Type=?', [FileType.foto._value_])
        tmp = c.fetchone()
        print(" Fotos: " + str(tmp[0]))
        c.execute('SELECT Count(FileId) FROM File WHERE Type=?', [FileType.video._value_])
        tmp = c.fetchone()
        print("Videos: " + str(tmp[0]))
        c.execute('SELECT Count(FileId) FROM File WHERE Type=?', [FileType.text._value_])
        tmp = c.fetchone()
        print(" Texte: " + str(tmp[0]))

if __name__ == "__main__":
    
    from fileclass import FileClass, FileType

    man = DBManager()
    album_link = "http://peekaboomoments.com/album_detail/537123580?id=167345424990729199"
    file_link = "http://alihk.peekaboocdn.com/jp/pictures/201504/537296689/d0c178361127433f9ebea9af268e5184.jpg"
    id = man.gen_id(album_link)
    man.stats()
    # print(man.get_album_links())
    id1 = '860343604286'
    id2 ='135059307223'

    man.sel("select * from File where AlbumId = 860343604286")
    man.sel("select * from File where AlbumId = 135059307223")