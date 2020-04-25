import requests
from bs4 import BeautifulSoup
import os
import csv

base_url = 'https://www.kigalitoday.com/'


def get_news_links(page_url):
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    news_articles = soup.find_all('div', class_='item-container')
    # headlines_articles = soup.find_all('div', class_='middle-news-1')
    # top_news = soup.find_all('div', class_='topnews-1')
    links = []
    for article in news_articles:
        if article is None:
            continue
        link = article.find('a', class_='headline-image', href=True)
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


def next_page_url(base, count):
    return f'{base}/?debut_amakuruaheruka_fromrub_arts1={count}#pagination_amakuruaheruka_fromrub_arts1'


def fetch_as_much_links(base, page=1, limit=200, saveToFile=None):
    count = 0
    page = page
    links = []
    while count < limit:
        print(f'count is {count}, page is {page} and have {len(links)} links')
        if(page == 1):
            url = base
        else:
            url = next_page_url(base, count)
        print(f'fetching articles on page {page}')
        additional_links = get_news_links(url)
        if len(additional_links) < 1:
            break
        for link in additional_links:
            if link is None:
                continue
            links.append(link)
        count += len(additional_links)
        page += 1
    if(links):
        save_new_links_to_file(links, saveToFile)


def get_article_content(url, category='news'):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    text = ''
    if(soup.find('h1', class_='wsj-article-headline') is None):
        article_title = 'N/A'
    else:
        article_title = soup.find(
            'h1', class_='wsj-article-headline').getText()
    if(soup.find('div', class_='article-wrap') is None):
        text = ''
    else:
        article_paragraphs = soup.find(
            'div', class_='article-wrap').find_all('p')
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


business_articles = 'https://www.kigalitoday.com/ubukungu'
tech_articles = 'https://www.kigalitoday.com/ikoranabuhanga'
health_articles = 'https://www.kigalitoday.com/ubuzima'
education_articles = 'https://www.kigalitoday.com/uburezi'
# fetch_as_much_links(business_articles, 'kt_business_articles.txt')
# create_csv_file('kt_business_articles.txt',
#                 'kt_business_articles.csv', 'Business')
# fetch_as_much_links(tech_articles, 'kt_tech_articles.txt')
# create_csv_file('kt_tech_articles.txt',
#                 'kt_tech_articles.csv', 'Tech')
# fetch_as_much_links(health_articles, 6, 200, 'kt_health_articles.txt')
# create_csv_file('kt_health_articles.txt',
#                 'kt_health_articles.csv', 'Health')
fetch_as_much_links(education_articles, 1, 300, 'kt_education_articles.txt')
create_csv_file('kt_education_articles.txt',
                'kt_education_articles.csv', 'Education')
