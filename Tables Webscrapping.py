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
               #"16/17":"34",
               "15/16":"27",
               "14/15":"20",
               "13/14":"15",
               "12/13":"8",
               "11/12":"4",
               "10/11":"3",
               "09/10":"2",
               "08/09":"1"}

jogos_temp={"20/21":[],
               "19/20":[],
               "18/19":[],
               "17/18":[],
               #"16/17":[],
               "15/16":[],
               "14/15":[],
               "13/14":[],
               "12/13":[],
               "11/12":[],
               "10/11":[],
               "09/10":[],
               "08/09":[]}

results_temp={"20/21":'',
               "19/20":'',
               "18/19":'',
               "17/18":'',
               #"16/17":'',
               "15/16":'',
               "14/15":'',
               "13/14":'',
               "12/13":'',
               "11/12":'',
               "10/11":'',
               "09/10":'',
               "08/09":''}

df_results= pd.DataFrame()

for temp in cod_temp:
    url="https://lnb.com.br/nbb/tabela-de-jogos/?season%5B%5D="+cod_temp[temp]+"&wherePlaying=-1&played=-1"
    page=requests.get(url)
    soup=BeautifulSoup(page.text,'html.parser')
    for link in soup.find_all('a',href=True):
        if (("noticias" in link['href'] and re.search("/noticias/(.*)/$",link['href'])!=None) or ("partidas" in link['href'])) and link['href'] not in jogos_temp[temp]:
            jogos_temp[temp].append(link['href'])
        else:
            pass
    dates=soup.find_all(class_="date_value show-for-medium")
    date=[i.text.replace("\n","")[0:10] for i in dates]
    time=[i.text.replace("\n","")[10:15] for i in dates]
    teams=soup.find_all(class_="team-shortname")
    results_home=soup.find_all(class_="home")
    results_away=soup.find_all(class_="away")
    results_home=[i.text for i in results_home][1::2]
    results_away=[i.text for i in results_away][1::2]
    home_teams=[]
    away_teams=[]
    index=0
    for team in teams:
        if index%2==0:
            home_teams.append(team.text)
        else:
            away_teams.append(team.text)
        index+=1
    df_temp = pd.DataFrame({'Season':temp,'Game Date':date,'Game Time':time,'Home Team':home_teams,
                   'Home Score':results_home,'Away Score':results_away,
                   'Away Team':away_teams,'Report Link':jogos_temp[temp]
                   })
    df_results=df_results.append(df_temp)
    
#Coleta de tabelas de Estatísticas

links=[]
df_results=df_results.reset_index(drop=True)

for item in df_results.index:
    links.append(df_results['Report Link'][item])

full_df= pd.DataFrame()
for url in links:
    try:
        page=requests.get(url)
        soup=BeautifulSoup(page.text,'html.parser')

        home_table=soup.find_all(class_="team_general_table tablesorter")
        away_table=soup.find_all(class_="team_two_table tablesorter")

    #essa parte temos que revisar! como pegar a tabela do time de casa e fora sem ser assim?
        try:
            home=home_table[0]
            away=away_table[0]
        except:
            home_table=soup.find_all(class_="stats_real_time_table_home")
            away_table=soup.find_all(class_="stats_real_time_table_away")
            home=home_table[0]
            away=away_table[0]

        results=[]
        for row in home.find_all('tr'):
            result=[]
            result.append("Home"+row.text.replace("\n\r\n",",").replace(" ","").replace("\n",","))
            results.append(result)
    

        for row in away.find_all('tr'):
            result=[]
            result.append("Away"+row.text.replace("\n\r\n",",").replace(" ","").replace("\n",","))
            results.append(result)
    
        df = pd.DataFrame(results,columns=['Full Data'])
        df['URL']=url
        full_df=full_df.append(df)
        print("Ok")
    except:
        print("Error->"+str(url))
        pass


full_df[['Home/Away','Nr.','Jogador','JO','Min','Pts','RD+RORT','AS','3P%','2P%','LL%','BR','TO','FC','FR','ER','EN','+/-','EF','TBD2']] = df['Full Data'].str.split(',',expand=True)
full_df = full_df.drop(columns=['TBD2','Full Data'])
full_df=full_df[(full_df['Nr.'] != 'Nr.')]
full_df=full_df.reset_index(drop=True)
full_df.to_csv("C:\\Users\\fcastro\\OneDrive - Digicorner\\TCC\\BRILHAMOS_v3.csv")
