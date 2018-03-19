from gensim.models import word2vec
import jieba
import logging, os

raw_data = "G:/"
generate_data_path = "D:/Project/Python/NLP/Gensim/Word2Vec/Data/Generate_Data/Create/CreateAll.txt"

class word_2_vec(object):

    def __init__(self):
        pass

    def get_all_txt(self, path):
        "返回一个目录下所有.txt文件名所组成的列表"
        txts = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file[-4:] == '.txt':
                    txts.append(str(file))
        return txts

    def create_W2V_txt(self, sentence, generate_path):
        "写入文件"
        f = open(generate_path, 'a', encoding='utf-8')
        seg_list = jieba.cut(sentence, cut_all=False)
        f.write(" ".join(seg_list))
        f.close()

    def get_string(self, file_path_list, file_path):
        "获取文章组成的字符串"
        # python3.x
        # -*- encoding:utf-8 -*-
        decode_set = ["utf-8", 'gb18030', 'ISO-8859-2', 'gb2312', "gbk", "Error"]  # 编码集
        for file in file_path_list:
            PATH = str(file_path) + str(file)
            for k in decode_set:  # 编码集循环
                try:
                    file = open(PATH, "r", encoding=k)
                    # 打开路径中的文本
                    readfile = file.readlines()  # 这步如果解码失败就会引起错误，跳到except。
                    print(k, " can decode this txt file")
                    sentence = ""
                    for line in readfile:
                        line.replace('\t', '').replace('\n', '').replace(' ', '')
                        sentence += str(line.strip())
                    self.create_W2V_txt(sentence, generate_data_path)
                except:
                    if k == "Error":  # 如果碰到这个程序终止运行
                        # raise Exception("%s had no way to decode" % PATH)
                        print("emmm")
                    continue

    def word_2_ver(self, generate_data_path):
        logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', level=logging.INFO)
        sentences =word2vec.Text8Corpus(generate_data_path)  # 加载语料
        model =word2vec.Word2Vec(sentences, size=200)  #训练skip-gram模型，默认window=5

        print(model)
        # 计算两个词的相似度/相关程度
        try:
            y1 = model.similarity(u"文艺", u"青年")
        except KeyError:
            y1 = 0
        print(u"【文艺】和【青年】的相似度为：", y1)
        print("-----\n")

        # 计算某个词的相关词列表
        y2 = model.most_similar(u"文艺", topn=20)  # 20个最相关的
        print(u"和【文艺】最相关的词有：\n")
        for item in y2:
            print(item[0], item[1])
        print("-----\n")

        # 寻找对应关系
        print(u"文学-艺术，献身-")
        y3 = model.most_similar([u'现身', u'艺术'], [u'文学'], topn=3)
        for item in y3:
            print(item[0], item[1])
        print("----\n")

        # 寻找不合群的词
        y4 = model.doesnt_match(u"文艺 艺术 作品 食物".split())
        print(u"“文艺 艺术 作品 食物” 中不合群的词：", y4)
        print("-----\n")

        # 保存模型以便重用
        model.save(u"D:/Project/Python/NLP/Gensim/Word2Vec/Data/Generate_Data/Model/All/All.model")

# create_W2V_txt(raw_data, generate_data)

wtv = word_2_vec()

def file():
    import datetime
    start = datetime.datetime.now()

    txt_list = wtv.get_all_txt(raw_data)
    print("\n获取txt文件结束, 开始jieba分词\n")

    print("\njieba分词结束, 开始写入目标文件\n")
    wtv.get_string(txt_list, raw_data)

    end = datetime.datetime.now()
    print("结束, 文本处理用时", end - start, "\n")

def train():
    print("\n开始word2vec训练\n")

    import datetime
    start = datetime.datetime.now()

    wtv.word_2_ver(generate_data_path)

    end = datetime.datetime.now()
    print("结束, 训练用时", end-start, "\n")

# file()

# train()
