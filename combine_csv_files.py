# import pandas as pd

# igihe_csv = pd.read_csv('igihe_articles.csv')
# umuseke_csv = pd.read_csv('umuseke_articles.csv')
# combined_csv = pd.concat([igihe_csv, umuseke_csv])

# combined_csv.to_csv('kinya_articles.csv', index=False, encoding='utf-8-sig')

import os
import glob
import pandas as pd
os.chdir('Data')

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
for name in all_filenames:
    print(name)
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
combined_csv.to_csv("amakuru.csv", index=False, encoding='utf-8-sig')
