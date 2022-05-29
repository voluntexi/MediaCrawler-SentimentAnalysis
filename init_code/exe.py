import BilibiliCrawler
import DouyinCrawler
import WeiboCrawler
import addExcel
'''
程序控制流程示例
'''
web=input("输入要爬取的网站:1：哔哩哔哩 2.抖音 3.微博\n")
if web=="1":
# oid的获取 到视频网页后按F12 搜索callback  然后点标头-常规-请求网址 -》就可查看oid
# 示例：oid=255582553
    print("oid的获取: 在所需要爬取的视频网页按F12->搜索callback->然后点标头-常规-请求网址就可查看oid")
    oid=input("输入爬取的oid\n")
    BilibiliCrawler.BilibiliCrawler(oid)
elif web=="2":
# URL的获取  到视频网页后按F12 搜索comment 然后获得请求网址 复制下来
# url='https://www.douyin.com/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7075139608815750437&cursor=20&count=20&item_type=0&rcFT=AAK-tWBiA&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=99.0.4844.51&browser_online=true&engine_name=Blink&engine_version=99.0.4844.51&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=0&webid=7082249047388145183&msToken=hpxUHA9vWtNbomaVvJPcwuc8xlCO9tQaFyfQBgDaSQ8t1PigpqY69qerDAWDKq2jhyLW3nel2f_KgccBnppvYwxMWComajoiD7MhBmSAnpS-smo658--9Nbh3iDP2IXU3A==&X-Bogus=DFSzswVE34zANG54SAoynGUClL90&_signature=_02B4Z6wo00001vf-UFAAAIDD3HQLlvbMmYr3.lTAAN-wLXUYNq9qMyaUQ2Sl2-2lLRcGrOYThxYWgrDfN5QbFBuRfsZk4MPNQyg.v4EJBwWHtx43RP3sJ3o.ynblAYqDW4GmMkurgz6uOvwNb6'
    print("URL的获取:在所需要爬取的视频网页按F12->搜索comment->然后获得请求网址,复制下来")
    url=input("输入爬取的URL\n")
    DouyinCrawler.DouyinCrawler(url)


elif web=="3":
# url='https://weibo.cn/comment/LofPqmSbn?uid=1883881851&rl=0#cmtfrm'#一个微博的评论首页
    print("URL的获取:到https://weibo.cn/中找到评论网页后直接复制网址")
    url=input("输入爬取的URL\n")
    print('爬取的新闻标题为:'+WeiboCrawler.WeiboCrawler(url))
p=input("输入要计算的评论：1：哔哩哔哩 2.抖音 3.微博\n")
ex=None
if p=="1":
    filename = "BilibiliComment.xls"
elif p=="2":
    filename = "DouyinComment.xls"
elif p=="3":
    filename = "WeiboComment.xls"
addExcel.WriteSenti(filename)

