import sys
from bs4 import BeautifulSoup
from torpy.http.requests import TorRequests


def scraper():
    lista = ""
    print('scraper : INFO : requesting elcano...', flush=True)

    with open('caches/site.txt', 'r') as f:
        line = f.read()
        link = line.strip()
        f.close()

    try:
        with TorRequests() as tor_requests:
            with tor_requests.get_session() as sess:
                grab = sess.get(link)
                print(grab)
    except:
        # El error de la librería torpy no tiene importancia y no afecta a futuros runs
        print("scraper : ERROR : torpy linea 22")
        #sys.exit(1)

    soup = BeautifulSoup(grab.text, 'html.parser')
    for enlace in soup.find_all('a'):
        acelink = enlace.get('href')
        canal = enlace.text

        if not str(acelink).startswith("acestream://") or canal == "aquÃ­":
            pass
        else:
            link = str(acelink).replace("acestream://", "")
            lista += str((canal + "\n" + link + "\n"))
            contenido = ((lista.replace(u'\xa0', u' ')).strip())

    if contenido != "":
        print("scraper : OK : channels retrieved")
        write_cache(contenido)
    else:
        print("scraper : INFO : could not access elcano")
    

def write_cache(contenido):
    with open("caches/cachedList.txt", "w") as cachedlist:
        cachedlist.write(contenido)
        cachedlist.close()
        print("scraper : INFO : elcano cached")

"""
def read_cache():
    with open('caches/cachedList.txt', 'r') as cachedlist:
        contenido = cachedlist.read()
        cachedlist.close()
        print("scrap: INFO: returning elcano cached List")
        #return (contenido)
"""

scraper()
