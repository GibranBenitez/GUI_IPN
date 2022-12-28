from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QSpinBox, QRadioButton, QCheckBox, QLabel, QFileDialog, QShortcut
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QKeySequence, QKeyEvent
from pathlib import Path
import sys, glob, os, time, random, shutil 
from threading import Timer

classes_id = ["D0X: No-gest", "B0A: Point-1f", "B0B: Point-2f", "G01: Click-1f", "G02: Click-2f", "G03: Th-up", "G04: Th-down", 
				"G05: Th-left", "G06: Th-right", "G07: Open-2", "G08: 2click-1f", "G09: 2click-2f", "G10: Zoom-in", "G11: Zoom-o", "G12: Catch"]
random.seed(42)
colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(classes_id))]
colors.append([255, 255, 255])


class UI_report(QMainWindow):
	def __init__(self, MainWindow):
		super(UI_report, self).__init__()

		# Load the ui file
		uic.loadUi("report.ui", self)
		self.shortcut_close = QShortcut(QKeySequence('Ctrl+Q'), self)
		self.shortcut_close.activated.connect(lambda: self.close())

		# Define our widgets
		self.button = self.findChild(QPushButton, "pb_1")
		
		self.lbt = self.findChild(QLabel, "lb_t")
		self.lb0 = self.findChild(QLabel, "lb_0")
		self.lb1 = self.findChild(QLabel, "lb_1")
		self.lb2 = self.findChild(QLabel, "lb_2")
		self.lb3 = self.findChild(QLabel, "lb_3")
		self.lb4 = self.findChild(QLabel, "lb_4")
		self.lb5 = self.findChild(QLabel, "lb_5")
		self.lb6 = self.findChild(QLabel, "lb_6")
		self.lb7 = self.findChild(QLabel, "lb_7")
		self.lb8 = self.findChild(QLabel, "lb_8")
		self.lb9 = self.findChild(QLabel, "lb_9")
		self.lb10 = self.findChild(QLabel, "lb_10")
		self.lb11 = self.findChild(QLabel, "lb_11")
		self.lb12 = self.findChild(QLabel, "lb_12")
		self.lb13 = self.findChild(QLabel, "lb_13")
		self.lb14 = self.findChild(QLabel, "lb_14")
		self.lb15 = self.findChild(QLabel, "lb_15")
		self.lb16 = self.findChild(QLabel, "lb_16")

		self.rb0 = self.findChild(QRadioButton, "rb_0")
		self.rb1 = self.findChild(QRadioButton, "rb_1")
		self.rb2 = self.findChild(QRadioButton, "rb_2")
		self.rb3 = self.findChild(QRadioButton, "rb_3")
		self.rb4 = self.findChild(QRadioButton, "rb_4")
		self.rb5 = self.findChild(QRadioButton, "rb_5")
		self.rb6 = self.findChild(QRadioButton, "rb_6")
		self.rb7 = self.findChild(QRadioButton, "rb_7")
		self.rb8 = self.findChild(QRadioButton, "rb_8")
		self.rb9 = self.findChild(QRadioButton, "rb_9")

		self.rb10 = self.findChild(QRadioButton, "rb_10")
		self.rb11 = self.findChild(QRadioButton, "rb_11")
		self.rb12 = self.findChild(QRadioButton, "rb_12")
		self.rb13 = self.findChild(QRadioButton, "rb_13")
		self.rb14 = self.findChild(QRadioButton, "rb_14")
		self.rb15 = self.findChild(QRadioButton, "rb_15")
		self.rb16 = self.findChild(QRadioButton, "rb_16")
		self.rb17 = self.findChild(QRadioButton, "rb_17")
		self.rb18 = self.findChild(QRadioButton, "rb_18")
		self.rb19 = self.findChild(QRadioButton, "rb_19")

		self.rb20 = self.findChild(QRadioButton, "rb_20")
		self.rb21 = self.findChild(QRadioButton, "rb_21")
		self.rb22 = self.findChild(QRadioButton, "rb_22")
		self.rb23 = self.findChild(QRadioButton, "rb_23")
		self.rb24 = self.findChild(QRadioButton, "rb_24")
		self.rb25 = self.findChild(QRadioButton, "rb_25")
		self.rb26 = self.findChild(QRadioButton, "rb_26")
		self.rb27 = self.findChild(QRadioButton, "rb_27")
		self.rb28 = self.findChild(QRadioButton, "rb_28")
		self.rb29 = self.findChild(QRadioButton, "rb_29")

		self.rb30 = self.findChild(QRadioButton, "rb_30")
		self.rb31 = self.findChild(QRadioButton, "rb_31")
		self.rb32 = self.findChild(QRadioButton, "rb_32")
		self.rb33 = self.findChild(QRadioButton, "rb_33")
		self.rb34 = self.findChild(QRadioButton, "rb_34")
		self.rb35 = self.findChild(QRadioButton, "rb_35")
		self.rb36 = self.findChild(QRadioButton, "rb_36")
		self.rb37 = self.findChild(QRadioButton, "rb_37")
		self.rb38 = self.findChild(QRadioButton, "rb_38")
		self.rb39 = self.findChild(QRadioButton, "rb_39")

		self.rb40 = self.findChild(QRadioButton, "rb_40")
		self.rb41 = self.findChild(QRadioButton, "rb_41")
		self.rb42 = self.findChild(QRadioButton, "rb_42")
		self.rb43 = self.findChild(QRadioButton, "rb_43")
		self.rb44 = self.findChild(QRadioButton, "rb_44")
		self.rb45 = self.findChild(QRadioButton, "rb_45")

		self.rb0.setVisible(False)
		self.rb1.setVisible(False)
		self.rb2.setVisible(False)
		self.rb3.setVisible(False) 
		self.rb4.setVisible(False) 
		self.rb5.setVisible(False)
		self.rb6.setVisible(False) 
		self.rb7.setVisible(False) 
		self.rb8.setVisible(False) 
		self.rb9.setVisible(False) 

		self.rb10.setVisible(False) 
		self.rb11.setVisible(False) 
		self.rb12.setVisible(False) 
		self.rb13.setVisible(False) 
		self.rb14.setVisible(False) 
		self.rb15.setVisible(False) 
		self.rb16.setVisible(False) 
		self.rb17.setVisible(False) 
		self.rb18.setVisible(False) 
		self.rb19.setVisible(False) 

		self.rb20.setVisible(False) 
		self.rb21.setVisible(False) 
		self.rb22.setVisible(False) 
		self.rb23.setVisible(False) 
		self.rb24.setVisible(False) 
		self.rb25.setVisible(False) 
		self.rb26.setVisible(False) 
		self.rb27.setVisible(False) 
		self.rb28.setVisible(False) 
		self.rb29.setVisible(False) 

		self.rb30.setVisible(False) 
		self.rb31.setVisible(False) 
		self.rb32.setVisible(False) 
		self.rb33.setVisible(False) 
		self.rb34.setVisible(False) 
		self.rb35.setVisible(False)
		self.rb36.setVisible(False) 
		self.rb37.setVisible(False)
		self.rb38.setVisible(False) 
		self.rb39.setVisible(False)

		self.rb40.setVisible(False) 
		self.rb41.setVisible(False)
		self.rb42.setVisible(False) 
		self.rb43.setVisible(False) 
		self.rb44.setVisible(False)
		self.rb45.setVisible(False)

		# Click the dropdown box
		self.rb0.toggled.connect(lambda: self.btnstate(self.rb0))
		self.rb1.toggled.connect(lambda: self.btnstate(self.rb1))
		self.rb2.toggled.connect(lambda: self.btnstate(self.rb2))
		self.rb3.toggled.connect(lambda: self.btnstate(self.rb3))
		self.rb4.toggled.connect(lambda: self.btnstate(self.rb4))
		self.rb5.toggled.connect(lambda: self.btnstate(self.rb5))
		self.rb6.toggled.connect(lambda: self.btnstate(self.rb6))
		self.rb7.toggled.connect(lambda: self.btnstate(self.rb7))
		self.rb8.toggled.connect(lambda: self.btnstate(self.rb8))
		self.rb9.toggled.connect(lambda: self.btnstate(self.rb9))

		self.rb10.toggled.connect(lambda: self.btnstate(self.rb10))
		self.rb11.toggled.connect(lambda: self.btnstate(self.rb11))
		self.rb12.toggled.connect(lambda: self.btnstate(self.rb12))
		self.rb13.toggled.connect(lambda: self.btnstate(self.rb13))
		self.rb14.toggled.connect(lambda: self.btnstate(self.rb14))
		self.rb15.toggled.connect(lambda: self.btnstate(self.rb15))
		self.rb16.toggled.connect(lambda: self.btnstate(self.rb16))
		self.rb17.toggled.connect(lambda: self.btnstate(self.rb17))
		self.rb18.toggled.connect(lambda: self.btnstate(self.rb18))
		self.rb19.toggled.connect(lambda: self.btnstate(self.rb19))

		self.rb20.toggled.connect(lambda: self.btnstate(self.rb20))
		self.rb21.toggled.connect(lambda: self.btnstate(self.rb21))
		self.rb22.toggled.connect(lambda: self.btnstate(self.rb22))
		self.rb23.toggled.connect(lambda: self.btnstate(self.rb23))
		self.rb24.toggled.connect(lambda: self.btnstate(self.rb24))
		self.rb25.toggled.connect(lambda: self.btnstate(self.rb25))
		self.rb26.toggled.connect(lambda: self.btnstate(self.rb26))
		self.rb27.toggled.connect(lambda: self.btnstate(self.rb27))
		self.rb28.toggled.connect(lambda: self.btnstate(self.rb28))
		self.rb29.toggled.connect(lambda: self.btnstate(self.rb29))

		self.rb30.toggled.connect(lambda: self.btnstate(self.rb30))
		self.rb31.toggled.connect(lambda: self.btnstate(self.rb31))
		self.rb32.toggled.connect(lambda: self.btnstate(self.rb32))
		self.rb33.toggled.connect(lambda: self.btnstate(self.rb33))
		self.rb34.toggled.connect(lambda: self.btnstate(self.rb34))
		self.rb35.toggled.connect(lambda: self.btnstate(self.rb35))
		self.rb36.toggled.connect(lambda: self.btnstate(self.rb36))
		self.rb37.toggled.connect(lambda: self.btnstate(self.rb37))
		self.rb38.toggled.connect(lambda: self.btnstate(self.rb38))
		self.rb39.toggled.connect(lambda: self.btnstate(self.rb39))

		self.rb40.toggled.connect(lambda: self.btnstate(self.rb40))
		self.rb41.toggled.connect(lambda: self.btnstate(self.rb41))
		self.rb42.toggled.connect(lambda: self.btnstate(self.rb42))
		self.rb43.toggled.connect(lambda: self.btnstate(self.rb43))
		self.rb44.toggled.connect(lambda: self.btnstate(self.rb44))
		self.rb45.toggled.connect(lambda: self.btnstate(self.rb45))
		self.button.clicked.connect(lambda: self.clicker(MainWindow))
		self.MainWindow = MainWindow

		# Show the App
		self.show()

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Q:
			if self.button.isVisible():
				self.clicker(self.MainWindow)
		# if e.key() == Qt.Key_1:
		# 	self.cambia_class(1)
		# if e.key() == Qt.Key_2:
		# 	self.cambia_class(2)

	def btnstate(self, b):
		if b.isChecked():
			b_idx = int(b.objectName().split('_')[-1])
			self.i = self.instances[b_idx][0]
			self.button.setText("Show frame: " + str(self.instances[b_idx][1]))

	def clicker(self, MainWindow):
		# fpath = QFileDialog.getExistingDirectory(self, "Select Directory", "D:\\") D:\Pytorch\yolov5\runs\4CM11_24_L_#61
		# self.label.setText(str(fpath))

		MainWindow.i = self.i
		self.hide()
		MainWindow.setClean_mode(self.i)

	def get_ins(self, inst, unique, vid_name):
		self.i = 0
		self.vid_name = vid_name
		self.button.setText("Show frame: " + str(self.i))
		self.lb14.setStyleSheet("color: rgb(0,0,185)")
		self.lb15.setStyleSheet("color: rgb(0,0,185)")
		self.lb15.setText("Total: [{}] ({}) ".format(len(inst), sum(unique)))
		self.lbt.setText(vid_name)
		self.lbt.setStyleSheet("background-color: rgb(150,200,255)")
		self.instances = []
		for i, insta in enumerate(inst):
			idx, s, e, f, s_i = insta
			if i < 1:
				bold = True if s > 1 else False
			else:
				_, _, e_prev, _, _ = inst[i-1]
				bold = True if s-e_prev > 1 else False
			self.set_radio(i, idx, '{:04d}'.format(s), '{:04d}'.format(e), f, bold)
			self.instances.append([s_i, s])
		for idx_, cnt in zip(range(len(classes_id)), unique):
			self.set_label(idx_, cnt)

	def set_label(self, idx, cnt):
		if idx == 0:
			pb = self.lb0
		elif idx == 1:
			pb = self.lb1
		elif idx == 2:
			pb = self.lb2
		elif idx == 3:
			pb = self.lb3
		elif idx == 4:
			pb = self.lb4
		elif idx == 5:
			pb = self.lb5
		elif idx == 6:
			pb = self.lb6
		elif idx == 7:
			pb = self.lb7
		elif idx == 8:
			pb = self.lb8
		elif idx == 9:
			pb = self.lb9
		elif idx == 10:
			pb = self.lb10
		elif idx == 11:
			pb = self.lb11
		elif idx == 12:
			pb = self.lb12
		elif idx == 13:
			pb = self.lb13
		elif idx == 14:
			pb = self.lb16
		pb.setText("{}: [{}]".format(classes_id[idx], cnt))
		col_ = "rgb(0,0,0)" if cnt > 0 else "rgb(195,0,0)"
		if cnt > 3:
			col_ = "rgb(20,140,20)"
		pb.setStyleSheet("color: {}".format(col_))


	def set_radio(self, idx, cid, st, en, fr, bold=False):
		rb = self.rb10
		if idx == 0:
			rb = self.rb0
		elif idx == 1:
			rb = self.rb1
		elif idx == 2:
			rb = self.rb2
		elif idx == 3:
			rb = self.rb3
		elif idx == 4:
			rb = self.rb4
		elif idx == 5:
			rb = self.rb5
		elif idx == 6:
			rb = self.rb6
		elif idx == 7:
			rb = self.rb7
		elif idx == 8:
			rb = self.rb8
		elif idx == 9:
			rb = self.rb9
		elif idx == 10:
			rb = self.rb10
		elif idx == 11:
			rb = self.rb11
		elif idx == 12:
			rb = self.rb12
		elif idx == 13:
			rb = self.rb13
		elif idx == 14:
			rb = self.rb14
		elif idx == 15:
			rb = self.rb15
		elif idx == 16:
			rb = self.rb16
		elif idx == 17:
			rb = self.rb17
		elif idx == 18:
			rb = self.rb18
		elif idx == 19:
			rb = self.rb19
		elif idx == 20:
			rb = self.rb20
		elif idx == 21:
			rb = self.rb21
		elif idx == 22:
			rb = self.rb22
		elif idx == 23:
			rb = self.rb23
		elif idx == 24:
			rb = self.rb24
		elif idx == 25:
			rb = self.rb25
		elif idx == 26:
			rb = self.rb26
		elif idx == 27:
			rb = self.rb27
		elif idx == 28:
			rb = self.rb28
		elif idx == 29:
			rb = self.rb29
		elif idx == 30:
			rb = self.rb30
		elif idx == 31:
			rb = self.rb31
		elif idx == 32:
			rb = self.rb32
		elif idx == 33:
			rb = self.rb33
		elif idx == 34:
			rb = self.rb34
		elif idx == 35:
			rb = self.rb35
		elif idx == 36:
			rb = self.rb36
		elif idx == 37:
			rb = self.rb37
		elif idx == 38:
			rb = self.rb38
		elif idx == 39:
			rb = self.rb39
		elif idx == 40:
			rb = self.rb40
		elif idx == 41:
			rb = self.rb41
		elif idx == 42:
			rb = self.rb42
		elif idx == 43:
			rb = self.rb43
		elif idx == 44:
			rb = self.rb44
		elif idx == 45:
			rb = self.rb45
		rb.setText("[{:02d}] {}: {} - {}".format(idx+1, classes_id[cid].split(":")[0], st, en))
		col_ = "rgb(0,0,0)" if cid > 2 else "rgb(20,120,20)"
		col_ = col_ if cid > 0 else "rgb(220,20,20)"
		fr = int(en) - int(st) + 1
		if fr < 10:
			col_ = "rgb(0,0,245)"
		if bold:
			rb.setStyleSheet("font-weight: bold; color: {}".format(col_))
		else:
			rb.setStyleSheet("color: {}".format(col_))
		rb.setVisible(True)


if __name__ == "__main__":
	# Initialize the app
	app = QApplication(sys.argv)
	UIWindow = UI_report()
	app.exec_()