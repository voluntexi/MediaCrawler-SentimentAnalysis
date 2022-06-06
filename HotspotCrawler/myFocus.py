import sys
import time

import dateutil
import pandas as pd
import requests
headers = {
      "user-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
		"cookie":'input your cookie'
    }
url = 'https://m.weibo.cn/feed/friends?'
res = requests.get(url, headers = headers)
data = res.json()['data']
next_id = data['max_id']
data=data['statuses']
allData=[]
num=1
for i in range(20):
	print("正在爬取第{}个博文".format(num))
	try:
		re_data=singleMess['retweeted_status']
	except:
		re_data=None
	try:
		singleMess=data[i]
		id=singleMess['user']['id']
		messageid=singleMess['id']
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
		transmitFlag=0
		if(transmit!=0):
			transmitFlag=1
		comment=singleMess['comments_count']
		re_comment = 'Null'
		re_username='Null'
		re_transmitFlag=0
		re_messageid=0
		re_id=0
		if(re_data!=None):
			re_username=re_data['user']['screen_name']
			re_comment=re_data['text']
			re_transmitFlag=1
			re_id = re_data['user']['id']
			re_messageid=re_data['id']
		singleData=[num,diss,id,username,messageid,message,transmitFlag,re_id,re_username,re_messageid,re_comment,re_transmitFlag]
		allData.append(singleData)
		num+=1
		time.sleep(0.5)
	except:
		print("数据异常")
while num<=1000:
	if (next_id != None):
		next_url = 'https://m.weibo.cn/feed/friends?max_id={}'.format(next_id)
	else:
		break
	res = requests.get(next_url, headers=headers)
	data = res.json()['data']
	try:
		next_id = data['max_id']
	except:
		next_id = None
	data=data['statuses']
	for i in range(20):
		print("正在爬取第{}个博文".format(num))
		try:
			re_data = singleMess['retweeted_status']
		except:
			re_data = None
		try:
			singleMess = data[i]
			id = singleMess['user']['id']
			messageid = singleMess['id']
			username = singleMess['user']['screen_name']
			messagetime = singleMess['created_at']
			messagetime = dateutil.parser.parse(messagetime)
			years = dateutil.parser.parse('Sat Jan 1 0:00:00 +0800 2022')
			diss = str(messagetime - years)
			diss = diss.replace(' ', '')
			diss = diss.replace('days', '天')
			message = singleMess['text']
			like = singleMess['attitudes_count']
			transmit = singleMess['reposts_count']
			transmitFlag = 0
			if (transmit != 0):
				transmitFlag = 1
			comment = singleMess['comments_count']
			re_comment = 'Null'
			re_username = 'Null'
			re_transmitFlag = 0
			re_messageid = 0
			re_id=0
			if (re_data != None):
				re_username = re_data['user']['screen_name']
				re_comment = re_data['text']
				re_transmitFlag = 1
				re_id = re_data['user']['id']
				re_messageid = re_data['id']
			singleData = [num, diss, id, username, messageid, message, transmitFlag, re_id, re_username, re_messageid,
						  re_comment, re_transmitFlag]
			allData.append(singleData)
			num += 1
			time.sleep(0.5)
		except:
			print("数据异常")
data=pd.DataFrame(allData)
data.columns=['序号','时间(2022年1月1日至今)','发文/转发用户ID','发文/转发用户昵称','发文/转发内容ID','发文/转发内容','发文/转发标识','转发/评论用户ID','转发/评论用户昵称','转发/评论ID','转发/评论内容','转发/评论标识']
writer = pd.ExcelWriter('./{}.xlsx'.format('我的关注'))
# data['时间(2022年1月1日至今)'] = data['时间(2022年1月1日至今)'].dt.tz_localize(None)
data.to_excel(writer,sheet_name='cx',index=False)
writer.save()
sys.exit()
