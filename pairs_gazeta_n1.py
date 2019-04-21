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

def get_html(url):
    response = requests.get(url)
    return response.text
 
 
def get_all_links(html): #, state, news):
    soup = BeautifulSoup(html, 'lxml')

    title = soup.find('h1')
    aftertitle = soup.find('div', class_ = 'preview-text')#.find_all('div', class_ = 'news-item')
    text = soup.find('div', class_ ='detail-text')

    apaftertitle = str(aftertitle)[35:-16]
    aptitle = str(title)[4:-6]

    before_aptext = str(str(title) + ' ' + str(aptitle) + ' ' + str(text))

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

def main():
    page = 'https://gazeta-n1.ru/news/' # 60143/ - 73269/

    for i in range(60143, 73269):#, 230):
        print(i - 60142, end='\n')
        url = page + str(i) + '/'
        all_links = get_all_links(get_html(url)) # state, news)
        print(i)    

    my_file = open("gazeta_n1_pairs.txt", "a")
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
