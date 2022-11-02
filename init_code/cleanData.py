# #coding='utf-8'
# import xlrd
# import re
# import xlwt
# import os
# from multiprocessing.dummy import Pool as ThreadPool
#
# def stoplist():
#     with open('停用词表.txt','r',encoding='utf-8')as f:
#         stops=f.readlines()
#     return stops
#
#
# def extract(inpath,l):
#     """取出一列数据"""
#     data = xlrd.open_workbook(inpath, encoding_override='utf-8')
#     table = data.sheets()[0]#选定表
#     nrows = table.nrows#获取行号
#     ncols = table.ncols#获取列号
#     numbers=[]
#     for i in range(1, nrows):#第0行为表头
#         alldata = table.row_values(i)#循环输出excel表中每一行，即所有数据
#         result = alldata[l]#取出表中第一列数据
#         numbers.append(result)
#     return numbers
#
# def clean(line):
#     """对一个文件的数据进行清洗"""
#     URL_REGEX = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',re.IGNORECASE)
#     n_alls=[]
#     pattern_0=re.compile('#.*?#')#在用户名处匹配话题名称
#     pattern_1=re.compile('<a.*?</a>')#在内容处匹配图片地址
#     pattern_2=re.compile("(@.*? )+|(@.*)")#匹配首尾标点符号
#     pattern_3=re.compile('\d+')#匹配纯数字
#     pattern_4=re.compile(u'[\U00010000-\U0010ffff\uD800-\uDBFF\uDC00-\uDFFF]')#匹配表情
#     pattern_5=re.compile('(.*?)')#匹配一部分颜文字
#     pattern_6=re.compile(u'[\u4e00-\u9fa5]+')#匹配中文
#     try:#没有匹配到的情况解决
#         h_0=re.search(pattern_0,line[1]).group()
#     except:
#         h_0=' '
#     try:
#         h_1=re.search(pattern_1,line[2]).group()
#     except:
#         h_1=' '
#     try:
#         h_2=re.search(pattern_2,line[2]).group()#转换为str
#     except:
#         h_2=' '
#     try:
#         h_3=re.search(pattern_3,line[2]).group()
#     except:
#         h_3='占位符'
#     line[1]=line[1].replace(h_0,'')
#     line[1]=line[1].replace('超话社区','')#去除无意义名称
#     line[2]=line[2].replace(h_1,'')
#     line[2]=line[2].replace(h_2,'')#清除无用字符
#     rep=['回复:','回复的表态','图片评论 ','图片评论','//:  ','【】','【','】','转发微博','下午好','下午好','👍','🤝','。。','外交部：','信息发布微平台',
#          '扩散','信息发布的微平台','🐮','🙏','🇨🇳','👏','❤️','………','信息传播微平台','🐰','...、、','，，','..','💪','🤓','晚安吉祥！',
#          '来互动喽','来看看哦','收藏了','看一下。','点个赞','来看看哦','我来看看你','啊啊啊啊啊啊啊啊！','嘿嘿嘿嘿嘿、嘿','划重点！划重点！',
#          '天啦噜','⚕️','👩','转发','🙃','😇','🍺','🐂','🙌🏻','😂','📖','😭','赞赞','✧٩(ˊωˋ*)و✧','🦐','？？？？','//','😊','💰','😜','😯',
#          '(ღ˘⌣˘ღ)','✧＼٩(눈౪눈)و/／✧','传递信息微平台','🌎','传递新闻资讯~','🍀','传递有用的信息','？？','🐴','扩散周知','转！',
#          '转发周知','🌻','🌱','🌱','🌻','收藏转发～～～','🙈','优质内容','信息发布微平台！！！','(ง•̀_•́)ง！','🉑️','直播！','💩','信息发布微平台！',
#          '🐎','⊙∀⊙！','🙊','【？','+1','菲总统府：','😄','🙁','早安','午安','晚安','你想知道的都在这！','👇🏻','📚','🙇','收藏','【《面对面》正在播出：！】',
#          '🙋','康康','深夜好','占个位置','！！！！','🎉','＼(^▽^)／','👌','晚上好','【最全解答！】','🆒','🏻','上午好','下午好','晚上好','深夜好',
#          '🙉','🎵','🎈','🎊','0371-12345','☕️','🌞','😳','👻','🐶','👄','\U0001f92e\U0001f92e','😔','＋1','🛀','🐸','🐷','新闻1》|？','➕1',
#          '🌚','：：','💉','√','x','！！！','🙅','♂️','💊','👋','o(^o^)o','mei\u2006sha\u2006shi','💉','😪','早上好','😱','多互动','\U0001f9a0',
#          '🤗','关注','……','(((╹д╹;)))','⚠️','Ծ‸Ծ','⛽️','😓','🐵','了解','关注热点，传递正能量','传播法治正能量','传播法治正能量~！',
#          '传递法治力量','传播法治正能量传播法治正能量','信息发布微平','🙄️','已经','8⃣️','来串门','互动来啦','强者与弱者的分界就在于谁更愿意评论和点赞',
#          '🌕','新冠疫苗最快何时上市？8个最新权威问答来了！','…','😋','[]','[',']','→_→','💞','😨','&quot;','😁','ฅ۶•ﻌ•♡','😰','🎙️',
#          '🤧','😫','(ง•̀_•́)ง','😁','✊','🚬','😤','👻','😣','：','😷','(*^▽^)/★*☆','🐁','🐔','😘','🍋','(✪▽✪)','转收','马了','(❁´ω`❁)','1⃣3⃣','(^_^)／','☀️',
#          '🎁','😅','🌹','🏠','→_→','🙂','✨','❄️','•','🌤','💓','🔨','回复的表态','👏','的表态','趣图评论','转发','😏','⊙∀⊙！','👍','✌(̿▀̿\u2009̿Ĺ̯̿̿▀̿̿)✌',
#          '😊','👆','💤','😘','😊','😴','😉','🌟','♡♪..𝙜𝙤𝙤𝙙𝙣𝙞𝙜𝙝𝙩•͈ᴗ•͈✩‧₊˚','👪','💰','😎','🍀','🛍','🖕🏼','😂','(✪▽✪)','🍋','🍅','👀','♂️','🙋🏻','✌️','🥳','￣￣)σ',
#          '😒','😉','🦀','💖','✊','💪','关注热点，传递正能量','🙄','🎣','🌾','✔️','踩踩','欢迎互动','感谢分享，欢迎回访','😡','😌','🔥','❤',
#          '🏼','热点','热点，传递法治资讯','扩转周知','🤭','谢谢','热点，传递正能量','立足检察职能以检察视角各界动态','发布的信息',
#          '🌿','丨','✅','🏥','ﾉ','☀','5⃣⏺1⃣0⃣','te\u2006s\u2006t','世卫组织国药疫苗易储存，','法治ing','🚣','🎣','🤯','🌺','周三快乐！',
#          '急转','🌸','周知','午餐快乐！','推荐!','加v','博主v','设置闹钟，每天只需30秒点亮闪电，看教程下载注册，有不懂的微博私信我',
#          '注册挖矿','到时卖我','大写＋小写＋数学','已加','来了','转扩','蔡徐坤','！！','同问','唉。','传播正能量','，传播正能量'
#
#          ]
#     #太多无用字符，懒得添加在停用词表了
#     # if line[1].isspace()==False:#用户名不为空
#     for i in rep:
#         line[2]=line[2].replace(i,'')
#     line[2]=re.sub(pattern_1, '', line[2]) #去除链接文字混合中的链接
#     line[2]=re.sub(pattern_2, '', line[2]) #去除首尾标点
#     line[2]=re.sub(pattern_4, '', line[2]) #去除表情
#     line[2]=re.sub(pattern_5, '', line[2]) #去除一部分颜文字
#     # line[2]=re.sub(r'\[\S+\]', '', line[2]) #去除表情符号
#     line[2]= re.sub(URL_REGEX,'', line[2])# 去除网址
#     line[2]=line[2].replace('🈷️','月')#文字转换
#     line[2]=line[2].replace('🈚','无')
#     line[2]=line[2].replace('🉐️','得')
#     line[2]=line[2].replace('🈶','有')
#     line[2]=line[2].replace('9⃣️命','救命')
#     line[2]=line[2].replace('❓','？')
#     line[2]=line[2].replace('🍵','茶')
#     line[2]=line[2].replace('➕','加')
#     line[2]=line[2].replace('⛰️','山')
#     match_0=pattern_6.search(line[2])#判断是否包含中文字符
#     if line[2].isspace()==False:#内容不为空
#         for i in stoplist():
#             if line[2]!=i:#去停用词
#                 if line[2]!='':#不为空
#                     if len(line[2])>=20:#清除单字
#                         if line[2]!=h_3:#该字符串不是纯数字
#                             if line[2].isalpha()==False:#不是纯英文
#                                 if match_0:
#                                     if line not in n_alls:#去重
#                                         n_alls.append(line)
#     return n_alls
#
#
#
# def file(inpath):
#     """提取一个文件为一个大列表"""
#     data = xlrd.open_workbook(inpath, encoding_override='utf-8')
#     table = data.sheets()[0]#选定表
#     nrows = table.nrows#获取行号
#     ncols = table.ncols#获取列号
#     numbers=[]
#     for i in range(1, nrows):#第0行为表头
#         alldata = table.row_values(i)#循环输出excel表中每一行，即所有数据
#         numbers.append(alldata)
#     return numbers
#
# def save_afile(alls,filename):
#     """将一个基金的论文数据保存在一个excel"""
#     f=xlwt.Workbook()
#     sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
#     sheet1.write(0,0,'用户ID')
#     sheet1.write(0,1,'Comment_Name')
#     sheet1.write(0,2,'Comment_Content')
#     i=1
#     for data in alls:#遍历每一行
#         for j in range(len(data)):#取第一个元素的每一单元格
#             sheet1.write(i,j,data[j])#写入单元格
#         i=i+1#往下一行
#     f.save(filename)
#
# if __name__ == '__main__':
#     # filenames=os.listdir(r'评论_xlsx')#文件名
#     # for j in filenames:
#         items=file(r'WeiboComment.xls')
#         print(items)
#         pool = ThreadPool()
#         alls=pool.map(clean, items)#多线程和普通的列表嵌套不一样，是直接将列表里面的元素取出来了。而且输出是二次嵌套列表
#         pool.close()
#         pool.join()
#         #print(alls)
#         #去除空列表，将嵌套列表取出
#         alls_1=[]
#         n=[]
#         for i in alls:
#             if i!=n:
#                 alls_1.append(i[0])
#         save_afile(alls_1,'清洗评论.xls')
