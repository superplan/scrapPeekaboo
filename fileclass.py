from commentclass import CommentClass
from enum import Enum 

class Access(Enum):
    all = 1
    family = 2
    parents = 3
    personal = 4
    
class FileType(Enum):
    foto = 1
    video = 2

class FileClass:
    
    def __init__(self):
        self.src = None
        self.access = Access.all
        self.type = FileType.foto
        self.date = None
        self.comment_list = []
        self.caption = None
        
    def __str__(self):
        out =  "------- File ------- \n"
        out += "    Type: " + self.type.name + "\n"
        out += "  Access: " + self.access.name + "\n"
        out += "    Date: " + self.date + "\n"
        out += " Caption: " + self.caption + "\n"
        out += "Comments: \n"
        for com in self.comment_list:
            out += "   " + str(com) + "\n"
        return out  
    
    def add_comment(self, comm):
        self.comment_list.extend(comm)
        
    def example_data(self):
        pic = FileClass()
        comm = CommentClass()
        pic.src = "http://qwe/qwe.png"
        pic.add_comment(comm.example_data())
        pic.is_foto = True
        pic.date = "01.01.2018"
        pic.caption = "Here ist somthg"
        return pic
    
if __name__ == "__main__":
    
    pic = FileClass()
    print(pic.example_data())
    