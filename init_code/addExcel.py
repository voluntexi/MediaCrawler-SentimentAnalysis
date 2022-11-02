from xlutils.copy import copy
import xlrd
import sentiAnalysis
'''
功能：读取excel表中用户的评论，计算出每个评论的具体情感值，然后写入excel表中
使用：def WriteSenti(filename): 参数为excel的文件名
'''
def excelwrite(filename,singleEmo):
    workbook = xlrd.open_workbook(filename, formatting_info=True)
    sheet = workbook.sheet_by_index(0)
    rowNum = sheet.nrows
    colNum = sheet.ncols
    if (colNum >= 5):
        print("已经存在情感值")
        # 在末尾增加新行
    else:
        newbook = copy(workbook)
        newsheet = newbook.get_sheet(0)
        newsheet.write(0, colNum, "Comment_Value")
        j=0
        for i in range(1,rowNum):
            try:
                newsheet.write(i, colNum, str(singleEmo[j]))
            except:
                continue
            j+=1
        # 覆盖保存
        newbook.save(filename)
def WriteSenti(filename):
    ex=xlrd.open_workbook(filename)
    ws=ex.sheet_by_index(0)
    row=ws.nrows
    list=[]
    for i in range(1,row):
        list.append(ws.cell_value(i,2))
    singleEmo=sentiAnalysis.singleSentiment(list)
    totalSenti=sentiAnalysis.calculation(list)
    print("总的情感值为："+str(totalSenti))
    excelwrite(filename,singleEmo)
    return totalSenti
def readExcel(filename):
    ex = xlrd.open_workbook(filename)
    ws = ex.sheet_by_index(0)
    row = ws.nrows
    col=ws.ncols
    list = []
    for i in range(1, row):
        li=[]
        for j in range(0,col):
            li.append(ws.cell_value(i, j))
        list.append(li)
    return list