from lxml import etree
from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup


NSMAP = {'fictionbook': 'http://www.gribuser.ru/xml/fictionbook/2.0'}


def detect_encoding(file_path: str):
    encoding = "utf-8"
    try:
        l = open(file_path, 'r', encoding='utf-8').read()
        if l.startswith("\ufeff"):
            encoding = "utf-8-sig"
    except UnicodeDecodeError:
        try:
            open(file_path, 'r', encoding="utf-16").read()
            encoding = "utf-16"
        except UnicodeError:
            encoding = "cp1251"
    return encoding


"""
Code section with readers.
    Included:
        .fb2
        .txt
        .epub
"""


def fb2reader(fb2_filepath: str) -> str:
    tree = etree.parse(fb2_filepath)
    t_root = tree.getroot()

    bodies = t_root.xpath('//fictionbook:body', namespaces=NSMAP)

    book = ''
    for body in bodies:
        paragraphs = body.xpath('.//fictionbook:p/text()', namespaces=NSMAP)
        for p in paragraphs:
            book += (p.strip()) + ' '
    return book


def txt_linesreader(txt_filepath: str) -> list:
    encoding = detect_encoding(txt_filepath)
    with open(txt_filepath, 'r', encoding=encoding) as f:
        return f.readlines()


def txt_reader(txt_filepath: str) -> str:
    encoding = detect_encoding(txt_filepath)
    with open(txt_filepath, 'r', encoding=encoding) as f:
        return f.read()


def epub_reader(epub_filepath: str) -> str:
    try:
        encoding = detect_encoding(epub_filepath)

        book = epub.read_epub(epub_filepath)
        chapters = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
        full_text = ''

        for chapter in chapters:
            content = chapter.get_content().decode(encoding)
            soup = BeautifulSoup(content, 'html.parser')
            chapter_text = soup.get_text().strip()
            full_text += chapter_text + ' '

        return full_text
    except epub.EpubException:
        return '0'


"""
Code section with writers.
    Included:
        .txt
"""


def txt_writer(data, filepath, encoding='utf-8'):
    if type(data) is not str:
        data = str(data)

    if not filepath.endswith('.txt'):
        filepath += '.txt'

    with open(filepath, 'w', encoding=encoding) as f:
        f.write(data)
