from fileclass import FileClass, FileType, Access
from commentclass import CommentClass


class AlbumClass:

    def __init__(self, caption="", date=""):
        self.file_list = []
        self.caption = caption
        self.date = date
        self.src = ""

    def __str__(self):
        out = "---------- Album ---------- \n"
        out += "           Datum: " + self.date + "\n"
        out += "         Caption: " + self.caption + "\n"
        out += "          Source: " + self.src + "\n"

        out += "Total (pic, vid): " + str(len(self.file_list)) + " " + self.get_number_foto()
        return out

    def show_all(self):
        print(self)
        for im in self.file_list:
            print(im)

    def add_image(self, im):
        self.file_list.extend(im)

    def get_number_foto(self):
        foto = 0
        vids = 0
        for image in self.file_list:
            if image.type == FileType.foto:
                foto += 1
            if image.type == FileType.video:
                vids += 1
        return "(" + str(foto) + ", " + str(vids) + ")"

    @staticmethod
    def example_data():
        alb = AlbumClass()
        file = FileClass()
        alb.src = "http://qwe/einAlbum/blabla"
        alb.caption = "Oh eine Überschrift :D"
        alb.date = "01.02.2042"
        file1 = file.example_data()
        file2 = file.example_data()
        file2.type = FileType.video
        file2.access = Access.me
        file2.src = file2.src + ".mp4"
        alb.add_image([file1, file2])
        return alb


if __name__ == "__main__":
    test = AlbumClass().example_data()
    # test.show_all()
    print(test)
