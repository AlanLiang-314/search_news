from fetch_news import preprocess_text
import save
import os

pickler = save.pickler(r"urls\urls.pkl")

def read_md(path: str):
    # 讀取md檔中不含yaml的部分，回傳文字和檔名
    title = os.path.basename(path).split('.')[0]
    with open(path, 'r', encoding='utf-8') as f:
        md = f.read()
        if md.find('---',0)==0:
            md = md[md.find('---',1):]
        return title, md


def preprocess_md(path: str):
    # 讀取特定路徑的md檔之後，儲存uuid並回傳md檔和uuid
    title, md = read_md(path)
    md = preprocess_text(md,windows_size=3)
    id = pickler.add(path)
    #id = save_url(path,force_to_add=True)
    
    return md, id


def walk_md(path: str):
    passages = []
    for dirPath, _, fileNames in os.walk(path):
        for f in fileNames:
            if os.path.splitext(f)[-1] == ".md":
                f_abspath = os.path.join(dirPath, f)
                print(f_abspath)
                md, id = preprocess_md(f_abspath)
                passages.extend(md)

    print(passages)
    pickler.show()



walk_md(r"D:\konwledge_vault\konwledge_md")