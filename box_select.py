from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QVBoxLayout, QRadioButton, QLabel, QFileDialog, QShortcut
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QKeySequence, QKeyEvent
from pathlib import Path
import sys, glob, os, time, random, shutil 
from threading import Timer
from natsort import natsorted, os_sorted, realsorted, humansorted
from utils import draw_boxes

classes_id = ["D0X: No-gest", "B0A: Point-1f", "B0B: Point-2f", "G01: Click-1f", "G02: Click-2f", "G03: Th-up", "G04: Th-down", 
				"G05: Th-left", "G06: Th-right", "G07: Open-2", "G08: 2click-1f", "G09: 2click-2f", "G10: Zoom-in", "G11: Zoom-o"]

# init_path = "C:\\Users\\Luis Bringas\\Desktop\\New_gt"
# init_path = "D:/Pytorch/yolov5/runs/Test_DB/frames"
init_path = "C:/Users/gjben/Documents/yolov5/runs/detect/bad_bunny"
frames_path = "C:/Users/gjben/Documents/yolov5/runs/detect/frames"
random.seed(42)
colors = [[70,70,120]]
colors.append([230, 0, 230])
colors.append([230, 230, 0])
colors.append([0, 250, 250])


class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()

		# Load the ui file
		uic.loadUi("box_select.ui", self)

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
		self.radS1 = self.findChild(QRadioButton, "radioSub1")
		self.radS2 = self.findChild(QRadioButton, "radioSub2")
		self.radS3 = self.findChild(QRadioButton, "radioSub3")
		self.radS4 = self.findChild(QRadioButton, "radioSub4")

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

		self.shortcut_fast = QShortcut(QKeySequence('Shift+L'), self)
		self.shortcut_fast.activated.connect(self.play_)
		self.shortcut_fastb = QShortcut(QKeySequence('Shift+K'), self)
		self.shortcut_fastb.activated.connect(self.play_back)
		self.shortcut_copyb = QShortcut(QKeySequence('Shift+Z'), self)
		self.shortcut_copyb.activated.connect(self.copy_bbox)

		# Click the dropdown box
		self.button.clicked.connect(self.clicker)
		self.buttonSend.clicked.connect(self.send_box)
		self.buttonDelete.clicked.connect(self.del_chosen)
		self.buttonAll.clicked.connect(self.cambia_sb)
		self.buttonSend.setAutoDefault(True)
		self.radioNo.setChecked(True)
		self.radS1.setChecked(True)

		# Set button states
		self.radioB1.toggled.connect(lambda: self.btnstate(self.radioB1))
		self.radioB2.toggled.connect(lambda: self.btnstate(self.radioB2))
		self.radioNo.toggled.connect(lambda: self.btnstate(self.radioNo))

		self.radS1.toggled.connect(lambda: self.Sbtnstate(self.radS1))
		self.radS2.toggled.connect(lambda: self.Sbtnstate(self.radS2))
		self.radS3.toggled.connect(lambda: self.Sbtnstate(self.radS3))
		self.radS4.toggled.connect(lambda: self.Sbtnstate(self.radS4))

		# Show the App
		self.show()

	def sbvis(self, blen, tdown=False):
		self.radS1.setChecked(True)
		if len(blen) < 2:
			self.plotter2(blen, tdown)
			self.text_chosen = blen
			return
		if len(blen) > 1:
			self.cambia_sb(1)
			self.buttonAll.setVisible(True)
			self.radS1.setVisible(True)
			self.radS2.setVisible(True)
		if len(blen) > 2:
			self.radS3.setVisible(True)
		if len(blen) > 3:
			self.radS4.setVisible(True)

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

	def Sbtnstate(self, b):
		if self.pflag:
			return
		if b.isChecked():
			self.cambia_sb(int(b.text()[-2]))

	def send_box(self):
		if self.pflag:
			return
		txt_ = self.bad_list[self.i]
		txt_path = os.path.join(self.sele_path, os.path.basename(txt_))
		self.write_txt(txt_path, self.text_chosen)
		self.next_()
		# self.label_msg.setText("enter")

	def keyPressEvent(self, e):
		# print(e.key())
		if e.key() == 93:
			self.send_box()
		if e.key() == Qt.Key_S:
			self.flag = True
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
		if e.key() == Qt.Key_D:
			self.del_chosen()

		if e.key() == Qt.Key_E:
			self.radioNo.setChecked(True)
		if e.key() == Qt.Key_Q:
			if self.radioB1.isVisible():
				self.radioB1.setChecked(True)
		if e.key() == Qt.Key_W:
			if self.radioB2.isVisible():
				self.radioB2.setChecked(True)
		if e.key() == Qt.Key_1:
			if self.radS1.isVisible():
				self.radS1.setChecked(True)
		if e.key() == Qt.Key_2:
			if self.radS2.isVisible():
				self.radS2.setChecked(True)
		if e.key() == Qt.Key_3:
			if self.radS3.isVisible():
				self.radS3.setChecked(True)
		if e.key() == Qt.Key_4:
			if self.radS4.isVisible():
				self.radS4.setChecked(True)
		if e.key() == Qt.Key_R:
			if self.buttonAll.isVisible():
				self.cambia_sb()

	def del_chosen(self):
		if self.pflag:
			return
		try:
			txt_ = self.bad_list[self.i]
			txt_path = os.path.join(self.sele_path, os.path.basename(txt_))
			os.remove(txt_path)
			self.label_msg.setText("Chosen Deleted")
			self.set_idc(2)
			pixmap = QPixmap("temp_img.jpg")
			self.label.setPixmap(pixmap)
			self.text_chosen = None
			self.buttonDelete.setVisible(False)
		except:
			print("NOT FOUND {}".format(os.path.basename(txt_)))

	def next_(self, flagg=False):
		if self.pflag:
			return
		if self.i < len(self.bad_list) - 1:
			self.i += 1
		else:
			self.i = len(self.bad_list) - 1
		if flagg:
			txt_ = self.bad_list[self.i]
			txt_path = os.path.join(self.sele_path, os.path.basename(txt_))
			img_ = os.path.join(self.img_path, os.path.basename(txt_).replace(self.ext, '.jpg'))
			if os.path.exists(txt_path):
				self.plotter2(self.read_txt(txt_path), True, idx=-1, img_path=img_, label_="chosen") 
				self.label_msg.setText("BBOX Chosen")
				self.buttonDelete.setVisible(True)
				self.set_idc(1)
			else:
				self.plotter2(self.read_txt(txt_), True, idx=0, img_path=img_, label_=None) 
				self.buttonDelete.setVisible(False)
				self.label_msg.setText("")
				self.set_idc(0)
			self.label_frame.setText(os.path.basename(img_))
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
			txt_ = self.bad_list[self.i]
			txt_path = os.path.join(self.sele_path, os.path.basename(txt_))
			img_ = os.path.join(self.img_path, os.path.basename(txt_).replace(self.ext, '.jpg'))
			if os.path.exists(txt_path):
				self.plotter2(self.read_txt(txt_path), True, idx=-1, img_path=img_) 
				self.label_msg.setText("BBOX Chosen")
				self.buttonDelete.setVisible(True)
				self.set_idc(1)
			else:
				self.plotter2(self.read_txt(txt_), True, idx=0, img_path=img_, label_=None) 
				self.buttonDelete.setVisible(False)
				self.label_msg.setText("")
				self.set_idc(0)
			self.label_frame.setText(os.path.basename(img_))
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
				txt_ = self.bad_list[j]
				txt_path = os.path.join(self.sele_path, os.path.basename(txt_))
				img_ = os.path.join(self.img_path, os.path.basename(txt_).replace(self.ext, '.jpg'))
				if os.path.exists(txt_path):
					self.plotter2(self.read_txt(txt_path), True, idx=-1, img_path=img_) 
					self.label_msg.setText("BBOX Chosen")
					self.set_idc(1)
				else:
					self.plotter2(self.read_txt(txt_), True, idx=0, img_path=img_, label_=None) 
					self.label_msg.setText("")
					self.set_idc(0)
				self.label_frame.setText(os.path.basename(img_))
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
				txt_ = self.bad_list[j]
				txt_path = os.path.join(self.sele_path, os.path.basename(txt_))
				img_ = os.path.join(self.img_path, os.path.basename(txt_).replace(self.ext, '.jpg'))
				if os.path.exists(txt_path):
					self.plotter2(self.read_txt(txt_path), True, idx=-1, img_path=img_) 
					self.label_msg.setText("BBOX Chosen")
					self.set_idc(1)
				else:
					self.plotter2(self.read_txt(txt_), True, idx=0, img_path=img_, label_=None) 
					self.label_msg.setText("")
					self.set_idc(0)
				self.label_frame.setText(os.path.basename(img_))
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
			# self.label_msg.setText("NO BBOX")
			return ["NO BBOX u.u"]

	def write_txt(self, txt_path, text_list=None):
		if text_list is not None:
			out_file = open(txt_path, 'w')
			out_file.write('\n'.join(text_list))    
		else:
			return

	def copy_bbox(self, idx=1):
		if self.pflag:
			return
		if self.text_chosen == None:
			try:
				prev_path = self.sele_path + os.path.basename(self.bad_list[self.i+idx])
				txt_path = self.sele_path + os.path.basename(self.bad_list[self.i])
				shutil.copy(prev_path, txt_path)
				self.label_msg.setText("BBOX Copiado!!")
				self.set_idc(2)
				self.plotter2(self.read_txt(txt_path), True)
			except:
				print("NOT FOUND {}".format(os.path.basename(self.bad_list[self.i+idx])))
				return None

	def plotter2(self, txt_, tdown=False, idx=-1, img_path="temp_img.jpg", label_="chosen"): 
		draw_boxes(img_path, txt_, colors[idx], label_, True, None, tdown, imname="temp_img2")
		# Open the image
		pixmap = QPixmap("temp_img2.jpg")
		# Add pic to label
		self.label.setPixmap(pixmap)

	def plotter(self, indx):
		self.label_msg.setText("")
		self.set_idc(0)
		self.buttonDelete.setVisible(False)
		self.radioB1.setVisible(True)
		self.radioB2.setVisible(True)
		self.radS1.setVisible(False)
		self.radS2.setVisible(False)
		self.radS3.setVisible(False)
		self.radS4.setVisible(False)
		self.buttonAll.setVisible(False)
		self.radioNo.setChecked(True)
		self.text_chosen = None

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
			self.plotter2(self.read_txt(txt_path), True)
			self.label_msg.setText("BBOX Chosen")
			self.buttonDelete.setVisible(True)
			self.set_idc(1)
		
	def cambia_sb(self, idx=0):
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
		if idx > 0:
			if len(txt_) > idx-1:
				self.label_msg.setText("{}({})".format(lab_, idx))
				self.set_idc(0)
				self.plotter2([txt_[idx-1]], tdown)
				self.text_chosen = [txt_[idx-1]	]
		else:
			self.label_msg.setText("{}(all)".format(lab_))
			self.set_idc(0)
			self.radS1.setChecked(False)
			self.radS2.setChecked(False)
			self.radS3.setChecked(False)
			self.radS4.setChecked(False)
			self.plotter2(txt_, tdown)
			self.text_chosen = txt_

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