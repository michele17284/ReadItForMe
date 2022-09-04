import pdfplumber

'''
with pdfplumber.open(book_path) as pdf:
    first_page = pdf.pages[1]
    print(first_page.extract_text())
'''
import ebooklib
from ebooklib import epub


def extract_text(book_path):
    book = epub.read_epub(book_path)
    items = list(book.get_items())
    chapters = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    texts = {}
    for c in chapters:
        texts[c.get_name()] = chapter_to_str(c)
    to_keep = []
    keep = False
    for chapter in texts:
        if keep == True:
            to_keep.append(chapter)
        if "Copyright" in texts[chapter]:
            keep = True

    clean_text = {}
    i = 1
    for chapter in to_keep:
        clean_text["Chapter " + str(i)] = texts[chapter]
        i += 1
    return book.title,clean_text


from bs4 import BeautifulSoup
def chapter_to_str(chapter):
    soup = BeautifulSoup(chapter.get_body_content(), 'html.parser')
    text = [para.get_text() for para in soup.find_all('p')]
    #p = soup.find_all('p')
    return ''.join(text)


import nltk
nltk.download('punkt')


def clean_text(text):
    chapters = {}
    for chapter in text:
        text_string = text[chapter]
        sent_text = nltk.sent_tokenize(text_string)  # this gives us a list of sentences
        # now loop over each sentence and tokenize it separately
        tokenized_sent_text = []
        #'''
        for sentence in sent_text:
            tokenized_text = nltk.word_tokenize(sentence)
            tagged = nltk.pos_tag(tokenized_text)
            tokenized_sent_text.append(tokenized_text)
        #'''
        #chapters[chapter] = tokenized_sent_text
        chapters[chapter] = sent_text
    return chapters




