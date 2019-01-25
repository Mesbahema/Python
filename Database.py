import re
import requests
from bs4 import BeautifulSoup
table = {1776: 48,  # 0 
         1777: 49,  # 1
         1778: 50,  # 2
         1779: 51,  # 3
         1780: 52,  # 4
         1781: 53,  # 5
         1782: 54,  # 6
         1783: 55,  # 7
         1784: 56,  # 8
         1785: 57}  # 9
DATA = []
def filter_comma(string):
    s = ''
    s1 = ''
    s2 = ''
    y = 0
    for i in range(len(string)):
        if string[i] == '،':
          y = 1  
        elif y == 0:
            s = s + string[i]
        elif y == 1 :
            s1 = s1 + string[i]
    if s1 == '':
        return s
    else:
        for i in range(1,len(s1)):
            s2 = s2 + s1[i]
        return s2
page = 10
for j in range(1,page + 1):
    r = requests.get('https://www.ihome.ir/خرید-فروش/املاک/ایران/%i'%j)
    string = str(r)
    if re.search(r'200',string) == None: break
    soup = BeautifulSoup(r.text,'html.parser')
    id_ = soup.find_all("li", "blocks ls-super-hot ls-mn sticky_ads")
    data = soup.find_all("div","sh-content left")
    data = list(map(lambda x: str(x),data))
    id_ = list(map(lambda x: str(x),id_))
    id_ = list(map(lambda x: int(re.findall(r'(\d+)\.html',x)[0]),id_))
    data = list(map(lambda x: u'%s'%x.translate(table),data))
    price = list(map(lambda x: re.findall(r'\s(\S+)<span class="currency">',x)[0],data))
    price = list(map(lambda x: int(x.replace(',','')),price))
    beds = list(map(lambda x: re.findall(r'<i class="ihome-bed"><\/i>\n\s+(\d+)',x),data))
    area = list(map(lambda x: int(re.findall(r'<i class="ihome-arrows"><\/i>\n\D+(\d+)',x)[0]),data))
    location = list(map(lambda x: re.findall(r'<div class="location ">\n<span>(.+)<\/span>',x),data))
    check_list = []
    for i in range(len(beds)):
        if beds[i] == []: check_list.append(i)
    check_list.sort(reverse = True)
    for i in check_list:
        del id_[i],price[i],location[i],area[i]
    beds = list(filter(lambda x: x != [],beds))
    beds = list(map(lambda x: int(x[0]),beds))
    check_list = []
    for i in range(len(location)):
        if location[i] == []: check_list.append(i)
    check_list.sort(reverse = True)
    for i in check_list:
        del id_[i],price[i],beds[i],area[i]
    location = list(filter(lambda x: x != [],location))
    location = list(map(lambda x: x[0],location))
    location = list(map(lambda x: filter_comma(x),location))
    print('From page %i, %i data are extracted.'%(j,len(id_)))
    for i in range(len(id_)):
        temp = []
        temp.append(id_[i])
        temp.append(area[i])
        temp.append(beds[i])
        temp.append(location[i])
        temp.append(price[i])
        DATA.append(temp)
import mysql.connector
cnx = mysql.connector.connect(user='root', password='mesbah',host='127.0.0.1',database='data')
cursor = cnx.cursor()
query = 'SELECT * FROM houses;'
cursor.execute(query)
DATA_1 = list(cursor)
DATA_1 = list(map(lambda x: list(x),DATA_1))
check_list = []
for i in range(len(DATA_1)):
    for j in range(len(DATA)):
        if DATA_1[i][0] == DATA[j][0]: check_list.append(j)
check_list.sort(reverse = True)
for i in check_list:
    del DATA[i]
cursor = cnx.cursor()
for i in range(len(DATA)):
    cursor.execute('INSERT INTO houses VALUES(\'%i\',\'%i\',\'%i\',\'%s\',\'%i\')'%(DATA[i][0],DATA[i][1],DATA[i][2],DATA[i][3],DATA[i][4]))
    cnx.commit()
cnx.close()
