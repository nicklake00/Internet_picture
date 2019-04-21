from datetime import datetime
import requests
from bs4 import BeautifulSoup
import itertools
import pymorphy2
import re

morph = pymorphy2.MorphAnalyzer()
state = []
nully = []
news = [[]]
d = {} 
#counter = 0

def get_html(url):
    response = requests.get(url)
    return response.text
 
 
def get_all_links(html): #, state, news):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('div', id = 'front_news_main_center').find_all('div', class_ = 'news-item')
    #print(tds)

    for td in tds:
        a = td.find('a').get('href')
        #print(a)
        new_url = 'https://www.baikal-daily.ru' + a

        get_page_data(get_html(new_url))

    return 0 #news

def get_page_data(html):
    #my_file = open("daily_pairs.txt", "a")

    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1', itemprop = 'name headline')
    text = soup.find('div', class_ = 'news-text')

    aptitle = str(title)[29:-5]

    before_aptext = str(text)[50:-6]

    #my_file.write(aptitle)
    #my_file.write('\n')

    while (before_aptext.find('<br/>') != -1):
        num1 = before_aptext.find('<br/>')

        str1 = before_aptext[:num1]
        str2 = before_aptext[num1 + 5:]
        before_aptext = str1 + str2

    while (before_aptext.find('<div>') != -1):
        num1 = before_aptext.find('<div>')

        str1 = before_aptext[:num1]
        str2 = before_aptext[num1 + 5:]
        before_aptext = str1 + str2

    while (before_aptext.find('</div>') != -1):
        num1 = before_aptext.find('</div>')

        str1 = before_aptext[:num1]
        str2 = before_aptext[num1 + 6:]
        before_aptext = str1 + str2

    while (before_aptext.find('<b>') != -1):
        num1 = before_aptext.find('<b>')

        str1 = before_aptext[:num1]
        str2 = before_aptext[num1 + 3:]
        before_aptext = str1 + str2

    while (before_aptext.find('</b>') != -1):
        num1 = before_aptext.find('</b>')

        str1 = before_aptext[:num1]
        str2 = before_aptext[num1 + 4:]
        before_aptext = str1 + str2

    s = set()
    new = []


    str1 = before_aptext.split()
    for i in str1: #data[0]:
        p = morph.parse(i)[0]
        l = p.tag.POS
        p = p.normal_form
        result = re.sub(r',' , '', p)
        result = re.sub(r'»', '', result)
        result = re.sub(r'«', '', result)
        result = re.sub(r'<br/>', '', result)
        result = re.sub(r'-', '', result)
        result = re.sub(r'–', '', result)
        result = re.sub(r'<b>', '', result)
        result = re.sub(r'</b>', '', result)
        result = re.sub(r'<div', '', result)
        result = re.sub(r'</div>', '', result)
        #result = re.sub(r'.', '', result)
        if (result.find('.') != -1):
            result = result[:-1]
        if (result.find(':') != -1):
            result = result[:-1]
        if (result.find('?') != -1):
            result = result[:-1]
        #print(result.find('.'))

        if ((l == 'NOUN') or (l == None)):
        #if ((l == 'VERB') or (l == None) or (l == 'INFN') or (l == 'PRTS') or (l == 'PRTF') or (l == 'GRND')):
        #if (l == 'ADJF' or l == 'ADJS' or l == 'ADVB' or l == None):
            if (result != '' and result != ' ' and result not in s):
                new.append(result)
                s.add(result)

    pairs = list(itertools.combinations(new, 2))
    for i in range(len(pairs)):
        if d.get(pairs[i]) == None:
            d[pairs[i]] = 1
        else:
            d[pairs[i]] += 1
    print(counter)
 
def main():
    page = 'https://www.baikal-daily.ru/news/20/?PAGEN_1='

    for i in range(1, 393):
        url = page + str(i)
        all_links = get_all_links(get_html(url))

    my_file = open("daily_pairs.txt", "a")
    for w in sorted(d, key=d.get, reverse=True):
        #print(w[0], ' ', d[w])
        if d[w] > 100:
            print("yahoo!")
            my_file.write(str(max(w[0], w[1])))
            my_file.write(' ')
            my_file.write(str(min(w[1], w[0])))
            my_file.write(' ')
            my_file.write(str(d[w]))
            my_file.write('\n')

    my_file.close()

if __name__ == '__main__':
    main()
