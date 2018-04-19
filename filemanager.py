# -*- coding: utf-8 -*-

from os.path import expanduser
from fileclass import FileClass, FileType
import os

class FileManager:

    def __init__(self):

        ### Wo bin ich hier?
        home = expanduser("~")
        if home == r'C:\Users\michaelk':
            self.root_dir = 'C:/Users/michaelk/dev/python/pkb_files/'
        else:
            self.root_dir = '/home/michael/dev/python/pkb_files??/'
            
        self.img_dir = self.root_dir + "img/"
        self.vid_dir = self.root_dir + "vid/"
        self.txt_dir = self.root_dir + "txt/"
            
#         os.path.exists("/home/el/myfile.txt")
        self.make_dir(self.img_dir)
        self.make_dir(self.vid_dir)
        self.make_dir(self.txt_dir)
            
    @staticmethod
    def make_dir(dir_path):
        if not os.path.isdir(dir_path):
            print("HINWEIS: Verzeichnis angelegt: " + dir_path)
            os.makedirs(dir_path)

    # date = "dd.mm.yyyy"
    def get_target_path(self, file):
        tmp = file.date.split(".")
        if file.type == FileType.foto:
            path = self.img_dir + tmp[2] + "_" + tmp[1] + "/"
        if file.type == FileType.video:
            path = self.vid_dir + tmp[2] + "_" + tmp[1] + "/"
        if file.type == FileType.text:
            path = self.txt_dir + tmp[2] + "/"
            
        self.make_dir(path)
        return path
        

if __name__ == "__main__":
    fm = FileManager()
#     test = FileClass()
#     test.date = "30.05.2019"
#     test.type = FileType.video
#     print(fm.get_target_path(test))

    import urllib.request
    urllib.request.urlretrieve("http://alihk.peekaboocdn.com/jp/pictures/original/201612/537296975/9f609a0c176a40abb8100d85fa86e9c8.jpg", 'C:/Users/michaelk/dev/python/scrapPeekaboo/bla.jpg')
