from bs4 import BeautifulSoup
import requests
import m3u8_To_MP4
import os
import time

class Episode:
    def __init__(self, url,path, filename):
        
        print("New Episode")
        self.path = path
        self.url = url
        self.filename = filename
        
        response = requests.get(self.url)
        if response.status_code == 200:
            self.htmlsoup = BeautifulSoup(response.text, "html.parser")
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)
            return
        
        
        
        self.downloadready = True
        self.episodenNummer = self.get_episodenNummer()
        self.episodentitel = self.get_titelofEpisode()
        self.german = self.get_german()

        
        self.finalFilename = ""
        self.downloadready = self.get_downloadready()
        
        if not self.downloadready:
            return
        
        self.downloadLink = self.get_downloadLink()

        self.download()



    def get_episodenNummer(self):
        active_links = self.htmlsoup.find_all('ul')
        for link in active_links:
            if "<strong>Episoden:</strong>" in str(link) or "<strong>Filme:</strong>" in str(link):
                active_links = link.find_all('a', class_='active')
                for link in active_links:
                    return link.text
    
    
    def get_titelofEpisode(self):
        h2_tags = self.htmlsoup.find_all('h2')
        for h2_tag in h2_tags:
            return h2_tag.text



    def get_german(self):                   
        element = self.htmlsoup.find(class_="changeLanguageBox")
        if element:
            if "German, Deutsch, Flagge, Sprache" in (str(element)):
                return True
            else:
                return False


    def get_downloadready(self):
        if self.german:
            self.finalFilename = (str(self.path+"\\"+self.correctString(self.filename)+"_"+self.correctString(self.episodenNummer)+"_"+self.correctString(str(self.episodentitel).replace("_"," ")) +"_"+"German.mp4").replace("\n",""))
            if os.path.exists(self.finalFilename):
                return False
            if os.path.exists((str(self.path+"\\"+self.correctString(self.filename)+"_"+self.correctString(self.episodenNummer)+"_"+self.correctString(str(self.episodentitel).replace("_"," ")) +"_"+"GermanSub.mp4").replace("\n",""))):
                os.remove((str(self.path+"\\"+self.correctString(self.filename)+"_"+self.correctString(self.episodenNummer)+"_"+self.correctString(str(self.episodentitel).replace("_"," ")) +"_"+"GermanSub.mp4").replace("\n","")))
        else:
            self.finalFilename = (str(self.path+"\\"+self.correctString(self.filename)+"_"+self.correctString(self.episodenNummer)+"_"+self.correctString(str(self.episodentitel).replace("_"," ")) +"_"+"GermanSub.mp4").replace("\n",""))
            if os.path.exists(self.finalFilename):
                return False
        print("DOWNLOAD: "+self.filename+" "+self.episodenNummer)
        return True
    



    def get_downloadLink(self):
        s = str(self.htmlsoup).split("\"")
        for a in s:
            if "/redirect/" in a:
                response = requests.get(("https://aniworld.to"+a))
                if not self.german:
                    response = requests.get(self.getRightDonwloadLink(response)) 
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    #print(soup)
                    res = (str(soup)).split("'")
                    for r in res:
                        if "m3u8" in r:
                            return r
                else:
                    print("Failed to retrieve the webpage. Status code:", response.status_code)
                    return
                

                
    def download(self):
        try:
            if self.downloadready:
                if not os.path.exists(self.finalFilename):
                    m3u8_To_MP4.multithread_download(self.downloadLink, self.finalFilename)
        except Exception as e:
            print(f"Unexpected error: {e}")


    def correctString(self, string):
        ersetzte_string = ""
        ersetzungszeichen = "/\\:*?\"<>|"
        for char in string:
            if char in ersetzungszeichen:
                ersetzte_string += ' '
            else:
                ersetzte_string += char
        return ersetzte_string
    

    def getRightDonwloadLink(self,string):
        div_element = self.htmlsoup.find('div', class_='changeLanguageBox')
        if div_element:
            img_count = len(div_element.find_all('img'))
            if img_count == 2:
                sp = str(self.htmlsoup).split("\"")
                list_of_re = []
                for s in sp:
                    if "/redirect/" in s:
                        list_of_re.append("https://aniworld.to"+s)
                return (list_of_re[int(len(list_of_re)/2)])
            else:
                sp = str(self.htmlsoup).split("\"")
                list_of_re = []
                for s in sp:
                    if "/redirect/" in s:
                        return "https://aniworld.to"+s
        return string

