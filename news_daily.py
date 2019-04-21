from datetime import datetime
import requests
from bs4 import BeautifulSoup
 
state = []
nully = []
news = [[]] 

def get_html(url):
    response = requests.get(url)
    return response.text
 
 
def get_all_links(html):
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
    my_file = open("daily.txt", "a")
    my_file2 = open("daily_2.txt", "a")

    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1', itemprop = 'name headline')
    text = soup.find('div', class_ = 'news-text')
    theme = soup.find('span', class_ = 'news-section')
    time = soup.find('span', class_ = 'news-date-time')
    tags = soup.find('div', class_ = 'news-tags')

    aptitle = str(title)[29:-5]
    aptheme = str(theme)[47:-12]

    before_aptext = str(text)[50:-6]

    l1 = str(time).find('Published')
    aptime = str(time)[l1 + 11:-14]

    l2 = str(tags).find('tags=')
    helper = str(tags)[l2 + 5:]
    l3 = helper.find('">')
    aptags = helper[:l3]

    my_file2.write(aptags)
    my_file2.write('\n')

    my_file.write(aptitle)
    my_file.write('\n')

    print(aptime, '\n')
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
        

    my_file.write(before_aptext)
    my_file.write('\n\n')
    my_file.close()
    my_file2.close()
    
 
def main():
    page = 'https://www.baikal-daily.ru/news/20/?PAGEN_1='
    #start = datetime.now()
    #state = []
    #nully = []
    #news = [] 

    for i in range(1, 393):
        url = page + str(i)
        all_links = get_all_links(get_html(url)) # state, news)

if __name__ == '__main__':
    main()
