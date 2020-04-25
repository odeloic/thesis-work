import re
import unicodedata
from bs4 import BeautifulSoup


def normalize_omissions(text):
    pattern = re.compile(r"\w*['’]\w*", re.IGNORECASE)
    tokens = text.split()
    norm_str = text
    for token in tokens:
        if re.match(pattern, token):
            m = re.split(r"['’]", token)
            n = ("a ").join(m)
            norm_str = norm_str.replace(token, n)
    return norm_str


def strip_html_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    [s.extract() for s in soup(['iframe', 'script'])]
    stripped_text = soup.get_text()
    stripped_text = re.sub(r'[\r|\n|\r\n]+', '\n', stripped_text)
    return stripped_text


def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode(
        'ascii', 'ignore').decode('utf-8', 'ignore')
    return text


def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text


def normalize_text(doc, html_stripping=True, handle_omissions=True, accented_char_removal=True, text_lower_case=True, special_chars_removal=True, remove_digits=True):
    # strip html
    if html_stripping:
        doc = strip_html_tags(doc)
    if handle_omissions:
        doc = normalize_omissions(doc)
    # remove accented chars
    if accented_char_removal:
        doc = remove_accented_chars(doc)
    # lowercase the text
    if text_lower_case:
        doc = doc.lower()
    # remove extra newlines
    doc = re.sub(r'[\r|\n|\r\n]+', ' ', doc)
    # remove special characters and digits
    if special_chars_removal:
        special_chars_pattern = re.compile(r'([{.(-)!}])')
        doc = special_chars_pattern.sub(" \\1 ", doc)
        doc = remove_special_characters(doc, remove_digits=remove_digits)
    # remove extra whitespace
    doc = re.sub(' +', ' ', doc)

    return doc

