from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import m3u8_To_MP4
import os
import time
import requests
from bs4 import BeautifulSoup


class Episode:
    def __init__(self, episoden_titel="", episoden_url="", staffel="",episoden_nummer = 0, german_vorhanden=False, voe_vorhanden=False, path="", bereits_gedownloaded=False, download_link="", episoden_info=""):
        self._episoden_info = episoden_info
        if(self._episoden_info == ""):
            self._episoden_titel = episoden_titel
            self._episoden_url = episoden_url
            self._staffel = staffel

            self._episoden_nummer = episoden_nummer
            self._german_vorhanden = german_vorhanden
            self._voe_vorhanden = voe_vorhanden
            self._path = path
            self._bereits_gedownloaded = bereits_gedownloaded
            self._download_link = download_link
        else:
            self._episoden_info = self._episoden_info.replace('[', '').replace(']', '')
            result = self._episoden_info.split(',')
            for res in result:
                if "episoden_titel=" in res:
                    self._episoden_titel = (res.replace('episoden_titel=','')).strip()
                if "episoden_url=" in res:
                    self._episoden_url = (res.replace('episoden_url=','')).strip()
                if "staffel=" in res:
                    self._staffel = (res.replace('staffel=','')).strip()
                if "episoden_nummer" in res:
                    self._episoden_nummer = (res.replace('episoden_nummer=','')).strip()
                if "german_vorhanden=" in res:
                    self._german_vorhanden = (res.replace('german_vorhanden=','')).strip()
                if "voe_vorhanden=" in res:
                    self._voe_vorhanden = (res.replace('voe_vorhanden=','')).strip()
                if "path=" in res:
                    self._path = (res.replace('path=','')).strip()
                if "bereits_gedownloaded=" in res:
                    self._bereits_gedownloaded = (res.replace('bereits_gedownloaded=','')).strip()
                if "download_link=" in res:
                    self._download_link = (res.replace('download_link=','')).strip()

    # Getter-Methoden
    def get_episoden_titel(self):
        return self._episoden_titel

    def get_episoden_url(self):
        return self._episoden_url

    def get_staffel(self):
        return self._staffel
    
    def get_episoden_nummer(self):
        return self._episoden_nummer 

    def is_german_vorhanden(self):
        return self._german_vorhanden

    def is_voe_vorhanden(self):
        return self._voe_vorhanden

    def get_path(self):
        return self._path

    def is_bereits_gedownloaded(self):
        return self._bereits_gedownloaded

    def get_download_link(self):
        return self._download_link

    # Setter-Methoden
    def set_episoden_titel(self, episoden_titel):
        self._episoden_titel = episoden_titel

    def set_episoden_url(self, episoden_url):
        self._episoden_url = episoden_url

    def set_staffel(self, staffel):
        self._staffel = staffel

    def set_episoden_nummer(self, episoden_nummer):
        self._episoden_nummer = episoden_nummer

    def set_german_vorhanden(self, german_vorhanden):
        self._german_vorhanden = german_vorhanden

    def set_voe_vorhanden(self, voe_vorhanden):
        self._voe_vorhanden = voe_vorhanden

    def set_path(self, path):
        self._path = path

    def set_bereits_gedownloaded(self, bereits_gedownloaded):
        self._bereits_gedownloaded = bereits_gedownloaded

    def set_download_link(self, download_link):
        self._download_link = download_link

    def __str__(self):
            return f"[episoden_titel={self._episoden_titel}, episoden_url={self._episoden_url}, staffel={self._staffel}, episoden_nummer={self._episoden_nummer}, german_vorhanden={self._german_vorhanden}, voe_vorhanden={self._voe_vorhanden}, path={self._path}, bereits_gedownloaded={self._bereits_gedownloaded}, download_link={self._download_link}]"
    
    def __eq__(self, other):
        if isinstance(other, Episode):
            return True
        return False


class download:
    def __init__(self, aniworldURL, path):

        self.aniworldURL = aniworldURL
        self.folgen = {}

        position = self.aniworldURL.rfind("/")
        self.titel = self.aniworldURL[position + 1:]
        self.path = path+"\\"+self.titel

        self.get_list()
        self.episodenInfo()

        if not os.path.exists(self.path):
            os.makedirs(self.path)
        else:
            if os.path.exists(self.path+"\\"+"edit.txt"):
                with open(self.path+"\\"+"edit.txt", 'r') as datei:
                    for zeile in datei:
                        epi = Episode(episoden_info=zeile)
                        self.checkExistingfile(epi)

        for key in self.folgen:
            if not os.path.exists(self.path+"\\"+self.folgen[key].get_staffel()):
                os.makedirs(self.path+"\\"+self.folgen[key].get_staffel())

        print("start with selenizum")
        self.selenium()
        for key in self.folgen:
            print(self.folgen[key])
        i = 1
        staffelchange = "e"
        for key in self.folgen: 
            try:
                if self.folgen[key].is_voe_vorhanden():
                    if(staffelchange != self.folgen[key].get_staffel()):
                        staffelchange = self.folgen[key].get_staffel()
                        i = 1
                    m3u8_To_MP4.multithread_download(self.folgen[key].get_download_link(),self.path+"\\"+self.folgen[key].get_staffel()+"\\"+self.titel+"_"+str(i)+"_"+self.folgen[key].get_episoden_titel()+".mp4")
                    self.folgen[key].set_bereits_gedownloaded(True)
                    self.folgen[key].set_path(self.path+"\\"+self.folgen[key].get_staffel()+"\\"+self.titel+"_"+str(i)+"_"+self.folgen[key].get_episoden_titel()+".mp4")
                    i = i+1
            except Exception as e:
                print(f"An error occurred: {e}")

        self.toFile()



    def checkExistingfile(self, episode):
                #episoden url, staffel,nummer,  voe, german, titel
        for key in self.folgen:
            if episode.get_staffel == self.folgen[key].get_staffel and episode.get_episoden_nummer == self.folgen[key].get_episoden_nummer:
                if (episode.is_german_vorhanden() == False and self.folgen[key].is_german_vorhanden() == True):
                    if os.path.exists(episode.get_path()):
                        os.remove(episode.get_path())

                
                #if (episode.is_voe_vorhanden() == False and self.folgen[key].is_voe_vorhanden() == True):
                  
        i = 0

    
    def episodenInfo(self):
        for key in self.folgen:
            episode = self.folgen[key]
            episode.set_episoden_nummer(int(episode.get_episoden_url()[-1]))
            response = requests.get(episode.get_episoden_url())
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                element = soup.find(class_="changeLanguageBox")
                if element:
                    if "German, Deutsch, Flagge, Sprache" in (str(element)):
                        episode.set_german_vorhanden(True)
                        element = soup.find(class_="episodeGermanTitle")
                        episode.set_episoden_titel((str(element.text)))
                    else: 
                        episode.set_german_vorhanden(False)
                        element = soup.find(class_="episodeEnglishTitle")
                        episode.set_episoden_titel((str(element.text)))

                ziel_h4 = soup.find('h4', string='VOE')
                if ziel_h4:
                    episode.set_voe_vorhanden(True)
                else:
                    episode.set_voe_vorhanden(False)

    def get_list(self):
        response = requests.get(self.aniworldURL)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            element = soup.find(id="stream")
            links = element.find_all("a")
            for link in links:
                href = link.get("href")
                if href:
                    if not("episode" in href) and not("div" in href):
                        self.get_episode("https://aniworld.to"+href)   
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)

    def get_episode(self,href):
        list_of_episode = []
        inner_response = requests.get(href)
        if inner_response.status_code == 200:
            inner_soup = BeautifulSoup(inner_response.text, "html.parser")
            inner_elements = inner_soup.find_all(class_="seasonEpisodesList")
            for inner_element in inner_elements:
                inner_links = inner_element.find_all("a")
                for inner_link in inner_links:
                    inner_href = inner_link.get("href")
                    if inner_href:
                        if "https://aniworld.to"+inner_href not in list_of_episode:
                            self.order_episode("https://aniworld.to"+inner_href)
        else:
            print("Failed to retrieve the webpage. Status code:", inner_response.status_code)
        


    def order_episode(self, episode):
        new_episode = Episode()
        new_episode.set_episoden_url(episode)

        letzte_position = episode.rfind("/")
        zweites_von_hinten = episode.rfind("/", 0, letzte_position)
        ausgeschnittener_teil = episode[zweites_von_hinten+1 :letzte_position]
        new_episode.set_staffel(ausgeschnittener_teil)

        if episode not in self.folgen:
            self.folgen[episode] = new_episode 
        return 

    

    def selenium(self):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        #driver.maximize_window()
        for key in self.folgen.keys():
            episode = self.folgen[key]
            try:
                driver.get(episode.get_episoden_url())
                print("new one")
                time.sleep(1)
                page_source = driver.page_source
                elements = page_source.split("\"")
                for element in elements:
                    if "/redirect/" in element:
                        response = requests.get(("https://aniworld.to" + element))
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.text, "html.parser")
                            res = (str(soup)).split("'")
                            for r in res:
                                if "m3u8" in r:
                                    episode.set_download_link(r)
                                    break
                            break
            except Exception as e:
                print(f"An error occurred: {e}")
        driver.quit()




    def toFile(self):
        with open(self.path+"\\edit.txt", 'w', encoding='utf-8') as file:
            for key in self.folgen:
                file.write(str(self.folgen[key])+"\n")






dateipfad = 'F:\\Serien\\ZUG ZEUG\\serien.txt'
with open(dateipfad, 'r') as datei:
    for zeile in datei:
        inhalt = (zeile.replace('\n','')).strip()
        print(inhalt)
        d = download(str(inhalt), "F:\\Serien\\ZUG ZEUG")
