import csv
urls = []
with open('igihe_business_articles.csv', 'r+') as cfile:
    reader = csv.DictReader(cfile, delimiter=',')
    for row in reader:
        urls.append(row['Url'])

print(len(urls))
print(reader)
