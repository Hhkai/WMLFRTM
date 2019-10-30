# coding:utf-8
import myutils
import os
def checkP():
    # 全区平衡有功
    mx = myutils.readfile('LF.L6')
    load = 0
    for i in mx:
        load += i[4]
    mx2 = myutils.readfile('LF.L5')
    gen = 0
    for i in mx2:
        gen += i[3]
    stdgen = load * 1.011
    r = stdgen / gen
    for i in range(len(mx2)):
        if mx2[i][2] == 1:
            mx2[i][3] = mx2[i][3] * r
            mx2[i][4] = mx2[i][4] * r
        if mx2[i][2] == -1:
            mx2[i][3] = mx2[i][3] * r
    return 0
def changemx(b):
    # 调整潮流
    mx = myutils.readfile('LF.L6')
    for i in range(len(mx)):
        print(mx[i][4], type(mx[i][4]))
        mx[i][4] = mx[i][4] * b
        mx[i][5] = mx[i][5] * b
    myutils.writefile("LF.L6", mx)
    mx2 = myutils.readfile('LF.L5')
    for i in range(len(mx2)):
        mx2[i][3] = mx2[i][3] * b
    myutils.writefile('LF.L5', mx2)
def setG(linen):
    print('aaaaaaaaaaaaaaa')
    # 调整单个发电机
    mx = myutils.readfile("LF.L5")
    name = 0
    P = (0.1, 0.1)

    oldtype = mx[linen][2]
    oldValueP = mx[linen][3]
    oldValueQ = mx[linen][4]
    mx[linen][2] = 0
    name = mx[linen][-1]
    myutils.writefile("LF.L5", mx)
    os.system("WMLFRTMsg")
    if myutils.getflag():
        P = myutils.readslackval(myutils.readslack(), name)
    else:
        return "fail"
    mx[linen][2] = oldtype
    mx[linen][3] = float(P[0][:4])
    mx[linen][4] = float(P[1][:4])
    
    f = myutils.readflag()
    r = f['r']
    with open('ops.txt', 'a', encoding='utf-8') as f:
        f.write('所用知识: 设置平衡机观察有功和无功平衡\n')
        f.write('修改方案: 调整发电机\n')
        f.write('\t%s:%.2f+%.2fj->%.2f+%.2fj\n' % (mx[linen][-1], oldValueP / r, 
            oldValueQ / r, mx[linen][3] / r, mx[linen][4] / r))

    myutils.writefile("LF.L5", mx)
    return 'pause'
def setbyhand(x, toohigh):
    print('bbbbbbbbbbbbbb')
    # open a -5 will make it higher
    # 调电容电抗器
    mx = myutils.readfile('LF.L2')
    flag = False
    linen = 0
    for i in range(len(mx)):
        if mx[i][1] == x and mx[i][2] == x:
            if toohigh:
                if mx[i][0] == 0 and mx[i][5] > 0:
                    mx[i][0] = 1
                    myutils.writefile('LF.L2', mx)
                    flag = True
                    linen = i + 1
                    r = '无效 -> 有效'
                    break
                if mx[i][0] == 1 and mx[i][5] < 0:
                    mx[i][0] = 0
                    myutils.writefile('LF.L2', mx)
                    flag = True
                    linen = i + 1
                    r = '有效 -> 无效'
                    break
            else:
                if mx[i][0] == 0 and mx[i][5] < 0:
                    mx[i][0] = 1
                    myutils.writefile('LF.L2', mx)
                    flag = True
                    linen = i + 1
                    r = '无效 -> 有效'
                    break
                if mx[i][0] == 1 and mx[i][5] > 0:
                    mx[i][0] = 0
                    myutils.writefile('LF.L2', mx)
                    flag = True
                    linen = i + 1
                    r = '有效 -> 无效'
                    break
    if flag:
        with open('ops.txt', 'a', encoding='utf-8') as f:
            f.write('所用知识: 根据母线电压高低投切附近的电容电抗器\n')
            f.write('修改方案: 调整电容电抗器\n')
            f.write('\tLF.L2 %s行:%s\n' % (linen, r))
        return 'pause'
    return 1
def go2():
    genList = dict()
    loadList = dict()
    mx5 = myutils.readfile('LF.L5')
    for ind, i in enumerate(mx5):
        if i[2] != 0:
            genList[i[1]] = ind
    mx6 = myutils.readfile('LF.L6')
    for ind, i in enumerate(mx6):
        loadList[i[1]] = ind
    genDis = myutils.readfile('genDis.txt')
    
    f = myutils.readflag()
    markList = f['markList']
    lastLoad_list = f['lastLoad_list']
    
    cur = f['cur']
    r = f['r']
    
    b = cur/r
    f['r'] = cur
    changemx(b)
    myutils.writeflag(f)
    os.system('WMLFRTMsg')
    if not myutils.getflag():
        # pau = input()
        f['goone'] = -1
        myutils.writeflag(f)
        return -1  #failure
    x = findLP1(genList, loadList, markList)
    if x[0] == -2:
        print('x[0] == -2, goonestep return 1')
        f['goone'] = 1
        myutils.writeflag(f)
        return 'continue'
        return 1  #continue, try once again
    if x[0] == -1:
        if myutils.getflag():
            f['goone'] = 0
            myutils.writeflag(f)
            return 0  # break, fixed, cur++
        else:
            f['goone'] = -1
            myutils.writeflag(f)
            return -1  # fail
    if x[0] == 0:
        ttt = setG(x[1])
        if ttt == "fail":
            f['goone'] = ttt
            myutils.writeflag(f)
            return ttt
        else:
            return 'pause'
    if x[0] == 1:
        if x[1] == lastLoad_list[0]:
            lastLoad_list[1] = lastLoad_list[1] + 1
        else:
            lastLoad_list[0] = x[1]
            lastLoad_list[1] = 0
        f['lastLoad_list'] = lastLoad_list
        if lastLoad_list[1] > 3:
            # xxxx
            ttt = setbyhand(lastLoad_list[0], x[2])
            if ttt == 1:
                markList.append(lastLoad_list[0])
            print('append', lastLoad_list[0])
            f['markList'] = markList
            f['goone'] = 1
            myutils.writeflag(f)
            return 'pause'
            return 1  # continue, try again
        genid = genDis[lastLoad_list[0] - 1][lastLoad_list[1]]
        for ind, i in enumerate(mx5):
            if i[1] == genid:
                ttt = setG(ind)
                if ttt == "fail":
                    f['goone'] = ttt
                    myutils.writeflag(f)
                    return ttt
                break
    if myutils.getflag():
        f['goone'] = 0
        myutils.writeflag(f)
        return 'pause'
        return 0  # break, fixed, cur++
    else:
        f['goone'] = -1
        myutils.writeflag(f)
        return -1  # fail
    print('error', x)
def findLP1(genList, loadList, markList):
    lp1 = myutils.readfile('LF.LP1', coding='gb2312')
    n = 0
    loadsdown = []
    loadsup = []
    loadssum = 0
    abss = []
    for i in lp1:
        if len(i) == 4:
            loadssum += i[1]
            n += 1
    #
    gen = None
    val = 1
    mx5 = myutils.readfile('LF.L5')
    if n * 0.85 > loadssum:
        for i in lp1:
            if len(i) == 4:
                if i[1] < val and (i[0] in genList):
                    gen = genList[i[0]]
                    val = i[1]
        P = mx5[gen][3]
        r = (P + 0.5) / P
        if P < 0:
            r = -1
        mx5[gen][3] = mx5[gen][3] * r
        mx5[gen][4] = mx5[gen][4] * r
        writefile('LF.L5', mx5)
        print('0.85', gen)
        return (-2, 1)
    #
    gen = None
    val = 0
    if n * 1.15 < loadssum:
        for i in lp1:
            if len(i) == 4:
                if i[1] > val and (
                        i[0] in genList) and mx5[genList[i[0]]][3] > 0.1:
                    gen = genList[i[0]]
                    val = i[1]
        if gen == None:
            pass  ########## gao !!!!!!!!!!!!!!
        else:
            P = mx5[gen][3]
            r = (P - 0.5) / P
            if r < 0:
                r = 0.5
            mx5[gen][3] = mx5[gen][3] * r
            mx5[gen][4] = mx5[gen][4] * r
            myutils.writefile('LF.L5', mx5)
            print('1.15', gen)
            return (-2, 1)
    #
    fixtype = -1
    fixline = 0
    fixnum = 1.0
    for i in lp1:
        if len(i) == 4:
            if abs(i[1] - 1) > 0.1:
                curtype = -2
                if i[0] in genList:
                    curtype = 1
                if i[0] in loadList:
                    curtype = 0
                    if i[0] in markList:
                        continue
                if curtype >= fixtype:
                    if abs(i[1] - 1) > abs(fixnum - 1):
                        fixline = i[0]
                        fixtype = curtype
                        fixnum = i[1]
            #
    if fixtype == -1:
        return (-1, 1)
    if fixtype == -2:
        print('error')
        exit()
    if fixline in genList:
        gen = genList[fixline]
        print(0, gen)
        return (0, gen)  # line num
    if fixline in loadList:
        load = loadList[fixline]
        print(1, load)
        # return (1, load, fixnum > 1) # line num
        return (1, fixline, fixnum > 1)  # L1 id
    return (-3, 1)
#
fundict = {
    'goone' : go2
}
def doOps(s):
    if s in fundict:
        r = fundict[s]()
        return r
    else :
        print('doOps(s):s:', s)
        return -1