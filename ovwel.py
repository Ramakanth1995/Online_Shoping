import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
Vulnerability = []
Published_Date = []
Severity = []

page_count_number = True
page_count = 1

while page_count_number == True:

#for page_count in range(0,100):

    URL = f"https://www.rapid7.com/db/?q=&type=nexpose&page={page_count}"
    req = requests.get(URL)
    #print(req)
    soup = bs(req.text, 'html.parser')
    # print(soup)

    titles = soup.find_all('div', attrs={'class', 'resultblock__info-title'})  # resultblock__info active

    titles2 = soup.find_all('div', attrs={'class', 'resultblock__info-meta'})

    if not titles:
        page_count_number = False

    for i in range(len(titles)):
        s = "".join(titles[i].text.split())
        Vulnerability.append(s)

    for i in range(len(titles2)):
        s = "".join(titles2[i].text.split())
        x = s.replace('|', ' ').split()
        Published_Date.append(x[0])
        Severity.append(x[1])

    page_count = page_count+1
    print('page_count:',page_count)



df = pd.DataFrame({'Vulnerability,':Vulnerability,
                   'Published_Date':Published_Date,'Severity':Severity})

writer = ExcelWriter('Pandas-Example2.xlsx')

df.to_excel(writer,'Sheet1',index=False)

writer.save()

print('Successfully data loaded in to Excel Sheet')