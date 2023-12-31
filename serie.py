from bs4 import BeautifulSoup
import requests
from staffel import Staffel
import os

class Serie:
    
    def __init__(self, url, path):
        
        self.path = path
        self.url = url
        self.staffel = []

        response = requests.get(self.url)
        if response.status_code == 200:
            self.htmlsoup = BeautifulSoup(response.text, "html.parser")
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)
            return
        
        self.titleOfTheSeries = (self.correctString(self.getTitleOfTheSeries())).strip()
        self.checkpath()
        self.get_list()


    def getTitleOfTheSeries(self):
        spanObjects = self.htmlsoup.find_all('h1')
        for h1 in spanObjects:
            return h1.text

    def checkpath(self):
        if not os.path.exists(self.path+"\\"+self.titleOfTheSeries):
            os.makedirs(self.path+"\\"+self.titleOfTheSeries)
        if not os.path.exists(self.path+"\\"+self.titleOfTheSeries+"\\information.txt"):
            with open(self.path+"\\"+self.titleOfTheSeries+"\\information.txt", 'w') as datei:
                datei.write(self.url)
        self.path = self.path+"\\"+self.titleOfTheSeries


    def get_list(self):
        stream_element = self.htmlsoup.find(id='stream')
        li_elements = stream_element.find_all('li')
        for li in li_elements:
            a_element = li.find('a')
            if a_element:
                if "episode" not in str(a_element):
                    staff = Staffel("https://aniworld.to"+a_element.get('href'), self.path, self.titleOfTheSeries)
                    self.staffel.append(staff)
        return

    def correctString(self, string):
        ersetzte_string = ""
        ersetzungszeichen = "/\\:*?\"<>|"
        for char in string:
            if char in ersetzungszeichen:
                ersetzte_string += ' '
            else:
                ersetzte_string += char
        return ersetzte_string