from commentclass import CommentClass
from enum import Enum


class Access(Enum):
    all = 1  # Family Members and Fans
    family = 2  # Family Members
    parents = 3  # Parents
    me = 4  # Only Me

    @staticmethod
    def set(arg):
        mapping = {
            "Family Members and Fans": Access.all,
            "Family Members": Access.family,
            "Parents": Access.parents,
            "Only Me": Access.me
        }
        return mapping[arg]


class FileType(Enum):
    foto = 1
    video = 2
    text = 3


class FileClass:

    def __init__(self, data = None):
        self.src = None
        self.access = Access.all
        self.type = FileType.foto
        self.date = None
        self.comment_list = []
        self.caption = ""

        if data != None:
            (self.src, self.date, self.type) = data
            # convert FileType to Enum
            self.type = FileType(self.type)

    def __str__(self):
        out = "------- File ------- \n"
        out += "  Source: " + self.src + "\n"
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

    @staticmethod
    def example_data():
        pic = FileClass()
        comm = CommentClass()
        pic.src = "http://qwe/qwe.png"
        pic.add_comment(comm.example_data())
        pic.is_foto = True
        pic.date = "01.01.2018"
        pic.caption = "Here ist something"
        pic.access = Access.set("Family Members and Fans")
        return pic


if __name__ == "__main__":
    pic = FileClass()
    print(pic.example_data())
