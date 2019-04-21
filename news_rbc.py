from datetime import datetime
import requests
from bs4 import BeautifulSoup
 
state = []
nully = []
news = [[]] 

def get_html(url):
    response = requests.get(url)
    return response.text
 
 
def get_all_links(html, state, news):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('div', class_ ='l-row g-overflow js-search-container').find_all('div', class_='search-item js-search-item')

    for td in tds:
        a = td.find('a', class_='search-item__link').get('href')
        state = []
        get_page_data(get_html(a), state, news)

    return news

def get_page_data(html, state, news):
    my_file = open("rbc.txt", "a")
    my_file2 = open("rbc_2.txt", "a")
    my_file3 = open("rbc_3.txt", "a")
    aptag = ''
    apnewt = ''
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('div', class_ = 'article__header__title')

    aptitle = str(title)[86:-14]
    state.append(aptitle)
    my_file.write(aptitle)
    my_file.write(' ')

    header = soup.find('div', class_ = 'article__header__info-block')

    theme = header.find('a', class_ = 'article__header__category')
    time = header.find('span', class_ = 'article__header__date')

    tags = soup.find('div', class_ = 'article__tags').find_all('a', class_ = 'article__tags__link')
    text = soup.find('div', class_ = 'l-col-center-590 article__content').find_all('p')
    #print(text)
    
    l1 = str(theme).find('Section')
    l2 = str(time).find('">')
    l3 = str(tags[0]).find('">')

    #print(str(theme)[l1 + 9:-4])
    #print(str(time)[l2 + 2:-7])
    #print(str(tags[0])[l3 + 2: -4])

    taggy = str(tags[0])[l3 + 2: -4]
    aptag += taggy

    aptheme = str(theme)[l1 + 9:-4]
    aptime = str(time)[l2 + 2:-7]
    state.append(aptheme)
    state.append(aptime)
    print(aptime, '\n')

    my_file2.write(aptheme)
    my_file2.write('\n\n')

    for i in range(1, len(tags)):
        l4 = str(tags[i]).find('">')
        taggy = str(tags[i])[l4 + 4: -4]
        aptag += ', '
        aptag += taggy
        #print(str(tags[i])[l4 + 4: -4])

    state.append(aptag)
    my_file3.write(aptag)
    my_file3.write('\n\n')
        
    for t in text:
        newt = (str(t)[3:-4])
        while (newt.find('<a') != -1) :
            num1 = newt.find('<a')
            num2 = newt.find('</a>')
            numm = newt.find('">')
            word = newt[numm + 2:num2]
            str1 = newt[:num1]
            str2 = newt[num2 + 4:]
            
            newt = str1 + word + str2
        #print(newt)
        apnewt += newt
        apnewt += '\n'
        my_file.write(newt)
        my_file.write(' ')
    
    state.append(apnewt)
    news.append(state)
    my_file.close()
    my_file2.close()
    my_file3.close()

    state = []
    return 0
 

 
def main():
    #start = datetime.now()
    state = []
    nully = []
    news = [] 


    url = 'https://www.rbc.ru/tags/?tag=%D0%91%D1%83%D1%80%D1%8F%D1%82%D0%B8%D1%8F'
    all_links = get_all_links(get_html(url), state, news)

    for i in range(len(all_links)):
        for j in range(len(all_links[i])):
            print(all_links[i][j], '\n')
        print('\n\n')
 
if __name__ == '__main__':
    main()
