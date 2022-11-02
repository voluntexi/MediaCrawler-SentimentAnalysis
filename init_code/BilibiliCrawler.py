import time
import xlwt
import requests
import re
import json

from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip

'''
功能：爬取B站ID、用户名、用户评论
使用方法：
在def BilibiliCrawler(Old_url)函数中 输入爬取的网站链接 即可实现信息的爬取和视频的下载，下载路径为video/Bvideo.mp4
在爬取完毕后会将数据以EXCEL表的形式存入当前目录，命名为：BilibiliComment.xls
'''
com=[]
def require(url):
    headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/39.0.2171.95 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'cookie': "LIVE_BUVID=AUTO8815482373118512; rpdid=|(um~RJk~~JJ0J'ullYumlu|J; fts=1560587796; blackside_state=1; video_page_version=v_old_home_10; fingerprint_s=b8b766f8af1fcfec4818d8a8289fd56b; buvid3=E2A91CCF-55C4-4C85-B1F8-6DF487BEDAE9148802infoc; i-wanna-go-back=-1; b_ut=5; buvid_fp=E2A91CCF-55C4-4C85-B1F8-6DF487BEDAE9148802infoc; buvid_fp_plain=undefined; fingerprint3=ee6ee36f0d5d98cbb2bad272e71dcf5e; CURRENT_QUALITY=0; CURRENT_BLACKGAP=0; nostalgia_conf=-1; is-2022-channel=1; CURRENT_FNVAL=4048; bp_video_offset_397563377=660432194805694500; fingerprint=f9fcaba1da89d19527f68276b797d106; SESSDATA=8c8ea1cb,1668241180,1c42d*51; bili_jct=09e7861f5f39f86014feb2e904ce1890; DedeUserID=587803794; DedeUserID__ckMd5=0fdc9b2014e96c2a; sid=4l12om00"
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
        ctime = time.strftime("%Y-%m-%d",time.localtime(comment['ctime']))
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
        list.append(ctime)
        com.append(list)
def save_afile(alls,filename):
    """将一个评论数据保存在一个excle"""
    f=xlwt.Workbook()
    sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    sheet1.write(0,0,'Comment_ID')
    sheet1.write(0,1,'Comment_Name')
    sheet1.write(0,2,'Comment_Content')
    sheet1.write(0,3,'Comment_Time')
    i=1
    for data in alls:
        for j in range(len(data)):
            sheet1.write(i,j,data[j])
            # print(i,j,data[j])
        i=i+1
    f.save(filename+'.xls')
def biliVideo(url):
    headers = {
        'Referer': 'https://www.bilibili.com/video/BV1bK4y19743?spm_id_from=333.5.b_64616e63655f6f74616b75.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    url=url.partition('?')[0]
    print(url)
    print('获取中')
    response = requests.get(url, headers).text
    pattern = '<script>window\.__playinfo__=(.*?)</script>'
    list = re.findall(pattern, response, re.S)
    list_json = json.loads(list[0])
    title_pattern = '<span class="tit">(.*?)</span>'
    try:
        title = re.findall(title_pattern, response, re.S)[0]
    except:
        title = 'B站未知视频'
    video_url = list_json['data']['dash']['video'][0]['baseUrl']
    volume_url = list_json['data']['dash']['audio'][0]['baseUrl']
    print(title[0:6] + '获取成功，准备下载')
    video_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37',
        'cookie': "_uuid=165C46B1-C976-4E75-4FBB-DF7CFCE9B78361416infoc; buvid3=E74152CF-4259-4805-8FB0-3EA62B1A5FE118565infoc; sid=8dy5swfr; buvid_fp=E74152CF-4259-4805-8FB0-3EA62B1A5FE118565infoc; DedeUserID=437098665; DedeUserID__ckMd5=58f089438dd790da; SESSDATA=8509a172%2C1632993914%2Cf1dcc*41; bili_jct=db8c6082bba38c59445d89a6dc2bc8eb; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(k)~u~lR)|m0J'uYu~RRk||Y; fingerprint3=9ea3019a6caf79f955972512cf343226; buvid_fp_plain=E74152CF-4259-4805-8FB0-3EA62B1A5FE118565infoc; LIVE_BUVID=AUTO1616186326504349; fingerprint=654b13db806dedf4a8363492a4c50757; fingerprint_s=5f802b1000417d59e0227513b1f22a3e; bp_t_offset_437098665=526477194229905374; bp_video_offset_437098665=531352875458576657; PVID=1; CURRENT_QUALITY=116",
        'referer': 'https://www.bilibili.com/v/dance/?spm_id_from=333.851.b_7072696d6172794368616e6e656c4d656e75.18'
    }
    video_param = {
        'accept_description': '360P 流畅',
        'accept_quality': 60,
    }
    print("视频url："+video_url)
    print('-----开始下载-----')
    video = requests.get(url=video_url, headers=video_headers, params=video_param).content
    # with open('../video/'+r'.\B站{}.mp4'.format(title), 'wb') as f:
    with open('../video/BVideo.mp4', 'wb') as f:
        f.write(video)
        print('视频下载中')
    audio = requests.get(url=volume_url, headers=video_headers).content
    with open('./audio.mp3', 'wb') as f:
        f.write(audio)
    # print('-----视频合成中-----')
    # print('-----请耐心等候-----')
    # # video_path = './B站视频.mp4'
    # # videoclip = VideoFileClip(video_path)
    # audio_path = './audio.mp3'
    # audio = AudioFileClip(audio_path)
    # # videoclip_3 = videoclip.set_audio(audio)
    # path = r'.\B站{}.mp4'.format(title[0:6])
    # videoclip_3.write_videofile(path)
    # import os
    # if os.path.exists(video_path):
    #     os.remove(video_path)
    # else:
    #     pass
    # if os.path.exists(audio_path):
    #     os.remove(audio_path)
    #     print('success!!!')
    # else:
    #     pass
    return title
def getOid(url):
    bv = re.findall('https://www.bilibili.com/video/(.*?)\?', url, re.S)[0]
    print(bv)
    resp = requests.get("https://www.bilibili.com/video/" + bv)
    obj = re.compile(f'"aid":(?P<id>.*?),"bvid":"{bv}"')  # 在网页源代码里可以找到id，用正则获取到
    oid = obj.search(resp.text).group('id')
    return oid
def BilibiliCrawler(url):
    videoName=biliVideo(url)
    oid=getOid(url)
    print(oid)
    Old_url = 'https://api.bilibili.com/x/v2/reply?type=1&sort=1&oid=' + str(oid) + '&pn='
    e=0
    page=1
    while e == 0 :
        url = Old_url+str(page)
        try:
            html=require(url)
            Html(html)
            page=page+1
            if page%10 == 0:
                time.sleep(3)
            if page>30:
                break
        except:
            e=1
    save_afile(com,"bilibili_comment")
    return videoName
# BilibiliCrawler("https://www.bilibili.com/video/BV1F5411R7jb?spm_id_from=333.337.search-card.all.click")
biliVideo("https://www.bilibili.com/video/BV1r5411U7yq?spm_id_from=333.337.search-card.all.click")