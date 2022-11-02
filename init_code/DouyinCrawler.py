import os
import re
import sys
import time
import requests
import xlwt
import you_get
from selenium import webdriver
from you_get import common



'''
功能：爬取抖音ID、用户名、用户评论、视频、抖音标题
使用方法：
在def DouyinCrawler(url)函数中 输入爬取的网站url 即可实现信息的爬取
在爬取完毕后会将数据以EXCEL表的形式存入当前目录，命名为：DouyinComment.xls
视频会存放在video文件夹中
'''
# def require(url):
#     headers={
#         'path': '/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7083293845496073510&cursor=80&count=20&item_type=0&rcFT=&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=99.0.4844.51&browser_online=true&engine_name=Blink&engine_version=99.0.4844.51&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=0&webid=7082249047388145183&msToken=QWSrXp1LBsAJx5ebu3Xk7Ngwx3nHhQVsOCDXXYdq3e_pA-zZ9fJQjIUvVtcXRt1QsuhdrP-F47kapoadK_ZlMkYZbtgFHK6gO7Yvg5_FOLbVyvxugb_Azp-WjXGZ4w9q&X-Bogus=DFSzswVL9c0ANr98SlqafGUClL9E&_signature=_02B4Z6wo00001OaWiIgAAIDBzRzTTsCKJKzmlowAAFvuTAqjP5WE9ZlERwOQJsQRqw5IfPL3OR3ay.tAxct-hAEFfBTSSxfJPx4JOtmjEkqpbIbXVBKVk9.Q5JXAJ9XdKE.-VfGi5xy9Lrxg23',
#         'referer': 'https://www.douyin.com/search/%E6%88%90%E9%83%BD%E7%96%AB%E6%83%85%E6%9C%80%E6%96%B0%E6%B6%88%E6%81%AF?source=recom_search&aid=3e537954-a78f-4f98-8bd9-0c8b01cd977b&enter_from=search_result',
#         'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
#         'sec-fetch-mode': 'cors',
#         'sec-fetch-site': 'same-origin',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
#         'cookie': 'ttwid=1|3io6PeRHfVVAUN6jLN1TXOFMVh65YdBtttV1qoqxEng|1648964616|eac543ab7eea1375686ab59473ee6754c1ef3bc7411b26ae33a92c86aa002cc3; _tea_utm_cache_6383=undefined; home_can_add_dy_2_desktop=0; passport_csrf_token=93e4c5e474347189b777170b1ccc64dd; passport_csrf_token_default=93e4c5e474347189b777170b1ccc64dd; AB_LOGIN_GUIDE_TIMESTAMP=1648964616819; _tea_utm_cache_1300=undefined; ttcid=8af5c82ed80c4a968221424b5f80914439; _tea_utm_cache_2018=undefined; d_ticket=8ddc58068f79de4352e3d4746c998639f2c9d; n_mh=jh7oPlpGH3_DxYv2V0bXs9NyISDrORg0eWZZZCormJM; passport_auth_status=b822b5c6908a089fb594e86b928e8653,; passport_auth_status_ss=b822b5c6908a089fb594e86b928e8653,; sso_auth_status=300ee4c1042c535975d524908a93b2a5; sso_auth_status_ss=300ee4c1042c535975d524908a93b2a5; sso_uid_tt=894cd3b45425849eaf0c2b958cf81c05; sso_uid_tt_ss=894cd3b45425849eaf0c2b958cf81c05; toutiao_sso_user=5ecfe57eec37bd47206a241495d3ce01; toutiao_sso_user_ss=5ecfe57eec37bd47206a241495d3ce01; sid_ucp_sso_v1=1.0.0-KDZiZmJlMGZkYmYyOWI4ZTk2NDhkYmI5ZjU5M2ZjZjM0MDgxYzM4NGQKHwjYteDKvvXaBRCl6KSSBhjvMSAMMPir-u0FOAJA8QcaAmxmIiA1ZWNmZTU3ZWVjMzdiZDQ3MjA2YTI0MTQ5NWQzY2UwMQ; ssid_ucp_sso_v1=1.0.0-KDZiZmJlMGZkYmYyOWI4ZTk2NDhkYmI5ZjU5M2ZjZjM0MDgxYzM4NGQKHwjYteDKvvXaBRCl6KSSBhjvMSAMMPir-u0FOAJA8QcaAmxmIiA1ZWNmZTU3ZWVjMzdiZDQ3MjA2YTI0MTQ5NWQzY2UwMQ; odin_tt=27b3404a8fa9cd5fb1095f380da39fe97a3eeeb9174b45156afd9505b5009a7f7331b03da8573e1c00acb626c65866b917d54a64fd9e7501c27bb54a4c67e1d2; sid_guard=5ecfe57eec37bd47206a241495d3ce01|1648964646|5184000|Thu,+02-Jun-2022+05:44:06+GMT; uid_tt=894cd3b45425849eaf0c2b958cf81c05; uid_tt_ss=894cd3b45425849eaf0c2b958cf81c05; sid_tt=5ecfe57eec37bd47206a241495d3ce01; sessionid=5ecfe57eec37bd47206a241495d3ce01; sessionid_ss=5ecfe57eec37bd47206a241495d3ce01; sid_ucp_v1=1.0.0-KDdmNzliODI1MDExNDEzZTRhZDA5NzQ5NmM3Y2RiYTMyMTNmMzNjMGUKHwjYteDKvvXaBRCm6KSSBhjvMSAMMPir-u0FOAJA8QcaAmxxIiA1ZWNmZTU3ZWVjMzdiZDQ3MjA2YTI0MTQ5NWQzY2UwMQ; ssid_ucp_v1=1.0.0-KDdmNzliODI1MDExNDEzZTRhZDA5NzQ5NmM3Y2RiYTMyMTNmMzNjMGUKHwjYteDKvvXaBRCm6KSSBhjvMSAMMPir-u0FOAJA8QcaAmxxIiA1ZWNmZTU3ZWVjMzdiZDQ3MjA2YTI0MTQ5NWQzY2UwMQ; _tea_utm_cache_2285=undefined; _tea_utm_cache_1243=undefined; MONITOR_WEB_ID=8d20cb13-f4fc-4a22-9dab-85a7b93493e8; THEME_STAY_TIME=299514; IS_HIDE_THEME_CHANGE=1; douyin.com; strategyABtestKey=1649225120.677; s_v_web_id=verify_l1n620lp_YRNU3Odn_wVtD_4Ws3_8lD7_RwdRcTRwYZWg; pwa_guide_count=3; NEW_HOME_VIDEO_CONSUMPTION_COUNT=4; msToken=wkPUW3u6KKDxYGuVaK-AEAEJfl3wXAa0c8ePwrE4nWV32M1bQ5dKb-YkDaQR1m5yEGrEIr4P6POv7HG-PhgUQpJr9nx4DSij08Ittq8rlP3-AmN6vkAMEDbFBz6qgkKp2A==; __ac_nonce=0624d3d1a00953cd8ab53; __ac_signature=_02B4Z6wo00f01DXNH7AAAIDBHkdEdGD.S9A17RsAAG9F8GrCQr2PLClNqygxHbyS3AemvEq7dZy32SLuObmFxQW4zjFeYfypvfWg1KziDkynny5F-VXtoi4sOdXSPlb.yeLIy15yy6I9Yi2Zf2; msToken=tTcNHwBsSp7mOzEbcYQfcOZzjhHtDiXsxoYv9PpOH7v_-0cgLuYlqoAt1Be7-faktjiXBqKbhHTesLU7tmvANe0EFn-rHlP2C6IfjjtS71K7ULaisPbwrdO6OpmqDkm8; tt_scid=ngzzUNOfZJdMRly0Eo8LZTGyd1vsDShAMvb1cdgCn74v4IRd1mzrxmda3WX3wXSQ2523'
#     }
#
#     try:
#         r = requests.get(url, headers=headers)
#         r.raise_for_status()
#         print(url)
#         return r.text
#     except requests.HTTPError as e:
#         print(e)
#     except requests.RequestException as e:
#         print(e)
#     except:
#         print("Unknow error")
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
# def Html(html):
#     #     获取所需内容
#     s=json.loads(html)
#     comment=s['comments']
#     for i in comment:
#         floor = i['aweme_id']
#         ctime = time.strftime("%Y-%m-%d",time.localtime(i['create_time']))
#         username=i['user']['nickname']
#         content=i['text']
#         list=[]
#         list.append(floor)
#         list.append(username)
#         list.append(content)
#         list.append(ctime)
#         com.append(list)
def download(url):
    # word = input('请输入链接： ')
    # url = 'https://www.douyin.com/video/6967296943450066214?previous_page=main_page'
    directory = r'../video'
    filepath ='../video/DouyinVideo.mp4'
    if (os.path.exists(filepath)):
        os.remove(filepath)
    headers = {
        'path': '/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7083293845496073510&cursor=80&count=20&item_type=0&rcFT=&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Chrome&browser_version=99.0.4844.51&browser_online=true&engine_name=Blink&engine_version=99.0.4844.51&os_name=Windows&os_version=10&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=0&webid=7082249047388145183&msToken=QWSrXp1LBsAJx5ebu3Xk7Ngwx3nHhQVsOCDXXYdq3e_pA-zZ9fJQjIUvVtcXRt1QsuhdrP-F47kapoadK_ZlMkYZbtgFHK6gO7Yvg5_FOLbVyvxugb_Azp-WjXGZ4w9q&X-Bogus=DFSzswVL9c0ANr98SlqafGUClL9E&_signature=_02B4Z6wo00001OaWiIgAAIDBzRzTTsCKJKzmlowAAFvuTAqjP5WE9ZlERwOQJsQRqw5IfPL3OR3ay.tAxct-hAEFfBTSSxfJPx4JOtmjEkqpbIbXVBKVk9.Q5JXAJ9XdKE.-VfGi5xy9Lrxg23',
        'referer': 'https://www.douyin.com/search/%E6%88%90%E9%83%BD%E7%96%AB%E6%83%85%E6%9C%80%E6%96%B0%E6%B6%88%E6%81%AF?source=recom_search&aid=3e537954-a78f-4f98-8bd9-0c8b01cd977b&enter_from=search_result',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'cookie': 'ttwid=1|3io6PeRHfVVAUN6jLN1TXOFMVh65YdBtttV1qoqxEng|1648964616|eac543ab7eea1375686ab59473ee6754c1ef3bc7411b26ae33a92c86aa002cc3; _tea_utm_cache_6383=undefined; home_can_add_dy_2_desktop=0; passport_csrf_token=93e4c5e474347189b777170b1ccc64dd; passport_csrf_token_default=93e4c5e474347189b777170b1ccc64dd; AB_LOGIN_GUIDE_TIMESTAMP=1648964616819; _tea_utm_cache_1300=undefined; ttcid=8af5c82ed80c4a968221424b5f80914439; _tea_utm_cache_2018=undefined; d_ticket=8ddc58068f79de4352e3d4746c998639f2c9d; n_mh=jh7oPlpGH3_DxYv2V0bXs9NyISDrORg0eWZZZCormJM; passport_auth_status=b822b5c6908a089fb594e86b928e8653,; passport_auth_status_ss=b822b5c6908a089fb594e86b928e8653,; sso_auth_status=300ee4c1042c535975d524908a93b2a5; sso_auth_status_ss=300ee4c1042c535975d524908a93b2a5; sso_uid_tt=894cd3b45425849eaf0c2b958cf81c05; sso_uid_tt_ss=894cd3b45425849eaf0c2b958cf81c05; toutiao_sso_user=5ecfe57eec37bd47206a241495d3ce01; toutiao_sso_user_ss=5ecfe57eec37bd47206a241495d3ce01; sid_ucp_sso_v1=1.0.0-KDZiZmJlMGZkYmYyOWI4ZTk2NDhkYmI5ZjU5M2ZjZjM0MDgxYzM4NGQKHwjYteDKvvXaBRCl6KSSBhjvMSAMMPir-u0FOAJA8QcaAmxmIiA1ZWNmZTU3ZWVjMzdiZDQ3MjA2YTI0MTQ5NWQzY2UwMQ; ssid_ucp_sso_v1=1.0.0-KDZiZmJlMGZkYmYyOWI4ZTk2NDhkYmI5ZjU5M2ZjZjM0MDgxYzM4NGQKHwjYteDKvvXaBRCl6KSSBhjvMSAMMPir-u0FOAJA8QcaAmxmIiA1ZWNmZTU3ZWVjMzdiZDQ3MjA2YTI0MTQ5NWQzY2UwMQ; odin_tt=27b3404a8fa9cd5fb1095f380da39fe97a3eeeb9174b45156afd9505b5009a7f7331b03da8573e1c00acb626c65866b917d54a64fd9e7501c27bb54a4c67e1d2; sid_guard=5ecfe57eec37bd47206a241495d3ce01|1648964646|5184000|Thu,+02-Jun-2022+05:44:06+GMT; uid_tt=894cd3b45425849eaf0c2b958cf81c05; uid_tt_ss=894cd3b45425849eaf0c2b958cf81c05; sid_tt=5ecfe57eec37bd47206a241495d3ce01; sessionid=5ecfe57eec37bd47206a241495d3ce01; sessionid_ss=5ecfe57eec37bd47206a241495d3ce01; sid_ucp_v1=1.0.0-KDdmNzliODI1MDExNDEzZTRhZDA5NzQ5NmM3Y2RiYTMyMTNmMzNjMGUKHwjYteDKvvXaBRCm6KSSBhjvMSAMMPir-u0FOAJA8QcaAmxxIiA1ZWNmZTU3ZWVjMzdiZDQ3MjA2YTI0MTQ5NWQzY2UwMQ; ssid_ucp_v1=1.0.0-KDdmNzliODI1MDExNDEzZTRhZDA5NzQ5NmM3Y2RiYTMyMTNmMzNjMGUKHwjYteDKvvXaBRCm6KSSBhjvMSAMMPir-u0FOAJA8QcaAmxxIiA1ZWNmZTU3ZWVjMzdiZDQ3MjA2YTI0MTQ5NWQzY2UwMQ; _tea_utm_cache_2285=undefined; _tea_utm_cache_1243=undefined; MONITOR_WEB_ID=8d20cb13-f4fc-4a22-9dab-85a7b93493e8; THEME_STAY_TIME=299514; IS_HIDE_THEME_CHANGE=1; douyin.com; strategyABtestKey=1649225120.677; s_v_web_id=verify_l1n620lp_YRNU3Odn_wVtD_4Ws3_8lD7_RwdRcTRwYZWg; pwa_guide_count=3; NEW_HOME_VIDEO_CONSUMPTION_COUNT=4; msToken=wkPUW3u6KKDxYGuVaK-AEAEJfl3wXAa0c8ePwrE4nWV32M1bQ5dKb-YkDaQR1m5yEGrEIr4P6POv7HG-PhgUQpJr9nx4DSij08Ittq8rlP3-AmN6vkAMEDbFBz6qgkKp2A==; __ac_nonce=0624d3d1a00953cd8ab53; __ac_signature=_02B4Z6wo00f01DXNH7AAAIDBHkdEdGD.S9A17RsAAG9F8GrCQr2PLClNqygxHbyS3AemvEq7dZy32SLuObmFxQW4zjFeYfypvfWg1KziDkynny5F-VXtoi4sOdXSPlb.yeLIy15yy6I9Yi2Zf2; msToken=tTcNHwBsSp7mOzEbcYQfcOZzjhHtDiXsxoYv9PpOH7v_-0cgLuYlqoAt1Be7-faktjiXBqKbhHTesLU7tmvANe0EFn-rHlP2C6IfjjtS71K7ULaisPbwrdO6OpmqDkm8; tt_scid=ngzzUNOfZJdMRly0Eo8LZTGyd1vsDShAMvb1cdgCn74v4IRd1mzrxmda3WX3wXSQ2523'
    }
    response = requests.get(url=url, headers=headers)
    html_data = re.findall('src(.*?)%253D%2', response.text)[0]
    dem = requests.utils.unquote(html_data)
    print(html_data)
    video_url = html_data.replace('%2F', '/').replace('%22%3A%22', 'https:').replace('%3F', '?').replace('%26', '&')
    video_url = re.sub(r'.*https', 'https', video_url)
    sys.argv = ['you-get','-o',directory,'-O','DouyinVideo','--no-caption',video_url]
    # common.any_download(url=video_url, stream_id='mp4', info_only=False, output_dir=directory, merge=True)
    you_get.main()
def Douyinselenium(url):
    userData=[]
    driver = webdriver.Chrome("../chromedriver.exe")
    driver.get(url)
    time.sleep(3)
    try:
        click = driver.find_element_by_xpath('//*[@id="login-pannel"]/div[2]')
        click.click()
        time.sleep(0.5)
    except:
        print("没有该元素，正常爬取中")
    try:
        click2=driver.find_element_by_xpath('//*[@id="verify-bar-close"]')
        click2.click()
    except:
        print("没有该元素，正常爬取中")
    topic=driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div[1]/div[1]/div[3]/div/div[1]/div').text
    driver.execute_script('window.scrollBy(0,2000)')
    for count in range(1, 21):
        id = str(count)
        comment = driver.find_element_by_xpath(
            ' // *[ @ id = "root"] / div / div[2] / div / div / div[1] / div[3] / div / div / div[4] / div['+str(count)+'] / div / div[2] / \
                               div[1] / p').text

        username = driver.find_element_by_xpath(
            '//*[@id="root"]/div/div[2]/div/div/div[1]/div[3]/div/div/div[4]/div[' + str(
                count) + ']/div/div[2]/div[1]/div[2]/div[1]/div/a/span/span/span/span/span').text
        datetime = driver.find_element_by_xpath(
            '//*[@id="root"]/div/div[2]/div/div/div[1]/div[3]/div/div/div[4]/div[' + str(
                count) + ']/div/div[2]/div[1]/div[2]/div[1]/p').text
        time.sleep(0.5)
        if len(username)==0:
            count-=1
        else:
            if len(comment)==0:
                comment="空"
            datetime = datetime.replace('.', '-')
            single=[id, username ,comment ,datetime]
            userData.append(single)
        driver.execute_script('window.scrollBy(0,150)')
    driver.quit()
    return userData,topic
def DouyinCrawler(url):
    download(url)
    data,topic=Douyinselenium(url)
    save_afile(data,"douyin_comment")
    return topic
# print(DouyinCrawler("https://www.douyin.com/video/7096325380675554591"))
