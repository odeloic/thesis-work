import csv
import requests
from igihe_scraper import get_igihe_article_content
from umuseke_scraper import get_umuseke_article_content
import os


def create_umuseke_csv(fileName=None, saveTo=None, category=None):
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
            count += 1
            continue
        else:
            print(f'Article {count} is downloading...')
            content = get_umuseke_article_content(link, category)
            try:
                with open(saveTo, 'a+', newline='') as cfile:
                    writer = csv.DictWriter(cfile, fieldnames=columns)
                    if os.stat(saveTo).st_size == 0:
                        writer.writeheader()
                    writer.writerow(content)
                    count += 1
            except IOError:
                print("I/O Error")


# create_umuseke_csv('umuseke_health_articles_links.txt',
#                    'umuseke_health_articles.csv', 'Health')
# create_umuseke_csv('umuseke_ent_articles_links.txt',
#                    'umuseke_ent_articles.csv', 'Entertainment')
create_umuseke_csv('umuseke_sport_articles_links.txt',
                   'umuseke_sport_articles.csv', 'Entertainment')
