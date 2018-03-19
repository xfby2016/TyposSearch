# coding=gbk

import gensim
from snownlp import SnowNLP

model_all = "D:/Project/Python/NLP/Gensim/Word2Vec/Data/Generate_Data/Model/All/All.model"
model_economic = "D:/Project/Python/NLP/Gensim/Word2Vec/Data/Generate_Data/Model/Economic/Economic.model"
model_history = "D:/Project/Python/NLP/Gensim/Word2Vec/Data/Generate_Data/Model/History/History.model"
model_literature = "D:/Project/Python/NLP/Gensim/Word2Vec/Data/Generate_Data/Model/Literature/Literature.model"
model_politics = "D:/Project/Python/NLP/Gensim/Word2Vec/Data/Generate_Data/Model/Politics/Politics.model"
model_sports = "D:/Project/Python/NLP/Gensim/Word2Vec/Data/Generate_Data/Model/Sports/Sports.model"
model_technology = "D:/Project/Python/NLP/Gensim/Word2Vec/Data/Generate_Data/Model/Technology/Technology.model"

print("\n \033[1;31m Loading model, please wait ... ... \033[0m \n")

modelAll = gensim.models.Word2Vec.load(model_all)
modelEconomic = gensim.models.Word2Vec.load(model_economic)
modelHistory = gensim.models.Word2Vec.load(model_history)
modelLiterature = gensim.models.Word2Vec.load(model_literature)
modelPolitics = gensim.models.Word2Vec.load(model_politics)
modelSports = gensim.models.Word2Vec.load(model_sports)
modelTechnology = gensim.models.Word2Vec.load(model_technology)

print("\033[1;31m Model loading complete \033[0m \n")

class Cluster(object):

    def __init__(self):
        pass

    def get_mean(self, l, digits):
        "���ؾ�ֵ"
        return round(sum(l)/len(l), digits)

    def get_most_possible_category(self, word_list, digits=4):
        "�������ƶ�"
        probability = []
        model_category = [modelEconomic, modelHistory, modelLiterature, modelPolitics, modelSports, modelTechnology]
        category = ["����", "��ʷ", "��ѧ", "����", "����", "�Ƽ�"]
        for model in model_category:
            index = model_category.index(model)
            kw = category[index]
            probability_list = []
            for word in word_list:
                if word in model:       # �жϹؼ����Ƿ���ģ����
                    probability_list.append(model.similarity(kw, word))
            probability.append(self.get_mean(probability_list, digits))     # �����ƶȵľ�ֵ�����б�

        return max(probability), category[probability.index(max(probability))]      # �����������Լ�����Ӧ���

def main():
    "������"
    while True:
        content = input("Please enter a word or paragraph:")
        sentence = SnowNLP(content)
        keyword_num = 8
        keywords = sentence.keywords(limit=keyword_num)
        print(keywords)

        cluster = Cluster()
        probability, category = cluster.get_most_possible_category(keywords)
        print(probability, category)

if __name__ == '__main__':
    main()
