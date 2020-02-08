# coding:utf-8

import myutils
import os

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
    
    b = cur/r
    f['r'] = cur
    changemx(b)
    myutils.writeflag(f)
    os.system('WMLFRTMsg')
    
    with open('ops.txt', 'a', encoding='utf-8') as fi:
        fi.write('当前潮流水平:%d%%\n' % int(cur * 100))
    conv = None
    if not myutils.getflag():
        f['goone'] = -1
        myutils.writeflag(f)
        conv = '不收敛'
        #return -1  #failure
    else:
        conv = '收敛'
    with open('ops.txt', 'a', encoding='utf-8') as fi:
        fi.write('当前收敛状态:%s\n' % conv)
    checked = None
    if ('findLP1' in f) and (f['findLP1'] != None):
        checked = '已检查'
    elif ('findLP1' in f) and (f['findLP1'] == None):
        checked = '已调节'
    else:
        checked = '未检查'
    with open('ops.txt', 'a', encoding='utf-8') as fi:
        fi.write('异常母线:%s\n' % checked)
    ####
    if checked == '已检查':
        return '有异常母线'
    
    if 'goone' in f:
        goone = f['goone']
        if goone == "fail":
            return 'fail'
        if goone == -1:  # fail
            return 'goone=-1'
        if goone == 0:  # success
            if (r - 1) < 0.001 and (r - 1) > -0.001:
                print('success')
                return 'success'
            return 'goone=0'
        if goone == 1:  # unknown , continue
            print('goone==1')
            return 'goone' #'goone':检查
    else:
        return 'goone'
