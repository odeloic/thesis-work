import requests
from bs4 import BeautifulSoup as bs


def get_umuseke_links(page_url=None):
    page = requests.get(page_url)
    soup = bs(page.content, 'html.parser')
    links = []
    news_articles = soup.find_all('h2', class_='post-title')
    for article in news_articles:
        link = article.find('a', href=True)
        if link['href'].startswith('http') or link['href'].startswith('https'):
            links.append(link['href'])
        else:
            links.append(page_url+link['href'])
    return links


def get_umuseke_article_content(url, category='news'):
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')
    text = ''
    if(soup.find('h1', class_='post-title') is None):
        article_title = 'N/A'
    else:
        article_title = soup.find('h1', class_='post-title').getText()
    if(soup.find('div', class_='post-body') is None):
        text = ''
    else:
        article_paragraphs = soup.find('div', class_='post-body').find_all('p')
        for p in article_paragraphs:
            text += p.getText() + '\n'
    return {'Title': article_title, 'Body': text, 'Url': url, 'Category': category}


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


def fetch_as_much_links(url, saveToFile=None):
    count = 0
    page = 1
    links = []
    pageUrl = url + '/page/'
    while count < 200:
        print(f'count is {count}, page is {page} and have {len(links)} links')
        if(page == 1):
            url = url
        else:
            url = pageUrl + str(page)
        print(f'fetching articles on {url}')
        additional_links = get_umuseke_links(url)
        print(len(additional_links))
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


business_articles = 'https://umuseke.rw/category/ubukungu'
sport_articles = 'https://umuseke.rw/category/imikino'
health_articles = 'https://umuseke.rw/category/ubuzima'
ent_articles = 'https://umuseke.rw/category/imyidagaduro'

# fetch_as_much_links(business_articles,
#                     'umuseke_business_articles_links.txt')
# fetch_as_much_links(sport_articles, 'umuseke_sport_articles_links.txt')
# fetch_as_much_links(
#     health_articles, 'umuseke_health_articles_links.txt')
# fetch_as_much_links(
#     ent_articles, 'umuseke_ent_articles_links.txt')
