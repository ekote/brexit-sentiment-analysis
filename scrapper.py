from bs4 import BeautifulSoup
import requests
import pandas as pd

def getdata(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, features = "html.parser")
    h2s = soup.find(lambda elm: elm.name == "h2")
    name = ''
    party = ''
    try:
        for h2 in h2s:
            name = h2.a.text.strip()
            div = h2.find_next('div')
            party = div.find_next('strong').text.strip()
    except:
        print(url)
    return name, party

df = pd.read_csv('debates.csv')
df1 = pd.DataFrame(columns = ['url', 'name', 'party'])

urls = df.debate_politician_url.unique()
print(len(urls))
for url in urls:
    name, party = getdata(url)
    row = [url, name, party]
    print(row, len(df1))
    df1.loc[len(df1)] = row
df1.to_csv('names.csv', index=False)




