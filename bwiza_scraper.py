import requests
from bs4 import BeautifulSoup
import os
import csv

base_url = 'https://bwiza.com/'

url = "http://www.amazon.com/dp/" + 'B004CNH98C'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def get_news_links(page_url):
    page = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    news_articles = soup.find_all('div', class_='post-header')
    # headlines_articles = soup.find_all('div', class_='middle-news-1')
    # top_news = soup.find_all('div', class_='topnews-1')
    links = []
    for article in news_articles:
        if article is None:
            continue
        link = article.find('a', href=True)
        if link['href'].startswith('http') or link['href'].startswith('https'):
            links.append(link['href'])
        else:
            links.append(base_url+link['href'])
    return links


def save_new_links_to_file(links=None, fileName=None):
    new_articles_links = []
    with open(fileName, 'w+') as fl:
        old_news_links = fl.readlines()

    links = [link.strip() for link in links]
    old_news_links = [link.strip() for link in old_news_links]

    for link in links:
        if link not in old_news_links:
            new_articles_links.append(link)

    with open(fileName, 'a+') as fl:
        for link in new_articles_links:
            if link is None:
                continue
            fl.write(link+'\n')


def next_page_url(base, category, count):
    return f'{base}&debut_articles={count}#pagination_articles'


def fetch_as_much_links(base, category, limit=100, saveToFile=None):
    index = 0
    count = 0
    page = 1
    links = []
    while count < limit:
        print(f'count is {count}, page is {page} and have {len(links)} links')
        if(page == 1):
            url = base
        else:
            url = next_page_url(base, category, index)
        # print(f'fetching articles on page {page}')
        print(f'{url}')
        additional_links = get_news_links(url)
        if len(additional_links) < 1:
            break
        for link in additional_links:
            if link is None:
                continue
            links.append(link)
        count += len(additional_links)
        index += 10
        page += 1
    if(links):
        save_new_links_to_file(links, saveToFile)


def get_article_content(url, category='news'):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    text = ''
    if(soup.find('h2', class_='post-detail-title') is None):
        article_title = 'N/A'
    else:
        article_title = soup.find(
            'h2', class_='post-detail-title').getText()
    if(soup.find('div', class_='post-content') is None):
        text = ''
    else:
        article_paragraphs = soup.find(
            'div', class_='post-content').find_all('p')
        for p in article_paragraphs:
            text += p.getText() + '\n'
    return {'Title': article_title, 'Body': text, 'Url': url, 'Category': category}


def create_csv_file(fileName=None, saveTo=None, category=None):
    # initialize articles csv file
    columns = ['Title', 'Body', 'Url', 'Category']
    urls_in_file = []
    empty_articles = []
    if(os.path.isfile(saveTo)):
        with open(saveTo, 'r') as cfile:
            reader = csv.DictReader(cfile, delimiter=",")
            for row in reader:
                if row['Title'] == 'N/A':
                    empty_articles.append(row['Url'])
                urls_in_file.append(row['Url'])
        urls_in_file = [link.strip() for link in urls_in_file]
        empty_articles = [link.strip() for link in empty_articles]
    # get links
    with open(fileName, 'r') as file:
        new_links = file.readlines()
    new_links = [link.strip() for link in new_links]
    count = 0
    for link in new_links:
        if link in urls_in_file and link not in empty_articles:
            count += 1
            continue
        else:
            print(f'Article {count} is downloading...')
            content = get_article_content(link, category)
            try:
                with open(saveTo, 'a+', newline='') as cfile:
                    writer = csv.DictWriter(cfile, fieldnames=columns)
                    if os.stat(saveTo).st_size == 0:
                        writer.writeheader()
                    writer.writerow(content)
                    count += 1
            except IOError:
                print("I/O Error")


politics_articles = 'https://bwiza.com/?-politiki-'
# fetch_as_much_links(politics_articles, 'politiki',
#                     200, 'bwiza_politics_articles.txt')
# ent_articles = 'http://umuryango.rw/imyidagaduro'
# get_article_content(
#     'https://bwiza.com/?kigali-leo-mugesera-yanze-kuburanishwa-n-039-umucamanza-avuga-ko-amwanga')
# # get_news_links('http://umuryango.rw/imyidagaduro/')
# # fetch_as_much_links(ent_articles, 200, 'umuryango_ent_articles.txt')
create_csv_file('bwiza_politics_articles.txt',
                'bwiza_politics_articles.csv', 'Politics')
