
from pypinyin import lazy_pinyin
import string, re
import jieba

PATH1 = "jieba.txt"
PATH2 = "cn_dict.txt"
PATH3 = "words.txt"
PATH4 = "pinyin.txt"

PUNCTUATION_LIST = string.punctuation
PUNCTUATION_LIST += "。，？：；、｛｝［］‘“”’《》／！％……（）"

def match_Chinese(word):
    return True if re.match(u'[\u4e00-\u9fa5]', word) != None else False

def getPinyin(word):
    p = ""
    for py in lazy_pinyin(word):
        p += str(py)
    return p

def read_pinyin(file_path):
    word_freq = []
    with open(file_path, "r", encoding='utf-8') as f:
        for line in f:
            info = line.split()
            word = getPinyin(info[0])
            word_freq.append(word)
    return word_freq

def construct_dict( file_path, isPinyin=True, isDictionary=True):
    if isDictionary == True:
        if isPinyin == True:
            word_freq = {}
            with open(file_path, "r", encoding='utf-8') as f:
                for line in f:
                    info = line.split()
                    word = getPinyin(info[0])
                    frequency = info[1]
                    word_freq[word] = frequency
            return word_freq
        else:
            word_freq = {}
            with open(file_path, "r", encoding='utf-8') as f:
                for line in f:
                    info = line.split()
                    word = info[0]
                    frequency = info[1]
                    word_freq[word] = frequency
            return word_freq
    else:
        if isPinyin == True:
            word_freq = []
            with open(file_path, "r", encoding='utf-8') as f:
                for line in f:
                    info = line.split()
                    word = getPinyin(info[0])
                    # frequency = info[1]
                    word_freq.append(word)
            return word_freq
        else:
            word_freq = []
            with open(file_path, "r", encoding='utf-8') as f:
                for line in f:
                    info = line.split()
                    word = info[0]
                    # frequency = info[1]
                    word_freq.append(word)
            return word_freq

NWORDS = construct_dict(PATH1, isPinyin=True, isDictionary=True)

def get_alphabet(file_path):
    alphabet = []
    for py in open(file_path):
        alphabet.append(str(py.strip()))
    return alphabet

alphabet = get_alphabet(PATH4)

def edits1(word):
    word = getPinyin(word)
    n = len(word)
    return set([word[0:i] + word[i + 1:] for i in range(n)] +  # deletion
               [word[0:i] + word[i + 1] + word[i] + word[i + 2:] for i in range(n - 1)] +  # transposition
               [word[0:i] + c + word[i + 1:] for i in range(n) for c in alphabet] +  # alteration
               [word[0:i] + c + word[i:] for i in range(n + 1) for c in alphabet])  # insertion

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct_pinyin(word):
    candidates = known([getPinyin(word)]) or known(edits1(word)) or known_edits2(word) or [getPinyin(word)]
    return max(candidates, key=lambda w: NWORDS[w])

def read_jiebatxt(file_path):
    wordsdic = construct_dict(file_path, isPinyin=False, isDictionary=True)
    pinyinDic = read_pinyin(file_path)
    pinyindic = set(pinyinDic)
    dictionary = {}
    for word in wordsdic:
        py = getPinyin(word)
        if py in pinyindic:
            l = []
            l.append(word)
            l.append(int(wordsdic[word]))
            if py not in dictionary:
                dictionary[getPinyin(word)] = l
            else:
                dictionary[py].append(word)
                dictionary[py].append(int(wordsdic[word]))
    return dictionary

def correct(py, dictionary):
    if py in dictionary:
        L = dictionary[py]
        num = []
        index = 0
        while index < len(L):
            num.append(L[index + 1])
            index += 2
        m = max(num)
        return L[L.index(m) - 1]
    else:
        return "有问题"

def cut_sentence(sentence):
    jieba_cut = jieba.cut(sentence, cut_all=False)
    return "\t".join(jieba_cut).split("\t")


def main():
    # import datetime
    # start = datetime.datetime.now()


    print("正在载入默认词典, 请稍后... ...\n")
    dictionary_pinyin = read_jiebatxt(PATH1)
    dictionary_hanzi = construct_dict(PATH1, isPinyin=False, isDictionary=False)
    print("载入完成\n")
    while True:
        content = input("请输入一个词语或者一段话:")
        correct_sentence = ""
        words = cut_sentence(content)
        for word in words:
            if match_Chinese(word):
                if word not in PUNCTUATION_LIST:
                    if word in dictionary_hanzi:
                        correct_sentence += word
                    else:
                        correctpinyin = correct_pinyin(word)
                        correct_sentence += correct(correctpinyin, dictionary_pinyin)
                else:
                    correct_sentence += word
            else:
                correct_sentence += word
        print("\n")
        print(correct_sentence)
        print("\n")


    # end = datetime.datetime.now()
    # print("\n\n", end-start)


if __name__ == '__main__':
    main()
