import re
import whois
import xlrd


# 1 url的长度，小于54判为正常
def url_length(url):
    if len(url) < 54:
        return 1
    elif len(url) >= 54:
        return 0


# 2 短链接服务 斟酌！
def shortening_service(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        return 0
    else:
        return 1


# 3 检查url中是够含有 @ 符号
def having_at_symbol(url):
    match = re.search('@', url)
    if match:
        return 0
    else:
        return 1


# 4 url中 最后的//字符的个数
def double_slash_redirecting(url):
    list = [x.start(0) for x in re.finditer('//', url)]
    if len(list) > 1:
        if list[len(list) - 1] > 4:
            return 0
    else:
        return 1


# 5 url中 // 出现的次数大于等于4次
def double_slash_num(url):
    list = [x.start(0) for x in re.finditer('//', url)]
    if len(list) > 3:
        return 0
    else:
        return 1


# 6 url中 /出现的次数大于等于5次
def slash_num(url):
    # since the position starts from, we have given 6 and not 7 which is according to the document
    list = [x.start(0) for x in re.finditer('/', url)]
    if len(list) > 4:
        return 0
    else:
        return 1


# 7 %出现的次数
def percent_sign(url):
    # since the position starts from, we have given 6 and not 7 which is according to the document
    list = [x.start(0) for x in re.finditer('%', url)]
    if len(list) > 4:
        return 0
    else:
        return 1


# 8 匹配 - 符号
def prefix_suffix(domain):
    match = re.search('-', domain)
    if match:
        return 0
    else:
        return 1


# 9 检查url中的http是否出现多次
def https_token(url):
    match = re.search('https://|http://', url)
    if match.start(0) == 0:
        url = url[match.end(0):]
    match = re.search('http|https', url)
    if match:
        return 0
    else:
        return 1


# 主函数
def main():
    file = open('D:\\PycharmProjects\\pythonProject\\src\\url_training_dataset.txt', 'a', encoding='utf-8')
    # 读取excel中存取的url数据集
    # 正常url选择top_size.xlsx
    # 恶意url选择Malicious.xlsx
    excel = xlrd.open_workbook("D:\\PycharmProjects\\pythonProject\\url_dataset\\Malicious.xlsx")
    sheet = excel.sheet_by_index(0)
    # 返回一个URL列表
    url_list = sheet.col_values(0)
    for url in url_list:

        # status是一个列表
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
        #多看文献考虑更改234的特征
        # append在列表末尾追加新的对象
        # 特征1 URL的长度
        status.append(url_length(url))
        # 特征2 短链接
        status.append(shortening_service(url))
        # 特征3 检查域名中是否出现@符号
        status.append(having_at_symbol(url))
        # 特征4 检查//符号后的字符个数
        status.append(double_slash_redirecting(url))
        # 特征5 检查/符号出现的次数
        status.append(double_slash_num(url))
        # 特征6 检查/符号出现的次数
        status.append(slash_num(url))
        # 特征7 检查%符号出现的次数
        status.append(percent_sign(url))
        # 特征8 检查-符号的存在
        status.append(prefix_suffix(hostname))

        # 以下特征有关域名
        dns = 1
        try:
            domain = whois.query(hostname)
        except:
            dns = -1

        # 特征9 http标志是否仅出现一次
        status.append(https_token(url))

        # print(status)
        # 将特征向量存入训练集文件
        s = str(status).replace("[", "").replace("]", "").replace(" ", "")
        print(s)
        file.write(s + ",malicious" + "\n")

    file.close()


# 如果features_extraction.py作为独立文件运行，请使用以下两行。如果将此文件作为从 chrome 扩展名开始的工作流管道的一部分运行，请注释掉这两行。
if __name__ == "__main__":
    main()
