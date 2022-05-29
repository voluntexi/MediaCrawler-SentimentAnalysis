import requests
import json
import time
import xlwt
'''
功能：爬取B站ID、用户名、用户评论
使用方法：
在def BilibiliCrawler(Old_url)函数中 输入爬取的网站oid 即可实现信息的爬取
在爬取完毕后会将数据以EXCEL表的形式存入当前目录，命名为：BilibiliComment.xls
'''
com=[]
def require(url):
    # 获取网页源码
    headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'cookie':"LIVE_BUVID=AUTO8815482373118512; rpdid=|(um~RJk~~JJ0J'ullYumlu|J; fts=1560587796; blackside_state=1; video_page_version=v_old_home_10; fingerprint_s=b8b766f8af1fcfec4818d8a8289fd56b; buvid3=E2A91CCF-55C4-4C85-B1F8-6DF487BEDAE9148802infoc; i-wanna-go-back=-1; b_ut=5; buvid_fp=E2A91CCF-55C4-4C85-B1F8-6DF487BEDAE9148802infoc; buvid_fp_plain=undefined; fingerprint3=ee6ee36f0d5d98cbb2bad272e71dcf5e; sid=jplsab3z; CURRENT_QUALITY=0; CURRENT_BLACKGAP=0; nostalgia_conf=-1; CURRENT_FNVAL=4048; bp_video_offset_518871228=642693756587343900; DedeUserID=397563377; DedeUserID__ckMd5=47ff0a8a3c14924a; bili_jct=27d55ccc054b6c5771eec36057bcd890; bp_t_offset_397563377=642650381715767304; bp_video_offset_397563377=642650381715767300; fingerprint=9e7fbeb79c306225512cfa21bafb8214; innersign=1"
    }
    try:
        r=requests.get(url,headers=headers)
        r.raise_for_status()
        print(url)
        return r.text
    except requests.HTTPError as e:
        print(e)
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknow error")
def Html(html):
#     获取所需内容
    s=json.loads(html)
    for i in range(20):
        comment=s['data']['replies'][i]
        floor = comment['member']['mid']
        sex=comment['member']['sex']
        ctime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(comment['ctime']))
        content = comment['content']['message']
        likes = comment['like']
        rcounts = comment['rcount']
        username=comment['member']['uname']
        content=comment['content']['message']
        list=[]
        print(floor)
        list.append(floor)
        list.append(username)
        list.append(content)
        com.append(list)
def save_afile(alls,filename):
    """将一个评论数据保存在一个excle"""
    f=xlwt.Workbook()
    sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    sheet1.write(0,0,'ID')
    sheet1.write(0,1,'用户名')
    sheet1.write(0,2,'评论内容')
    i=1
    for data in alls:
        for j in range(len(data)):
            sheet1.write(i,j,data[j])
            # print(i,j,data[j])
        i=i+1
    f.save(filename+'.xls')
def BilibiliCrawler(oid):
    Old_url = 'https://api.bilibili.com/x/v2/reply?type=1&sort=2&oid=' + oid + '&pn='
    e=0
    page=0
    while e == 0 :
        url = Old_url+str(page)
        try:
            html=require(url)
            Html(html)
            page=page+1
            if page%10 == 0:
                time.sleep(5)
            if page==30:
                break
        except:
            e=1
    save_afile(com,"BilibiliComment")
BilibiliCrawler("810372428")
