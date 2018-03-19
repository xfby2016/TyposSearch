import gensim
from gensim.models import word2vec

Data_path = "D:/Project/Python/NLP/Gensim/Word2Vec/Data/Generate_Data/Model/"
Type = "All/All.model"
model_path = Data_path + Type

model = gensim.models.Word2Vec.load(model_path)
print(model)

y = model.most_similar('微博', topn=25)
print("和【微博】最相关的词有：\n")
for item in y:
    print(item[0], item[1])
print("------------------")

try:
    y1 = model.similarity("微信", "朋友")
except KeyError:
    y1 = 0
print(y1)
