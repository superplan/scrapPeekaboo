# -*- coding: utf-8 -*-
"""
Peekaboo Download
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from fileclass import FileClass, FileType
from commentclass import CommentClass
from albumclass import AlbumClass

import time
import utils

class scrapPeekaboo:
    
    ### Konstanten
    TIME_OUT = 10
    
    def __init__(self):    
        
        ### Selenium Konfig
        self.driver = webdriver.Firefox()
        self.driver.get("http://peekaboomoments.com/en/home/537123580")

    def login(self):
        elem = self.driver.find_element_by_name("user[login]")
        elem.clear()
        elem.send_keys("michael.kamfor@tu-dortmund.de")
        elem = self.driver.find_element_by_name("user[password]")
        elem.clear()
        elem.send_keys("qqquuu")
        elem = self.driver.find_element_by_xpath("//input[@value='Sign in']")
        elem.send_keys(Keys.RETURN)
  
  
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
            if new_height == last_height:
                break
            last_height = new_height
        
    def scrap(self, limit):
        albumListe = self.driver.find_elements_by_class_name("main-list-item")
        
        loop_nr = 0
        for albumListeElement in albumListe:
            
            if loop_nr >= limit:
                break;
                
            loop_nr +=1
            
            albumLink = albumListeElement.find_element_by_class_name("swiper-detail-enter")
            window_before = self.driver.window_handles[0]
            albumLink.click()
            
            ### Warte bis Album geladen hat        
            WebDriverWait(self.driver, self.TIME_OUT).until(EC.new_window_is_opened(self.driver.window_handles))
            
            window_after = self.driver.window_handles[1]
            self.driver.switch_to_window(window_after)
            
            WebDriverWait(self.driver, self.TIME_OUT).until(EC.element_to_be_clickable((By.CLASS_NAME, "pic")))
            bildListe = self.driver.find_elements_by_class_name("pic")
            
            
            print(str(loop_nr) + " von " + str(len(albumListe)))
            
            album = AlbumClass()
            
            tmp_date = self.driver.find_element_by_class_name("detail-date").text
            album.date = utils.format_date(tmp_date)
            
            tmp_caption = self.driver.find_element_by_class_name("describe-content").text
            if tmp_caption != "Write down the story of this day...":                                
                album.caption = tmp_caption
                
            for bild in bildListe:
                
                file = FileClass()
                bild.click()
                
                ### warten und jetzt endlich die daten holen
                WebDriverWait(self.driver, self.TIME_OUT).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='comments-info-content' or @class='comments-null']")))
                    
                link = self.driver.find_element_by_xpath("//*[@class='view-wrap-pic' or @class='view-wrap-video']")
                file.src = link.get_attribute("src")
                file.date = album.date
                
                comments = self.driver.find_elements_by_class_name("comments-info-content")
                for com in comments:
                    tmpCom = CommentClass()
                    tmpCom.text = com.find_element_by_tag_name("mark").text
                    tmpCom.date = com.find_element_by_tag_name("i").text
                    tmpCom.who = com.find_element_by_tag_name("span").text                    
                    tmpCom.is_like = (tmpCom.text == "Liked this photo")
                    file.add_comment([tmpCom])
                    
                album.add_image([file])    
                self.driver.execute_script('{$(".view").hide(), $(".view-wrap-describe").empty(), $(".view-wrap-box").remove(), $(".view-wrap-loading").show(), $(".view-wrap-load").hide();var e = $(".view-content").find("video");0 != e.length && e.each(function() {$(this).get(0).pause()}), T = 0, w = {}}')
                

            # back to man window
            self.driver.switch_to_window(window_before)
            
            album.show_all()
#             break;
                

    def run(self):
        
        self.login()
        
        ### Warte bis Seite geladen hat
        time.sleep(4)

        ### herunterscrollen(wartezeit, anzahl scrolls)
        self.scroll(pauseTime = 1, limit = -1)

        ### hole Daten
        self.scrap(limit = 1)
    
        ### beende selenium        
        self.driver.close()
        
        '''
        TODO
        
        filetype (foto oder video) herausfinden und bestücken
        berechtigung bestücken
        album in datenbank modellieren
        
        '''
        
    def play(self):
        self.login()
        time.sleep(4)
        self.scroll(pauseTime = 1, limit = -1)
        ####################  HIER kann man was ausprobieren
#         self.driver
        ####################
        self.driver.close()
        


if __name__ == "__main__":    
    bla = scrapPeekaboo()
    bla.run()

    

### Hiermit wird direkt nach unten gescrollt

#driver.find_element_by_xpath("/html/body/div[2]/div/div[7]/ul/li[5]").click()
#time.sleep(1)
#driver.find_element_by_xpath("/html/body/div[2]/div/div[7]/ul/li[5]/ul/li/a").click()

### dann kann man das unterste element auswählen und sich nach oben durcharbeiten
### mann muss aber irgendwann wieder nach oben scrollen

#elem = driver.find_element_by_xpath("//*[@id='moments_4_-1']")
#print(elem.get_attribute("data-param"))
