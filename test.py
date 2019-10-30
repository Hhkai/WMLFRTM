# coding:utf-8
from PyQt5.QtCore import pyqtSignal, QThread

from Ui_MainWindow import Ui_MainWindow
import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap

import main


class Worker(QThread):
    sinOut = pyqtSignal()
    def __init__(self):
        super(Worker, self).__init__()

    def run(self):
        main.run()
        self.sinOut.emit()


class Test(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Test, self).__init__()
        self.thread = Worker()
        self.setupUi(self)
        self.connector()
        self.show()

    def connector(self):
        self.chooseButton.clicked.connect(self.choose_file)
        self.searchButton_actions.clicked.connect(self.display_running_state)  # 多步调整
        # self.searchButton_actions.clicked.connect(self.search_actions)  # 多步调整

        self.searchButton_actions_one_step.clicked.connect(self.search_actions_one_step)  # 单步调整
        # self.searchButton_knowledge.clicked.connect(self.search_knowledge) # 查询知识

        # 为线程按钮绑定函数
        # self.searchButton_knowledge.clicked.connect(self.slot_start)

    #########################################################
    # 线程中每个循环结束发送一个信号，接收信号运行slot_add在文本框里打印
    # def slot_start(self):
    #     # self.searchButton_knowledge.setEnabled(False)
    #     self.thread.start()
    #     self.thread.sinOut.connect(self.slot_add)
    #
    # def slot_add(self, index):
    #     self.textEdit_display_knowledge.append(index)

    #########################################################

    def search_actions_one_step(self):
        # self.textEdit_display_actions.setText("Hello World")
        r = main.runOne()
        self.textEdit_display_actions.append(r)

    def search_knowledge(self):
        input_knowledge = self.lineEdit_input_knowledge.text()  # 输入的查询知识

        self.textEdit_display_knowledge.setText("Hello World")

    def display_running_state(self):
        self.textEdit_display_actions.setText('调整中...')
        # QApplication.processEvents()
        self.thread.start()
        self.thread.sinOut.connect(self.search_actions)

    def show_graph(self, graph_path):
        self.label_graph.setPixmap(QPixmap(graph_path))
        self.label_graph.setScaledContents(True)

    def search_actions(self):
        #main.run()
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
            import myutils


if __name__ == '__main__':
    app = QApplication(sys.argv)
    T = Test()
    T.show_graph("9.bmp")
    sys.exit(app.exec_())
