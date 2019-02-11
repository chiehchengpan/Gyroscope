import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd


today = datetime.datetime.now()
df = pd.DataFrame(columns=('活動', '時間', '地點', '賽程', '主辦單位', '活動連結'))


html = BeautifulSoup(requests.get('http://www.taipeimarathon.org.tw/contest.aspx').text)
for i in html.find_all('tr')[2:]:

    # 找出活動日期, 超過今天的就不要
    event_month = int(i.find_all('td')[3].text.strip().split(' ')[0].split('/')[0])
    event_date = int(i.find_all('td')[3].text.strip().split(' ')[0].split('/')[1])

    if event_month < int(today.month):
        continue
    elif event_date < int(today.day):
        continue

    try:
        # 可能有多種賽程, 用空字串累加
        s = ""
        for j in i.find_all('td')[5].find_all('button'):
            s = s + (j.text + '/')
        # print('活動名字:', i.find_all('td')[1].text.strip())
        # print('活動時間:', i.find_all('td')[3].text.strip())
        # print('活動地點:', i.find_all('td')[4].text)
        # print('賽程種類:', s)
        # print('主辦單位:', i.find_all('td')[6].text)
        # print('活動連結:', i.find_all('td')[1].find('a')['href'])

        # 連結有些抓不到, 抓的到就抓, 抓不到就是原本設定的空值
        dummy = ""
        dummy = i.find_all('td')[1].find('a')['href']
    except TypeError:
        pass

    # 用pd.series把要的資訊append到Dataframe裡面
    ser = pd.Series({'活動': i.find_all('td')[1].text.strip(),
                     '時間': i.find_all('td')[3].text.strip(),
                     '地點': i.find_all('td')[4].text,
                     '賽程': s,
                     '主辦單位': i.find_all('td')[6].text,
                     '活動連結': dummy})
    df = df.append(ser, ignore_index=True)

df.to_csv('marathon_info.csv', encoding='utf-8', index=False)