from py2neo import Graph, Node, Relationship, cypher, Path
import neo4j
class Neo4j():
    graph = None
    def __init__(self):
        print("create neo4j class ...")

    def connectDB(self):
        self.graph = Graph("http://localhost:7474", username="neo4j", password="123456")

    def matchItembyTitle(self,value):

        sql = "MATCH (n:Item { title: '" + str(value) + "' }) return n;"
        answer = self.graph.run(sql).data()
        return answer

    # 根据title值返回互动百科item
    def matchHudongItembyTitle(self,value):
        sql = "MATCH (n:HudongItem { title: '" + str(value) + "' }) return n;"
        try:
            answer = self.graph.run(sql).data()
        except:
            print(sql)
        return answer

    # 根据entity的名称返回关系
    def getEntityRelationbyEntity(self,value):
        answer = self.graph.run("MATCH (entity1) - [rel] -> (entity2)  WHERE entity1.title = \"" +str(value)+"\" RETURN rel,entity2").data()
        return answer

    #查找entity1及其对应的关系（与getEntityRelationbyEntity的差别就是返回值不一样）
    def findRelationByEntity(self,entity1):
        answer = self.graph.run("MATCH (n1 {title:\""+str(entity1)+"\"})- [rel] -> (n2) RETURN n1,rel,n2" ).data()
        # if(answer is None):
        #     answer = self.graph.run("MATCH (n1:NewNode {title:\""+entity1+"\"})- [rel] -> (n2) RETURN n1,rel,n2" ).data()
        return answer

    #查找entity2及其对应的关系
    def findRelationByEntity2(self,entity1):
        answer = self.graph.run("MATCH (n1)- [rel] -> (n2 {title:\""+str(entity1)+"\"}) RETURN n1,rel,n2" ).data()

        # if(answer is None):
        #     answer = self.graph.run("MATCH (n1)- [rel] -> (n2:NewNode {title:\""+entity1+"\"}) RETURN n1,rel,n2" ).data()
        return answer

    #根据entity1和关系查找enitty2
    def findOtherEntities(self,entity,relation):
        answer = self.graph.run("MATCH (n1 {title:\"" + str(entity) + "\"})- [rel {type:\""+str(relation)+"\"}] -> (n2) RETURN n1,rel,n2" ).data()
        #if(answer is None):
        #    answer = self.graph.run("MATCH (n1:NewNode {title:\"" + entity + "\"})- [rel:RELATION {type:\""+relation+"\"}] -> (n2) RETURN n1,rel,n2" ).data()

        return answer

    #根据entity2和关系查找enitty1
    def findOtherEntities2(self,entity,relation):
        answer = self.graph.run("MATCH (n1)- [rel {type:\""+str(relation)+"\"}] -> (n2 {name:\"" + str(entity) + "\"}) RETURN n1,rel,n2" ).data()
        #if(answer is None):
        #    answer = self.graph.run("MATCH (n1)- [rel:RELATION {type:\""+relation+"\"}] -> (n2:NewNode {title:\"" + entity + "\"}) RETURN n1,rel,n2" ).data()

        return answer

    #根据两个实体查询它们之间的最短路径
    def findRelationByEntities(self,entity1,entity2):
        answer = self.graph.run("MATCH (p1:HudongItem {title:\"" + str(entity1) + "\"}),(p2:HudongItem{title:\""+str(entity2)+"\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN rel").evaluate()
        #answer = self.graph.run("MATCH (p1:HudongItem {title:\"" + entity1 + "\"})-[rel:RELATION]-(p2:HudongItem{title:\""+entity2+"\"}) RETURN p1,p2").data()
        
        if(answer is None):    
            answer = self.graph.run("MATCH (p1:HudongItem {title:\"" + str(entity1) + "\"}),(p2:NewNode {title:\""+str(entity2)+"\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN p").evaluate()
        if(answer is None):
            answer = self.graph.run("MATCH (p1:NewNode {title:\"" + str(entity1) + "\"}),(p2:HudongItem{title:\""+str(entity2)+"\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN p").evaluate()
        if(answer is None):
            answer = self.graph.run("MATCH (p1:NewNode {title:\"" + str(entity1) + "\"}),(p2:NewNode {title:\""+str(entity2)+"\"}),p=shortestpath((p1)-[rel:RELATION*]-(p2)) RETURN p").evaluate()
        #answer = self.graph.data("MATCH (n1:HudongItem {title:\"" + entity1 + "\"})- [rel] -> (n2:HudongItem{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
        #if(answer is None):
        #    answer = self.graph.data("MATCH (n1:HudongItem {title:\"" + entity1 + "\"})- [rel] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
        #if(answer is None):
        #    answer = self.graph.data("MATCH (n1:NewNode {title:\"" + entity1 + "\"})- [rel] -> (n2:HudongItem{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
        #if(answer is None):
        #    answer = self.graph.data("MATCH (n1:NewNode {title:\"" + entity1 + "\"})- [rel] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" )
        relationDict = []
        if(answer is not None):
            for x in answer:
                tmp = {}
                start_node = x.start_node
                end_node = x.end_node
                tmp['n1'] = start_node
                tmp['n2'] = end_node
                tmp['rel'] = x
                relationDict.append(tmp)        
        return relationDict

    #查询数据库中是否有对应的实体-关系匹配
    def findEntityRelation(self,entity1,relation,entity2):
        answer = self.graph.run("MATCH (n1:HudongItem {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\""+str(relation)+"\"}] -> (n2:HudongItem{title:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
        if(answer is None):
            answer = self.graph.run("MATCH (n1:HudongItem {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\""+str(relation)+"\"}] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
        if(answer is None):
            answer = self.graph.run("MATCH (n1:NewNode {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\""+str(relation)+"\"}] -> (n2:HudongItem{title:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()
        if(answer is None):
            answer = self.graph.run("MATCH (n1:NewNode {title:\"" + str(entity1) + "\"})- [rel:RELATION {type:\""+str(relation)+"\"}] -> (n2:NewNode{title:\""+entity2+"\"}) RETURN n1,rel,n2" ).data()

        return answer
    def findOps(self,entity2):
        ans = self.findOtherEntities2(entity2,'有特征')
        return [i['n1'].get('name') for i in ans]
    def search3(self, n1, n2, n3):
        ans = self.graph.run("MATCH (n1:ett {name:\"%s\"})- [rel:RELATION {type:\"%s\"}] -> (n2:ett{name:\"%s\"}) RETURN n1,rel,n2" % (n1,n2,n3)).data()
        return [(i['n1'].get('name'), i['rel'].get('type'), i['n2'].get('name')) for i in ans]
    def search2(self, n1, n2):
        res = []
        ans = self.graph.run("MATCH (n1:ett {name:\"%s\"})- [rel] -> (n2:ett{name:\"%s\"}) RETURN n1,rel,n2" % (n1,n2)).data()
        res.extend(ans)
        ans = self.graph.run("MATCH (n1:ett )- [rel:RELATION {type:\"%s\"}] -> (n2:ett{name:\"%s\"}) RETURN n1,rel,n2" % (n1,n2)).data()
        res.extend(ans)
        ans = self.graph.run("MATCH (n1:ett {name:\"%s\"})- [rel:RELATION {type:\"%s\"}] -> (n2:ett) RETURN n1,rel,n2" % (n1,n2)).data()
        res.extend(ans)
        return [(i['n1'].get('name'), i['rel'].get('type'), i['n2'].get('name')) for i in res]
    def search1(self, n1):
        res = []
        ans = self.graph.run("MATCH (n1:ett )- [rel:RELATION {type:\"%s\"}] -> (n2:ett) RETURN n1,rel,n2" % n1).data()
        res.extend(ans)
        ans = self.graph.run("MATCH (n1:ett {name:\"%s\"})- [rel] -> (n2:ett) RETURN n1,rel,n2" % n1).data()
        res.extend(ans)
        ans = self.graph.run("MATCH (n1:ett )- [rel] -> (n2:ett{name:\"%s\"}) RETURN n1,rel,n2" % n1).data()
        res.extend(ans)
        return [(i['n1'].get('name'), i['rel'].get('type'), i['n2'].get('name')) for i in res]
    def search(self, word_lists):
        len_w = len(word_lists)
        res = []
        if len_w >= 3:
            n1 = word_lists[0]
            n2 = word_lists[1]
            n3 = word_lists[2]
            #print(n1,n2,n3)
            ans = self.search3(n1,n2,n3)
            if len(ans) > 0:
                return ans
            res = []
            ans = self.search2(n1,n2)
            res.extend(ans)
            ans = self.search2(n1,n3)
            res.extend(ans)
            ans = self.search2(n2,n3)
            res.extend(ans)
            if len(res) > 0:
                return res
            res = []
            ans = self.search1(n1)
            res.extend(ans)
            ans = self.search1(n2)
            res.extend(ans)
            ans = self.search1(n3)
            res.extend(ans)
            if len(res) > 0:
                return res
        elif len_w == 2:
            n1 = word_lists[0]
            n2 = word_lists[1]
            return self.search2(n1,n2)
        elif len_w == 1:
            n1 = word_lists[0]
            return self.search1(n1)
        else:
            return []
        return 
    def addonetuple(self, tuple_in):
        n1 = tuple_in[0]
        n2 = tuple_in[1]
        n3 = tuple_in[2]
        ans1 = self.graph.run("MATCH (n:ett { name: \"%s\" }) return n" % n1).data()
        if len(ans1) == 0: 
            self.graph.run("create(n:ett{name:\"%s\",cls:\"2\"})" % n1)
        ans3 = self.graph.run("MATCH (n:ett { name: \"%s\" }) return n" % n3).data()
        if len(ans3) == 0: 
            self.graph.run("create(n:ett{name:\"%s\",cls:\"2\"})" % n3)
        ans2 = self.graph.run("MATCH (n1:ett {name:\"%s\"})- [rel:RELATION {type:\"%s\"}] -> (n2:ett{name:\"%s\"}) RETURN n1,rel,n2" % (n1,n2,n3)).data()
        if len(ans2) == 0:
            self.graph.run("MATCH (entity1:ett{name:\"%s\"}), (entity2:ett{name:\"%s\"}) CREATE (entity1)-[:RELATION { type: \"%s\" }]->(entity2)" % (n1,n3,n2))
    def del_knowledge(self, list_in):
        n1 = list_in[0]
        n2 = list_in[1]
        n3 = list_in[2]
        ans = self.graph.run("MATCH (n1:ett {name:\"%s\"})- [rel:RELATION {type:\"%s\"}] -> (n2:ett{name:\"%s\"}) return n1,rel,n2" % (n1,n2,n3)).data()
        if len(ans) == 0:
            return '没有这条知识:%s %s %s' % (n1,n2,n3)
        self.graph.run("MATCH (n1:ett {name:\"%s\"})- [rel:RELATION {type:\"%s\"}] -> (n2:ett{name:\"%s\"}) delete rel" % (n1,n2,n3))
        return '删除成功:%s %s %s' % (n1,n2,n3)

global_model = Neo4j()
global_model.connectDB()

if __name__ == '__main__':
    model = Neo4j()
    model.connectDB()
    #a = model.findRelationByEntity('母线')
    #print(a[0]['n1'].get('title'),type(a[0]['n1']))
    #print(dir(a[0]['n1']))
    #print(model.graph.run("MATCH (n:ett { name: \"%s\" }) return n" % '母线1').data())
    #model.graph.run("MATCH (n:ett { name: \"%s\" }) return n" % '母线1')
    #print(model.graph.run("MATCH (n1:ett {name:\"%s\"})- [rel:RELATION {type:\"%s\"}] -> (n2:ett{title:\"%s\"}) RETURN n1,rel,n2" % ('母线','有属性','电压')).data())
    print(model.search(['母线','有属性','电压']))