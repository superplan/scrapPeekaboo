# -*- coding: utf-8 -*-
"""
Peekaboo Download
"""

from scrappeekaboo import ScrapPeekaboo
from dbmanager import DBManager
from filemanager import FileManager


# first run
def setup():
    db = DBManager()
    db.reset()


# get album links
def get_album_links():
    db = DBManager()
    scrap = ScrapPeekaboo()
    scrap.db = db
    scrap.get_album_links()


# get sources for files, comments ect
def get_album_content():
    db = DBManager()
    scrap = ScrapPeekaboo()
    scrap.db = db
    scrap.get_album_content(db.get_album_links())


# download files
def download_files():
    db = DBManager()
    fm = FileManager()
    scrap = ScrapPeekaboo(fm)
    scrap.db = db
    scrap.download_all_files()



    scrap.get_album_content(db.get_album_links())


# view database
def view():
    db = DBManager()
    db.sel("SELECT * FROM File ")
    db.sel("SELECT * FROM Comment ")


# view()
# get_album_links()
# get_album_content()
download_files()