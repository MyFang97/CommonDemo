import requests
from lxml import etree
import time
import threading
import os
import re

from selenium import webdriver  # 驱动浏览器
from selenium.webdriver import ActionChains  # 滑动
from selenium.webdriver.common.by import By  # 选择器
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys  # 键盘按键操作
from selenium.webdriver.support import expected_conditions as EC  # 等待所有标签加载完毕
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载完毕 寻找某些元素


# def write_video(name, video_url):
#     name = "./video/" + name.strip() + '.mp4'
#     if os.path.exists(name):
#         print('已存在')
#         return
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
#     }
#     requests.packages.urllib3.disable_warnings()
#     response = requests.get(video_url, headers=headers)
#     video = response.content
#     with open(name, "wb") as f:
#         f.write(video)
#     print(name, '开始下载')
#     # content_size = int(response.headers['content-length'])
#     # n = 1
#     # with open(name, "wb") as f:
#     #     print(name, '开始下载')
#     #     for i in response.iter_content(chunk_size=1024):
#     #         rate = n * 1024 / content_size
#     #         print("下载进度：{0:%}".format(rate))
#     #         f.write(i)
#     #         n += 1
#     #     print(name + "下载完成")
#     #     time.sleep(5)


def get_index(index_url):
    # 从首页获取二级页面地址，写入字典
    print('打开浏览器')
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=option)  # 调用Chrome 驱动，生成浏览器对象
    wait = WebDriverWait(browser, 10)  # 设置selenium等待浏览器加载完毕的最大等待时间
    wait1 = browser.implicitly_wait(10)  # 隐式等待：等待所有标签加载完毕
    # browser = webdriver.Chrome()
    browser.get(index_url)
    print('html')
    html = browser.page_source
    # 91
    # nodes = browser.find_elements_by_xpath('//*[@id="wrapper"]/div[1]/div[3]/div/div/div')  # //*[@id="wrapper"]/div[1]/div[3]/div/div/div
    # 41
    nodes = browser.find_elements_by_xpath('//*[@id="body-container"]/div[2]/div[2]/div[3]/div[1]/div/div')  # //*[@id="wrapper"]/div[1]/div[3]/div/div/div
    global video_dict
    for node in nodes:
        name = node.find_elements_by_tag_name('span')[2].text
        print(name)
        if name in video_dict:
            continue
        two_page_href = node.find_elements_by_tag_name('a')[0].get_attribute("href")
        print(two_page_href)
        video_dict[name] = two_page_href
    print(video_dict)
    browser.quit()


def get_video():
    # 获取二级页面内容，从二级页面获取视频连接，写入本地
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=option)  # 调用Chrome 驱动，生成浏览器对象
    # browser = webdriver.Chrome()
    # wait = WebDriverWait(browser, 10)  # 设置selenium等待浏览器加载完毕的最大等待时间
    wait1 = browser.implicitly_wait(10)  # 隐式等待：等待所有标签加载完毕
    global video_dict
    print('开始循环')
    for name, two_page_url in video_dict.items():
        print('打开二级页面' + two_page_url)
        try:
            browser.get(two_page_url)
            node_video = browser.find_elements_by_xpath('//*[@id="player_one_html5_api"]/source')
            m3u8_url = node_video[0].get_attribute('src')
            print('m3u8', m3u8_url)
            # vid = browser.find_element_by_xpath('//*[@id="VID"]').text # 视频id
            vid = browser.find_element_by_id('VID').text  # 视频id
            vid = m3u8_url.split('.m3u8')[0].split('/')[-1]
            print('vid', vid)
            mp4_dict[name] = m3u8_url
        except Exception as e:
            print(e)
            continue
        # 开启写入线程
        # base_url = <source src="https://v2.91p48.com/m3u8/419986/419986.m3u8?
        ts_url_list = get_ts_urls(m3u8_url)
        # write_video(name, video_url)
        print('ts_url_list', ts_url_list)
        base_url = "https://v2.91p48.com/m3u8/{}/".format(vid)
        print('base_url', base_url)
        write_thread = threading.Thread(target=write_video, args=(name, ts_url_list, base_url,))
        write_thread.start()
        browser.implicitly_wait(5)
        time.sleep(5)
    browser.quit()


# 从m3u8文件中取出并生成ts文件的下载链接
def get_ts_urls(m3u8_path):
    # urls = []
    print('进入ts解析')
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    response = requests.get(url=m3u8_path, headers=headers)
    res = response.text
    # print(res)
    ts = re.findall(r"/.*?\.ts", res, flags=re.S)
    print(len(ts), ts)
    return ts


def write_video(name, video_urls, base_url):
    name = "./video/" + name.strip() + '.mp4'

    if os.path.exists(name):
        print('已存在')
        return
    print(name, '开始下载')
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    requests.packages.urllib3.disable_warnings()
    times = 1
    for url in video_urls:
        response = requests.get(base_url + url, headers=headers)
        content_size = int(response.headers['content-length'])
        n = 1
        with open(name, "ab+") as f:
            for i in response.iter_content(chunk_size=1024):
                rate = n * 1024 / content_size
                # print("下载进度：{0:%}".format(rate))
                f.write(i)
                n += 1
        times += 1
        print('第' + str(times) + '次/共' + str(len(video_urls)) + '次：' + name + "下载完成")
        time.sleep(1)


if __name__ == '__main__':
    # 先运行get_index获取video_dict
    # 在复制video_dict运行get_video
    # index_url = 'https://810.workarea2.live/index.php' # 91
    # 41
    mp4_dict = {}
    video_dict = {}
    for num in range(1,2):
        index_url = 'http://41fa1.xyz/video/lists/orderCode/reco.html?orderCode=reco&tag_id=60&sub_cid=0&cid=14&page={}'.format(num)
        get_index(index_url)
    get_video()
