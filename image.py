from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QShortcut
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QKeySequence, QKeyEvent
from pathlib import Path
import sys, glob, os, time, random, shutil 
from threading import Timer
from natsort import natsorted, os_sorted, realsorted, humansorted

classes_id = ["D0X: No-gest", "B0A: Point-1f", "B0B: Point-2f", "G01: Click-1f", "G02: Click-2f", "G03: Th-up", "G04: Th-down", 
				"G05: Th-left", "G06: Th-right", "G07: Open-2", "G08: 2click-1f", "G09: 2click-2f", "G10: Zoom-in", "G11: Zoom-o"]
random.seed(42)
colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(classes_id))]
colors.append([255, 255, 255])

init_path = "C:\\Users\\Luis Bringas\\Desktop\\New_gt"
# init_path = "D:/Pytorch/yolov5/runs/Test_DB/frames"

class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()

		# Load the ui file
		uic.loadUi("image.ui", self)

		self.flag = False
		self.pflag = False
		self.bad_flag = False
		self.i = 0

		# Define our widgets
		self.button = self.findChild(QPushButton, "pushButton")
		self.buttonF = self.findChild(QPushButton, "GenerarD")
		self.eliminarB = self.findChild(QPushButton, "EliminarB")
		self.badB = self.findChild(QPushButton, "BadB")
		self.goodB = self.findChild(QPushButton, "GoodB")
		self.copyB = self.findChild(QPushButton, "CopiarB")
		self.label = self.findChild(QLabel, "label")
		self.clabel = self.findChild(QLabel, "label_color")

		self.set_idc()

		self.shortcut_open = QShortcut(QKeySequence('Ctrl+O'), self)
		self.shortcut_open.activated.connect(self.clicker)
		self.shortcut_close = QShortcut(QKeySequence('Ctrl+Q'), self)
		self.shortcut_close.activated.connect(lambda: app.quit())

		self.shortcut_fast = QShortcut(QKeySequence('Shift+P'), self)
		self.shortcut_fast.activated.connect(self.play_)
		self.shortcut_fastb = QShortcut(QKeySequence('Shift+L'), self)
		self.shortcut_fastb.activated.connect(self.play_back)

		# Click the dropdown box
		self.button.clicked.connect(self.clicker)
		self.buttonF.clicked.connect(self.cambia_class)
		self.eliminarB.clicked.connect(self.elimnar_bbox)
		self.badB.clicked.connect(self.bad_bbox)
		self.goodB.clicked.connect(self.good_bbox)
		self.copyB.clicked.connect(self.copy_bbox)

		# Show the App
		self.show()

	def keyPressEvent(self, e):
		if e.key() == Qt.Key_S:
			self.flag = True
		if e.key() == Qt.Key_M:
			self.next_()
		if e.key() == Qt.Key_N:
			self.back_()
		if e.key() == Qt.Key_P:
			self.play_(True)
		if e.key() == Qt.Key_L:
			self.play_back(True)

		if e.key() == Qt.Key_F:
			self.cambia_class(0)
		if e.key() == Qt.Key_1:
			self.cambia_class(1)
		if e.key() == Qt.Key_2:
			self.cambia_class(2)
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


		if e.key() == Qt.Key_R:
			self.elimnar_bbox()
		if e.key() == Qt.Key_K:
			self.bad_bbox()
		if e.key() == Qt.Key_Q:
			self.good_bbox()
		if e.key() == Qt.Key_Z:
			self.copy_bbox()


	def next_(self):
		if self.i < len(self.img_list) - 1:
			self.i += 1
		else:
			self.i = len(self.img_list) - 1
		self.plotter(self.i)

	def back_(self):
		if self.i > 0:
			self.i -= 1
		else:
			self.i = 0
		self.plotter(self.i)

	def play_(self, fflag=False):
		if self.pflag:
			return
		self.flag = False
		self.pflag = True
		for j in range(self.i, len(self.img_list)):
			self.plotter(j)
			app.processEvents()
			if self.flag:
				break
			if fflag:
				time.sleep(0.1)
		self.i = j
		self.flag = False
		self.pflag = False

	def play_back(self, fflag=False):
		if self.pflag:
			return
		self.flag = False
		self.pflag = True
		for j in range(self.i, 0, -1):
			self.plotter(j)
			app.processEvents()
			if self.flag:
				break
			if fflag:
				time.sleep(0.05)
		self.i = j
		self.flag = False
		self.pflag = False

	def elimnar_bbox(self):
		if self.pflag:
			return
		if self.text_list is not None:
			try:
				txt_path = self.ano_path + os.path.basename(self.img_list[self.i]).replace(self.ext, '.txt')
				del_path = self.bin_path + os.path.basename(self.img_list[self.i]).replace(self.ext, '.txt')
				shutil.move(txt_path, del_path)
				self.label_msg.setText("BBOX BORRADO!!")
				print(self.label_msg.text())
				self.good_bbox()
			except:
				ptn = "CAN'T DELETE {}".format(os.path.basename(self.img_list[self.i-1]))
				self.label_msg.setText(ptn)
				print(ptn)

	def bad_bbox(self):
		if self.pflag:
			return
		self.label_msg.setText("A BAD BBOX")
		self.label_msg.setStyleSheet("background-color: rgb({},{},{})".format(197, 119, 119))
		txt_path = self.bad_path + os.path.basename(self.img_list[self.i]).replace(self.ext, '.txt')
		self.write_txt(txt_path, self.text_list)
		self.bad_flag = True
		self.next_()

	def good_bbox(self):
		if self.pflag:
			return
		if self.bad_flag:
			txt_path = self.bad_path + os.path.basename(self.img_list[self.i]).replace(self.ext, '.txt')
			os.remove(txt_path)
			if self.label_msg.text() != "BBOX BORRADO!!":
				self.label_msg.setText("GOOD BBOX")
			self.bad_flag = False

	def copy_bbox(self):
		if self.pflag:
			return
		if self.text_list == None:
			try:
				prev_path = self.ano_path + os.path.basename(self.img_list[self.i-1]).replace(self.ext, '.txt')
				txt_path = self.ano_path + os.path.basename(self.img_list[self.i]).replace(self.ext, '.txt')
				shutil.copy(prev_path, txt_path)
				self.bad_bbox()
				self.label_msg.setText("BBOX Copiado!!")
			except:
				self.label_msg.setText("NO {}".format(os.path.basename(self.img_list[self.i-1])))
				print("NOT FOUND {}".format(os.path.basename(self.img_list[self.i-1])))
				return None

	def set_idc(self, idx=-1):
		id_color = colors[idx]
		self.clabel.setStyleSheet("background-color: rgb({},{},{})".format(id_color[2], id_color[1], id_color[0]))

	def read_txt(self, indx):
		txt_path = self.ano_path + os.path.basename(self.img_list[indx]).replace(self.ext, '.txt')
		try:
			my_file = open(txt_path, "r")
			dlab = my_file.read()
			text_list = dlab.split(" ")
			return text_list
		except:
			self.label_msg.setText("NO BBOX")
			return None

	def write_txt(self, txt_path, text_list=None):
		out_file = open(txt_path, 'w')
		if text_list is not None:
			out_file.write(" ".join(text_list) + '\n')    
		else:
			out_file.write("NO BBOX u.u" + '\n')    

	def plotter(self, indx):
		self.label_msg.setText("")
		self.label_msg.setStyleSheet("background-color: rgb({},{},{})".format(240,240,240))
		img_ = self.img_list[indx]
		# Open the image
		self.pixmap = QPixmap(img_)
		# Add pic to label
		self.label.setPixmap(self.pixmap)
		self.label_frame.setText(os.path.basename(img_))
		txt_l = self.read_txt(indx)
		if txt_l is not None:
			c_id = int(txt_l[0])
		else:
			self.label_msg.setText("NO BBOX")
			self.label_msg.setStyleSheet("background-color: rgb({},{},{})".format(140, 119, 119))
			c_id = 0
		self.label_id.setText(classes_id[c_id])
		self.set_idc(c_id)
		self.text_list = txt_l

		bad_list = glob.glob("{}/*txt".format(self.bad_path))
		bad_list = [os.path.basename(s) for s in bad_list]
		if os.path.basename(self.img_list[indx]).replace(self.ext, '.txt') in bad_list:
			self.label_msg.setText("BAD BBOX")
			self.label_msg.setStyleSheet("background-color: rgb({},{},{})".format(197, 119, 119))
			self.bad_flag = True
		else:
			self.bad_flag = False

	def cambia_class(self, idx=0):
		print(int(idx))
		if self.pflag:
			return
		if self.text_list is not None:
			self.text_list[0] = str(int(idx))
			txt_path = self.ano_path + os.path.basename(self.img_list[self.i]).replace(self.ext, '.txt')
			self.write_txt(txt_path, self.text_list)
		else:
			print("WARNING: No se puede cambiar clase porque no hay BOX!")
			return
		self.label_id.setText(classes_id[idx])
		self.set_idc(idx)
		if idx > 2:
			self.label_msg.setText("CLASE Cambiada a G{}".format(idx-2))
		elif idx == 1:
			self.label_msg.setText("CLASE Cambiada a B0A")
		elif idx == 2:
			self.label_msg.setText("CLASE Cambiada a B0B")
		else:
			self.label_msg.setText("CLASE A D0X!!")


	def clicker(self):
		# fpath = QFileDialog.getExistingDirectory(self, "Select Directory", "D:\\") D:\Pytorch\yolov5\runs\4CM11_24_L_#61
		# self.label.setText(str(fpath))

		fname = QFileDialog.getOpenFileName(self, "Open Image", init_path, "Image Files (*.jpg *.png)")
		iPath = fname[0]
		self.ext = os.path.splitext(iPath)[-1]
		img_path = os.path.dirname(iPath)
		print(img_path.split(os.sep))
		self.ano_path = "{}/anotations/{}/".format(Path(iPath).parents[2], img_path.split('/')[-1])

		self.bad_path = "{}/bad_bboxes/{}/".format(Path(iPath).parents[2], img_path.split('/')[-1])
		self.bin_path = "{}/bad_bboxes/RecycleBin/".format(Path(iPath).parents[2])
		if not os.path.exists(self.bad_path):
			os.makedirs(self.bad_path)
		if not os.path.exists(self.bin_path):
			os.makedirs(self.bin_path)

		img_list = glob.glob("{}/*{}".format(img_path, self.ext))
		self.img_list = os_sorted([s.replace('\\', '/') for s in img_list])

		self.i = self.img_list.index(iPath.replace('\\', '/'))

		self.plotter(self.i)

if __name__ == "__main__":
	# Initialize the app
	app = QApplication(sys.argv)
	UIWindow = UI()
	app.exec_()