import requests
from bs4 import BeautifulSoup
import csv

landing_page_url = 'https://m.igihe.com/'


def get_news_links(page_url):
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    news_articles = soup.find_all('div', class_='middle-news')
    # headlines_articles = soup.find_all('div', class_='middle-news-1')
    # top_news = soup.find_all('div', class_='topnews-1')
    # all_articles = news_articles + headlines_articles + top_news
    links = []
    for article in news_articles:
        if article is None:
            continue
        link = article.find('a', href=True)
        if link['href'].startswith('http') or link['href'].startswith('https'):
            links.append(link['href'])
        else:
            links.append(landing_page_url+link['href'])
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


def get_igihe_article_content(url, category='news'):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    text = ''
    if(soup.find('div', class_='inkuru-section') is None):
        article_title = 'N/A'
    else:
        article_title = soup.find(
            'div', class_='inkuru-section').find('h1').getText()
    if(soup.find('div', class_='inkuru-title-2') is None):
        text = ''
    else:
        article_paragraphs = soup.find(
            'div', class_='inkuru-title-2').find_all('p')
        for p in article_paragraphs:
            text += p.getText() + '\n'
    return {'Title': article_title, 'Body': text, 'Url': url, 'Category': category}


def next_page_url(base, count):
    return f'{base}/?debut_articles_recents={count}#pagination_articles_recents'


def fetch_as_much_links(base, limit=100, saveToFile=None):
    index = 0
    count = 0
    page = 1
    links = []
    while count < limit:
        print(f'count is {count}, page is {page} and have {len(links)} links')
        if(page == 1):
            url = base
        else:
            url = next_page_url(base, index)
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
        index += 50
        page += 1
    if(links):
        save_new_links_to_file(links, saveToFile)


business_articles = 'https://m.igihe.com/ubukungu'
tech_articles = 'https://m.igihe.com/ikoranabuhanga'
# sport_articles = get_news_links('https://m.igihe.com/imikino/')
# health_articles = get_news_links('https://m.igihe.com/imikino/')
# health_articles = get_news_links('https://m.igihe.com/imikino/')
# ent_articles = get_news_links('https://m.igihe.com/imyidagaduro/')
# politics_articles = 'https://m.igihe.com/politiki'
# env_articles = 'https://m.igihe.com/ibidukikije'
# gospel_articles = 'https://m.igihe.com/iyobokamana'
# tourism_articles = 'https://m.igihe.com/ubukerarugendo'
# opinion_articles = 'https://m.igihe.com/twinigure'
diaspora_articles = 'https://m.igihe.com/diaspora'
culture_articles = 'https://m.igihe.com/umuco'
politics_articles = 'https://m.igihe.com/politiki'

# fetch_as_much_links(politics_articles, 200, 'igihe_politics_articles.txt')
# fetch_as_much_links(business_articles, 200, 'igihe_business_articles.txt')
# fetch_as_much_links(tech_articles, 200, 'igihe_tech_articles.txt')
# fetch_as_much_links(env_articles, 200, 'igihe_env_articles.txt')
# fetch_as_much_links(gospel_articles, 200, 'igihe_gospel_articles.txt')
# fetch_as_much_links(tourism_articles, 200, 'igihe_tourism_articles.txt')
# fetch_as_much_links(opinion_articles, 200, 'igihe_opinion_articles.txt')
# fetch_as_much_links(culture_articles, 200, 'igihe_culture_articles.txt')
# fetch_as_much_links(diaspora_articles, 200, 'igihe_diaspora_articles.txt')
