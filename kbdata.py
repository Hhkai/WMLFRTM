from py2neo import Graph, Node, Relationship, NodeMatcher
import re 

m='\s*(.*?)\s*\[\s*label\s*=\s*"(.*)"\s*\]\s*'
m = re.compile(m)
m2 = '\s*(.*?)\s*->\s*(.*)\s*'
m2 = re.compile(m2)

class Data(object):
    def __init__(self):
        self.g = Graph(
            host = "127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="123456"
        )
        self.matcher = NodeMatcher(self.g)
    def clear(self):
        self.g.delete_all()
    def first_init(self):
        self.g.delete_all()
        matcher = NodeMatcher(self.g)
        with open('aaa.txt', encoding='utf-8') as f:
            for i in f.readlines():
                i = i.strip()
                r = m.match(i)
                if r:
                    print(r.groups()) 
                    #('A1 -> A2', '是') or ('A1', '潮流收敛调整')
                    r2 = m2.match(r.group(1))
                    if r2:
                        #print(r2.groups())
                        #('A1', 'A3')
                        n1 = matcher.match(r2.group(1)).first()
                        n2 = matcher.match(r2.group(2)).first()
                        tempN = Relationship(n1, r.group(2), n2)
                    else:
                        tempN = Node(r.group(1),name=r.group(2))
                    self.g.create(tempN)
#
if __name__ == '__main__':
    handler = Data()
    # handler.first_init()
    s = handler.matcher.match(name="集合")
    for i in s:
        print(type(i))