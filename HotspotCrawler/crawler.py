import json
import re
import time
import dateutil
import pandas as pd
import requests
def crawler(url,page,name):
	num=0
	c=0
	allData=[]
	for i in range(page):
		res=requests.get("{}&page={}".format(url,i))
		data=res.json()['data']['statuses']
		for singleMess in data:
			try:
				id=singleMess['user']['id']
				messageid=singleMess['id']
				mid=singleMess['mid']
				username=singleMess['user']['screen_name']
				messagetime=singleMess['created_at']
				messagetime = dateutil.parser.parse(messagetime)
				years=dateutil.parser.parse('Sat Jan 1 0:00:00 +0800 2022')
				diss=str(messagetime-years)
				diss=diss.replace(' ','')
				diss=diss.replace('days','天')
				message=singleMess['text']
				like=singleMess['attitudes_count']
				transmit=singleMess['reposts_count']
				commentNum=singleMess['comments_count']
				halfData=[]
				if(commentNum!=0):
					halfData,user_diss=getSingleMicroblogInfo(id,mid)
					temp=[]
					singleData = [num, diss, id, username, messageid, message, 1]
					for i in halfData:
						fullData=singleData+i
						allData.append(fullData)
						print("正在爬取第{}条数据".format(c))
						c+=1
				else:
					singleData=[num,diss,id,username,messageid,message,user_diss,1,0,'null',0,'null',0]
					allData.append(singleData)
					print("正在爬取第{}条数据".format(c))
					c+=1
				time.sleep(0.5)
			except:
				print("数据异常")
			time.sleep(1)
			num+=1
	data=pd.DataFrame(allData)
	data.columns=['序号','发文/转发时间(2022年1月1日至今)','发文/转发用户ID','发文/转发用户昵称','发文/转发内容ID','发文/转发内容','发文/转发标识','转发/评论时间(2022年1月1日至今)','转发/评论用户ID','转发/评论用户昵称','转发/评论ID','转发/评论内容','转发/评论标识']
	writer = pd.ExcelWriter('./{}.xlsx'.format(name))
	# data['时间(2022年1月1日至今)'] = data['时间(2022年1月1日至今)'].dt.tz_localize(None)
	data.to_excel(writer,sheet_name='cx',index=False)
	writer.save()
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
	for (url,name) in zip(urls,urlsname):
		crawler(url, 5,name)
def getSingleMicroblogInfo(id,mid):
	headers = {
		  "user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36",
		"cookie":'input your cookie'
		}
	microblog=[]
	url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(id,mid)
	num=1
	while num<=100:
		res = requests.get(url,headers=headers)
		data = res.json()['data']
		max_id = data['max_id']
		user_info = data['data']
		for single_info in  user_info:
			Retext=single_info['text']
			Retext_id=single_info['id']
			user_id=single_info['user']['id']
			user_name=single_info['user']['screen_name']
			user_messagetime = single_info['created_at']
			user_messagetime = dateutil.parser.parse(user_messagetime)
			years = dateutil.parser.parse('Sat Jan 1 0:00:00 +0800 2022')
			user_diss = str(user_messagetime - years)
			user_diss = user_diss.replace(' ', '')
			user_diss = user_diss.replace('days', '天')
			comment_flag=1
			user_comment=[user_diss,user_id,user_name,Retext_id,Retext,comment_flag]
			microblog.append(user_comment)
			num+=1
			time.sleep(1)
		if max_id!=0:
			url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type=0'.format(id, mid, max_id)
		else:
			break
	return microblog,user_diss
start()



