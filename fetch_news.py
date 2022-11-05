from newspaper import Article
from const import URL_PATH
import save
import re


def zng(paragraph):
        for sent in re.findall(u'[^!?。\.\!\?]+[!?。\.\!\?]?', paragraph, flags=re.U):
            sent = re.sub(r'!?\[([^\[]+)\]\(([^\)]+)\)','',sent) #去除超連結
            sent = re.sub('\*|#+ |- |==|`+|> |\[\[|\]\]|---','',sent) #去除強調，程式碼，螢光筆等記號
            sent = re.sub(r'\n',' ',sent) #去除多餘的換行符
            if len(sent):
                yield sent



def preprocess_text(article: str, windows_size: int=3):
    paragraphs = article.split('\n\n')
    passages = []

    for paragraph in paragraphs:
        paragraph = list(zng(paragraph))
        #print(paragraph)
        for start_idx in range(0,len(paragraph), windows_size):
            end_idx = min(start_idx+windows_size, len(paragraph))
            passages.append("".join(paragraph[start_idx:end_idx]))

    return passages


def fetch(url: str, windows_size: int=3):
    article = Article(url)
    article.download()
    article.parse()

    # get text
    article = article.text
    
    passages = preprocess_text(article)
    #print(passages)

    pickler = save.pickler(URL_PATH)
    article_id = pickler.add(url)
    if article_id == None:
        raise ValueError("the file already exist")
    pickler.show()
    pickler.save()

    return passages, article_id

#fetch("https://pansci.asia/archives/348757")