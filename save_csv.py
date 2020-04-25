import csv
import requests
import os
from igihe_scraper import get_igihe_article_content


def save_igihe_csv(fileName=None, saveTo=None, category=None):
    # initialize articles csv file
    columns = ['Title', 'Body', 'Url', 'Category']
    urls_in_file = []
    if(os.path.isfile(saveTo)):
        with open(saveTo, 'r') as cfile:
            reader = csv.DictReader(cfile, delimiter=",")
            for row in reader:
                urls_in_file.append(row['Url'])
        urls_in_file = [link.strip() for link in urls_in_file]
    # # get links
    with open(fileName, 'r') as file:
        new_links = file.readlines()
    new_links = [link.strip() for link in new_links]
    count = 0
    for link in new_links:
        if link in urls_in_file:
            continue
        else:
            print(f'Article {count} is downloading...')
            content = get_igihe_article_content(link, category)
            if len(content['Body']) < 1:
                count += 1
                continue
            try:
                with open(saveTo, 'a+', newline='') as cfile:
                    writer = csv.DictWriter(cfile, fieldnames=columns)
                    if os.stat(saveTo).st_size == 0:
                        writer.writeheader()
                    writer.writerow(content)
                    count += 1
            except IOError:
                print("I/O Error")


def create_articles_csv(fileName=None, saveTo=None, category=None):
    igihe_news_links = []
    with open(fileName, 'r') as file:
        igihe_news_links = file.readlines()
    igihe_news_links = [link.strip() for link in igihe_news_links]

    sample_articles = []
    count = 0
    for link in igihe_news_links:
        print(f'index {count}')
        content = get_igihe_article_content(link, category)
        sample_articles.append(content)
        count += 1

    columns = ['Title', 'Body', 'Url', 'Category']

    try:
        with open(saveTo, 'w+') as cfile:
            writer = csv.DictWriter(cfile, fieldnames=columns)
            writer.writeheader()
            for data in sample_articles:
                writer.writerow(data)
    except IOError:
        print("I/O Error")


save_igihe_csv('igihe_business_articles.txt',
               'igihe_business_articles.csv', 'Business')
print('Business DOne..')
# save_igihe_csv('igihe_tech_articles.txt',
#                'igihe_tech_articles_articles.csv', 'Tech')
# save_igihe_csv('igihe_sport_articles_links.txt',
#                'igihe_sport_articles_articles.csv', 'Sport')
# save_igihe_csv('igihe_health_articles_links.txt',
#                'igihe_health_articles_articles.csv', 'Health')
# save_igihe_csv('igihe_ent_articles.txt',
#                'igihe_ent_articles_articles.csv', 'Entertainment')
# create_umuseke_csv('umuseke_business_articles_links.txt',
#                    'umuseke_business_articles.csv', 'Business')
# save_igihe_csv('igihe_culture_articles.txt',
#                'igihe_culture_articles.csv', 'Culture')
# print('Culture Done...')
# save_igihe_csv('igihe_opinion_articles.txt',
#                'igihe_opinion_articles.csv', 'Opinion')
# print('Opinion Done...')
# save_igihe_csv('igihe_politics_articles.txt',
#                'igihe_politics_articles.csv', 'Politics')
# print('Politics Done ...')
# save_igihe_csv('igihe_env_articles.txt',
#                'igihe_env_articles.csv', 'Environment')
# print('Environment Done ...')
save_igihe_csv('igihe_gospel_articles.txt',
               'igihe_gospel_articles.csv', 'Gospel')
print('Gospel Done ...')
save_igihe_csv('igihe_tourism_articles.txt',
               'igihe_tourism_articles.csv', 'Tourism')
print('Tourism Done ...')
save_igihe_csv('igihe_culture_articles.txt',
               'igihe_culture_articles.csv', 'Culture')
print('Culture Done ...')
save_igihe_csv('igihe_diaspora_articles.txt',
               'igihe_diaspora_articles.csv', 'Diaspora')
print('Diaspora Done ...')
