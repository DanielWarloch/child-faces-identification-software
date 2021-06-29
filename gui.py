import os.path

import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog

from database import person_database, face_encodings_database, photos_database, videos_database
from face_recognition import ChildFinder


class Ui_MainWindow(object):

    def __init__(self):
        self.child_finder = ChildFinder(person_database=person_database,
                                        face_encodings_database=face_encodings_database,
                                        photos_database=photos_database, video_database=videos_database)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1564, 824)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1551, 761))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        self.download_path_input = QtWidgets.QPlainTextEdit(self.tab)
        self.download_path_input.setGeometry(QtCore.QRect(60, 140, 651, 51))
        self.download_path_input.setObjectName("download_path_input")
        self.download_label = QtWidgets.QLabel(self.tab)
        self.download_label.setGeometry(QtCore.QRect(70, 50, 431, 51))

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)

        self.download_label.setFont(font)
        self.download_label.setObjectName("download_label")
        self.download_start_button = QtWidgets.QPushButton(self.tab)
        self.download_start_button.setGeometry(QtCore.QRect(50, 490, 651, 121))
        self.download_start_button.setObjectName("download_start_button")
        self.download_start_button.clicked.connect(self.download_start_button_Clicked)
        self.download_browse_button = QtWidgets.QPushButton(self.tab)
        self.download_browse_button.setGeometry(QtCore.QRect(540, 50, 171, 61))
        self.download_browse_button.setObjectName("download_browse_button")
        self.download_browse_button.clicked.connect(self.browse_txt_file_path)
        self.download_output_text = QtWidgets.QPlainTextEdit(self.tab)
        self.download_output_text.setGeometry(QtCore.QRect(910, 40, 541, 651))
        self.download_output_text.setObjectName("download_output_text")

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.encode_path_label = QtWidgets.QLabel(self.tab_2)
        self.encode_path_label.setGeometry(QtCore.QRect(80, 70, 321, 61))
        self.encode_path_label.setFont(font)
        self.encode_path_label.setObjectName("encode_path_label")
        self.encode_start_button = QtWidgets.QPushButton(self.tab_2)
        self.encode_start_button.setGeometry(QtCore.QRect(1180, 450, 221, 81))
        self.encode_start_button.setObjectName("encode_start_button")
        self.encode_start_button.clicked.connect(self.encode_start_button_Clicked)
        self.encode_path_input = QtWidgets.QPlainTextEdit(self.tab_2)
        self.encode_path_input.setGeometry(QtCore.QRect(410, 70, 861, 61))
        self.encode_path_input.setObjectName("encode_path_input")
        self.encode_progressbar = QtWidgets.QProgressBar(self.tab_2)
        self.encode_progressbar.setGeometry(QtCore.QRect(90, 450, 891, 71))
        self.encode_progressbar.setProperty("value", 0)
        self.encode_progressbar.setObjectName("encode_progressbar")
        self.encode_browse_button = QtWidgets.QPushButton(self.tab_2)
        self.encode_browse_button.setGeometry(QtCore.QRect(1310, 70, 171, 61))
        self.encode_browse_button.setObjectName("encode_browse_button")
        self.encode_browse_button.clicked.connect(self.browse_folder_path)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.find_label = QtWidgets.QLabel(self.tab_3)
        self.find_label.setGeometry(QtCore.QRect(10, 40, 201, 61))
        self.find_label.setFont(font)
        self.find_label.setObjectName("find_label")
        self.find_progressbar = QtWidgets.QProgressBar(self.tab_3)
        self.find_progressbar.setGeometry(QtCore.QRect(90, 580, 681, 81))
        self.find_progressbar.setProperty("value", 0)
        self.find_progressbar.setObjectName("find_progressbar")
        self.find_start_button = QtWidgets.QPushButton(self.tab_3)
        self.find_start_button.setGeometry(QtCore.QRect(640, 250, 161, 61))
        self.find_start_button.setObjectName("find_start_button")
        self.find_start_button.clicked.connect(self.find_start_button_Clicked)
        self.find_path_input = QtWidgets.QPlainTextEdit(self.tab_3)
        self.find_path_input.setGeometry(QtCore.QRect(220, 50, 221, 41))
        self.find_path_input.setObjectName("find_path_input")
        self.find_browse_button = QtWidgets.QPushButton(self.tab_3)
        self.find_browse_button.setGeometry(QtCore.QRect(470, 40, 141, 61))
        self.find_browse_button.setObjectName("find_browse_button")
        self.find_browse_button.clicked.connect(self.browse_photo_path)
        self.find_photo_to_find = QtWidgets.QLabel(self.tab_3)
        self.find_photo_to_find.setGeometry(QtCore.QRect(50, 120, 551, 421))
        self.find_photo_to_find.setFont(font)
        self.find_photo_to_find.setText("")
        self.find_photo_to_find.setObjectName("find_photo_to_find")
        self.find_photo_found = QtWidgets.QLabel(self.tab_3)
        self.find_photo_found.setGeometry(QtCore.QRect(900, 100, 551, 421))
        self.find_photo_found.setFont(font)
        self.find_photo_found.setText("")
        self.find_photo_found.setObjectName("find_photo_found")
        self.find_output_text = QtWidgets.QPlainTextEdit(self.tab_3)
        self.find_output_text.setGeometry(QtCore.QRect(890, 570, 581, 131))
        self.find_output_text.setObjectName("find_output_text")

        self.tabWidget.addTab(self.tab_3, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1564, 34))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.find_path_input, self.find_browse_button)
        MainWindow.setTabOrder(self.find_browse_button, self.find_start_button)
        MainWindow.setTabOrder(self.find_start_button, self.download_browse_button)
        MainWindow.setTabOrder(self.download_browse_button, self.encode_start_button)
        MainWindow.setTabOrder(self.encode_start_button, self.encode_path_input)
        MainWindow.setTabOrder(self.encode_path_input, self.encode_browse_button)
        MainWindow.setTabOrder(self.encode_browse_button, self.download_start_button)
        MainWindow.setTabOrder(self.download_start_button, self.tabWidget)
        MainWindow.setTabOrder(self.tabWidget, self.download_path_input)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.download_label.setText(_translate("MainWindow", "Select path to file with links to videos"))
        self.download_start_button.setText(_translate("MainWindow", "Start"))
        self.download_browse_button.setText(_translate("MainWindow", "Browse file"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Download videos"))
        self.encode_path_label.setText(_translate("MainWindow", "Select person folder path"))
        self.encode_start_button.setText(_translate("MainWindow", "Start"))
        self.encode_browse_button.setText(_translate("MainWindow", "Browse file"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Encode folder"))
        self.find_label.setText(_translate("MainWindow", "Select person photo"))
        self.find_start_button.setText(_translate("MainWindow", "Start"))
        self.find_browse_button.setText(_translate("MainWindow", "Browse file"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Find person"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))

    def browse_txt_file_path(self):
        fname = QFileDialog.getOpenFileName(QFileDialog(), 'Open file', os.path.abspath(os.getcwd() + '/..'),
                                            'TXT (*.txt)')
        self.download_path_input.setPlainText(fname[0])

    def browse_folder_path(self):
        fname = QFileDialog.getExistingDirectory(None, "Select Folder", os.path.abspath(os.getcwd() + '/..'))
        self.encode_path_input.setPlainText(fname)

    def browse_photo_path(self):
        fname = QFileDialog.getOpenFileName(QFileDialog(), 'Open file', os.path.abspath(os.getcwd() + '/..'),
                                            "Images (*.png *.xpm *.jpg)")
        self.find_path_input.setPlainText(fname[0])
        self.showSelectedPhoto(self.find_photo_to_find, self.find_path_input.toPlainText())

    def handle_Progress1(self, block_num, total_size):
        if total_size > 0:
            download_percentage = block_num * 100 / total_size
            self.encode_progressbar.setValue(download_percentage)
            QApplication.processEvents()

    def handle_Progress2(self, block_num, total_size):
        if total_size > 0:
            download_percentage = block_num * 100 / total_size
            self.find_progressbar.setValue(download_percentage)
            QApplication.processEvents()

    def handle_download_output(self, current):
        self.download_output_text.appendPlainText(current)
        QApplication.processEvents()

    def download_start_button_Clicked(self):
        print(self.download_path_input.toPlainText())
        self.child_finder.download_videos_from_urls_file(self, self.download_path_input.toPlainText(), download=True)

    def encode_start_button_Clicked(self):
        self.child_finder.encode_person_folder(ui=self,
                                               person_folder_path=self.encode_path_input.toPlainText(),
                                               add_to_database=True)

    def find_start_button_Clicked(self):
        person = self.child_finder.recognize_person_from_photo(img_path=self.find_path_input.toPlainText(), ui=self)
        print(person['photo_path'].values[0])
        self.showSelectedPhoto(self.find_photo_found, person['photo_path'].values[0])
        self.find_output_text.setPlainText(person.head(1).to_string())

    def showSelectedPhoto(self, obj, img_path):
        p = QPixmap(img_path)  # load pixmap
        # get label dimensions
        w = self.find_photo_to_find.width()
        h = self.find_photo_to_find.height()
        # set a scaled pixmap
        obj.setPixmap(p.scaled(w, h))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(dark_stylesheet)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
