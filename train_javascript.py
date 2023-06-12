# 数据格式：最后一列为类别，其余列是样本特征
# 两种类别：safe,malicious
import classifier as classifier
from sklearn import svm
import numpy as np
import sklearn
from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler
import sklearn.model_selection as ms


# define converts(字典)
def label(s):
    it = {b'malicious': 0, b'safe': 1}
    return it[s]


# 1.读取数据集
path = 'D:\\PycharmProjects\\pythonProject\\src\\js_training_dataset.txt'
# converters={4:Iris_label}中“9”指的是第10列：将第10列的str转化为label(number)
data = np.loadtxt(path, dtype=float, delimiter=',', converters={9: label})

# 2.划分数据与标签
# train_data:训练样本，test_data：测试样本，train_label：训练样本标签，test_label：测试样本标签
# x为数据，y为标签,axis是分割的方向，1表示横向，0表示纵向，默认为0
x, y = np.split(data, indices_or_sections=(9,), axis=1)

# random作用是通过随机数来随机取得一定量得样本作为训练样本和测试样本
# x = x[:, 0:9]
# 归一化处理
min_max_scaler = MinMaxScaler()
x_minmax = min_max_scaler.fit_transform(x)
train_data, test_data, train_label, test_label = sklearn.model_selection.train_test_split(x_minmax,
                                                                                          y,
                                                                                          random_state=1,
                                                                                          train_size=0.75,
                                                                                          test_size=0.25)

# 3.训练svm分类器
# 惩罚参数C，
# kernel核函数类型，str类型，默认为’rbf’高斯核
# gamma：核函数系数
# ovr:一对多策略
# decision_function_shape ：决策函数类型，可选参数’ovo’和’ovr’
params = [{
    'kernel': ['rbf'],
    'C': [1, 10, 100, 1000],
    'gamma': [10, 1, 0.1, 0.01]}]

# classifier = svm.SVC(C=1, kernel='rbf', gamma=10, decision_function_shape='ovr')
classifier = svm.SVC(probability=True)
classifier = ms.GridSearchCV(estimator=classifier, param_grid=params, cv=5)
classifier.fit(train_data, train_label.ravel())

if __name__ == '__main__':
    # ravel函数在降维时默认是行序优先
    # 4.计算svc分类器的准确率
    print("训练集：", classifier.score(train_data, train_label))
    print("测试集：", classifier.score(test_data, test_label))
    y_pre = classifier.predict(x_minmax)
    print(classification_report(y, y_pre))

    # 网格搜索训练后的
    print("模型的最优参数：", classifier.best_params_)
    print("最优模型分数：", classifier.best_score_)
    print("最优模型对象：", classifier.best_estimator_)

