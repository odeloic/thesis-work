import itertools
from pathlib import Path


def getTopSortedKElements(tdfidfDict, K=100):
    sortedValues = {k: v for k, v in sorted(
        tdfidfDict.items(), key=lambda item: item[1])}
    return dict(itertools.islice(sortedValues.items(), K)).keys()


def saveWordsToFile(fileName, words=[]):
    with open(f'../Data/{fileName}', 'w') as file:
        for word in words:
            file.write('%s\n' % word)


def getStopwordsFromFile(fileName):
    path = Path(__file__).parent / f"../Data/{fileName}"
    stopwords = [line.rstrip('\n') for line in path.open()]
    # with open(path, 'r') as file:
    #     stopwords = [line.rstrip('\n') for line in file]
    # print(len(stopwords))
    return stopwords
