import os
from wsgiref.simple_server import make_server

import numpy as np
import sklearn
import sklearn.model_selection as ms
import whois
from flask import Flask, redirect, url_for, request, render_template
from sklearn import svm
import js_features_extraction
import crawl_js
import re
import url_features_extraction
import train_javascript
import train_url

# 用flask类创建了一个实例app
app = Flask(__name__)


# route是修饰器，将URL绑定到函数
@app.route('/success/<value>')
def success(value):
    if value == 0:
        return '该网页为恶意网页'
    else:
        return '该网页为正常网页'


def crawl(url):
    html = crawl_js.down_html(url)
    # (html)
    print(url + "网页下载完成")
    # 提取js
    name = url.replace("https://", "").replace("http://", "")
    name = re.sub('[’!"#$%&\'()*+,/:;<>?@，。?★、…【】《》？“”‘’！[\\]^`{|}~]+', "", name)
    crawl_js.parse_html(html, name, url)
    crawl_js.js_link(html, name)
    print("保存完成...")


# 返回特征向量，是一个数组
def url_extract(url):
    status = []
    # 提取域名（域名也就是主机名）
    hostname = url
    h = [(x.start(0), x.end(0)) for x in re.finditer('https://|http://|www.|https://www.|http://www.', hostname)]
    z = int(len(h))
    if z != 0:
        y = h[0][1]
    hostname = hostname[y:]
    h = [(x.start(0), x.end(0)) for x in re.finditer('/', hostname)]
    z = int(len(h))
    if z != 0:
        hostname = hostname[:h[0][0]]
    # 多看文献考虑更改234的特征
    # append在列表末尾追加新的对象
    # 特征1 URL的长度
    status.append(url_features_extraction.url_length(url))
    # 特征2 短链接
    status.append(url_features_extraction.shortening_service(url))
    # 特征3 检查域名中是否出现@符号
    status.append(url_features_extraction.having_at_symbol(url))
    # 特征4 检查//符号后的字符个数
    status.append(url_features_extraction.double_slash_redirecting(url))
    # 特征5 检查/符号出现的次数
    status.append(url_features_extraction.double_slash_num(url))
    # 特征6 检查/符号出现的次数
    status.append(url_features_extraction.slash_num(url))
    # 特征7 检查%符号出现的次数
    status.append(url_features_extraction.percent_sign(url))
    # 特征8 检查-符号的存在
    status.append(url_features_extraction.prefix_suffix(hostname))

    # 特征9 http标志是否仅出现一次
    status.append(url_features_extraction.https_token(url))

    # # print(status)
    # s = str(status).replace("[", "").replace("]", "").replace(" ", "")
    # print(s)
    return status


# 返回一个1或者0
def url_detect(pre_url):
    tag_u = train_url.model.predict([pre_url])
    return tag_u


# 从js中提取特征向量
def js_extract():
    # 用来存储特征向量的数组
    path = 'D:\\PycharmProjects\\pythonProject\\test'
    # file是存放特征向量的
    file = open('D:\\PycharmProjects\\pythonProject\\src\\js_test.txt', 'a', encoding='utf-8')
    files = os.listdir(path)
    for f in files:
        filename = str(f)
        # 为每个文件创建特征向量
        vec = js_features_extraction.create_matrix(path, filename)
        v = str(vec).replace("[", "").replace("]", "").replace(" ", "")
        # print(v)
        file.write(v + "\n")
    file.close()


def js_detect():
    # 1.读取数据集
    path = 'D:\\PycharmProjects\\pythonProject\\src\\js_test.txt'
    # converters={4:Iris_label}中“9”指的是第10列：将第10列的str转化为label(number)
    data = np.loadtxt(path, dtype=float, delimiter=',')
    tag_j = train_javascript.classifier.predict(data)
    for t in tag_j:
        if t == 0:
            return 0
    return 1


@app.route('/detect', methods=['POST', 'GET'])
def detect():
    if request.method == 'POST':
        url = request.form['input']
        # 提取出该url中的js代码
        k = "URL检测正常，JavaScript检测正常，该网页为正常网页"
        # m是判断url的标志值
        pre_url = url_extract(url)
        m = url_detect(pre_url)
        if m == 0:
            k = "URL检测异常，无需进行JavaScript检测，该网页为异常网页"
        else:
            crawl(url)
            js_extract()
            n = js_detect()
            if n == 0:
                k = "URL检测正常，JavaScript检测异常，该网页为异常网页"
        return render_template("detect.html",result=k)
        # return redirect(url_for('success', value=k))
    else:
        url = request.form['input']
        # 提取出该url中的js代码
        k = "URL检测正常，JavaScript检测正常，该网页为正常网页"
        # m是判断url的标志值
        pre_url = url_extract(url)
        m = url_detect(pre_url)
        if m == 0:
            k = "URL检测异常，无需进行JavaScript检测，该网页为异常网页"
        else:
            crawl(url)
            js_extract()
            n = js_detect()
            if n == 0:
                k = "URL检测正常，JavaScript检测异常，该网页为异常网页"
        return render_template("detect.html",result=k)
        # return redirect(url_for('success', url=url))


# 象征着程序的主入口
if __name__ == '__main__':
    # 默认本机的5000端口
    server = make_server('127.0.0.1', 5000, app)
    server.serve_forever()
    app.run(debug=True)
