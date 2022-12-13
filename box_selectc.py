from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QSpinBox, QRadioButton, QCheckBox, QLabel, QFileDialog, QShortcut
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QKeySequence, QKeyEvent
from pathlib import Path
import sys, glob, os, time, random, shutil 
from threading import Timer
from natsort import natsorted, os_sorted, realsorted, humansorted
from utils import draw_boxes, draw_change_boxes, xml_to_yolo

classes_id = ["D0X: No-gest", "B0A: Point-1f", "B0B: Point-2f", "G01: Click-1f", "G02: Click-2f", "G03: Th-up", "G04: Th-down", 
				"G05: Th-left", "G06: Th-right", "G07: Open-2", "G08: 2click-1f", "G09: 2click-2f", "G10: Zoom-in", "G11: Zoom-o"]

init_path = "C:\\Users\\Luis Bringas\\Desktop\\New_gt\\bad_bboxes"
frames_path = "F:\\IPN_Hand\\frames"
# init_path = "C:/Users/gjben/Documents/yolov5/runs/detect/bad_bunny"
# frames_path = "C:/Users/gjben/Documents/yolov5/runs/detect/frames"
# init_path = "D:/Pytorch/yolov5/runs/test_gordo/bad_bboxes"
# frames_path = "F:/Datasets/IPN_hand/frames"
random.seed(42)
colors = [[70,70,120]]
colors.append([230, 0, 230])
colors.append([230, 230, 0])
colors.append([0, 250, 250])


class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()

		# Load the ui file
		uic.loadUi("box_selectc.ui", self)

		self.flag = False
		self.pflag = False
		self.bad_flag = False
		self.i = 0

		# Define our widgets
		self.button = self.findChild(QPushButton, "pushButton")
		self.buttonSend = self.findChild(QPushButton, "pushButton_Enter")
		self.buttonDelete = self.findChild(QPushButton, "pushButton_Del")
		self.buttonAll = self.findChild(QPushButton, "pushButton_All")
		self.label = self.findChild(QLabel, "label")
		self.radioB1 = self.findChild(QRadioButton, "radioBox1")
		self.radioB2 = self.findChild(QRadioButton, "radioBox2")
		self.radioNo = self.findChild(QRadioButton, "radioNone")
		self.radS1 = self.findChild(QCheckBox, "radioSub1")
		self.radS2 = self.findChild(QCheckBox, "radioSub2")
		self.radS3 = self.findChild(QCheckBox, "radioSub3")
		self.radS4 = self.findChild(QCheckBox, "radioSub4")

		self.sp_H1 = self.findChild(QSpinBox, "spinBox_H1")
		self.sp_H2 = self.findChild(QSpinBox, "spinBox_H2")
		self.sp_W1 = self.findChild(QSpinBox, "spinBox_W1")
		self.sp_W2 = self.findChild(QSpinBox, "spinBox_W2")

		self.radS1.setVisible(False)
		self.radS2.setVisible(False)
		self.radS3.setVisible(False)
		self.radS4.setVisible(False)
		self.buttonAll.setVisible(False)
		self.buttonSend.setVisible(False)
		self.radioB1.setVisible(False)
		self.radioB1.setStyleSheet("color: rgb(185,0,185)")
		self.radioB2.setVisible(False)
		self.radioB2.setStyleSheet("color: rgb(0,185,185)")
		self.radioNo.setVisible(False)
		self.buttonDelete.setVisible(False)
		self.buttonDelete.setStyleSheet("background-color: rgb(119,119,140)")

		self.shortcut_open = QShortcut(QKeySequence('Ctrl+O'), self)
		self.shortcut_open.activated.connect(self.clicker)
		self.shortcut_close = QShortcut(QKeySequence('Ctrl+Q'), self)
		self.shortcut_close.activated.connect(lambda: app.quit())

		self.shi_A = QShortcut(QKeySequence('Shift+A'), self)
		self.shi_A.activated.connect(self.gen_2ndBox)
		self.shi_L = QShortcut(QKeySequence('Shift+L'), self)
		self.shi_L.activated.connect(self.play_)
		self.shi_K = QShortcut(QKeySequence('Shift+K'), self)
		self.shi_K.activated.connect(self.play_back)
		self.shi_Z = QShortcut(QKeySequence('Shift+Z'), self)
		self.shi_Z.activated.connect(self.copy_bbox)
		self.shi_S = QShortcut(QKeySequence('Shift+S'), self)
		self.shi_S.activated.connect(lambda: self.change_spb('H1_0'))
		self.shi_D = QShortcut(QKeySequence('Shift+D'), self)
		self.shi_D.activated.connect(lambda: self.change_spb('H2_0'))
		self.shi_X = QShortcut(QKeySequence('Shift+X'), self)
		self.shi_X.activated.connect(lambda: self.change_spb('W1_0'))
		self.shi_C = QShortcut(QKeySequence('Shift+C'), self)
		self.shi_C.activated.connect(lambda: self.change_spb('W2_0'))

		# Click the dropdown box
		self.button.clicked.connect(self.clicker)
		self.buttonSend.clicked.connect(self.send_box)
		self.buttonDelete.clicked.connect(self.del_chosen)
		self.buttonSend.setAutoDefault(True)
		self.radioNo.setChecked(True)
		self.radS1.setChecked(True)

		# Set button states
		self.radioB1.toggled.connect(lambda: self.btnstate(self.radioB1))
		self.radioB2.toggled.connect(lambda: self.btnstate(self.radioB2))
		self.radioNo.toggled.connect(lambda: self.btnstate(self.radioNo))

		self.radS1.toggled.connect(lambda: self.Sbtnstate(False))
		self.radS2.toggled.connect(lambda: self.Sbtnstate(False))
		self.radS3.toggled.connect(lambda: self.Sbtnstate(False))
		self.radS4.toggled.connect(lambda: self.Sbtnstate(False))
		self.buttonAll.clicked.connect(lambda: self.Sbtnstate(True))

		self.sp_H1.textChanged.connect(lambda: self.Sstate(self.sp_H1))
		self.sp_H2.textChanged.connect(lambda: self.Sstate(self.sp_H2))
		self.sp_W1.textChanged.connect(lambda: self.Sstate(self.sp_W1))
		self.sp_W2.textChanged.connect(lambda: self.Sstate(self.sp_W2))
		self.sp_H1.setVisible(False)
		self.sp_H2.setVisible(False)
		self.sp_W1.setVisible(False)
		self.sp_W2.setVisible(False)
		self.text_change = None

		# Show the App
		self.show()

	def change_spb(self, opt):
		if opt == "change_mod":
			self.sp_H1.setVisible(True)
			self.sp_H2.setVisible(True)
			self.sp_W1.setVisible(True)
			self.sp_W2.setVisible(True)
			text_change = self.text_chosen if len(self.text_chosen) < 2 else [self.text_chosen[self.choose_change]]
			self.text_change = draw_change_boxes(text_change, xml_in=False)
			pixmap = QPixmap("temp_img3.jpg")
			self.label.setPixmap(pixmap)
			return
		if self.sp_H1.isVisible():
			if opt == "H1_0":
				self.sp_H1.stepBy(-2)
			if opt == "H1_1":
				self.sp_H1.stepBy(2)
			if opt == "H2_0":
				self.sp_H2.stepBy(-2)
			if opt == "H2_1":
				self.sp_H2.stepBy(2)
			if opt == "W1_0":
				self.sp_W1.stepBy(-2)
			if opt == "W1_1":
				self.sp_W1.stepBy(2)
			if opt == "W2_0":
				self.sp_W2.stepBy(-2)
			if opt == "W2_1":
				self.sp_W2.stepBy(2)

	def Sstate(self, sp_btn):
		if self.sp_H1.isVisible():
			self.label_msg.setText(str(sp_btn.value()))
			if sp_btn.objectName().split('_')[-1] == "W1":
				ax = 0
			elif sp_btn.objectName().split('_')[-1] == "H1":
				ax = 1
			elif sp_btn.objectName().split('_')[-1] == "W2":
				ax = 2
			elif sp_btn.objectName().split('_')[-1] == "H2":
				ax = 3
			self.text_change = draw_change_boxes(self.text_change, ax, sp_btn.value())
			sp_btn.setValue(0)
			pixmap = QPixmap("temp_img3.jpg")
			self.label.setPixmap(pixmap)

	def btnstate(self, b):
		if self.pflag:
			return
		if b.isChecked():
			self.label_msg.setText(b.text())
			self.set_idc(0)
			self.radS1.setVisible(False)
			self.radS2.setVisible(False)
			self.radS3.setVisible(False)
			self.radS4.setVisible(False)
			self.buttonAll.setVisible(False)
			if b.text()[-1] == "1":
				self.sbvis(self.ano1)
			elif b.text()[-1] == "2":
				self.sbvis(self.ano2, True)
			else:
				pixmap = QPixmap("temp_img.jpg")
				self.label.setPixmap(pixmap)
				self.text_chosen = None

	def sbvis(self, blen, tdown=False):
		if len(blen) < 2:
			self.plotter2(blen, tdown)
			self.text_chosen = blen
			return
		if len(blen) > 1:
			chlag = [0 for s in range(len(blen))]
			chlag[0] = 1
			self.radS1.setChecked(True)
			self.radS2.setChecked(False)
			self.cambia_sb(chlag)
			self.buttonAll.setVisible(True)
			self.radS1.setVisible(True)
			self.radS2.setVisible(True)
		if len(blen) > 2:
			self.radS3.setVisible(True)
		else:
			self.radS3.setChecked(False)
		if len(blen) > 3:
			self.radS4.setVisible(True)
		else:
			self.radS4.setChecked(False)

	def Sbtnstate(self, all_=True):
		if self.pflag:
			return
		if self.radioB1.isChecked():
			chlag = [0 for s in range(len(self.ano1))]
		elif self.radioB2.isChecked():
			chlag = [0 for s in range(len(self.ano2))]
		else:
			return
		if all_:
			self.radS1.setChecked(True)
			chlag[0] = 1
			self.radS2.setChecked(True)
			chlag[1] = 1
			if len(chlag) > 2:
				self.radS3.setChecked(True)
				chlag[2] = 1
			if len(chlag) > 3:
				self.radS4.setChecked(True)
				chlag[3] = 1
		else:
			if self.radS1.isChecked():
				chlag[0] = 1
			else:
				chlag[0] = 0
			if self.radS2.isChecked() and self.radS2.isVisible():
				chlag[1] = 1
			elif self.radS2.isVisible():
				chlag[1] = 0
			if self.radS3.isChecked() and self.radS3.isVisible():
				chlag[2] = 1
			elif self.radS3.isVisible():
				chlag[2] = 0
			if self.radS4.isChecked() and self.radS4.isVisible():
				chlag[3] = 1
			elif self.radS4.isVisible():
				chlag[3] = 0
		self.cambia_sb(chlag)

	def cambia_sb(self, idx):
		if self.pflag:
			return
		if self.radioB1.isChecked():
			lab_ = self.radioB1.text()
			txt_ = self.ano1
			tdown = False
		elif self.radioB2.isChecked():
			lab_ = self.radioB2.text()
			txt_ = self.ano2
			tdown = True
		else:
			return
		if len(txt_) != len(idx):
			return
		if sum(idx) > 0:
			self.label_msg.setText("{}({})".format(lab_, idx.index(1)+1))
			self.set_idc(0)
			self.text_chosen = []
			for i_, val in enumerate(idx):
				if val > 0:
					self.text_chosen.append(txt_[i_])
			self.plotter2(self.text_chosen, tdown)
		else:
			self.text_chosen = None

	def send_box(self):
		if self.pflag:
			return
		txt_ = self.bad_list[self.i]
		txt_path = os.path.join(self.sele_path, os.path.basename(txt_))
		if not self.sp_H1.isVisible() and os.path.exists(txt_path):
			self.next_() 
		if self.sp_H1.isVisible() or not os.path.exists(txt_path):
			if self.sp_H1.isVisible() and self.text_change is not None:
				self.text_chosen[self.choose_change] = xml_to_yolo(self.text_change)
			if self.text_chosen is not None:
				self.write_txt(txt_path, self.text_chosen)
				self.next_()

	def gen_2ndBox(self):
		if self.pflag:
			return
		if self.sp_H1.isVisible() and len(self.text_chosen) < 2:
			self.choose_change = 1
			self.text_chosen = self.text_chosen + ['0 0.5 0.5 0.2 0.2']
			self.change_spb("change_mod")

	def keyPressEvent(self, e):
		# print(e.key())
		if e.key() == 93 or e.key() == 16777252 or e.key() == Qt.Key_A or e.key() == 16777219:
			self.send_box()
		if e.key() == Qt.Key_P:
			self.next_()
		if e.key() == Qt.Key_O:
			self.back_()
		if e.key() == Qt.Key_M:
			self.play_(True)
		if e.key() == Qt.Key_N:
			self.play_back(True)
		if e.key() == Qt.Key_L:
			self.next_(True)
		if e.key() == Qt.Key_K:
			self.back_(True)
		if e.key() == Qt.Key_Z:
			self.copy_bbox(-1)
		if e.key() == Qt.Key_F:
			self.del_chosen()

		if e.key() == Qt.Key_S:
			if self.pflag:
				self.flag = True
			else:
				if self.sp_H1.isVisible():
					self.change_spb("H1_1")
				elif not self.radioNo.isVisible():
					self.change_spb("change_mod")
				else:
					self.setClean_mode(self.i)
		if e.key() == Qt.Key_D:
			if self.sp_H1.isVisible():
				self.change_spb("H2_1")
			elif not self.radioNo.isVisible():
				self.change_spb("change_mod")
			else:
				self.setClean_mode(self.i)
		if e.key() == Qt.Key_X:
			if self.sp_H1.isVisible():
				self.change_spb("W1_1")
			elif not self.radioNo.isVisible():
				self.change_spb("change_mod")
			else:
				self.setClean_mode(self.i)
		if e.key() == Qt.Key_C:
			if self.sp_H1.isVisible():
				self.change_spb("W2_1")
			elif not self.radioNo.isVisible():
				self.change_spb("change_mod")
			else:
				self.setClean_mode(self.i)

		if e.key() == Qt.Key_E:
			self.radioNo.setChecked(True)
		if e.key() == Qt.Key_Q:
			if self.radioB1.isVisible():
				if self.radioB1.isChecked():
					if self.radS1.isVisible():
						self.rotate_checked()
				else:
					self.radioB1.setChecked(True)
		if e.key() == Qt.Key_W:
			if self.radioB2.isVisible():
				if self.radioB2.isChecked():
					if self.radS1.isVisible():
						self.rotate_checked()
				else:
					self.radioB2.setChecked(True)
		if e.key() == Qt.Key_1:
			if self.sp_H1.isVisible():
				if len(self.text_chosen) > 1:
					self.choose_change = 0
					self.change_spb("change_mod")
			if self.radS1.isVisible():
				self.radS1.setChecked(True)
				self.radS2.setChecked(False)
				self.radS3.setChecked(False)
				self.radS4.setChecked(False)
		if e.key() == Qt.Key_2:
			if self.sp_H1.isVisible():
				if len(self.text_chosen) > 1:
					self.choose_change = 1
					self.change_spb("change_mod")
				else:
					self.choose_change = 0
			if self.radS2.isVisible():
				self.radS2.setChecked(True)
				self.radS1.setChecked(False)
				self.radS3.setChecked(False)
				self.radS4.setChecked(False)
		if e.key() == Qt.Key_3:
			if self.radS3.isVisible():
				self.radS3.setChecked(True)
				self.radS1.setChecked(False)
				self.radS2.setChecked(False)
				self.radS4.setChecked(False)
		if e.key() == Qt.Key_4:
			if self.radS4.isVisible():
				self.radS4.setChecked(True)
				self.radS1.setChecked(False)
				self.radS2.setChecked(False)
				self.radS3.setChecked(False)
		if e.key() == Qt.Key_R:
			if self.buttonAll.isVisible():
				self.Sbtnstate(True)

	def rotate_checked(self):
		if self.radS2.isVisible() and self.radS1.isChecked():
			self.radS2.setChecked(True)
			self.radS1.setChecked(False)
			self.radS3.setChecked(False)
			self.radS4.setChecked(False)
		elif self.radS3.isVisible() and self.radS2.isChecked():
			self.radS3.setChecked(True)
			self.radS1.setChecked(False)
			self.radS2.setChecked(False)
			self.radS4.setChecked(False)
		elif self.radS4.isVisible() and self.radS3.isChecked():
			self.radS4.setChecked(True)
			self.radS1.setChecked(False)
			self.radS2.setChecked(False)
			self.radS3.setChecked(False)
		else:
			self.radS1.setChecked(True)
			self.radS2.setChecked(False)
			self.radS3.setChecked(False)
			self.radS4.setChecked(False)

	def del_chosen(self):
		if self.pflag:
			return
		if self.sp_H1.isVisible():
			self.setClean_mode(self.i)
		else:
			txt_ = self.bad_list[self.i]
			txt_path = os.path.join(self.sele_path, os.path.basename(txt_))
			if os.path.exists(txt_path):
				os.remove(txt_path)
				self.plotter(self.i)
				self.label_msg.setText("Chosen Deleted")
				self.set_idc(2)
				self.text_chosen = None
				self.buttonDelete.setVisible(False)
			else:
				print("NOT FOUND {}".format(os.path.basename(txt_)))

	def setClean_mode(self, idx):
		txt_ = self.bad_list[idx]
		txt_path = os.path.join(self.sele_path, os.path.basename(txt_))
		img_ = os.path.join(self.img_path, os.path.basename(txt_).replace(self.ext, '.jpg'))
		if os.path.exists(txt_path):
			txt_l = self.read_txt(txt_path)
			self.plotter2(txt_l , True, idx=-1, img_path=img_, label_="chosen")
			self.label_msg.setText("{} BBOX Chosen".format(len(txt_l)))
			self.buttonDelete.setVisible(True)
			self.set_idc(1)
		else:
			txt_l = self.read_txt(txt_)
			self.plotter2(txt_l, True, idx=0, img_path=img_, label_=None) 
			self.buttonDelete.setVisible(False)
			self.label_msg.setText("")
			self.set_idc(0)
		self.label_frame.setText(os.path.basename(img_))
		self.radioB1.setVisible(False)
		self.radioB2.setVisible(False)
		self.radioNo.setVisible(False)
		self.radS1.setVisible(False)
		self.radS2.setVisible(False)
		self.radS3.setVisible(False)
		self.radS4.setVisible(False)
		self.buttonAll.setVisible(False)
		self.text_chosen = txt_l
		self.choose_change = 0

	def next_(self, flagg=False):
		if self.pflag:
			return
		if self.i < len(self.bad_list) - 1:
			self.i += 1
		else:
			self.i = len(self.bad_list) - 1
		if flagg:
			self.setClean_mode(self.i)
		else:
			self.plotter(self.i)

	def back_(self, flagg=False):
		if self.pflag:
			return
		if self.i > 0:
			self.i -= 1
		else:
			self.i = 0
		if flagg:
			self.setClean_mode(self.i)
		else:
			self.plotter(self.i)

	def play_(self, fflag=False):
		if self.pflag:
			return
		self.flag = False
		self.pflag = True
		for j in range(self.i, len(self.bad_list)):
			if fflag:
				self.plotter(j)
			else:
				self.setClean_mode(j)
			app.processEvents()
			if self.flag:
				break
			time.sleep(0.05)
		self.i = j
		self.flag = False
		self.pflag = False

	def play_back(self, fflag=False):
		if self.pflag:
			return
		self.flag = False
		self.pflag = True
		for j in range(self.i, 0, -1):
			if fflag:
				self.plotter(j)
			else:
				self.setClean_mode(j)
			app.processEvents()
			if self.flag:
				break
			time.sleep(0.01)
		self.i = j
		self.flag = False
		self.pflag = False

	def set_idc(self, idx=0):
		clrs = [[240,240,240],[119,197,197],[119,119,140]]
		id_color = clrs[idx]
		self.label_msg.setStyleSheet("background-color: rgb({},{},{})".format(id_color[2], id_color[1], id_color[0]))

	def read_txt(self, patho, namae=None):
		if namae is not None:
			txt_path = os.path.join(patho, namae)
		else:
			txt_path = patho
		try:
			my_file = open(txt_path, "r")
			dlab = my_file.readlines()
			text_list = []
			for line_ in dlab:
				if len(line_.split()) > 2:
					text_list.append(line_.strip())
			return text_list
		except:
			return ["NO BBOX u.u"]

	def write_txt(self, txt_path, text_list=None):
		if text_list is not None:
			out_file = open(txt_path, 'w')
			out_file.write('\n'.join(text_list))    
		else:
			return

	def copy_bbox(self, idx=1):
		if self.pflag or self.sp_H1.isVisible():
			return
		txt_path = self.sele_path + os.path.basename(self.bad_list[self.i])
		if not os.path.exists(txt_path):
			prev_path = self.sele_path + os.path.basename(self.bad_list[self.i+idx])
			if os.path.exists(prev_path):
				shutil.copy(prev_path, txt_path)
				self.setClean_mode(self.i)
				self.label_msg.setText("BBOX Copiado!!")
				self.set_idc(2)
			else:
				print("NOT FOUND {}".format(os.path.basename(self.bad_list[self.i+idx])))
		else:
			if self.radioNo.isVisible():
				self.next_()
			else:
				self.next_(True)

	def plotter2(self, txt_, tdown=False, idx=-1, img_path="temp_img.jpg", label_="chosen"): 
		self.sp_H1.setVisible(False)
		self.sp_H2.setVisible(False)
		self.sp_W1.setVisible(False)
		self.sp_W2.setVisible(False)
		draw_boxes(img_path, txt_, colors[idx], label_, True, None, tdown, imname="temp_img2")
		pixmap = QPixmap("temp_img2.jpg")
		self.label.setPixmap(pixmap)

	def plotter(self, indx):
		self.label_msg.setText("")
		self.set_idc(0)
		self.buttonDelete.setVisible(False)
		self.radioB1.setVisible(True)
		self.radioB2.setVisible(True)
		self.radioNo.setVisible(True)
		self.radS1.setVisible(False)
		self.radS2.setVisible(False)
		self.radS3.setVisible(False)
		self.radS4.setVisible(False)
		self.radS1.setChecked(False)
		self.radS2.setChecked(False)
		self.radS3.setChecked(False)
		self.radS4.setChecked(False)
		self.buttonAll.setVisible(False)
		self.radioNo.setChecked(True)
		self.sp_H1.setVisible(False)
		self.sp_H2.setVisible(False)
		self.sp_W1.setVisible(False)
		self.sp_W2.setVisible(False)
		self.text_change = None
		self.text_chosen = None
		self.choose_change = 0

		txt_ = self.bad_list[indx]
		img_ = os.path.join(self.img_path, os.path.basename(txt_).replace(self.ext, '.jpg'))

		bad_txt = self.read_txt(txt_)
		ano1_txt = self.read_txt(self.ano1_path, os.path.basename(txt_))
		if len(ano1_txt) < 2 and ano1_txt[0].split()[0] == "NO":
			self.radioB1.setVisible(False)
		ano2_txt = self.read_txt(self.ano2_path, os.path.basename(txt_))
		if len(ano2_txt) < 2 and ano2_txt[0].split()[0] == "NO":
			self.radioB2.setVisible(False)
		draw_ = draw_boxes(img_, bad_txt, colors[0], None, False)
		draw_ = draw_boxes(img_, ano1_txt, colors[1], "bbox1", False, draw_)
		draw_boxes(img_, ano2_txt, colors[2], "bbox2", True, draw_, True)
		self.ano1 = ano1_txt
		self.ano2 = ano2_txt
		# Open the image
		pixmap = QPixmap("temp_img.jpg")
		# Add pic to label
		self.label.setPixmap(pixmap)
		self.label_frame.setText(os.path.basename(img_))
		txt_path = os.path.join(self.sele_path, os.path.basename(txt_))
		if os.path.exists(txt_path):
			txt_l = self.read_txt(txt_path)
			self.plotter2(txt_l, True)
			self.label_msg.setText("{} BBOX Chosen".format(len(txt_l)))
			self.buttonDelete.setVisible(True)
			self.set_idc(1)

	def clicker(self):
		self.buttonSend.setVisible(True)
		self.radioB1.setVisible(True)
		self.radioB2.setVisible(True)
		self.radioNo.setVisible(True)

		fname = QFileDialog.getOpenFileName(self, "Open BadBox Annot", init_path, "Txt Files (*.txt)")
		iPath = fname[0]
		self.ext = os.path.splitext(iPath)[-1]
		txt_path = os.path.dirname(iPath)
		print(txt_path)
		self.img_path = "{}/{}/".format(frames_path, txt_path.split('/')[-1])
		self.ano1_path = "{}/ipn_11c/{}/".format(Path(iPath).parents[2], txt_path.split('/')[-1])
		self.ano2_path = "{}/ipn_prune4/{}/".format(Path(iPath).parents[2], txt_path.split('/')[-1])

		self.sele_path = "{}/selected_boxes/{}/".format(Path(iPath).parents[2], txt_path.split('/')[-1])
		if not os.path.exists(self.sele_path):
			os.makedirs(self.sele_path)

		bad_list = glob.glob("{}/*{}".format(txt_path, self.ext))
		self.bad_list = os_sorted([s.replace('\\', '/') for s in bad_list])

		self.i = self.bad_list.index(iPath.replace('\\', '/'))

		self.plotter(self.i)

if __name__ == "__main__":
	# Initialize the app
	app = QApplication(sys.argv)
	UIWindow = UI()
	app.exec_()