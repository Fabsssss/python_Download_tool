import os
from serie import Serie
from controll import Controll


class download:
    def __init__(self, url, path):
        self.path = path
        self.serie = Serie(url, path)
        

def entferne_und_gebe_doppelte_aus(dateipfad):
    try:
        with open(dateipfad, 'r') as datei:
            zeilen = datei.readlines()
        doppelte_zeilen = [zeile for zeile in zeilen if zeilen.count(zeile) > 1]
        if not doppelte_zeilen:
            print('Keine doppelten Zeilen gefunden.')
        else:
            print('Doppelte Zeilen:')
            for zeile in set(doppelte_zeilen):
                print(zeile.strip())
            bereinigte_zeilen = list(set(zeilen))
            with open(dateipfad, 'w') as datei:
                datei.writelines(bereinigte_zeilen)
            print(f'Doppelte Zeilen in {dateipfad} wurden entfernt.')
    except FileNotFoundError:
        print(f'Die Datei {dateipfad} wurde nicht gefunden.')


def entferne_string_aus_datei(dateipfad, zu_entfernender_string):
    with open(dateipfad, 'r') as datei:
        inhalt = datei.read()
    neuer_inhalt = inhalt.replace(zu_entfernender_string, '')
    with open(dateipfad, 'w') as datei:
        datei.write(neuer_inhalt)
    print("Link entfernt")



kontrollpfad = 'G:\\Serien\\Anime\\kontroll.txt'
dateipfad = 'G:\\Serien\\Anime\\serien.txt'
entferne_und_gebe_doppelte_aus(dateipfad)
with open(dateipfad, 'r') as datei:
    for zeile in datei:
        inhalt = (zeile.replace('\n','')).strip()
        d = Controll(kontrollpfad, str(inhalt))

with open(kontrollpfad, 'r') as datei:
    for zeile in datei:
        inhalt = (zeile.replace('\n','')).strip()
        d = download(str(inhalt), os.path.dirname(dateipfad))
        entferne_string_aus_datei(kontrollpfad, zeile)



