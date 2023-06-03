import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import os
import PyPDF2
import warnings
import io


URL = 'https://en.wikipedia.org/wiki/DAX'


request = requests.get(URL)
response = request.content
df_list = pd.read_html(request.text) # this parses all the tables in webpages to a list
df = df_list[6].iloc[:,]

# soup  = BeautifulSoup(response,features="html.parser")

# dax_constituents = soup.find_all('table', attrs={'class':'wikitable'})[4]
# for row in dax_constituents.find_all('tr')[1:x]:
#     col = row.find_all('td')

print(df)


