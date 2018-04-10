class imageClass:
    
    def __init__(self):
        self.src = ""
        self.comment_list = []
        self.is_foto = True
        self.caption = ""
        
    def __str__(self):
        out =  "------- Image ------- \n"
        out += "  Format: " 
        if (self.is_foto):
            out += "photo\n"
        else:
            out += "video\n"
        out += " Caption: " + self.caption + "\n"
        out += "Comments: \n"
        for com in self.comment_list:
            out += "   " + str(com) + "\n"
        return out  
    
    def add_comment(self, comm):
        self.comment_list.extend(comm)
    
class commentClass:
    
    def __init__(self):
        self.is_like = False
        self.who = ""
        self.date = ""
        self.text = ""
        
    def __str__(self):
        out = self.date + "\t" + self.who + ": " 
        if (self.is_like):
            out += " like\n"
        else:
            out += self.text
        return out 
    
if __name__ == "__main__":
    com1 = commentClass()
    com1.date = "01.01.2018 12:31"
    com1.who = "Cool User"    
    com1.text = "Liked this photo"
    com2 = commentClass()
    com2.date = "01.01.2018 16:42"
    com2.who = "Hot User"
    com2.text = "erster!"
    
    pic = imageClass()
    pic.src = "/qwe/qwe.png"
    pic.add_comment([com1, com2])
    pic.caption = "Here ist somthg"
    print(pic)
    