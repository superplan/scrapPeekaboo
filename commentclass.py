class CommentClass:
    
    def __init__(self):
        self.is_like = False
        self.who = ""
        self.date = ""
        self.text = ""
        
    def __str__(self):
        out = self.date + "\t" + self.who + ": " 
        if (self.is_like):
            out += " like"
        else:
            out += self.text
        return out + "\n"
    
    def example_data(self):
        com1 = CommentClass()
        com1.date = "01.01.2018 12:31"
        com1.who = "Cool User"    
        com1.text = "Liked this photo"
        com2 = CommentClass()
        com2.date = "01.01.2018 16:42"
        com2.who = "Hot User"
        com2.text = "erster!"
        return [com1, com2]
    
if __name__ == "__main__":

    test = CommentClass()
    for com in test.example_data():
        print(com)
    