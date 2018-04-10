#from image import image, comment

from imageClass import imageClass, commentClass

class albumClass:
    
    
    def __init__(self, caption = "", date = ""):
        self.image_list = []  
        self.caption = caption
        self.date = date  
        
        self.format_date() 
        
    def __str__(self):
        out =  "---------- Album ---------- \n"
        out += "           Datum: " + self.date + "\n"
        out += "         Caption: " + self.caption + "\n"
        

        out += "Total (pic, vid): " + str(len(self.image_list)) + " " +self.get_number_foto()
        return out
    
    def show_all(self):
        print(self)
        for im in self.image_list:
            print(im)
    
    def add_image(self, im):
        self.image_list.extend(im)
        
    def format_date(self):
        self.date = self.date + "formated"
        
    def get_number_foto(self):
        foto = 0
        vids = 0
        for image in self.image_list:
            if(image.is_foto):
                foto += 1
            else:
                vids += 1
        return "(" + str(foto) + ", " + str(vids) + ")"
        
if __name__ == "__main__":
    com1 = commentClass()
    com1.date = "01.01.2018 12:31"
    com1.who = "Cool User"    
    com1.text = "Liked this photo"
    com2 = commentClass()
    com2.date = "01.01.2018 16:42"
    com2.who = "Hot User"
    com2.text = "erster!"
    com3 = commentClass()
    com3.date = "10.01.2016 00:12"
    com3.who = "Cool User"
    com3.text = "Liked this photo"
    
    pic = imageClass()
    pic.src = "/qwe/qwe.png"
    pic.add_comment([com1, com2])
    pic.caption = "Here ist somthg"
    
    vid = imageClass()
    vid.src = "/qwe/qwe123.mp4"
    vid.is_foto = False
    pic.add_comment([com3])
    
    
    bla = albumClass()
    bla.add_image([pic])
    bla.add_image([vid])
    bla.show_all()
    
    