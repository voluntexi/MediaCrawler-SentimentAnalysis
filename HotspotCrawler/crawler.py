import re
import sys
import time
import pandas as pd
import requests
from datetime import datetime

cookie = ''  # 微博 cookie
dataNumber = 1000  # 爬取的数据量
allData = []
num = 1
dictTrans = {}
dictComm = {}
names = ""


def crawler(url, page):
    global allData
    global num
    for i in range(page):
        res = requests.get("{}&page={}".format(url, i))
        data = res.json()['data']['statuses']
        for singleMess in data:
            try:
                id = singleMess['user']['id']
                messageid = singleMess['id']
                mid = singleMess['mid']
                username = singleMess['user']['screen_name']
                messagetime = singleMess['created_at']
                messagetime = getStandardTime(messagetime)
                message = singleMess['text']
                like = singleMess['attitudes_count']
                transmit = singleMess['reposts_count']
                commentNum = singleMess['comments_count']
                data = [commentNum, transmit, like]
                if commentNum != 0 or transmit != 0:
                    singleData = [num, messagetime, id, username, messageid, message, 1]
                    if commentNum != 0:
                        halfData, comment = getCommentInfo(id, mid)
                        data[0] = comment
                    if transmit != 0:
                        transpond, transmit = getTranspondInfo(mid)
                        data[1] = transmit
                    if halfData is not None:
                        for i in halfData:
                            fullData = singleData + i + data
                            allData.append(fullData)
                            print("\r", end="")
                            print("进度: {}%: ".format(((len(allData) + 1) / dataNumber) * 100 if (((len(allData) + 1) / dataNumber) * 100) <= 100 else 100),
                                  end="")
                        if len(allData) > dataNumber:
                            writeToExcel()
                            writeToTxt()
                            sys.exit()
                    if transpond is not None:
                        for i in transpond:
                            fullData = singleData + i + data
                            allData.append(fullData)
                            print("\r", end="")
                            print("进度: {}%: ".format(((len(allData) + 1) / dataNumber) * 100 if (((len(allData) + 1) / dataNumber) * 100) <= 100 else 100),
                                  end="")
                        # print(f"正在爬取第{len(allData)}条数据")
                        if len(allData) > dataNumber:
                            writeToExcel()
                            writeToTxt()
                            sys.exit()
                    num += 1
                # else:
                # 	NoneData=[num,messagetime,id,username,messageid,message,0,'null',0,'null',0,'null',0,commentNum,transmit,like]
                # 	allData.append(NoneData)
                # 	print(f"正在爬取第{len(allData)}条数据")
                # 	num += 1
                # 	if len(allData) > dataNumber:
                # 		writeToExcel()
                # 		sys.exit()
                time.sleep(0.5)
            except Exception as e:
                pass
                # print("")
                print(f"数据异常{e},重新爬取")
            time.sleep(1)
        break


def getTranspondInfo(id):
    global allData
    global num
    global cookie
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "cookie": cookie
    }
    url = 'https://m.weibo.cn/api/statuses/repostTimeline?id={}&page=1'.format(id)
    res = requests.get(url, headers=headers)
    try:
        data = res.json()['data']
        page = data['max']
        current_page = 1
        trans_num = 0
        total_number = data['total_number']
        microblog = []
        transpondInfo = data['data']
        while trans_num < total_number - 1:
            if current_page != 1:
                res = requests.get(url, headers=headers)
                data = res.json()['data']
                total_number = data['total_number']
                transpondInfo = data['data']
            else:
                pass
            for single_info in transpondInfo:
                # ReInfo = re.split("//<a href='.*?>@",single_info['text'])
                Retext = single_info['text']
                like = single_info['attitudes_count']
                mid = single_info['mid']
                Retext_id = single_info['id']
                user_id = single_info['user']['id']
                user_name = single_info['user']['screen_name']
                user_messagetime = single_info['created_at']
                commentNum = single_info['comments_count']
                user_messagetime = getStandardTime(user_messagetime)
                transpond_flag = 2
                transmit = single_info['reposts_count']
                # print(transmit)
                # Retext=ReInfo[0]
                user_comment = [user_messagetime, user_id, user_name, Retext_id, Retext, transpond_flag]
                microblog.append(user_comment)
                if commentNum != 0 or transmit != 0:
                    comment = 0
                    transmit_micor = 0
                    commentData = []
                    transpond = []
                    data = [commentNum, transmit, like]
                    singleData = [num, user_messagetime, user_id, user_name, Retext_id, Retext, 2]
                    if commentNum != 0:
                        if dictComm.get(Retext) is None:
                            commentData, comment = getCommentInfo(mid, Retext_id)
                            dictComm[Retext] = 1
                            data[0] = comment
                    if transmit != 0:
                        if dictTrans.get(Retext) is None:
                            transpond, transmit_micor = getTranspondInfo(mid)
                            dictTrans[Retext] = 1
                            data[1] = transmit_micor
                    if commentData is not None:
                        for i in commentData:
                            if dictComm.get(i[5]) is None:
                                fullData = singleData + i + data
                                allData.append(fullData)
                                print("\r", end="")
                                print("进度: {}%: ".format(((len(allData) + 1) / dataNumber) * 100 if (((len(allData) + 1) / dataNumber) * 100) <= 100 else 100),
                                      end="")
                        if len(allData) > dataNumber:
                            writeToExcel()
                            writeToTxt()
                            sys.exit()
                    if transpond is not None:
                        for i in transpond:
                            if dictTrans.get(i[5]) == None:
                                fullData = singleData + i + data
                                allData.append(fullData)
                                print("\r", end="")
                                print("进度: {}%: ".format(((len(allData) + 1) / dataNumber) * 100 if (((len(allData) + 1) / dataNumber) * 100) <= 100 else 100),
                                      end="")
                        if len(allData) > dataNumber:
                            writeToExcel()
                            writeToTxt()
                            sys.exit()
                        # print(allData)
                    if comment != 0 or transmit_micor != 0:
                        num += 1
                trans_num += 1
                time.sleep(1)
            if current_page <= page:
                current_page += 1
                url = 'https://m.weibo.cn/api/statuses/repostTimeline?id= {}&page={}'.format(id, current_page)
            else:
                break
        return microblog, trans_num
    except Exception as e:
        print(f"数据异常{e},重新爬取")
        return None, 0


def getCommentInfo(id, mid):
    global cookie
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36",
        "cookie": cookie
    }
    microblog = []
    url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(id, mid)
    comment_num = 0
    while True:
        res = requests.get(url, headers=headers)
        data = res.json()['data']
        max_id = data['max_id']
        user_info = data['data']
        for single_info in user_info:
            Retext = single_info['text']
            Retext_id = single_info['id']
            user_id = single_info['user']['id']
            user_name = single_info['user']['screen_name']
            user_messagetime = single_info['created_at']
            user_messagetime = getStandardTime(user_messagetime)
            comment_flag = 1
            user_comment = [user_messagetime, user_id, user_name, Retext_id, Retext, comment_flag]
            microblog.append(user_comment)
            comment_num += 1
            # print("正在爬取该微博评论内容")
            time.sleep(1)
        if max_id != 0:
            url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=0'.format(id, mid, max_id)
        else:
            break
    return microblog, comment_num


def cleanData(df):
    message = []
    comment = []
    for item, item2 in zip(df['发文/转发内容'], df['转发/评论内容']):
        scriptRegex = "<script[^>]*?>[\\s\\S]*?<\\/script>"
        styleRegex = "<style[^>]*?>[\\s\\S]*?<\\/style>"
        htmlRegex = "<[^>]+>"
        spaceRegex = "\\s*|\t|\r|\n"
        item = re.sub(scriptRegex, '', str(item))  # 去除网址
        item = re.sub(styleRegex, '', str(item))
        item = re.sub(htmlRegex, '', str(item))
        item = re.sub(spaceRegex, '', str(item))
        item = re.sub('网页链接', '', str(item))
        item2 = re.sub(scriptRegex, '', str(item2))
        item2 = re.sub(styleRegex, '', str(item2))
        item2 = re.sub(htmlRegex, '', str(item2))
        item2 = re.sub(spaceRegex, '', str(item2))
        item2 = re.sub('网页链接', '', str(item2))
        message.append(item)
        comment.append(item2)
    df['发文/转发内容'] = message
    df['转发/评论内容'] = comment


def getStandardTime(time):
    GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
    time = str(datetime.strptime(time, GMT_FORMAT)).split()
    simpleDate = time[0].split("-")
    specData = time[1].split(":")
    year = simpleDate[0]
    month = simpleDate[1]
    day = simpleDate[2]
    hour = specData[0]
    min = specData[1]
    second = specData[2]
    return "{}年{}月{}日{}时{}分{}秒".format(year, month, day, hour, min, second)


def writeToExcel():
    print("爬取完成，正在写入Excel")
    global names
    global allData
    data = pd.DataFrame(allData)
    data.columns = ['序号', '发文/转发时间(2022年1月1日至今)', '发文/转发用户ID', '发文/转发用户昵称',
                    '发文/转发内容ID', '发文/转发内容', '发文/转发标识', '转发/评论时间(2022年1月1日至今)',
                    '转发/评论用户ID', '转发/评论用户昵称', '转发/评论ID', '转发/评论内容', '转发/评论标识',
                    '评论数', '转发数', '点赞数'
                    ]
    cleanData(data)
    writer = pd.ExcelWriter('./{}.xlsx'.format(names))
    data.to_excel(writer, sheet_name='cx', index=False)
    writer.save()
    writer.close()
    print("写入Excel成功")


def writeToTxt():
    print("爬取完成，正在写入记事本")
    global names
    global allData
    file = open(f"{names}.txt", mode="w", encoding="utf-8")
    for i in allData:
        file.write(i + "\n")
    print("写入记事本成功")


def start():
    urls = [
        'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_5188_-_ctg1_5188',  ## 汽车
        # 'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_1588_-_ctg1_1588',  ## 美妆
        # 'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_4288_-_ctg1_4288',  ## 明星
        # 'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_2088_-_ctg1_2088',  ## 科技
        # 'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_4988_-_ctg1_4988',  ## 摄影
        # 'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_4888_-_ctg1_4888',  ## 游戏
        # 'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_2688_-_ctg1_2688',  ## 美食
        # 'https://m.weibo.cn/api/feed/trendtop?containerid=102803_ctg1_2588_-_ctg1_2588',  ## 旅行
    ]
    urlsname = [
        '汽车',
        # '美妆',
        # '明星',
        # '科技',
        # '摄影',
        # '游戏',
        # '美食',
        # '旅行',
    ]
    for (url, name) in zip(urls, urlsname):
        global names
        names = name
        crawler(url, 1000)


if __name__ == '__main__':
    start()
