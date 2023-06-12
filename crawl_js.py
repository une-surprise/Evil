import requests  # 获取网页
from bs4 import BeautifulSoup  # 网页解析
import os  # 文件读写操作
import random  # 获取随机数
import time  # 获取随机时间
import re
import xlrd
from requests.adapters import HTTPAdapter

# 随机用户代理
user_agent = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]


def down_html(url):
    s = requests.Session()
    s.keep_alive = False  # 关闭多余的连接
    # 增加重试连接次数
    s.mount('http://', HTTPAdapter(max_retries=300))
    s.mount('https://', HTTPAdapter(max_retries=300))
    resp = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.36",
        'Connection': 'close'
    }
    # 连接
    try:
        r = s.get(url, headers=resp)
    except:
        print("Connection refused by the server..")
        print("Let me sleep for 5 seconds")
        print("ZZzzzz...")
        time.sleep(5)
    # 文本形式打印源码，返回；修改网页的编码方式
    r.encoding = r.apparent_encoding
    h = r.text
    # print(r.text)
    # 关闭request连接
    r.close()
    s.close()
    requests.session().close()
    return h


def parse_html(h, name, url):
    dir = "D:\\PycharmProjects\\pythonProject\\test" + "\\"
    soup = BeautifulSoup(h, "html.parser")
    js_list = soup.find_all("script")
    for js in js_list:
        # print(js)
        with open(dir + name + ".txt", "a", encoding="utf-8") as f:
            f.write(str(js))
    # 整个html里所有的script标签中的内容
    print(url + "网页解析并保存")


def js_link(html, name):
    # name是域名，也就是主机名
    try:
        soup = BeautifulSoup(html, "html.parser")
        # 在整个HTML中查找script的src内容
        js_links = soup.find_all("script", src=True)
        if js_links:
            for js_link in js_links:
                # 读取链接
                # u是一个URL
                link = js_link["src"]
                # 标准化链接格式
                if link.startswith('http:') or link.startswith('https:'):
                    u = "".join(link)
                else:
                    if link.startswith('//'):  # 如果链接没有http头，添上
                        u = "http:" + "".join(link)
                    else:
                        if link.startswith('/'):
                            u = "http://" + name + "" + "".join(link)
                        else:
                            u = "http://" + name + "/" + "".join(link)
                # 判断链接是否为.js类型的文件
                if ".js" in u:
                    u = u.replace(" ", "")
                    js = down_html(u)  # 下载网页链接内容
                    (filepath, tempfilename) = os.path.split(u)  # 分离文件路径和文件名，主要原因：文件名中有\将不能正确存储
                    (filename, extension) = os.path.splitext(tempfilename)  # 分离文件后缀，防止文件后有？等提交，将文件统一为.js格式
                    filename = re.sub('[’!"#$%&\'()*+,/:;<>?@，。?★、…【】《》？“”‘’！[\\]^`{|}~]+', "", filename)  # 去除特殊字符
                    # 保存的文件名是脚本文件的名字
                    save_js_link(js, filename)
        else:
            print("不包含此类脚本")
    except Exception as e:
        print('wrong' + e)


def save_js_link(js, name):
    dir = "D:\\PycharmProjects\\pythonProject\\test" + "\\"
    with open(dir + name + ".txt", "a", encoding="utf-8") as f:
        f.write(js)
    print("网页链接下载中...")

    # urls=url_from_mysql()
    # for url in urls:
    #     #url转换为str类型
    #     u="".join(url)
    #     #下载网页


if __name__ == '__main__':
    # excel = ("D:\\PycharmProjects\\pythonProject\\url_dataset\\top_url.xlsx")
    # sheet = excel.sheet_by_index(0)
    # # # 返回一个URL列表
    # url_data = sheet.col_values(0)
    # for url in url_data[60:65]:
    url = "http://www.Ebrun.com"
    html = down_html(url)
    # (html)
    print(url + "网页下载完成")
    # 提取js
    name = url.replace("https://", "").replace("http://", "")
    parse_html(html, name, url)
    js_link(html, name)
    print("保存完成...")
