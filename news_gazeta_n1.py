from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_html(url):
    response = requests.get(url)
    return response.text
 
 
def get_all_links(html): #, state, news):
    my_file = open('gazeta_tags.txt', 'a')
    my_file1 = open('gazeta_n1.txt', 'a')
    soup = BeautifulSoup(html, 'lxml')

    title = soup.find('h1')
    aftertitle = soup.find('div', class_ = 'preview-text')
    text = soup.find('div', class_ ='detail-text')

    try:
        tags = soup.find('div', class_='news-tags').find_all('a')
    except:
        tags = ''
    #tags = soup.find('div', class_ = 'news-tags').find_all('a')
    time = soup.find('span', class_ = 'news-date-time')

    for i in tags:
        tag = str(i)
        l1 = tag.find('">')
        tag = tag[l1 + 2:-4]
        #print(tag)
        my_file.write(tag)
        my_file.write('\n')

    aptime = str(time)[29:-7]
    #aptags = str(tags)[55:-11]

    apaftertitle = str(aftertitle)[35:-16]
    aptitle = str(title)[4:-6]
 
    my_file1.write(aptitle)
    my_file1.write('\n')
    my_file1.write(apaftertitle)
    my_file1.write('\n')
    my_file1.write(str(text))
    my_file1.write('\n')
    my_file1.close()
    my_file.close()

    return 0
 
def main():
    page = 'https://gazeta-n1.ru/news/' # 60143/ - 73269/
    #start = datetime.now()
    #state = []
    #nully = []
    #news = [] 

    for i in range(60143, 73269):#, 230):
        url = page + str(i) + '/'
        all_links = get_all_links(get_html(url)) # state, news)
        print(i)
        #url = page + '60143' + '/'
        #all_links = get_all_links(get_html(url))

 
if __name__ == '__main__':
    main()
