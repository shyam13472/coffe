import sys
from PyQt5 import uic
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.run()
        self.pushButton_3.clicked.connect(self.open_editor)
        self.a = 0

    def run(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        res = cur.execute('SELECT * FROM coffee')
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(7)
        for i, row2 in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, row in enumerate(row2):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(row)))
        self.tableWidget.setHorizontalHeaderLabels(['id', 'Сорт',
                                                    'Степень обжарки', 'Молотый/в зернах',
                                                    'Вкус', 'Цена', 'Объем упаковки'])
        self.tableWidget.resizeColumnsToContents()
        con.close()

    def open_editor(self):
        ex.hide()
        edit.show()


class Edit(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton_5.clicked.connect(self.back)
        self.pushButton_4.clicked.connect(self.make)
        self.pushButton_3.clicked.connect(self.delete)
        self.con = sqlite3.connect("coffee.sqlite")
        cur = self.con.cursor()
        res = cur.execute('SELECT * FROM coffee')
        self.tableWidget.setColumnCount(7)
        for i, row2 in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, row in enumerate(row2):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(row)))
        self.tableWidget.setHorizontalHeaderLabels(['id', 'Сорт',
                                                    'Степень обжарки', 'Молотый/в зернах',
                                                    'Вкус', 'Цена', 'Объем упаковки'])
        self.tableWidget.resizeColumnsToContents()

        self.tableWidget.itemChanged.connect(self.item_changed)
        self.modified = {}

    def delete(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        cur = self.con.cursor()
        cur.execute("DELETE from coffee WHERE id in (" +
                    ", ".join('?' * len(ids)) + ")", ids)
        self.con.commit()
        res = cur.execute('SELECT * FROM coffee')
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(7)
        for i, row2 in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, row in enumerate(row2):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(row)))
        self.tableWidget.setHorizontalHeaderLabels(['id', 'Сорт',
                                                    'Степень обжарки', 'Молотый/в зернах',
                                                    'Вкус', 'Цена', 'Объем упаковки'])
        self.tableWidget.resizeColumnsToContents()

    def back(self):
        ex.run()
        ex.show()
        edit.hide()

    def item_changed(self, item):
        if item.row() not in self.modified:
            self.modified[item.row()] = [item.row() + 1, '', '', '', '', '', '']
        self.modified[item.row()][item.column()] = item.text()
        cur = self.con.cursor()
        for i in self.modified:
            try:
                cur.execute("""UPDATE coffee SET
                     id = {} WHERE id = {}""".format(self.modified[i][0], i + 1))
            except:
                pass
            try:
                cur.execute("""UPDATE coffee SET
                     Variety = {} WHERE id = {}""".format(self.modified[i][1], i + 1))
            except:
                pass
            try:
                cur.execute("""UPDATE coffee SET Degree = {}
                     WHERE id = {}""".format(self.modified[i][2], i + 1))
            except:
                pass
            try:
                cur.execute(
                    """UPDATE coffee SET Groundgrains = {}
                     WHERE id = {}""".format(self.modified[i][3], i + 1))
            except:
                pass
            try:
                cur.execute("""UPDATE coffee SET Taste = {}
                     WHERE id = {}""".format(self.modified[i][4], i + 1))
            except:
                pass
            try:
                cur.execute("""UPDATE coffee SET Price = {}
                     WHERE id = {}""".format(self.modified[i][5], i + 1))
            except:
                pass
            try:
                cur.execute("""UPDATE coffee SET Volume = {}
                     WHERE id = {}""".format(self.modified[i][6], i + 1))
            except:
                pass
            self.con.commit()

    def make(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        cur = self.con.cursor()
        res = cur.execute('SELECT * FROM coffee')
        a = 1
        for i in res:
            if a != i[0]:
                break
            a += 1
        cur.execute("INSERT INTO coffee(id, Variety, Degree, Groundgrains, Taste, Price, Volume) "
                    "VALUES({}, '', '', '', '', '', '')".format(a))
        self.con.commit()
        res = cur.execute('SELECT * FROM coffee')
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(7)
        for i, row2 in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, row in enumerate(row2):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(row)))
        self.tableWidget.setHorizontalHeaderLabels(['id', 'Сорт',
                                                    'Степень обжарки', 'Молотый/в зернах',
                                                    'Вкус', 'Цена', 'Объем упаковки'])
        self.tableWidget.resizeColumnsToContents()


app = QApplication(sys.argv)
ex = MyWidget()
edit = Edit()
ex.show()
sys.exit(app.exec())