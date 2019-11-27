def read():
    cnt = 0
    cntL = 0
    flag = 'DF'
    dic = dict()
    with open('aaa.txt', encoding = 'utf8') as f, open('bbb.txt', 'a', encoding='utf8') as w:
        lines = f.readlines()
        for line in lines:
            templine = line.strip().split()
            if len(templine)==0:
                continue
            for i in (templine[0], templine[2]):
                if i not in dic:
                    dic[i]=flag+str(cnt) 
                    cnt += 1
                    w.write('%s [label="%s"]\n' % (dic[i],i))
            #
            w.write('%s -> %s [label="%s"]\n' % (dic[templine[0]], dic[templine[2]], templine[1]))
read()