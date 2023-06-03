import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import os
import tabula
import warnings

START_DATE = '02/01/1992'
URL = 'https://www.bolsasymercados.es/'
EXT = 'bme-exchange/en/Indices/Ibex/Historical-Constituents'
FULL_URL = URL+EXT

request = requests.get(FULL_URL)
response = request.content
soup  = BeautifulSoup(response,features="html.parser")

files = soup.find_all('a', attrs={'class':'pdf'})

file_ext = files[0]['href']
full_file_url = URL+file_ext
request = requests.get(full_file_url)
response = request.content


df = tabula.read_pdf(full_file_url, pages='all')
df_0 = df[0].iloc[2:]
df_0.fillna('', inplace=True)
df_0.rename(columns={'Revisión / Review': 'Fecha'}, inplace=True)
df_0['Inclusiones'] = df_0['Unnamed: 0'] + ' ' + df_0['Unnamed: 1'] + ' ' + df_0['Unnamed: 2']
df_0['Exclusiones'] = df_0['Unnamed: 3'] + ' ' + df_0['Unnamed: 4'] + ' ' + df_0['Unnamed: 5']
df_0[['Inclusiones','Exclusiones']] = df_0[['Inclusiones','Exclusiones']].apply(lambda x: x.str.strip())
df_0.drop(['Unnamed: 0','Unnamed: 1','Unnamed: 2','Unnamed: 3','Unnamed: 4','Unnamed: 5'], axis=1, inplace=True)
df_0[['index','Fecha']] = df_0['Fecha'].str.split(' ', expand=True)
df_0.drop('index', axis=1, inplace=True)
df_inclusiones = (df_0
 .assign(Inclusiones=df_0['Inclusiones'].str.split())
 .explode('Inclusiones')
 .drop('Exclusiones',axis=1)
)
df_exclusiones = (df_0
 .assign(Exclusiones=df_0['Exclusiones'].str.split())
 .explode('Exclusiones')
 .drop('Inclusiones',axis=1)
)
print(df_inclusiones,df_exclusiones)