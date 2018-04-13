from fileclass import FileClass, FileType

class AlbumClass:
    
    
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
            if(image.type == FileType.foto):
                foto += 1
            if(image.type == FileType.video):
                vids += 1
        return "(" + str(foto) + ", " + str(vids) + ")"
        
if __name__ == "__main__":
        
    pic = FileClass().example_data()
    vid = FileClass().example_data()
    vid.src += ".mp4"
    vid.type = FileType.video
    
    
    bla = AlbumClass()
    bla.add_image([pic])
    bla.add_image([vid])
    bla.show_all()
    
    