# -*- coding:utf-8 -*-

import jieba, os, datetime
import logging
import sys
import codecs
import traceback
import pandas as pd
import numpy as np
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from collections import Counter
from sklearn import metrics
import matplotlib.pyplot as plt

# path = "D:/Project/Python/ItChat/sgxy"
stopwordspath = "D:/Project/Python/ItChat/sgxy/stopwords.txt"
file_path1 = "Temp"
file_path2 = "Text.txt"
num_clusters = 6        #体育 政治 经济 科技 历史 文学 其他
# 目标文件
tf_ResFileName = "D:/Project/Python/NLP/TyposSearch/TextCluster/Info/tf_ResFileName.txt"
tfidf_ResFileName = "D:/Project/Python/NLP/TyposSearch/TextCluster/Info/tfidf_ResFileName.txt"
cluster_ResFileName = "D:/Project/Python/NLP/TyposSearch/TextCluster/Info/cluster_ResFileName.txt"

class File(object):

    def __init__(self):
        pass

    def getStopWords(self, path):
        "返回停用词列表"
        stopwords = []
        for line in open(path, encoding='utf-8'):
            stopwords.append(line.strip())
        return stopwords

    def getAllTxt(self, path):
        "返回一个目录下所有.txt文件名所组成的列表"
        txts = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file[-4:] == '.txt':
                    txts.append(str(file))
        return txts

    def readContent(self, file_name, file_path):
        "读取一个文件内容作并为一个字符串返回"
        sentence = ""
        Path = str(file_path + "/" + file_name)
        try:
            decode_set = ["utf-8", 'gb18030', 'ISO-8859-2', 'gb2312', "gbk"]
            for code in decode_set:
                if open(Path, 'r', encoding=code):
                    print(code)
                    for line in open(Path, 'r'):
                        sentence += str(line.strip())
                    break
                else:
                    print(code, "can't decode")
                    continue
        except (UnicodeError) as error:
            print("File error: ", error)
        return sentence

    def seg_words(self, sentence, stopwords_path):
        "将字符串分割并返回(去除停用词)"
        wordsentence = ""
        stopwords = self.getStopWords(stopwords_path)
        for word in jieba.cut(sentence):
            if word not in stopwords:
                wordsentence += str(word)
        seg_list = jieba.cut(wordsentence)  # 默认是精确模式
        return " ".join(seg_list)

    def getTxtMatrix(self, txtList, stopwordspath, file_path):
        "返回一个分词矩阵"
        matrix = []
        for txt in txtList:
            sentence = self.readContent(str(txt), str(file_path))
            wordsentence = self.seg_words(sentence, stopwordspath)
            matrix.append(wordsentence)
        return matrix

    def writeToTxt(self, Matrix, file_path):
        "将这个分词矩阵写入txt文件中"
        f = open(file_path, 'a')
        for i in Matrix:
            s = i + "\n"
            f.write(s)
        f.close()

    def getMatrix(self, file_path):
        matrix = []
        for word in open(file_path):
            matrix.append(word.strip())
        return matrix

class kMeans(object):

    def __init__(self):
        pass

    def process(self, matrix, tf_ResFileName, tfidf_ResFileName, num_clusters, cluster_ResFileName):
        try:

            # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
            tf_vectorizer = CountVectorizer()

            # fit_transform是将文本转为词频矩阵
            tf_matrix = tf_vectorizer.fit_transform(matrix)
            tf_weight = tf_matrix.toarray()
            # print tf_weight

            # 该类会统计每个词语的tf-idf权值
            tfidf_transformer = TfidfTransformer()

            # fit_transform是计算tf-idf
            tfidf_matrix = tfidf_transformer.fit_transform(tf_matrix)

            # 获取词袋模型中的所有词语
            word_list = tf_vectorizer.get_feature_names()

            # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
            tfidf_weight = tfidf_matrix.toarray()

            # 打印特征向量文本内容
            # print 'Features length: ' + str(len(word_list))
            tf_Res = codecs.open(tf_ResFileName, 'w', 'utf-8')
            word_list_len = len(word_list)
            for num in range(word_list_len):
                if num == word_list_len - 1:
                    tf_Res.write(word_list[num])
                else:
                    tf_Res.write(word_list[num] + '\t')
            tf_Res.write('\r\n')

            # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
            for i in range(len(tf_weight)):
                # print u"-------这里输出第", i, u"类文本的词语tf-idf权重------"
                for j in range(word_list_len):
                    if j == word_list_len - 1:
                        tf_Res.write(str(tf_weight[i][j]))
                    else:
                        tf_Res.write(str(tf_weight[i][j]) + '\t')
                tf_Res.write('\r\n')
            tf_Res.close()

            # 输出tfidf矩阵
            tfidf_Res = codecs.open(tfidf_ResFileName, 'w', 'utf-8')

            for num in range(word_list_len):
                if num == word_list_len - 1:
                    tfidf_Res.write(word_list[num])
                else:
                    tfidf_Res.write(word_list[num] + '\t')
            tfidf_Res.write('\r\n')

            # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
            for i in range(len(tfidf_weight)):
                for j in range(len(word_list)):
                    if j == word_list_len - 1:
                        tfidf_Res.write(str(tfidf_weight[i][j]))
                    else:
                        tfidf_Res.write(str(tfidf_weight[i][j]) + '\t')
                tfidf_Res.write('\r\n')
            tfidf_Res.close()
            # 聚类分析
            km = KMeans(n_clusters=num_clusters)
            km.fit(tfidf_matrix)
            print(metrics.silhouette_score(tfidf_matrix, km.labels_, metric='euclidean'))
            print(Counter(km.labels_))  # 打印每个类多少人
            # 中心点
            # print(km.cluster_centers_)
            # 每个样本所属的簇
            clusterRes = codecs.open(cluster_ResFileName, 'w', 'utf-8')

            # data_class = pd.read_table('id2class.txt',header=None)
            count = 1
            while count <= len(km.labels_):
                clusterRes.write(str(count) + '\t' + str(km.labels_[count - 1]))
                clusterRes.write('\r\n')
                count = count + 1
            clusterRes.close()
            # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数  958.137281791
            # print(km.inertia_)
        except:
            logging.error(traceback.format_exc())
            return False, "process fail"


file = File()
km = kMeans()

start = datetime.datetime.now()

txtList = file.getAllTxt(file_path1)
matrix = file.getTxtMatrix(txtList, stopwordspath, file_path1)
file.writeToTxt(matrix, file_path2)
print("文本部分已经完成!!!!!\n")

end = datetime.datetime.now()
time = end - start
print("\n文本部分用时：", time)
print("\n\n")
print("Start KMeans!!\n")

start = datetime.datetime.now()

kM_Matrix = file.getMatrix(file_path2)
km.process(kM_Matrix, tf_ResFileName, tfidf_ResFileName, num_clusters, cluster_ResFileName)
print("\nK-Means部分已经完成!!!!!\n")

end = datetime.datetime.now()
time = end - start
print("K-Means部分用时：", time)
