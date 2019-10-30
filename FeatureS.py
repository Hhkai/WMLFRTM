# coding:utf-8

import myutils

def getFeatures():
    f = myutils.readflag()
    if len(f) == 0:
        f['r'] = 1.0
        f['cur'] = 0.3
        f['lastLoad_list'] = [-1, 0]
        f['step'] = 0.04
        f['markList'] = []
    r = f['r']
    cur = f['cur']
    step = f['step']
    myutils.writeflag(f)
    if 'goone' in f:
        goone = f['goone']
        if goone == "fail":
            return False
        if goone == -1:  # fail
            cur -= step
            step *= 0.5
            f['cur'] = cur
            f['step'] = step
            myutils.writeflag(f)
            if step < 0.002:
                return False
        if goone == 0:  # success
            if (r - 1) < 0.001 and (r - 1) > -0.001:
                print('success')
                return 'success'
            cur += step
            if cur > 1:
                cur = 1.0
            f['cur'] = cur
            myutils.writeflag(f)
            return 'goone'
        if goone == 1:  # unknown , continue
            print('goone==1')
            return 'goone'
    else:
        return 'goone'
    if 'cur' in f:
        pass 
    if 'r' in f:
        if (r - 1) < 0.001 and (r - 1) > -0.001:
            print('???')
            return 
        if r > 1:
            print('QAQ')
            return
    
    
    if myutils.getflag():
        return "收敛"
def findLP1(genList, loadList, markList):
    lp1 = readfile('LF.LP1', coding='gb2312')
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
    mx5 = readfile('LF.L5')
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
            writefile('LF.L5', mx5)
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