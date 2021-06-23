#importando bibliotecas a serem utilizadas

from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

'''
o url de cada página de tabela de jogos é formado por duas partes, separadas pelo
código de cada temporada
'''

url_parte1="https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D="
url_parte2="&wherePlaying=-1&played=-1"

cod_temp={"20/21":"59",
               "19/20":"54",
               "18/19":"47",
               "17/18":"41",
               "16/17":"34",
               "15/16":"27",
               "14/15":"20",
               "13/14":"15",
               "12/13":"8",
               "11/12":"4",
               "10/11":"3",
               "09/10":"2",
               "08/10":"1"}

jogos_temp={"20/21":[],
               "19/20":[],
               "18/19":[],
               "17/18":[],
               "16/17":[],
               "15/16":[],
               "14/15":[],
               "13/14":[],
               "12/13":[],
               "11/12":[],
               "10/11":[],
               "09/10":[],
               "08/10":[]}

for temp in cod_temp:
    url="https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D="+cod_temp[temp]+"&wherePlaying=-1&played=-1"
    page=requests.get(url)
    soup=BeautifulSoup(page.text,'html.parser')
    for link in soup.find_all('a',href=True):
        if (("noticias" in link['href'] and re.search("/noticias/(.*)/$",link['href'])!=None) or ("partidas" in link['href'])) and link['href'] not in jogos_temp[temp]:
            jogos_temp[temp].append(link['href'])
        else:
            pass
print("Sucess")


