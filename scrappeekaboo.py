# -*- coding: utf-8 -*-
"""
Peekaboo Download
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from fileclass import FileClass, FileType, Access
from dbmanager import DBManager
from commentclass import CommentClass
from albumclass import AlbumClass

import utils
import time
import urllib.request

from selenium.webdriver.common.action_chains import ActionChains
from filemanager import FileManager


class ScrapPeekaboo:
    ### Konstanten
    TIME_OUT = 10

    def __init__(self):

        ### Selenium Konfig
        # To prevent download dialog
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2) # custom location
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', 'C:/Users/michaelk/dev/python/pkb_files')
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
        # connection
        self.driver = webdriver.Firefox(firefox_profile=profile)

        ### Datenbank
        self.db = ""

    def login(self):
        self.driver.get("http://peekaboomoments.com/en/home/537123580")
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
    # https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    def scroll(self, pause_time, limit):

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        scrolls = 0
        while True and scrolls <= limit:

            # count scrolls
            scrolls += 1

            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height <= last_height:
                break
            last_height = new_height

    def scrap_album_sources(self, days_max):
        global meta_info
        album_liste = self.driver.find_elements_by_class_name("main-list-item")

        loop_nr = 0
        for albumListeElement in reversed(album_liste):

            if loop_nr >= days_max > 0:
                return

            loop_nr += 1

            try:
                meta_info = albumListeElement.find_element_by_class_name("update")
                tmp_date = meta_info.find_element_by_tag_name("span").text
            except NoSuchElementException:
                print(meta_info.text)
                continue

            try:
                album_link = albumListeElement.find_element_by_class_name("swiper-detail-enter")

            except NoSuchElementException:
                album_link = albumListeElement.find_element_by_class_name("text-more")

            album = AlbumClass()
            album.src = album_link.get_attribute("href")
            album.date = utils.format_date_album(tmp_date)

            if type(self.db) is DBManager:
                self.db.persist_album(album)
            else:
                print(album)

    def get_album_links(self):

        self.login()

        ### herunterscrollen(wartezeit zwischen scrolls)
        # self.click_through_time(5)
        self.scroll_down(5)
        # self.scroll_down_inf(0.1)

        ### hole Daten
        self.scrap_album_sources(days_max=-1)

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

        if "daily_detail" in link:
            text_entry = self.driver.find_element_by_class_name("daily-text")
            afile = self.scrap_text_file(text_entry)
            afile.src = link

            if type(self.db) is DBManager:
                self.db.persist_file(afile, self.db.gen_id(link), True)
            else:
                print(afile)

        else:
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
        loops = 0
        while loops < 2:
            loops += 1

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

        album_liste = self.driver.find_elements_by_class_name("main-list-item")
        for elem in album_liste:
            self.driver.execute_script("arguments[0].scrollIntoView();", elem)
            time.sleep(wait_time)

    def scroll_down(self, wait_time):

        while True:

            WebDriverWait(self.driver, self.TIME_OUT).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "dropload-down")))
            alben_vor_scroll = len(self.driver.find_elements_by_class_name("main-list-item"))
            letztes_element = self.driver.find_element_by_class_name("dropload-down")
            self.driver.execute_script("arguments[0].scrollIntoView();", letztes_element)
            time.sleep(wait_time)
            alben_nach_scroll = len(self.driver.find_elements_by_class_name("main-list-item"))

            if alben_vor_scroll == alben_nach_scroll:
                return

    def scroll_down_inf(self, wait_time):
        while True:
            self.driver.execute_script("window.scrollBy(0,10)", "")
            time.sleep(wait_time)

    # create a file-object and fill values
    def scrap_file(self, file_elem):

        res = FileClass()
        self.driver.execute_script("arguments[0].scrollIntoView();", file_elem)

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
#         self.driver.execute_script('return arguments[0].getElementsByClassName("more-edit")[0].click();', file_elem)
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
    def scrap_comment(self, comment_elem, text_file=False):

        # scroll to comment, otherwise it is not visible!
        # self.driver.execute_script("arguments[0].scrollIntoView();", comment_elem)

        # set attributes
        res = CommentClass()

        if not text_file:
            tmp_text = self.get_tag_text(comment_elem, "span")
        else:
#             tmp_text = comment_elem.find_element_by_class_name("comments-list-content").text.split(' : ')
            tmp_text = self.get_class_text(comment_elem, "comments-list-content")


        (res.who, res.text) = utils.html_to_user_comment(tmp_text)
        res.is_like = (res.text == "Liked this photo")

        # scroll to date, in case of a long comment
        res.date = self.get_tag_text(comment_elem, "i")
        return res
    
    def get_tag_text(self, dom_element, tag_name):
        tmp_text = self.driver.execute_script('return arguments[0].getElementsByTagName("{0}")[0].innerHTML;'.format(tag_name), dom_element)
        return tmp_text

    def get_class_text(self, dom_element, class_name):
        tmp_text = self.driver.execute_script('return arguments[0].getElementsByClassName("{0}")[0].innerHTML;'.format(class_name), dom_element)
        return tmp_text
        
    def download_file(self, db, fs, file):
        
        # check if already downloaded
        if db.file_is_downloaded(file.src):
            return
        # name
        path = fs.get_target_path(file) + file.src.split('/')[-1]

        # get it
        urllib.request.urlretrieve(file.src, path)

        # save metadata
        
    def play(self):
#         self.login()

        #########################################
        ### Ab hier kann man was ausprobieren ###
        #########################################

        db = DBManager()
        fs = FileManager()
        file = FileClass()
        file.src ="http://alihk.peekaboocdn.com/jp/pictures/original/201612/537296975/9f609a0c176a40abb8100d85fa86e9c8.jpg"
        file.type = FileType.foto
        file.date = "32.12.2008"
        
        self.download_file(db, fs, file)
        self.driver.close()

if __name__ == "__main__":
    bla = ScrapPeekaboo()
    bla.play()



