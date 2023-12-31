from bs4 import BeautifulSoup
from episodenhulle import Episodenhulle
import requests
import m3u8_To_MP4
import os
import time

class Controll:
    def __init__(self, kontrollpfad, url):
        if self.alreadyinlist(url, kontrollpfad):
            print("bereits in liste")
            return
        self.kontrollpfad = kontrollpfad
        self.titleofserie = ""
        self.url = url
        self.breakup = False
        self.list_of_staffeln_url = self.staffeln_url()
        for a in self.list_of_staffeln_url:
            print(a)
            self.controll(a)
            if self.breakup:
                break

    
    def staffeln_url(self):
        list = []
        htmlsoup = ""
        response = requests.get(self.url)
        if response.status_code == 200:
            htmlsoup = BeautifulSoup(response.text, "html.parser")
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)
            return
        
        spanObjects = htmlsoup.find_all('h1')
        for h1 in spanObjects:
            self.titleofserie = (self.correctString(h1.text)).strip()
            break

        stream_element = htmlsoup.find(id='stream')
        li_elements = stream_element.find_all('li')
        for li in li_elements:
            a_element = li.find('a')
            if a_element:
                if "episode" not in str(a_element):
                    list.append("https://aniworld.to"+a_element.get('href'))
        return list

    def alreadyinlist(self, string,dateipfad):
        try:
            with open(dateipfad, 'r') as datei:
                inhalt = datei.read()
                if string in inhalt:
                    return True
                else:
                    return False
        except FileNotFoundError:
            print(f'Die Datei "{dateipfad}" wurde nicht gefunden.')
            return False
        except Exception as e:
            print(f'Ein Fehler ist aufgetreten: {e}')
            return False
    
    def correctString(self, string):
        ersetzte_string = ""
        ersetzungszeichen = "/\\:*?\"<>|"
        for char in string:
            if char in ersetzungszeichen:
                ersetzte_string += ' '
            else:
                ersetzte_string += char
        return ersetzte_string




    def controll(self, url):
        htmlsoup = ""
        response = requests.get(url)
        if response.status_code == 200:
            htmlsoup = BeautifulSoup(response.text, "html.parser")
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)
            return
        
        sta = ""
        active_links = htmlsoup.find_all('a', class_='active')
        for link in active_links:
            sta = link.text
            if "Film" not in sta:
                sta = "Staffel "+sta
            break
                

        list_of_episodehulle = []
        episode_elements = htmlsoup.find_all(attrs={'itemprop': 'episode'})
        for episode in episode_elements:
            if "Deutsch/German" in str(episode):
                e = Episodenhulle("test",episode.get('data-episode-season-id'),True)
                list_of_episodehulle.append(e)
            else:
                e = Episodenhulle("test",episode.get('data-episode-season-id'),False)
                list_of_episodehulle.append(e)
        print(len(list_of_episodehulle))


        if os.path.exists(os.path.dirname(self.kontrollpfad)+"\\"+self.titleofserie+"\\"+sta):
            filenames = os.listdir(os.path.dirname(self.kontrollpfad)+"\\"+self.titleofserie+"\\"+sta)
            filenames = [filename for filename in filenames if os.path.isfile(os.path.join(os.path.dirname(self.kontrollpfad)+"\\"+self.titleofserie+"\\"+sta, filename))]
            print(len(filenames))

            if len(filenames) > len(list_of_episodehulle):
                with open(os.path.dirname(self.kontrollpfad)+"\\"+"Doppelte Folgen.txt","a+") as datei:
                    datei.write(self.url+"\n")
                    print("Doppelte folge")
                    self.breakup = True
            if len(filenames) < len(list_of_episodehulle):
                with open(self.kontrollpfad,"a+") as datei:
                    datei.write(self.url+"\n")
                    print("folgen nicht vorhanden")
                    self.breakup = True
        else:
            with open(self.kontrollpfad,"a+") as datei:
                datei.write(self.url+"\n")
                print("Staffel nicht gefunden")
                self.breakup = True





        return 





        filenames = os.listdir(self.path)
        #print(len(filenames))
        filenames = [filename for filename in filenames if os.path.isfile(os.path.join(self.path, filename))]
        for filename in filenames:
            split = str(filename).split("_")
            print(split[2])
            if "GermanSub" in split[4]:
                e = Episodenhulle(split[1],split[2],False)
                list_of_episodehulle.append(e)
            else:
                e = Episodenhulle(split[1],split[2],True)
                list_of_episodehulle.append(e)
            print(str(list_of_episodehulle[-1]))

        
        return





        #print(self.filename)
        #print("Number of elements:", len(episode_elements))
        for episode in episode_elements:
            if "Deutsch/German" in str(episode):
                e = Episodenhulle(self.staffelName,episode.get('data-episode-season-id'),True)
                list_of_episodehulle.append(e)
            else:
                e = Episodenhulle(self.staffelName,episode.get('data-episode-season-id'),False)
                list_of_episodehulle.append(e)
            print(str(list_of_episodehulle[-1]))
        




        return list_of_episodehulle



