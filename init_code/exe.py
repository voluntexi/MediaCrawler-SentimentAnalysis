import BilibiliCrawler
import DouyinCrawler
import WeiboCrawler
import addExcel
'''
程序控制流程示例
'''
i=0
while(i<=3):
    web=input("输入要爬取的网站:1：哔哩哔哩 2.抖音 3.微博\n")
    if web=="1":
        url=input("输入爬取的url\n")
        print('爬取的标题为:' +BilibiliCrawler.BilibiliCrawler(url))
    elif web=="2":
        url=input("输入爬取的URL\n")
        print('爬取的标题为:' +DouyinCrawler.DouyinCrawler(url))
    elif web=="3":
        print("URL的获取:到https://weibo.cn/中找到评论网页后直接复制网址")
        url=input("输入爬取的URL\n")
        print('爬取的新闻标题为:'+WeiboCrawler.WeiboCrawler(url))
    p=input("输入要计算的评论：1：哔哩哔哩 2.抖音 3.微博\n")
    ex=None
    if p=="1":
        filename = "bilibili_comment.xls"
    elif p=="2":
        filename = "douyin_comment.xls"
    elif p=="3":
        filename = "weibo_comment.xls"
    addExcel.WriteSenti(filename)
    i+=1

