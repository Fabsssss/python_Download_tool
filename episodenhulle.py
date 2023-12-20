from bs4 import BeautifulSoup
import requests
import m3u8_To_MP4
import os
import time

class Episodenhulle:
    def __init__(self, staffel,episode, german):
        self.staffel = staffel
        self.episode = episode
        self.german = german
        

    # Getter-Methode für staffel
    def get_staffel(self):
        return self._staffel

    # Setter-Methode für staffel
    def set_staffel(self, staffel):
        self._staffel = staffel

    # Getter-Methode für episode
    def get_episode(self):
        return self._episode

    # Setter-Methode für episode
    def set_episode(self, episode):
        self._episode = episode

    # Getter-Methode für german
    def get_german(self):
        return self._german

    # Setter-Methode für german
    def set_german(self, german):
        self._german = german


    def __str__(self):
        return f"Staffel: {self.staffel} Folge: {self.episode} German: {str(self.german)}"
