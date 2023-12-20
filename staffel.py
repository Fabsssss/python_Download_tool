from bs4 import BeautifulSoup
import requests
from episode import Episode
import os
from episodenhulle import Episodenhulle

class Staffel:

    def __init__(self, url,path,filename):
        self.path = path
        self.url = url
        self.filename = filename
        self.episodenListe = []

        response = requests.get(self.url)
        if response.status_code == 200:
            self.htmlsoup = BeautifulSoup(response.text, "html.parser")
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)
            return
        
        self.staffelName = self.get_staffel()
        self.checkpath() 
        self.get_episode()

    def get_staffel(self):
        active_links = self.htmlsoup.find_all('a', class_='active')
        for link in active_links:
            return link.text
        
    
    def checkpath(self):
        sta = self.staffelName
        if "Film" not in sta:
            sta = "Staffel "+sta
        if not os.path.exists(self.path+"\\"+sta):
            os.makedirs(self.path+"\\"+sta)
        self.path = self.path+"\\"+sta


    def get_episode(self):
        alreadyList = []
        a_elements = self.htmlsoup.select('.seasonEpisodesList a')
        for a_element in a_elements:
            if str(a_element.get('href')) not in alreadyList:
                try:
                    epidode = Episode("https://aniworld.to"+a_element.get('href'),self.path,self.filename+"_"+self.staffelName)
                    self.episodenListe.append(epidode)
                    alreadyList.append(str(a_element.get('href')))
                except Exception as e:
                    print(f"Unexpected error: {e}")
    
