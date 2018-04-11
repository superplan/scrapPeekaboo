from commentclass import CommentClass

class FileClass:
    
    def __init__(self):
        self.src = ""
        self.comment_list = []
        self.is_foto = True
        self.date = ""
        self.caption = ""
        
    def __str__(self):
        out =  "------- Image ------- \n"
        out += "  Format: " 
        if (self.is_foto):
            out += "photo\n"
        else:
            out += "video\n"
        out += " Caption: " + self.caption + "\n"
        out += "    Date: " + self.date + "\n"
        out += "Comments: \n"
        for com in self.comment_list:
            out += "   " + str(com) + "\n"
        return out  
    
    def add_comment(self, comm):
        self.comment_list.extend(comm)
        
    def example_data(self):
        pic = FileClass()
        comm = CommentClass()
        pic.src = "/qwe/qwe.png"
        pic.add_comment(comm.example_data())
        pic.is_foto = True
        pic.date = "01.01.2018"
        pic.caption = "Here ist somthg"
        return pic
    
if __name__ == "__main__":
    
    pic = FileClass()
    print(pic.example_data())
    