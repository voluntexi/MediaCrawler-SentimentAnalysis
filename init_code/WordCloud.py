import jieba
# 读取文本,生成词云图
import xlrd
def wordFrequency(filename):
    ex = xlrd.open_workbook(filename)
    ws = ex.sheet_by_index(0)
    row = ws.nrows
    lists = []
    for i in range(1, row):
        lists.append(ws.cell_value(i, 2))
    word=""
    for i in lists:
        word=word+i
    words  = jieba.lcut(word)
    counts = {}
    for word in words:
        if len(word) == 1:
            continue
        else:
            counts[word] = counts.get(word,0) + 1
    items = list(counts.items())
    items.sort(key=lambda x:x[1], reverse=True)
    dict={}
    for i in range(20):
        word, count = items[i]
        dict[word]=count;
    return dict