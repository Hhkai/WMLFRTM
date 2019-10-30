#coding:utf-8

import FeatureS
import ops
import os

import shutil

CUR_DIR = os.getcwd()

def compare_result(l2_before, l2_after, l5_before, l5_after, l6_before,
                   l6_after, l1, lfreport_file, outfile):
    # dic = ["有效", "无效"]
    with open(l6_before,
              "r", encoding="utf-8") as f1, open(l6_after,
                                                 "r",
                                                 encoding="utf-8") as f2:
        i = 1
        for row1, row2 in zip(f1, f2):
            row1 = row1.strip().split(",")
            row2 = row2.strip().split(",")
            active_power1 = float(row1[4].strip())
            active_power2 = float(row2[4].strip())
            reactive_power1 = float(row1[5].strip())
            reactive_power2 = float(row2[5].strip())
            if not (abs(active_power1 - active_power2) < 1e-3
                    and abs(active_power1 - active_power2) < 1e-3):
                return ("l6_" + str(i) + "error")
            i += 1

    bus_set = []
    with open(l1, "r", encoding="utf-8") as f:
        for row in f:
            bus_name = row.strip().split(",")[0][1:-1].strip()
            bus_set.append(bus_name)
    # print(bus_set)
    res = []
    res.append("发电机:")
    with open(l5_before,
              "r", encoding="utf-8") as f1, open(l5_after,
                                                 "r",
                                                 encoding="utf-8") as f2:
        for row1, row2 in zip(f1, f2):
            row1 = row1.strip().split(",")
            row2 = row2.strip().split(",")
            bus_name = row1[-2].strip()[1:-1]
            node_type = int(eval(row1[2].strip()))
            active_power1 = float(row1[3].strip())
            active_power2 = float(row2[3].strip())
            reactive_power1 = float(row1[4].strip())
            reactive_power2 = float(row2[4].strip())
            if node_type not in [0, 1, -1]:
                return "l5_node_type_error"
            elif node_type == 1:
                if active_power1 != active_power2 or reactive_power1 != reactive_power2:
                    res.append(bus_name + ": " + "%.3f" % active_power1 +
                               " + " + "%.3f" % reactive_power1 + "j --> " +
                               "%.3f" % active_power2 + " + " +
                               "%.3f" % reactive_power2 + "j")

            elif node_type == -1:
                if active_power1 != active_power2:
                    res.append(bus_name + ": " + "%.3f" % active_power1 +
                               " + " + " --> " + "%.3f" % active_power2)
    with open(l2_before,
              "r", encoding="utf-8") as f1, open(l2_after,
                                                 "r",
                                                 encoding="utf-8") as f2:
        i = 1
        res.append("电容电抗器:")
        for row1, row2 in zip(f1, f2):
            row1 = row1.split(",")[:3]
            row2 = row2.split(",")[:3]
            valid1 = int(eval(row1[0].strip()))
            valid2 = int(eval(row2[0].strip()))
            if row1[1] == row1[2]:
                if valid1 != valid2:
                    # res.append(
                    #     str(i) + ": " + dic[int(valid1)] + "改为" +
                    #     dic[int(valid2)])
                    # print(i)
                    res.append("line " + str(i) + ' :' +bus_set[int(row1[1].strip()) - 1] + ": " +
                               str(valid1) + " --> " + str(valid2))
            i += 1

    res.append("潮流计算结果:")
    with open(lfreport_file, "r", encoding="gbk") as f:
        res.append(f.read())
    with open(outfile, "a", encoding="utf-8") as f:
        # with open(outfile, "w", encoding="utf-8") as f:
        for row in res:
            f.write(row + "\n")

def run():
    while True:
        s = FeatureS.getFeatures()
        r = ops.doOps(s)
        if r == -1:
            break
    os.system('del result.txt')
    compare_result("../34/LF.L2", "LF.L2", "../34/LF.L5", "LF.L5", "../34/LF.L6", "LF.L6",
                "LF.L1", "lfreport.lis", "result.txt")
def runOne():
    while True:
        s = FeatureS.getFeatures()
        r = ops.doOps(s)
        if r == -1:
            return 'success'
        if r == 'pause':
            with open('ops.txt', encoding='utf-8') as f:
                r = f.read()
            os.system('del ops.txt')
            #print(r)
            return r

if __name__ == "__main__":
    cur_dir = os.path.join(CUR_DIR, '34n')
    os.chdir(cur_dir)
    
    import myutils
    
    while True:
        a=input('func:')
        if a=='1':
            print(runOne())
        if a=='2':
            run()
        if a == '0':
            exit()