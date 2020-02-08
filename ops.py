# coding:utf-8
import myutils
import os
import kb
import re
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
    with open('ops.txt', 'a', encoding='utf-8') as fi:
        fi.write('所用知识: 调整母线附近发电机\n')
        fi.write('修改方案: 调整发电机(设置平衡机来寻求最优值)\n')
        fi.write('\t%s:%.2f+%.2fj->%.2f+%.2fj\n' % (mx[linen][-1], oldValueP / r, 
            oldValueQ / r, mx[linen][3] / r, mx[linen][4] / r))

    myutils.writefile("LF.L5", mx)
    return 'pause'
def setbyhand(x):
    print('bbbbbbbbbbbbbb')
    # open a -5 will make it higher
    # 调电容电抗器
    toohigh = myutils.ishigh(x)
    mx = myutils.readfile('LF.L2')
    flag = False
    linen = 0
    r = 'ks'
    print(toohigh)
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
        with open('ops.txt', 'a', encoding='utf-8') as fi:
            fi.write('所用知识: 根据母线电压高低投切附近的电容电抗器\n')
            fi.write('修改方案: 调整电容电抗器\n')
            fi.write('\tLF.L2 %s行:%s\n' % (linen, r))
        return 'pause'
    return 1 # 调节失败
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
    # init end
    f = myutils.readflag()
    markList = f['markList']
    lastLoad_list = f['lastLoad_list']
    
    x = tuple(f['findLP1'])
    f['findLP1'] = 'None'
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
        if x[1] in genList:
            # 发电机
            linen = genList[x[1]]
            ttt = setG(linen)
            if ttt == "fail":
                f['goone'] = ttt
                myutils.writeflag(f)
                return ttt
            else:
                f['goone'] = 1
                myutils.writeflag(f)
                return 'pause'
        if x[1] in loadList:
        # 负荷
            linen = loadList[x[1]]
            if linen == lastLoad_list[0]:
                lastLoad_list[1] = lastLoad_list[1] + 1
            else:
                lastLoad_list[0] = linen
                lastLoad_list[1] = 0
            f['lastLoad_list'] = lastLoad_list
            if lastLoad_list[1] > 3:
                # 已调整负荷附近的发电机多次
                ttt = setbyhand(x[1])
                if ttt == 1:
                    markList.append(x[1])
                print('append', x[1])
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
def findLP1():
    # 查找异常母线
    with open('ops.txt', 'a', encoding='utf-8') as fi:
        fi.write('检查异常母线\n')
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
    # init end
    f = myutils.readflag()
    markList = f['markList']
    ###
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
        f['findLP1'] = [-2, 1]
        myutils.writeflag(f)
        with open('ops.txt', 'a', encoding='utf-8') as fi:
            fi.write('分区母线电压较低,提高发电机电压0.5个标幺值\n')
        return 'pause'
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
            f['findLP1'] = [-2, 1]
            myutils.writeflag(f)
            with open('ops.txt', 'a', encoding='utf-8') as fi:
                fi.write('分区母线电压较高,降低发电机电压0.5个标幺值\n')
            return 'pause'
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
        f['findLP1'] = [-1, 1]
        myutils.writeflag(f)
        return 'pause'
    print('ssss%s-%s' % (fixnum, fixline))
    with open('ops.txt', 'a', encoding='utf-8') as fi:
        fi.write('发现电压异常母线:%s行,电压%s\n' % (fixline, fixnum))
    f['findLP1'] = [0, fixline]
    myutils.writeflag(f)
    return 'pause'
#
def makeFlowHigher():
    with open('ops.txt', 'a', encoding='utf-8') as fi:
        fi.write('知识:低潮流已收敛无异常母线->调高潮流\n')
    f = myutils.readflag()
    cur = f['cur']
    step = f['step']
    cur += step
    if cur > 1:
        cur = 1.0
    f['cur'] = cur
    f['goone'] = 1
    myutils.writeflag(f)
    return 'pause'
def setBus(busn):
    # 尝试调单个母线
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
    # 
    if busn in genList:
        # 发电机
        linen = genList[busn]
        ttt = setG(linen)
        if ttt == "fail":
            return ttt
        else:
            return 'success'
    if busn in loadList:
        # 负荷
        linen = loadList[busn]
        if linen == lastLoad_list[0]:
            lastLoad_list[1] = lastLoad_list[1] + 1
        else:
            lastLoad_list[0] = linen
            lastLoad_list[1] = 0
        f['lastLoad_list'] = lastLoad_list
        if lastLoad_list[1] > 3:
            # 已调整负荷附近的发电机多次
            ttt = setbyhand(busn)
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
        return 'success'
def makeFlowLower():
    # 调低之前先试一下调整最大误差母线
    print('makeFlowLower')
    with open('ops.txt', 'a', encoding='utf-8') as fi:
        fi.write('知识:低潮流已调试不收敛->调低潮流\n')
    '''
    x = followIter()
    for i in x:
        r = setBus(x)
        if r == 'success':
            return 'success'
    # 试了没用
    '''
    f = myutils.readflag()
    cur = f['cur']
    step = f['step']
    cur -= step
    step *= 0.5
    f['cur'] = cur
    f['step'] = step
    f['goone'] = 1
    myutils.writeflag(f)
    if step < 0.002:
        with open('ops.txt', 'a', encoding='utf-8') as fi:
            fi.write('潮流调低步长太小,调节失败\n')
        return 'steptoosmall'
    return 'pause'
def followIter():
    # 根据迭代信息返回最大误差母线行号
    return myutils.readMaxBus()
def findOp(s):
    if s == 'success':
        return s
    if s == 'fail':
        return s
    model = kb.Neo4j()
    model.connectDB()
    ans = model.findOps(s)
    if len(ans)>0:
        return ans[0]
    return 'goone'
fundict = {
    'goone' : findLP1,
    '调低潮流' : makeFlowLower,
    '调高潮流' : makeFlowHigher,
    '调节异常母线' : go2
}
def doOps(s):
    op = findOp(s)
    if op in fundict:
        r = fundict[op]()
        return r
    else :
        print('doOps(s):s:', s)
        return 'nocmd'