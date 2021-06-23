from bs4 import BeautifulSoup
import pandas as pd
import requests

url="https://lnb.com.br/noticias/flamengo-86-x-79-unifacisa/"

page=requests.get(url)
soup=BeautifulSoup(page.text,'html.parser')
table=soup.find_all('table')

home=table[0]
away=table[5]

results=[]
for row in home.find_all('tr'):
    result=[]
    result.append(row.text.replace("\n\r\n",",").replace(" ","").replace("\n",","))
    results.append(result)
    
df = pd.DataFrame(results,columns=['Full Data'])
df[['TBD','Nr.','Jogador','JO','Min','Pts','RD+RORT','AS','3P%','2P%','LL%','BR','TO','FC','FR','ER','EN','+/-','EF','TBD2']] = df['Full Data'].str.split(',',expand=True)
df = df.drop(columns=['TBD', 'TBD2','Full Data'])
df = df.iloc[1:]
