"""
https://wm.cwttx.xyz/
无名网视频爬取
"""

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


def get_index(index_url):
    # 从首页获取二级页面地址，写入字典
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=option)  # 调用Chrome 驱动，生成浏览器对象
    # wait = WebDriverWait(browser, 10)  # 设置selenium等待浏览器加载完毕的最大等待时间
    wait1 = browser.implicitly_wait(10)  # 隐式等待：等待所有标签加载完毕
    try:
        browser.get(index_url)
        html = browser.page_source
        nodes = browser.find_elements_by_xpath(
            '//*[@id="wrapper"]/div[1]/div[3]/div/div/div')  # //*[@id="wrapper"]/div[1]/div[3]/div/div/div
        global video_dict
        for node in nodes:
            name = node.find_elements_by_tag_name('span')[1].text
            print(name)
            if name in video_dict:
                continue
            two_page_href = node.find_elements_by_tag_name('a')[0].get_attribute("href")
            print(two_page_href)
            video_dict[name] = two_page_href
        print(video_dict)
        browser.quit()
    except Exception as e:
        print(e)


def from_two_get_mp4():
    # 获取二级页面内容，从二级页面获取视频连接，写入本地
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=option)  # 调用Chrome 驱动，生成浏览器对象
    # browser = webdriver.Chrome()  # 调用Chrome 驱动，生成浏览器对象
    # wait = WebDriverWait(browser, 10)  # 设置selenium等待浏览器加载完毕的最大等待时间
    wait1 = browser.implicitly_wait(10)  # 隐式等待：等待所有标签加载完毕
    global video_dict
    print('开始循环')

    for name, two_page_url in video_dict.items():
        print('打开二级页面' + two_page_url)
        try:
            browser.get(two_page_url)
            first_m3u8 = browser.find_elements_by_xpath('//*[@id="player_one_html5_api"]/source')[0].get_attribute(
                'src')
            print('first_m3u8', first_m3u8)
            # https://cdn.91p07.com//m3u8/425137/425137.m3u8?st=HfdF9y-44EUa4KJ5OObx4g&e=1610534301&f=7c35O7FdKR/UVyQ1QGWYAnh4gtE0CcxbFZJ8sXU3flyNiftLGh/wgaIIT2hT48QGKf8IU32JS8LSR5qgHxrgm+XH1vdUcvVF9FEUrQ
            # base_url = 'https://cdn.91p07.com//m3u8/425137/'
            base_url = first_m3u8[:10]
            # final_m3u8_url = get_two_m3u8(first_m3u8, base_url)
            # print(final_m3u8_url)
            """直接获取m3u8,所以注释掉"""
            # video_urls = get_ts_urls(first_m3u8)
            # mp4_dict[name] = video_urls
        except Exception as e:
            print(e)
            continue
        # 开启写入线程
        video_urls = []
        video_urls.append(first_m3u8)
        print(name, video_urls)
        # print(name,first_m3u8)
        # write_video(name, video_url)
        write_thread = threading.Thread(target=write_video, args=(name, video_urls, base_url))
        write_thread.start()
        browser.implicitly_wait(5)
        time.sleep(5)
    browser.quit()


def get_two_m3u8(first_m3u8_path, base_url):
    print('进入获取two——m3u8')
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    global proxy
    response = requests.get(url=first_m3u8_path, headers=headers, proxies=proxy)
    res = base_url + response.text.split('\n')[2]
    return res


# 从m3u8文件中取出并生成ts文件的下载链接
def get_ts_urls(m3u8_path):
    # urls = []
    print('进入ts解析')
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    print('m3u8_path', m3u8_path)
    global proxy
    response = requests.get(url=m3u8_path, headers=headers, proxies=proxy)
    res = response.text
    print(res)
    ts = re.findall(r"\d{7}.*?\.ts", res, flags=re.S)
    print(len(ts), ts)
    return ts


def write_video(name, video_urls, base_url):
    name = "D:\\Desktop\\spiderTest\\video\\a\\" + name.strip() + '.mp4'

    if os.path.exists(name):
        print('已存在')
        return
    print(name, '开始下载')
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    requests.packages.urllib3.disable_warnings()
    times = 0
    for url in video_urls:
        print('视频请求路径', url)
        global proxy
        response = requests.get(url, headers=headers, proxies=proxy)
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
    mp4_dict = {}
    video_dict = {
        # '肛塞肉棒同时插入 淫荡学妹高潮不断': 'https://810.workarea2.live/view_video.php?viewkey=32314fbcf24e80a7390c&page=16&viewtype=basic&category=rf',
        # '把表嫂露脸的视频也分享给大家，TOU拍的不是很好，很刺激，贵在真实！': 'https://810.workarea2.live/view_video.php?viewkey=f7cb7bd7fae60ec3cde6&page=16&viewtype=basic&category=rf',
        # '女神下班后2': 'https://810.workarea2.live/view_video.php?viewkey=24ecbcb380cb2e55b1df&page=16&viewtype=basic&category=rf',
        # '君君首次3p': 'https://810.workarea2.live/view_video.php?viewkey=33fe492696dfb2da308f&page=16&viewtype=basic&category=rf',
        # '露脸大胸少妇淫荡口交做爱': 'https://810.workarea2.live/view_video.php?viewkey=116005c8ca1390332951&page=16&viewtype=basic&category=rf',
        # '露脸94年舞蹈小骚妻，极品颜值身材，足交无套，最后颜射，想操她的留言': 'https://810.workarea2.live/view_video.php?viewkey=3f4fe6db730a8af2b3df&page=16&viewtype=basic&category=rf',
        # '白丝吊带女神在落地窗前摁着被操': 'https://810.workarea2.live/view_video.php?viewkey=89b0d693faab9ae78d4b&page=16&viewtype=basic&category=rf',
        # '趁着孩子不在家和老婆在浴室干柴烈火的就搞起来了。': 'https://810.workarea2.live/view_video.php?viewkey=a896f63ecd33d1ca2f83&page=16&viewtype=basic&category=rf',
        # '露脸人妻熟女勾引到她家疯狂无套啪啪，射精第一视角': 'https://810.workarea2.live/view_video.php?viewkey=657f09c5649e46410426&page=16&viewtype=basic&category=rf',
        # '[微剧情]牌瘾少妇被老公麻将桌边就地正法': 'https://810.workarea2.live/view_video.php?viewkey=47aac9a13d3a322bc45a&page=16&viewtype=basic&category=rf',
        # '原创投稿 3p之被单男操爽了说让老公在旁边看 内射白虎 对白极度淫荡': 'https://810.workarea2.live/view_video.php?viewkey=5b9520fb8c11ce766455&page=16&viewtype=basic&category=rf',
        # '连云港极品小教师饥渴难耐来找我': 'https://810.workarea2.live/view_video.php?viewkey=8c6873ae0660043668e2&page=16&viewtype=basic&category=rf',
        # '半夜老婆想要好久没做的她被操的白浆直流。允许我内射': 'https://810.workarea2.live/view_video.php?viewkey=883181e6f0ef4e9e2537&page=16&viewtype=basic&category=rf',
        # 'JK装，潮喷。4K画质，超敏感阴蒂。极品骚货。阴道超级会收缩': 'https://810.workarea2.live/view_video.php?viewkey=803f0e0aa8d2f48712cb&page=16&viewtype=basic&category=rf',
        # 'E奶女神新买的高叉连体内衣': 'https://810.workarea2.live/view_video.php?viewkey=99af2f77d8f5930a4cb1&page=16&viewtype=basic&category=rf',
        '这种臀部不打不行': 'https://810.workarea2.live/view_video.php?viewkey=f4b869a661e424797556&page=16&viewtype=basic&category=rf',
        '去熟女出租房给她推油按摩': 'https://810.workarea2.live/view_video.php?viewkey=90b68214b4a1229a7cf5&page=16&viewtype=basic&category=rf',
        '奴性非常好的大三艺术学院大长腿女神': 'https://810.workarea2.live/view_video.php?viewkey=9fbe9f548e78432ed455&page=16&viewtype=basic&category=rf',
        '尝试下商场女厕所': 'https://810.workarea2.live/view_video.php?viewkey=92723e1b773115f64bde&page=16&viewtype=basic&category=rf',
        '哥不在，怀孕嫂子我照顾，完整版下翻': 'https://810.workarea2.live/view_video.php?viewkey=48e46de2988c460d5918&page=16&viewtype=basic&category=rf',
        '颜射刺激 御姐型寂寞少妇': 'https://810.workarea2.live/view_video.php?viewkey=b0d9804cc0eebeec4fd4&page=16&viewtype=basic&category=rf',
        '刺激！火车窗前露出调教，旁边有人就操起来了！！结尾举牌验证！剪辑完整': 'https://810.workarea2.live/view_video.php?viewkey=2099bb1906bf02088a33&page=16&viewtype=basic&category=rf',
        '叫我老王—续主题酒店': 'https://810.workarea2.live/view_video.php?viewkey=78a2d5e7d956577d83e6&page=16&viewtype=basic&category=rf',
        '露脸居家熟女疯狂啪啪骚浪淫叫': 'https://810.workarea2.live/view_video.php?viewkey=deafc408aaa6a521e462&page=16&viewtype=basic&category=rf',
        '熟妇糟糠之妻和邻家老王在做爱做的事': 'https://810.workarea2.live/view_video.php?viewkey=f6ffe4468ba0531157b3&page=17&viewtype=basic&category=rf',
        '申精！极骚女主重磅回归！听声能射！看jie': 'https://810.workarea2.live/view_video.php?viewkey=8d0d735443a54d5519a5&page=17&viewtype=basic&category=rf',
        '口交。肛交。22岁的小骚货，真的是天生就是母狗的料，': 'https://810.workarea2.live/view_video.php?viewkey=9cd7a73438d80f64d96f&page=17&viewtype=basic&category=rf',
        '技师上门服务老婆': 'https://810.workarea2.live/view_video.php?viewkey=6e875dbf23131d18cd16&page=17&viewtype=basic&category=rf',
        '和170黑丝空姐女友在家里休假，啊': 'https://810.workarea2.live/view_video.php?viewkey=a6924349ddc193b6d14e&page=17&viewtype=basic&category=rf',
        '骑乘熟女人妻激情啪啪呻吟骚叫不断。。又高潮了': 'https://810.workarea2.live/view_video.php?viewkey=9b405f1b47c2c6088fdf&page=17&viewtype=basic&category=rf',
        '连云港极品教师之私人影院激情做爱': 'https://810.workarea2.live/view_video.php?viewkey=1049327d91dbd1b89560&page=17&viewtype=basic&category=rf',
        '约会露脸美艳熟女酒店疯狂啪啪淫叫高潮': 'https://810.workarea2.live/view_video.php?viewkey=ebc4c20285fb09f0f606&page=17&viewtype=basic&category=rf',
        '连云港极品缠着我疯狂做爱的23岁完美人民教师': 'https://810.workarea2.live/view_video.php?viewkey=701c44c8056655b9e831&page=17&viewtype=basic&category=rf',
        '风骚人妻熟女激情啪啪美穴第一视角': 'https://810.workarea2.live/view_video.php?viewkey=084ffc7aee1bee5e3c81&page=17&viewtype=basic&category=rf',
        '我既然上了一个四十大几的妇女逼还那么黑': 'https://810.workarea2.live/view_video.php?viewkey=cc347e6461b8bc889d15&page=17&viewtype=basic&category=rf',
        '性感皮裤黑丝淫欲打电话两部': 'https://810.workarea2.live/view_video.php?viewkey=ab4d04431272bca70ec0&page=17&viewtype=basic&category=rf',
        '028奥迪销售上下两张嘴果然厉害': 'https://810.workarea2.live/view_video.php?viewkey=abe049cec257d01d35a3&page=17&viewtype=basic&category=rf',
        '00后极品巨乳学生妹骑屌淫叫高潮': 'https://810.workarea2.live/view_video.php?viewkey=3c5ee5149cad4da57c76&page=17&viewtype=basic&category=rf',
        '完美女神又来挨操了': 'https://810.workarea2.live/view_video.php?viewkey=0fa9893cf12f3c704b78&page=17&viewtype=basic&category=rf',
        '孕期也挡不住的性欲旺盛': 'https://810.workarea2.live/view_video.php?viewkey=863faf0e1c76c86c0fde&page=17&viewtype=basic&category=rf',
        '美甲女友蒙眼唾液口交，口内射精': 'https://810.workarea2.live/view_video.php?viewkey=cda03c1729c4487d720a&page=17&viewtype=basic&category=rf',
        '女神母狗，长腿黑丝内射~露脸': 'https://810.workarea2.live/view_video.php?viewkey=ce1d92743c72de638bdd&page=17&viewtype=basic&category=rf',
        '药物发作真实3P，她老公打电话来了': 'https://810.workarea2.live/view_video.php?viewkey=044e053258c569f00a24&page=17&viewtype=basic&category=rf',
        '南京3p大屌单男骑操母狗女友的骚逼，给干肿了': 'https://810.workarea2.live/view_video.php?viewkey=8a5a3fdba0c14b107851&page=17&viewtype=basic&category=rf',
        '露脸、超嫩年轻女模特情趣酒店淫欲内射': 'https://810.workarea2.live/view_video.php?viewkey=942882955cb5bca0f28a&page=17&viewtype=basic&category=rf',
        '黑丝高跟长腿大堂经理为了业绩出轨客户': 'https://810.workarea2.live/view_video.php?viewkey=0836962366ea3fc1b923&page=17&viewtype=basic&category=rf',
        '各种姿势猛操内射漂亮蜂腰小女友！': 'https://810.workarea2.live/view_video.php?viewkey=97b3ee2b135eea7a3d09&page=17&viewtype=basic&category=rf',
        '开大音量！被我操到哀嚎的大学生': 'https://810.workarea2.live/view_video.php?viewkey=a9b64a3f79740e00d284&page=18&viewtype=basic&category=rf',
        '和艺术生小姐姐': 'https://810.workarea2.live/view_video.php?viewkey=491d7f7af666afe88d2d&page=18&viewtype=basic&category=rf',
        '火车后入98年小仙女，差点被乘务员发现！！原创ID验证！': 'https://810.workarea2.live/view_video.php?viewkey=6c4ba0477369f4fbd118&page=18&viewtype=basic&category=rf',
        '破处干哭178女神': 'https://810.workarea2.live/view_video.php?viewkey=1a373151f4975f884a45&page=18&viewtype=basic&category=rf',
        '露脸全程边打电话边艹逼完整版！': 'https://810.workarea2.live/view_video.php?viewkey=a98b52b454503d820393&page=18&viewtype=basic&category=rf',
        '说起男朋友：18岁小母狗羞耻中高潮': 'https://810.workarea2.live/view_video.php?viewkey=4154a1166b1275ba1000&page=18&viewtype=basic&category=rf',
        '申精！郑州风骚新婚人妻，露脸淫语不断': 'https://810.workarea2.live/view_video.php?viewkey=67b4c4ce1e5a1105ccfe&page=18&viewtype=basic&category=rf',
        'A37高铁乘务员少妇迷上出轨上（附聊天记录）': 'https://810.workarea2.live/view_video.php?viewkey=a1054fcbab5eb9eb5bb6&page=18&viewtype=basic&category=rf',
        '（洋妞）白人美女跟中国男朋友': 'https://810.workarea2.live/view_video.php?viewkey=cfb0555a7aa9db507bef&page=18&viewtype=basic&category=rf',
        '[微剧情]把小偷当老公啪啪，电话来了怎么办？': 'https://810.workarea2.live/view_video.php?viewkey=30ce95d954019916bac0&page=18&viewtype=basic&category=rf',
        '全程给老公打电话！刺激无限': 'https://810.workarea2.live/view_video.php?viewkey=08b8a4a4bb4d153f2204&page=18&viewtype=basic&category=rf',
        '我回来了~调教白丝小猫咪高材生，喝尿肛交灌肠': 'https://810.workarea2.live/view_video.php?viewkey=5c61c34cd9dd1947548a&page=18&viewtype=basic&category=rf',
        '多次神级潮吹 ，最新2020收官之战已上新 里程碑作品': 'https://810.workarea2.live/view_video.php?viewkey=247571b2e90a454b899c&page=18&viewtype=basic&category=rf',
        '男朋友不在真的太开心了': 'https://810.workarea2.live/view_video.php?viewkey=291e45a08fd6cc5f0055&page=18&viewtype=basic&category=rf',
        '身材巨顶的短发健身小姐姐': 'https://810.workarea2.live/view_video.php?viewkey=02d666f5afdf1fbb22d2&page=18&viewtype=basic&category=rf',
        '淫娃新娘回来了！全第一人称集合，风骚加倍淫语升级': 'https://810.workarea2.live/view_video.php?viewkey=eb7bde2678b1d16f76da&page=18&viewtype=basic&category=rf',
        '极品少妇自拍': 'https://810.workarea2.live/view_video.php?viewkey=368dd7946a8691f42133&page=18&viewtype=basic&category=rf',
        '骚货黑丝情趣': 'https://810.workarea2.live/view_video.php?viewkey=813e19411d93a1b41616&page=18&viewtype=basic&category=rf',
        '3p连续内射 中途接两次电话 被听出来了 对白刺激！': 'https://810.workarea2.live/view_video.php?viewkey=a7f5059d95a666cdd67a&page=18&viewtype=basic&category=rf',
        '潮吹！可爱女神被操喷 腿发软站不稳': 'https://810.workarea2.live/view_video.php?viewkey=b1cdba1f7b01d122c50e&page=18&viewtype=basic&category=rf',
        '露脸勾引别人的女朋友给她男朋友戴绿帽子很淫荡': 'https://810.workarea2.live/view_video.php?viewkey=fe786df33e0bdfe8db00&page=18&viewtype=basic&category=rf',
        '电影院再战女神同事小姐姐': 'https://810.workarea2.live/view_video.php?viewkey=2e955fd31832b5643c05&page=18&viewtype=basic&category=rf',
        '高颜值蜂腰美奶女神小护士在家插入后秒骚': 'https://810.workarea2.live/view_video.php?viewkey=537fa239b4507838ad5f&page=18&viewtype=basic&category=rf',
        '露脸晚上女友她累了想休息，让她吃完鸡巴和精液再休息': 'https://810.workarea2.live/view_video.php?viewkey=f01bfd9048c284af38ca&page=18&viewtype=basic&category=rf',
        '边跟男友打电话边被操 最后内射': 'https://810.workarea2.live/view_video.php?viewkey=00a2414cb737e0c471a7&page=19&viewtype=basic&category=rf',
        '成都3p调教我的骚母狗': 'https://810.workarea2.live/view_video.php?viewkey=fd95c145478a439d9172&page=19&viewtype=basic&category=rf',
        '百人斩第三十一部 露脸无套极品双马尾 双马尾特辑二': 'https://810.workarea2.live/view_video.php?viewkey=c07a4fd6a7248602b0e7&page=19&viewtype=basic&category=rf',
        '兄弟们爱看的电影院小姐姐后续': 'https://810.workarea2.live/view_video.php?viewkey=8d0333cf7a23b23b7804&page=19&viewtype=basic&category=rf',
        '家教严厉的学生妹，完整版下翻': 'https://810.workarea2.live/view_video.php?viewkey=d9f63be8f814e3f119fb&page=19&viewtype=basic&category=rf',
        '这些年操过的极品骚货': 'https://810.workarea2.live/view_video.php?viewkey=384cb52c76af59efc0e4&page=19&viewtype=basic&category=rf',
        '后入黑丝老婆': 'https://810.workarea2.live/view_video.php?viewkey=8442ad9b38c9ea35ca43&page=19&viewtype=basic&category=rf',
        '这家KTV的小妹真是啥都能玩，边草边唱歌': 'https://810.workarea2.live/view_video.php?viewkey=557a0c0e490c532d3e90&page=19&viewtype=basic&category=rf',
        '电影院里草黑丝极品身材的女神，不看后悔系列！！！': 'https://810.workarea2.live/view_video.php?viewkey=d0c7056cf912a6b6cbad&page=19&viewtype=basic&category=rf',
        '操熟女抓着她的小腰上下永动机荷尔蒙快要爆炸': 'https://810.workarea2.live/view_video.php?viewkey=b284e043558091dacb61&page=19&viewtype=basic&category=rf',
        '大阴唇美女玩SM，灌肠，操屁眼，被操到喷水，': 'https://810.workarea2.live/view_video.php?viewkey=9191dfee8d512d7285be&page=19&viewtype=basic&category=rf',
        '按摩擦枪走火 ，内射。这是DuDu，official web⬇️': 'https://810.workarea2.live/view_video.php?viewkey=d688c96e2c57c30d38e2&page=19&viewtype=basic&category=rf',
        '露脸朋友的少妇情人叫来自己闺蜜一起玩4P': 'https://810.workarea2.live/view_video.php?viewkey=3e51ed593d23ec8d5203&page=19&viewtype=basic&category=rf',
        '小哥哥给巨臀露脸富婆推油按摩爱爱（大奶肥熟女老女大妈偷情自拍）': 'https://810.workarea2.live/view_video.php?viewkey=77fb2c906e4e4408f35e&page=19&viewtype=basic&category=rf',
        '周末主题酒店约E奶肥臀妹纸': 'https://810.workarea2.live/view_video.php?viewkey=6b49656d5c970625783a&page=19&viewtype=basic&category=rf',
        '开车时舔鸡巴真刺激，受不了停车就开操': 'https://810.workarea2.live/view_video.php?viewkey=76888a9c744c975a85cc&page=19&viewtype=basic&category=rf',
        '特写内射巨臀美女，单粗暴就好': 'https://810.workarea2.live/view_video.php?viewkey=41fbc3e62b4d1339efa9&page=19&viewtype=basic&category=rf',
        '晨勃难受卫生间来一发，每天一发其乐无穷啊': 'https://810.workarea2.live/view_video.php?viewkey=25253984073cc9472b9e&page=19&viewtype=basic&category=rf',
        '3P极度淫荡E奶少妇': 'https://810.workarea2.live/view_video.php?viewkey=8a656d3554bb465661f2&page=19&viewtype=basic&category=rf',
        '约别人的老婆然后把她操哭': 'https://810.workarea2.live/view_video.php?viewkey=ae9943389d3f46b87289&page=19&viewtype=basic&category=rf',
        '露脸福利，兄弟们爱看的KTV小妹结局': 'https://810.workarea2.live/view_video.php?viewkey=a19e1ee337aa39417703&page=19&viewtype=basic&category=rf',
        '北京人前女神，胯下母狗~我的2020': 'https://810.workarea2.live/view_video.php?viewkey=e0eec1d185816ba13adc&page=19&viewtype=basic&category=rf',
        '18岁可爱高三少女沉沦在肛交的快感中': 'https://810.workarea2.live/view_video.php?viewkey=6a1361a6eceb18e4330f&page=19&viewtype=basic&category=rf',
        '家里人管得严，真实非演员，完整版下翻': 'https://810.workarea2.live/view_video.php?viewkey=00af48dac3f514d9ea39&page=19&viewtype=basic&category=rf'
    }
    proxy = None
    # index_url = 'https://810.workarea2.live/index.php'
    # for num in range(16, 20):
    #     index_url = 'https://810.workarea2.live/v.php?category=rf&viewtype=basic&page={}'.format(num)
    #     get_index(index_url)
    from_two_get_mp4()
