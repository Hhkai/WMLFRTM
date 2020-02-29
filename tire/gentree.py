import csv
import pickle
import os
class Node:
    def __init__(self, c):
        self.name = c
        self.dic = dict()
        self.flag = False

def getwords(sentence):
    curpath = os.path.realpath(__file__)
    pathpre = curpath[:-10]
    with open(pathpre + 'tire.pk', 'rb') as f: # 这句是为了从外面调这个函数
        h = pickle.load(f)
    cur_n = h
    lenth_s = len(sentence)
    res = []
    begin_ind = -1
    end_ind = -1
    ind = -1
    while ind < lenth_s - 1:
        ind += 1
        cur_c = sentence[ind]
        if cur_c not in cur_n.dic:
            # 匹配不上 断了
            if begin_ind != -1 and end_ind > begin_ind:
                res.append(sentence[begin_ind:end_ind])
            begin_ind = -1
            end_ind = -1
            cur_n = h
            if cur_c in cur_n.dic:
                ind -= 1
            continue
        if begin_ind == -1:
            begin_ind = ind
        cur_n = cur_n.dic[cur_c]
        if cur_n.flag == True:
            end_ind = ind + 1
    if begin_ind != -1 and end_ind > begin_ind:
        res.append(sentence[begin_ind:end_ind])
    return res


if __name__ == '__main__':
    s = set()

    f = open('etts2.csv',encoding='utf-8')
    dict_reader = csv.DictReader(f)
    for row in dict_reader:
        s.add(row['name'])
    f.close()

    f = open('rels.csv',encoding='utf-8')
    dict_reader = csv.DictReader(f)
    for row in dict_reader:
        s.add(row['Entity'])
        s.add(row['AttributeName'])
        s.add(row['Attribute'])
    f.close()

    h = Node('#')
    for i in s:
        lenth_i = len(i)
        cur_n = h
        for ind in range(lenth_i):
            c = i[ind]
            if c not in cur_n.dic:
                cur_n.dic[c] = Node(c)
            cur_n = cur_n.dic[c]
            if ind == lenth_i - 1:
                cur_n.flag = True
    with open('tire.pk', 'wb') as f:
        pickle.dump(h, f)