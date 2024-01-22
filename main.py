import jieba.analyse
import jieba.posseg as pseg

jieba.load_userdict('user.txt')

with open('judgement13.txt', 'r') as file:
    text = file.read()

# todo
words = pseg.lcut(text)
words1 = words.copy()

# 删除words中得标点符号
for each in words1:
    if each.flag == 'x':
        words1.remove(each)

# 构建names,ethnicity,gender等集合
names = []
ethnicity = []
gender = []

for each in words:
    if each.flag == 'nr':
        names.append(each.word)
    if each.flag == 'nz' and '族' in each.word:
        ethnicity.append(each.word)
    if each.flag == 'n' and ('女' in each.word or '男' in each.word):
        gender.append(each.word)

# 构造names的方法
if len(words1) <= 200:
    names = set(jieba.analyse.extract_tags("".join(set(names)), topK=2, allowPOS=('nr', )))
elif len(words1) <= 400:
    names = set(jieba.analyse.extract_tags("".join(set(names)), topK=4, allowPOS=('nr', )))
elif len(words1) <= 600:
    names = set(jieba.analyse.extract_tags("".join(set(names)), topK=6, allowPOS=('nr', )))
elif len(words1) <= 800:
    names = set(jieba.analyse.extract_tags("".join(set(names)), topK=8, allowPOS=('nr', )))
else:
    names = set(jieba.analyse.extract_tags("".join(set(names)), topK=10, allowPOS=('nr', )))

ethnicity = set(ethnicity)
gender = set(gender)

jieba.analyse.set_idf_path("idf.txt")

# 构建动词集合
verbs = set(jieba.analyse.extract_tags(text, topK=10, allowPOS=('v',)))

# 形容词集合
adj = set(jieba.analyse.extract_tags(text, topK=5, allowPOS=('ad', 'a', 'an', )))

# 构建地名集合
location = []
tmp = ''
i = 0
last = 0
while i < len(words):
    if words[i].flag == 'ns':
        for j in range(i, i+6):
            if words[j].flag == 'ns':
                last = j
            if words[j].flag == 'x' or words[j].flag == 'p' or words[j].flag == 'v':
                break
        for k in range(i, last+1):
            tmp = tmp + words[k].word
        location.append(tmp)
        tmp = ''
        i = last+1
    i = i+1
location = set(location)

# 构建相关法院集合
courts = []
temp = ''
i = 0
first = 0
while i < len(words):
    if words[i].flag == 'nt':
        if i < 4:
            border = 0
        else:
            border = i-4
        for j in range(border, i+1):
            if words[j].flag == 'ns':
                first = j
                break
            else:
                first = i
        for k in range(first, i+1):
            temp = temp + words[k].word
            if words[k].flag == 'x' or words[k].flag == 'p':
                temp = ""
        if'法院' in temp:
            courts.append(temp)
        temp = ''
    i = i+1
courts = set(courts)
courts1 = courts.copy()
courts2 = courts.copy()

for each in courts1:
    courts2.remove(each)
    for tmp in courts2:
        if each in tmp and each in courts:
            courts.remove(each)
    courts2 = courts1.copy()

# 构建数词集合
num = []
tmp = ''
i = 0
last = 0
while i < len(words):
    if words[i].flag == 'm' or words[i].flag == 'x':
        if i+6 < len(words):
            for j in range(i, i+6):
                if words[j].flag == 'm' or words[j].flag == 'x':
                    last = j
                    if words[j].word == '元' or words[j].word == '万元':
                        break
                else:
                    break
        else:
            for j in range(i, len(words)):
                if words[j].flag == 'm' or words[j].flag == 'x':
                    last = j
                    if words[j].word == '元' or words[j].word == '万元':
                        break
                else:
                    break
        for k in range(i, last):
            tmp = tmp + words[k].word
        if words[last].flag == 'm':
            tmp = tmp + words[last].word
        if '元' in tmp or '万元' in tmp:
            num.append(tmp)
        tmp = ''
        i = last+1
    i = i+1
num = set(num)

# the end

# 下面代码仅用于测试
print("names", names)
print("ethnicity", ethnicity)
print("gender", gender)
print("location", location)
print("courts", courts)
print("verbs", verbs)
print("adjective", adj)
print("numbers", num)
