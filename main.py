# -*- coding: utf-8 -*-
"""
Peekaboo Download
"""

from scrappeekaboo import ScrapPeekaboo
from dbmanager import DBManager

# get album links
def get_album_links():
    db = DBManager()
    scrap = ScrapPeekaboo()
    scrap.db = db
    scrap.get_album_links()
    db.select()
    
# get sources for files, comments ect
def get_album_content():
    db = DBManager()
    scrap = ScrapPeekaboo()
    scrap.db = db
    scrap.get_album_content(db.get_album_links())
    db.select()
    
# view database
def view():
    db = DBManager()
    db.select()  
    
# get_album_content()
view()

