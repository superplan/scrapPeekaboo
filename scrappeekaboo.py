# -*- coding: utf-8 -*-
"""
Peekaboo Download
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from fileclass import FileClass, FileType, Access
from dbmanager import DBManager
from commentclass import CommentClass
from albumclass import AlbumClass

import utils
import time

from selenium.webdriver.common.action_chains import ActionChains

class ScrapPeekaboo:
    
    ### Konstanten
    TIME_OUT = 10
    
    def __init__(self):    
        
        ### Selenium Konfig
        self.driver = webdriver.Firefox()
        self.driver.get("http://peekaboomoments.com/en/home/537123580")
        
        ### Datenbank
        self.db = ""

    def login(self):
        elem = self.driver.find_element_by_name("user[login]")
        elem.clear()
        elem.send_keys("michael.kamfor@tu-dortmund.de")
        elem = self.driver.find_element_by_name("user[password]")
        elem.clear()
        elem.send_keys("qqquuu")
        elem = self.driver.find_element_by_xpath("//input[@value='Sign in']")
        elem.send_keys(Keys.RETURN)   
             
        ### Warte bis Seite geladen hat
        time.sleep(4)
  
  
    ### hiermit wird nach unten bis zum letzten vorgeladenen element gescrollt
    ### so kann man sukzessive nach ganz unten kommen, sodass alle elemente geladen sind
    #https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    def scroll(self, pauseTime, limit):
        
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        scrolls = 0
        while True and scrolls <= limit:
            
            # count scrolls
            scrolls += 1
            
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
            # Wait to load page
            time.sleep(pauseTime)
        
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height <= last_height:
                break
            last_height = new_height
        
    def scrap(self, days_max):
        albumListe = self.driver.find_elements_by_class_name("main-list-item")
        
        loop_nr = 0
        for albumListeElement in albumListe:
            
            if loop_nr >= days_max:
                break;
                
            loop_nr +=1

            album = AlbumClass()

            # Source
            albumLink = albumListeElement.find_element_by_class_name("swiper-detail-enter")
            album.src = albumLink.get_attribute("href")
            # window_before = self.driver.window_handles[0]
            # albumLink.click()
            #
            # ### Warte bis Album geladen hat
            # WebDriverWait(self.driver, self.TIME_OUT).until(EC.new_window_is_opened(self.driver.window_handles))
            #
            # window_after = self.driver.window_handles[1]
            # self.driver.switch_to_window(window_after)
            #
            # WebDriverWait(self.driver, self.TIME_OUT).until(EC.element_to_be_clickable((By.CLASS_NAME, "pic")))
            # bildListe = self.driver.find_elements_by_class_name("pic")
            #
            #
            # print(str(loop_nr) + " von " + str(len(albumListe)))
            #
            # album = AlbumClass()
            #
            # tmp_date = self.driver.find_element_by_class_name("detail-date").text
            # album.date = utils.format_date_file(tmp_date)
            #
            # tmp_caption = self.driver.find_element_by_class_name("describe-content").text
            # if tmp_caption != "Write down the story of this day...":
            #     album.caption = tmp_caption
            #
            # for bild in bildListe:
            #
            #     file = FileClass()
            #     bild.click()
            #
            #     ### warten und jetzt endlich die daten holen
            #     WebDriverWait(self.driver, self.TIME_OUT).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='comments-info-content' or @class='comments-null']")))
            #
            #     link = self.driver.find_element_by_xpath("//*[@class='view-wrap-pic' or @class='view-wrap-video']")
            #     file.src = link.get_attribute("src")
            #     file.date = album.date
            #
            #     comments = self.driver.find_elements_by_class_name("comments-info-content")
            #     for com in comments:
            #         tmpCom = CommentClass()
            #         tmpCom.text = com.find_element_by_tag_name("mark").text
            #         tmpCom.date = com.find_element_by_tag_name("i").text
            #         tmpCom.who = com.find_element_by_tag_name("span").text
            #         tmpCom.is_like = (tmpCom.text == "Liked this photo")
            #         file.add_comment([tmpCom])
            #
            #     album.add_image([file])
            #     self.driver.execute_script('{$(".view").hide(), $(".view-wrap-describe").empty(), $(".view-wrap-box").remove(), $(".view-wrap-loading").show(), $(".view-wrap-load").hide();var e = $(".view-content").find("video");0 != e.length && e.each(function() {$(this).get(0).pause()}), T = 0, w = {}}')
            #
            #
            # # back to man window
            # self.driver.switch_to_window(window_before)
            #
            # album.show_all()
#             break;

    def scrap_album_sources(self, days_max):
        albumListe = self.driver.find_elements_by_class_name("main-list-item")

        loop_nr = 0
        for albumListeElement in reversed(albumListe):

            if loop_nr >= days_max and days_max > 0:
                return

            loop_nr += 1

            try:
                meta_info = albumListeElement.find_element_by_class_name("update")
                tmp_date = meta_info.find_element_by_tag_name("span").text
            except NoSuchElementException:
                print(meta_info.text)
                continue           
            
            try:
                albumLink = albumListeElement.find_element_by_class_name("swiper-detail-enter")

            except NoSuchElementException:
                albumLink = albumListeElement.find_element_by_class_name("text-more")
                    
            album = AlbumClass()
            album.src = albumLink.get_attribute("href")
            album.date = utils.format_date_album(tmp_date)
            
            if type(self.db) is DBManager:
                self.db.persist_album(album)                
            else:
                print(album)
                    
    def get_album_links(self):
        
        self.login()

        ### herunterscrollen(wartezeit zwischen scrolls)
        self.click_through_time(1)

        ### hole Daten
        self.scrap_album_sources(days_max = -1)
    
        ### beende selenium        
        self.driver.close()
        
    def get_album_content(self, links):
        
        if type(self.db) is not DBManager:
            print("keine Datenbank gefunden")
            return
            
        self.login()

        for link in links:
            self.get_files_in_album(link)
    
        ### beende selenium        
        self.driver.close()
        
    def get_files_in_album(self, link):
        
        self.driver.get(link)
        WebDriverWait(self.driver, self.TIME_OUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".main-list-item, .daily-text")))

        try:
            text_entry = self.driver.find_element_by_class_name("daily-text")
            afile = self.scrap_text_file(text_entry, link)

            if type(self.db) is DBManager:
                self.db.persist_file(afile, self.db.gen_id(link), True)
            else:
                print(afile)

        except NoSuchElementException:

            # Foto oder Video
            file_list = self.driver.find_elements_by_class_name("main-list-item")

            for file_elem in file_list:
                afile = self.scrap_file(file_elem)

                if type(self.db) is DBManager:
                    self.db.persist_file(afile, self.db.gen_id(link), True)
                else:
                    print(afile)

    def scrap_text_file(self, text_entry):
        
        text_entry.click()
        WebDriverWait(self.driver, self.TIME_OUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".daily-text")))
        
        res = FileClass()

        # type
        res.type = FileType.text

        # date and access
        parent = self.driver.find_element_by_class_name("detail")
        child = parent.find_element_by_tag_name("mark")
        tmp_date_and_access = parent.text.replace(child.text, '')
        (tmp_date, tmp_access) = utils.format_date_access(tmp_date_and_access)
        res.date = tmp_date
        res.access = Access.set(tmp_access)


        # comments
        comments_list = self.driver.find_elements_by_class_name("comments-list-item")

        for com in comments_list:
            res.add_comment([self.scrap_comment(com, True)])

        return res

    def click_through_time(self, wait_time):
        years = self.driver.find_elements_by_class_name("timeline-wrap-item")
        # skip "Today"
        for year in years[1:]:
            self.driver.execute_script("arguments[0].click();", year)
            time.sleep(wait_time)
            months = year.find_elements_by_class_name("item-btn")
            # skip clicking on the year a second time
            for month in months[1:]:
                self.driver.execute_script("arguments[0].click();", month)
                time.sleep(wait_time)

    # create a file-object and fill values
    def scrap_file(self, file_elem):

        res = FileClass()

        # type
        try:
            file_elem.find_element_by_class_name("btn")
            # it's a video
            res.type = FileType.video
        except NoSuchElementException:
            # it's a photo
            res.type = FileType.foto

        # source link
        if res.type == FileType.foto:
            tmp_link = file_elem.find_element_by_class_name("pic")
            tmp_text = tmp_link.get_attribute("src")
            res.src = tmp_text.split('!large')[0]
        else:
            # open pop-up
            file_elem.click()

            # wait for pop-up to load
            WebDriverWait(self.driver, self.TIME_OUT).until(EC.visibility_of_element_located(
                (By.XPATH, "//*[@class='comments-info-content' or @class='comments-null']")))

            tmp_link = self.driver.find_element_by_xpath("//*[@class='view-wrap-pic' or @class='view-wrap-video']")
            res.src = tmp_link.get_attribute("src")

            # close pop-up
            self.driver.execute_script(
                '{$(".view").hide(), $(".view-wrap-describe").empty(), $(".view-wrap-box").remove(), $(".view-wrap-loading").show(), $(".view-wrap-load").hide();var e = $(".view-content").find("video");0 != e.length && e.each(function() {$(this).get(0).pause()}), T = 0, w = {}}')

        # date
        res.date = utils.format_date_file(self.driver.find_element_by_class_name("detail-date").text)

        # access (Berechtigung) and caption
        ## open edit-popup
        hover_menu = file_elem.find_element_by_class_name("contain")
        actions = ActionChains(self.driver)
        actions.move_to_element(hover_menu).perform()
        edit_menu = file_elem.find_element_by_class_name("operate-more")
        actions.click(edit_menu).perform()
        file_elem.find_element_by_class_name("more-edit").click()
        ## access
        access_prop = self.driver.find_element_by_class_name("edit-operate-power")
        res.access = Access.set(access_prop.find_element_by_tag_name("mark").text)
        ## caption
        res.caption = self.driver.find_element_by_class_name("edit-textarea").text
        ## close edit-popup
        self.driver.find_element_by_class_name("edit-across").click()

        # comments
        hover_menu = file_elem.find_element_by_class_name("contain")
        actions = ActionChains(self.driver)
        actions.move_to_element(hover_menu).perform()
        self.driver.execute_script("document.getElementsByClassName('operate-comment')[0].style.display='block';")
        file_elem.find_element_by_class_name("operate-comment").click()
        # hier ist entweder comment-null oder comment-popup
        WebDriverWait(self.driver, self.TIME_OUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".comment-popup, .comment-null")))
        comments_list = file_elem.find_elements_by_class_name("comment-content-item")

        for com in comments_list:
            res.add_comment([self.scrap_comment(com)])

        return res

    # create a comment-object and fill with values
    def scrap_comment(self, comment_elem, text_file = False):

        # scroll to comment, otherwise it is not visible!
        self.driver.execute_script("arguments[0].scrollIntoView();", comment_elem)

        # set attributes
        res = CommentClass()

        if not text_file:
            tmp_text = comment_elem.find_element_by_tag_name("span").text.split(' : ')
            print("hi")
        else:
            tmp_text = comment_elem.find_element_by_class_name("comments-list-content").text.split(' : ')

        res.who = tmp_text[0]
        res.text = tmp_text[1]
        res.is_like = (res.text == "Liked this photo")

        # scroll to date, in case of a long comment
        tmp_date = comment_elem.find_element_by_tag_name("i")
        self.driver.execute_script("arguments[0].scrollIntoView();", tmp_date)
        res.date = tmp_date.text
        return res

    def play(self):
        self.login()

        ####################
        ### Ab hier kann man was ausprobieren
        # ohne commentar
        # http://peekaboomoments.com/daily_detail/537123580?id=561216195715658404
        # mit kommentar
        # http://peekaboomoments.com/daily_detail/537123580?id=210012179038729147
        # self.get_files_in_album("http://peekaboomoments.com/album_detail/537123580?id=561212659812528779")


        self.scrap_album_sources(20)



if __name__ == "__main__":


    bla = ScrapPeekaboo()
    bla.play()
    

### Hiermit wird direkt nach unten gescrollt

#driver.find_element_by_xpath("/html/body/div[2]/div/div[7]/ul/li[5]").click()
#time.sleep(1)
#driver.find_element_by_xpath("/html/body/div[2]/div/div[7]/ul/li[5]/ul/li/a").click()

### dann kann man das unterste element auswählen und sich nach oben durcharbeiten
### mann muss aber irgendwann wieder nach oben scrollen

#elem = driver.find_element_by_xpath("//*[@id='moments_4_-1']")
#print(elem.get_attribute("data-param"))
