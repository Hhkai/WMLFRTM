import pickle
from gentree import Node

def getwords(sentence):
    with open('tire.pk', 'rb') as f:
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
    with open('tire.pk', 'rb') as f:
        h = pickle.load(f)
    for i in h.dic:
        print(h.dic[i].name)
    print(getwords('有潮流计算不收敛怎么办'))
    print(getwords('潮流计算不收敛'))
    print(getwords('有潮流'))
