# coding:utf-8
import sys
import os

curpath = os.path.realpath(__file__)
prepath = curpath[:-7]
sys.path.append(prepath)

from PyQt5.QtCore import pyqtSignal, QThread
from Ui_MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap

import cmds
import kb
import tire.gentree
from tire.gentree import Node
import genDis

class Worker(QThread):
    sinOut = pyqtSignal()

    def __init__(self):
        super(Worker, self).__init__()

    def run(self):
        cmds.run()
        self.sinOut.emit()


class Test(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Test, self).__init__()
        self.thread = Worker()
        self.setupUi(self)
        self.connector()
        self.show()
        
        ####
        self.dir_flag = 0

    def connector(self):
        self.chooseButton.clicked.connect(self.choose_file)
        self.searchButton_actions.clicked.connect(self.display_running_state)  # 多步调整

        self.searchButton_actions_one_step.clicked.connect(self.search_actions_one_step)  # 单步调整
        
        self.searchButton_knowledge.clicked.connect(self.search_knowledge) # 查询知识
        
        self.AddButton_knowledge.clicked.connect(self.add_knowledge)
        self.deleteButton_knowledge.clicked.connect(self.del_knowledge)
        
    def search_actions_one_step(self):
        # self.textEdit_display_actions.setText("Hello World")
        r = cmds.runOne()
        self.textEdit_display_actions.append(r)

    def search_knowledge(self):
        if self.dir_flag == 1:
            os.chdir('./../')
            self.dir_flag = 0
        input_knowledge = self.lineEdit_input_knowledge.text()  # 输入的查询知识
        r = ''
        q = tire.gentree.getwords(input_knowledge)
        print(q)
        model = kb.global_model
        ans = model.search(q)
        ans2 = model.search1(input_knowledge)
        ans.extend(ans2)
        ans = set(ans)
        if len(ans) == 0:
            self.textEdit_display_knowledge.setText('没有相关内容')
        else:
            for i in ans:
                for j in i:
                    r += j + ' '
                r+='\n'
            self.textEdit_display_knowledge.setText(r)
    def del_knowledge(self):
        input_knowledge = self.lineEdit_input_knowledge.text()
        sp = input_knowledge.split(' ')
        if len(sp) != 3:
            self.textEdit_display_knowledge.setText('请正确输入要删除的知识\n (空格分隔的三元组, 且前后无空格)')
            return
        model = kb.global_model
        r = model.del_knowledge(sp)
        self.textEdit_display_knowledge.setText(r)

    def display_running_state(self):
        self.textEdit_display_actions.setText('调整中...')
        # QApplication.processEvents()
        self.thread.start()
        self.thread.sinOut.connect(self.search_actions)

    def show_graph(self, graph_path):
        self.label_graph.setPixmap(QPixmap(graph_path))
        self.label_graph.setScaledContents(True)

    def search_actions(self):
        res = ''
        with open('result.txt', encoding="utf-8") as f:
            res = f.read()
        self.textEdit_display_actions.append(res)

    def choose_file(self):
        # file = QFileDialog.getOpenFileName(self, 'Select files', os.getcwd(), 'All Files (*)')
        # print(file[0])
        # if file[0]:
        # self.lineEdit_initLF.insert(file[0])
        folder = QFileDialog.getExistingDirectory(self, "Select folder", os.getcwd())
        if folder:
            self.lineEdit_initLF.insert(folder)
            os.chdir(folder)
            self.dir_flag = 1
            import myutils
            genDis.main()
    #####
    def add_knowledge(self):
        n1 = self.lineEdit_2.text()
        n2 = self.lineEdit_3.text()
        n3 = self.lineEdit_4.text()
        tuple_list = (n1,n2,n3)
        model = kb.global_model
        model.addonetuple(tuple_list)
        self.textEdit.setText('加入成功\n%s\n%s\n%s\n' % (n1,n2,n3))

def main():
    app = QApplication(sys.argv)
    T = Test()
    T.show_graph(prepath + "9.bmp")
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()