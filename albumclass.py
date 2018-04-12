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
            if(image.is_foto):
                foto += 1
            else:
                vids += 1
        return "(" + str(foto) + ", " + str(vids) + ")"
        
if __name__ == "__main__":
    
    from fileclass import FileClass, FileType
    
    pic = FileClass().example_data()
    vid = FileClass().example_data()
    vid.src += ".mp4"
    vid.type = FileType.video
    
    
    bla = AlbumClass()
    bla.add_image([pic])
    bla.add_image([vid])
    bla.show_all()
    
    