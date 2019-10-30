#coding:utf-8
import os
def getflag():
    with open("LF.CAL") as f:
        line = f.readline()
        line = line.strip().split(',')
    success = int(line[0])
    return success == 1
#
def readfile(filename, coding='utf-8'):
    mx = []
    with open(filename, 'r', encoding=coding) as f:
        lines = f.readlines()
        for line in lines:
            line = list(eval(line.strip()))
            mx.append(line)
    return mx
#
def writefile(filename, mx):
    with open(filename, "w", encoding='utf-8') as f:
        for i in mx:
            templine = []
            for j in i:
                templine.append(j)
            for ind, iii in enumerate(templine):
                if type(iii) == type(0.0):
                    templine[ind] = round(iii, 4)
            f.write(str(templine)[1:-1] + ',\n')
#
def readslack():
    store = 0
    ret = []
    with open("lfreport.lis") as f:
        lines = f.readlines()
        for line in lines:
            templine = line.strip().split()
            if templine[0] == "Slack":
                store = 1
                continue
            if store == 1:
                ret.append(templine)
    return ret
#
def readslackval(slack, busname):
    for i in slack:
        # print('hhhhh', i[0], busname)
        if i[0] == busname:
            return i[1], i[2]
    return 'xx', 'xx'
def readflag():
    dic = dict()
    if not os.path.exists('flags.txt'):
        f = open('flags.txt', 'w')
        f.close()
    with open('flags.txt') as f:
        lines = f.readlines()
        for line in lines:
            line = list(eval(line.strip()))
            dic[line[0]] = line[1]
    return dic 
def writeflag(dic):
    with open('flags.txt', 'w') as f:
        for i in dic:
            f.write("'%s',%s\n" % (i, str(dic[i])))
    return 0
#
# genList = dict()
# loadList = dict()
# mx5 = readfile('LF.L5')
# for ind, i in enumerate(mx5):
    # if i[2] != 0:
        # genList[i[1]] = ind
# mx6 = readfile('LF.L6')
# for ind, i in enumerate(mx6):
    # loadList[i[1]] = ind
# genDis = readfile('genDis.txt')