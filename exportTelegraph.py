import requests
import re
from bs4 import BeautifulSoup


def exportEvents():
    try:
        string = ""

        page1 = requests.get('https://telegra.ph/eventos-07-24')
        soup1 = BeautifulSoup(page1.text, 'html.parser')

        j = 0
        for content in soup1.find_all(['p', 'h3', 'h4', 'a']):

            if content.text == "":
                pass
            elif len(content.text.strip()) < 40:
                title = content.text
                j = 1
            elif len(content.text.strip()) == 40 and j == 1:
                ids = content.text
                string += str((title + "\n" + ids + "\n"))
                j = 0

            contenido = ((string.replace(u'\xa0', u' ')).strip())
        #print(contenido)

    except Exception as e:
        print("exportEvents : ERROR :", e)

    if contenido != "":
        print("exportEvents : INFO : eventos importados de Telegraph")
    else:
        print("exportEvents : INFO : no hay eventos en Telegraph")

    with open("caches/eventos telegraph.txt", "w") as f:
        f.write(contenido)
        print("exportEvents : OK : eventos telegraph exportados al disco")
        f.close()

    return contenido


def exportExtras():
    try:
        string = ""

        page2 = requests.get('https://telegra.ph/canales-07-24-4')
        soup2 = BeautifulSoup(page2.text, 'html.parser')

        j = 0
        for content in soup2.find_all(['p', 'h3', 'h4', 'a']):

            if content.text == "":
                pass
            elif len(content.text.strip()) < 40:
                title = content.text
                j = 1
            elif len(content.text.strip()) == 40 and j == 1:
                ids = content.text
                string += str((title + "\n" + ids + "\n"))
                j = 0
        
        contenido = ((string.replace(u'\xa0', u' ')).strip())
        print(contenido)

    except Exception as e:
        print("exportExtras : ERROR :", e)

    if contenido != "":
        print("exportExtras : INFO : extras importados de Telegraph")
    else:
        print("exportExtras : INFO : no hay extras en Telegraph")

    with open("caches/extras telegraph.txt", "w") as f:
        f.write(contenido)
        print("exportExtras : OK : extras telegraph exportados al disco")
        f.close()

    return contenido


def exportMisCanales():
    try:
        string = ""

        page3 = requests.get('https://telegra.ph/my-07-27-5')
        soup3 = BeautifulSoup(page3.text, 'html.parser')

        j = 0
        for content in soup3.find_all(['p', 'h3', 'h4', 'a']):

            if content.text == "":
                pass
            elif len(content.text.strip()) < 40:
                title = content.text
                j = 1
            elif len(content.text.strip()) == 40 and j == 1:
                ids = content.text
                string += str((title + "\n" + ids + "\n"))
                j = 0

        contenido = ((string.replace(u'\xa0', u' ')).strip())
        #print(contenido)

    except Exception as e:
        print("exportMisCanales : ERROR :", e)

    if contenido != "":
        print("exportMisCanales : INFO : eventos importados de Telegraph")
    else:
        print("exportMisCanales : INFO : no hay eventos en Telegraph")

    with open("caches/mis canales telegraph.txt", "w") as f:
        f.write(contenido)
        print("exportMisCanales : OK : mis canales telegraph exportados al disco")
        f.close()

    return contenido     




"""
if __name__ == "__main__": 
    exportEvents()
    exportExtras()
    exportMisCanales()
"""
