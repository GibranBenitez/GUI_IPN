from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QSpinBox, QRadioButton, QCheckBox, QLabel, QFileDialog, QShortcut
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QKeySequence, QKeyEvent
from pathlib import Path
import sys, glob, os, time, random, shutil 
from threading import Timer
from natsort import natsorted, os_sorted, realsorted, humansorted
from utils import draw_boxes, draw_change_boxes, xml_to_yolo, find_SE, calculate_iou_yolo, get_image_dim
from report import UI_report

classes_id = ["D0X: No-gest", "B0A: Point-1f", "B0B: Point-2f", "G01: Click-1f", "G02: Click-2f", "G03: Th-up", "G04: Th-down", 
				"G05: Th-left", "G06: Th-right", "G07: Open-2", "G08: 2click-1f", "G09: 2click-2f", "G10: Zoom-in", "G11: Zoom-o", "G12: Catch", ""]

fin_mode = True
# fin_mode = False
# frames_path = "F:\\IPN_Hand\\frames" #old IPN
frames_path = "C:\\Users\\Luis Bringas\\Desktop\\NEW_IPN_final_frames"
# frames_path = "C:/Users/gjben/Documents/yolov5/runs/detect/frames"
#frames_path = "E:/datasets/IPN_hand/frames"
# frames_path = "D:/data/IPN_hand/frames" 

if fin_mode:
	txt_folder = "NEW_IPN_annotations_txt"
	# txt_folder = "final_test_annots"
	# txt_folder = "annots"
	# init_path = "F:\\IPN_Hand\\annotations\\final_annots_yolo\\" + txt_folder
	init_path = "C:\\Users\\Luis Bringas\\Desktop\\" + txt_folder
	#init_path = "C:\\Users\\Luis Bringas\\Desktop\\New_gt\\" + txt_folder
	#init_path = "D:/Pytorch/yolov5/runs/test_gordo/" + txt_folder
	# init_path = "D:/data/IPN_hand/" + txt_folder
else:
	txt_folder = "NEW_IPN_annotations_txt"
	init_path = "C:\\Users\\Luis Bringas\\Desktop\\" + txt_folder
	# init_path = "C:\\Users\\Luis Bringas\\Desktop\\New_gt\\bad_bboxes"
	# init_path = "D:/Pytorch/yolov5/runs/test_gordo/bad_bboxes"
	# init_path = "D:/Pytorch/YOLOv5/bad_bboxes"

random.seed(42)
colorsl = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(classes_id))]
colorsl.append([240, 240, 240])
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
		self.buttonReport = self.findChild(QPushButton, "pushButton_rep")
		self.label = self.findChild(QLabel, "label")
		self.clabel = self.findChild(QLabel, "label_color")
		self.clabelt = self.findChild(QLabel, "label_ctext")
		self.set_idcl()

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
		self.buttonReport.setVisible(False)
		self.buttonReport.setStyleSheet("background-color: rgb(120,120,200)")
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
		self.f2nd = False
		self.shi_P = QShortcut(QKeySequence('Shift+P'), self)
		self.shi_P.activated.connect(lambda: self.play_(True))
		self.shi_O = QShortcut(QKeySequence('Shift+O'), self)
		self.shi_O.activated.connect(lambda: self.play_back(True))
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
		self.ctrl_zero = QShortcut(QKeySequence('Ctrl+0'), self)
		self.ctrl_zero.activated.connect(self.active_track)

		# Click the dropdown box
		self.button.clicked.connect(self.clicker)
		self.buttonSend.clicked.connect(self.send_box)
		self.buttonDelete.clicked.connect(self.del_chosen)
		self.buttonReport.clicked.connect(self.open_rep)
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
		self.f2nd = False
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

	def send_box(self, sig_=True):
		if self.pflag:
			return
		txt_ = self.bad_list[self.i]
		txt_path = os.path.join(self.sele_path, os.path.basename(txt_))
		if not self.sp_H1.isVisible() and os.path.exists(txt_path):
			if sig_:
				self.next_() 
		if self.sp_H1.isVisible() or not os.path.exists(txt_path):
			if self.sp_H1.isVisible() and self.text_change is not None:
				self.text_chosen[self.choose_change] = xml_to_yolo(self.text_change)
			if self.text_chosen is not None:
				self.write_txt(txt_path, self.text_chosen)
				if sig_:
					self.next_()

	def gen_2ndBox(self):
		if self.pflag:
			return
		if self.f2nd:
			return
		self.f2nd = True
		if self.sp_H1.isVisible() and len(self.text_chosen) < 4:
			self.choose_change = len(self.text_chosen)
			self.text_chosen = self.text_chosen + ['0 0.5 0.5 0.2 0.2']
			self.change_spb("change_mod")

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

	def cambia_class(self, idx=0):
		if self.pflag:
			return
		txt_l = self.text_saved
		# print(txt_l)
		if txt_l is not None:
			txt_path = os.path.join(self.sele_path, os.path.basename(self.bad_list[self.i]))
			new_l = []
			for line_ in txt_l:
				buff_ = line_.split(" ")
				buff_[0] = str(idx)
				new_l.append(' '.join(buff_))
			self.write_txt(txt_path, new_l)
		else:
			print("WARNING: No se puede cambiar clase porque no hay BOX!")
			return
		self.set_idcl(idx)
		if idx > 2:
			self.label_msg.setText("CLS a G{}".format(idx-2))
		elif idx == 1:
			self.label_msg.setText("CLS a B0A")
		elif idx == 2:
			self.label_msg.setText("CLS a B0B")
		else:
			self.label_msg.setText("CLS a D0X!!")
		self.next_(True)

	def del_chosen(self):
		if self.pflag:
			return
		if self.sp_H1.isVisible():
			if len(self.text_chosen) > 1:
				
				popped = self.text_chosen.pop(self.choose_change)
				print("WARNING: {} deleted: {}".format(self.choose_change, popped))
				self.choose_change = 0
				self.change_spb("change_mod")
				self.send_box(False)
				self.setClean_mode(self.i)
			else:
				self.setClean_mode(self.i)
		# if self.sp_H1.isVisible():
		# 	self.setClean_mode(self.i)
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
			self.set_idcl(int(txt_l[0].split(" ")[0]))
			self.plotter2(txt_l , True, idx=-1, img_path=img_)
			self.label_msg.setText("{} BBOX Chosen".format(len(txt_l)))
			self.buttonDelete.setVisible(True)
			self.set_idc(1)
			self.text_saved = txt_l
		else:
			txt_l = self.read_txt(txt_)
			self.set_idcl()
			self.plotter2(txt_l, True, idx=0, img_path=img_, label_=None) 
			self.buttonDelete.setVisible(False)
			self.label_msg.setText("")
			self.set_idc(0)
			self.text_saved = None
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
			time.sleep(0.001)
		self.i = j
		self.flag = False
		self.pflag = False

	def play_back(self, fflag=False):
		if self.pflag:
			return
		self.flag = False
		self.pflag = True
		j = 0
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

	def set_idcl(self, idx=-1):
		id_color = colorsl[idx]
		self.clabelt.setText(classes_id[idx])
		self.clabelt.setStyleSheet("background-color: rgb(240,240,240); color: rgb({},{},{})".format(id_color[2], id_color[1], id_color[0]))
		self.clabel.setStyleSheet("background-color: rgb({},{},{})".format(id_color[2], id_color[1], id_color[0]))

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
					if len(line_.split()) > 5:
						line_ = ' '.join(line_.split()[:5])
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

	def plotter2(self, txt_, tdown=False, idx=-1, img_path="temp_img.jpg", label_=None): 
		self.sp_H1.setVisible(False)
		self.sp_H2.setVisible(False)
		self.sp_W1.setVisible(False)
		self.sp_W2.setVisible(False)
		draw_boxes(img_path, txt_, colors[idx], label_, True, None, tdown, imname="temp_img2")
		self.img_size = get_image_dim(img_path)
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
		self.buttonReport.setVisible(True)
		self.radioNo.setChecked(True)
		self.sp_H1.setVisible(False)
		self.sp_H2.setVisible(False)
		self.sp_W1.setVisible(False)
		self.sp_W2.setVisible(False)
		self.text_change = None
		self.text_chosen = None
		self.choose_change = 0
		self.text_saved = None

		txt_ = self.bad_list[indx]
		img_ = os.path.join(self.img_path, os.path.basename(txt_).replace(self.ext, '.jpg'))
		self.img_size = get_image_dim(img_)

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
			self.set_idcl(int(txt_l[0].split(" ")[0]))
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
		print("iPath: ",iPath)
		self.ext = os.path.splitext(iPath)[-1]
		txt_path = os.path.dirname(iPath)
		vid_name = txt_path.split('/')[-1]
		print(vid_name)
		self.img_path = "{}/{}/".format(frames_path, vid_name)
		#self.ano1_path = "C:/Users/Luis Bringas/Desktop/YOLO_ima_detections/{}/".format(vid_name)
		self.ano1_path = "{}/ipn_11c/{}/".format(Path(iPath).parents[2], vid_name)
		# self.ano1_path = "{}/ipn_gordo/{}/".format(Path(iPath).parents[2], vid_name)
		self.ano2_path = "{}/ipn_prune4/{}/".format(Path(iPath).parents[2], vid_name)

		self.sele_path = "{}/{}/{}/".format(Path(iPath).parents[2], txt_folder, vid_name)
		# self.sele_path = "{}/anotations/{}/".format(Path(iPath).parents[2], vid_name)
		if not os.path.exists(self.sele_path):
			os.makedirs(self.sele_path)

		bad_list = glob.glob("{}/*{}".format(txt_path, self.ext))
		self.bad_list = os_sorted([s.replace('\\', '/') for s in bad_list])

		self.i = self.bad_list.index(iPath.replace('\\', '/'))

		self.plotter(self.i)
		self.setClean_mode(self.i)
		self.vid_name = vid_name
		self.inst = None
		self.f_ins = False
		self.a_flag = False

	def open_rep(self):
		self.inst, uniq = find_SE(self.sele_path)
		self.report_win = UI_report(self)
		self.report_win.get_ins(self.inst, uniq, self.vid_name)
		self.report_win.show()
		self.f_ins = True

	def close_rep(self):
		self.report_win.close()

	def active_hand(self, frame_i=None, idx_=None):
		if self.pflag:
			return
		if len(self.text_chosen) < 2:
			return
		idx__ = self.choose_change if idx_ == None else idx_
		f_i = self.i if frame_i == None else frame_i
		act_hnd = self.text_chosen.pop(idx__)
		self.text_chosen = [' '.join(['0'] + s.split()[1:]) for s in self.text_chosen] 
		self.text_chosen.insert(0, act_hnd)
		self.text_change = None
		self.send_box(False)
		txt_path = os.path.join(self.sele_path, os.path.basename(self.bad_list[f_i]))
		if self.text_chosen is not None:
			self.write_txt(txt_path, self.text_chosen)
	
	def del_overboxes(self, frame_i=None, iou_th=0.9):
		f_i = self.i if frame_i == None else frame_i
		active_bbox = self.text_chosen[0]
		del_box_idx = []
		for i, cur_bbox in enumerate(self.text_chosen):
			if i < 1:
				continue
			iou = calculate_iou_yolo(active_bbox, cur_bbox, self.img_size[0], self.img_size[1])
			if iou >= iou_th:
				print("-------AQUI HAY DOBLE", iou)
				del_box_idx.append(i)
		for i in sorted(del_box_idx, reverse=True):
			del_bbox = self.text_chosen.pop(i)
		txt_path = os.path.join(self.sele_path, os.path.basename(self.bad_list[f_i]))
		if self.text_chosen is not None:
			self.write_txt(txt_path, self.text_chosen)

	def active_track(self, iou_th=0.45):
		if self.pflag:
			return
		if not self.f_ins:
			return
		cur_frame = self.i + 1
		for inst_seg in self.inst:
			if cur_frame >= inst_seg[1] and cur_frame <= inst_seg[2]:
				cur_seg = inst_seg
				break
		if cur_seg[-1] < 1:
			return
		active_bbox = self.text_chosen[0]
		j = 0
		self.flag = False
		self.a_flag  = True
		for j in range(cur_frame, cur_seg[2]):
			self.setClean_mode(j)
			if len(self.text_chosen) > 1:
				for idx, new_bbox in enumerate(self.text_chosen):
					iou = calculate_iou_yolo(active_bbox, new_bbox, self.img_size[0], self.img_size[1])
					print(j+1, iou)
					if iou >= iou_th:
						active_bbox = new_bbox
						self.active_hand(j, idx)
						break
				if idx + 1 >= len(self.text_chosen):
					print(j+1, "WARNING: No hay BBOX que sobrepase el IoU_th")
					break
			else:
				active_bbox = self.text_chosen[0]
			if len(self.text_chosen) > 1:
				self.del_overboxes(j)
			self.setClean_mode(j)
			app.processEvents()
			if self.flag:
				break
			time.sleep(0.003)
		if j > 0:
			self.i = j
			self.setClean_mode(j)
		self.flag = False
		self.a_flag  = False

	def keyPressEvent(self, e):
		# print(e.key())
		if e.key() == Qt.Key_0:
			if self.sp_H1.isVisible():
				self.active_hand()
				self.setClean_mode(self.i)
		if e.key() == Qt.Key_A or e.key() == 16777219:
			self.send_box()
		if e.key() == 93 or e.key() == 16777252:
			self.send_box(False)
		if e.key() == Qt.Key_P:
			self.next_()
		if e.key() == Qt.Key_O:
			self.back_()
		if e.key() == Qt.Key_M:
			self.open_rep()
		if e.key() == Qt.Key_N:
			self.close_rep()
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
			elif self.a_flag:
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
		if e.key() == Qt.Key_R:
			if self.buttonAll.isVisible():
				self.Sbtnstate(True)

		if e.key() == Qt.Key_1:
			if self.sp_H1.isVisible():
				if len(self.text_chosen) > 1:
					self.choose_change = 0
					self.change_spb("change_mod")
			else:
				self.cambia_class(1)
		if e.key() == Qt.Key_2:
			if self.sp_H1.isVisible():
				if len(self.text_chosen) > 1:
					self.choose_change = 1
					self.change_spb("change_mod")
				else:
					self.choose_change = 0
			else:
				self.cambia_class(2)
		if e.key() == Qt.Key_3:
			if self.sp_H1.isVisible():
				if len(self.text_chosen) > 2:
					self.choose_change = 2
					self.change_spb("change_mod")
				elif len(self.text_chosen) > 1:
					self.choose_change = 1
					self.change_spb("change_mod")
				else:
					self.choose_change = 0
			else:
				self.cambia_class(0)
		if e.key() == Qt.Key_4:
			if self.sp_H1.isVisible():
				if len(self.text_chosen) > 3:
					self.choose_change = 3
					self.change_spb("change_mod")
				elif len(self.text_chosen) > 1:
					self.choose_change = 1
					self.change_spb("change_mod")
				else:
					self.choose_change = 0
		if e.key() == Qt.Key_F1:
			self.cambia_class(3)
		if e.key() == Qt.Key_F2:
			self.cambia_class(4)
		if e.key() == Qt.Key_F3:
			self.cambia_class(5)
		if e.key() == Qt.Key_F4:
			self.cambia_class(6)
		if e.key() == Qt.Key_F5:
			self.cambia_class(7)
		if e.key() == Qt.Key_F6:
			self.cambia_class(8)
		if e.key() == Qt.Key_F7:
			self.cambia_class(9)
		if e.key() == Qt.Key_F8:
			self.cambia_class(10)
		if e.key() == Qt.Key_F9:
			self.cambia_class(11)
		if e.key() == Qt.Key_F10:
			self.cambia_class(12)
		if e.key() == Qt.Key_F11:
			self.cambia_class(13)
		if e.key() == Qt.Key_F12:
			self.cambia_class(14)



if __name__ == "__main__":
	# Initialize the app
	app = QApplication(sys.argv)
	UIWindow = UI()
	app.exec_()