import os
import caculaEntofChar
import WordCount
import re
from sklearn.preprocessing import MinMaxScaler

# 危险函数列表
riskFunctionList = [
    'eval',
    'setInterval',
    'setTimeout',
    'escape',
    'document.write',
    'document.writeIn',
    'replace',
    'referrer'
]

# DOM修改函数
DOM_List = [
    'clearAttributes',
    'insertAdjacentElement',
    'replaceNode'
]

# 事件附属函数
attach_list = [
    'addEventListener',
    'attachEvent',
    'dispatchEvent',
    'fireEvent'
]


#可疑字符
speCharList = ['!', '"','#','$', '%','&',"'",'('')', '*','+',',', '-', '.','/',':',';', '<','=','>','?','@','[',']', '^', '_','{','}','|','~'
 ]

keywords = [
    'var',
    'for',
    'while',
    'if',
    'function',
    'this'
]


#关键词的频率

# 计算函数个数
def callTimes(path, filename, functionList):
    alltime = 0
    for func in functionList:
        rel = WordCount.word_count(path, filename, func)
        alltime = alltime + rel
    return alltime


# 计算最长的字符串的长度
def getLongestWord(path, filename):
    file = open(path + '\\' + filename, 'r+', encoding="ISO-8859-1")
    str = file.read()
    wordSet = re.split(r' ', str)
    longest = 0
    for word in wordSet:
        if (longest < len(word)):
            longest = len(word)
    return longest


# 计算长度大于30的字符串的个数
def getlongnum(path, filename):
    file = open(path + '\\' + filename, 'r+', encoding="ISO-8859-1")
    str = file.read()
    wordSet = re.split(r' ', str)
    num = 0
    for word in wordSet:
        if 30 < len(word):
            num = num + 1
    return num


#计算字符串平均长度
def get_average(path,filename):
    file = open(path + '\\' + filename, 'r+', encoding="ISO-8859-1")
    str = file.read()
    wordSet = re.split(r' ', str)
    sum = 0
    for word in wordSet:
        sum = sum + len(word)
    return sum/len(wordSet)


#计算可疑字符的频率
def sepfreq(path,filename,speCharList):
    file = open(path + '\\' + filename, 'r+', encoding="ISO-8859-1")
    str = file.read()
    #清除空格
    str = re.sub(' ', '', str)
    #转为字符列表
    testSet = list(str)
    alltime = 0
    for spechar in speCharList:
        rel = WordCount.word_count(path, filename, spechar)
        alltime = alltime + rel
        if(len(testSet)==0):
            return 0
        else:
            return alltime / len(testSet)

# 生成每个文件对应的样本特征向量
def create_matrix(path, filename):
    # 特征1，可疑函数字符串
    riskfun = callTimes(path, filename, riskFunctionList)
    # 特征2 DOM修改函数的个数
    DOM_num = callTimes(path, filename, DOM_List)
    # 特征3 事件附属函数的个数
    attach_num = callTimes(path, filename, attach_list)
    # 特征4 计算脚本的字符熵
    ent = caculaEntofChar.caculaEnt(path, filename)
    # 特征5  最长字符串的长度
    max_size = getLongestWord(path, filename)
    # 特征6 长字符串的数量
    long_num = getlongnum(path, filename)
    # 特征7 字符串平均长度
    average = get_average(path,filename)
    # 特征8 可疑字符出现的频率
    charfreq = sepfreq(path, filename, speCharList)
    # 特征9 关键词出现的频率
    keyfreq = callTimes(path, filename,keywords)

    sample_vector = [riskfun, DOM_num, attach_num, ent, max_size, long_num, average, charfreq, keyfreq]
    return sample_vector


# 存储特征向量
def createData(path):
    # 用来存储特征向量的数组
    file = open('D:\\PycharmProjects\\pythonProject\\src\\js_training_dataset.txt', 'a', encoding='utf-8')
    files = os.listdir(path)
    for f in files:
        filename = str(f)
        # 为每个文件创建特征向量
        vec = create_matrix(path, filename)
        v = str(vec).replace("[", "").replace("]", "").replace(" ", "")
        # print(v)
        file.write(v + ",malicious" + "\n")
    file.close()


if __name__ == '__main__':
    path = 'D:\\PycharmProjects\\pythonProject\\malicious'
    createData(path)
