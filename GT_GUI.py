from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QSlider, QFileDialog, QShortcut
from PyQt5.QtGui import QPixmap, QImage, QKeySequence
from PyQt5.QtCore import Qt, QTimer

import os, cv2, random
import numpy as np
import glob

classes_id = ["D0X: No-gest", "B0A: Point-1f", "B0B: Point-2f", "G01: Click-1f", "G02: Click-2f", "G03: Th-up", "G04: Th-down", 
                "G05: Th-left", "G06: Th-right", "G07: Open-2", "G08: 2click-1f", "G09: 2click-2f", "G10: Zoom-in", "G11: Zoom-o", "G12: Catch", ""]
random.seed(42)
colorsl = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(classes_id))]
colorsl.append([0, 255, 255])

folder_names = ["NEW_IPN_annotations_txt", "NEW_IPN_preds"]
# folder_names = ["'annots'", "preds"]

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        # GUI components
        self.title_label = QLabel(self)
        self.subtitle_label = QLabel(self)
        self.image_label = QLabel(self)
        self.subtitle2_label = QLabel(self)
        self.slider = QSlider(Qt.Horizontal, self)
        self.next_button = QPushButton('Next', self)
        self.previous_button = QPushButton('Previous', self)
        self.play_button = QPushButton('Play', self)
        self.stop_button = QPushButton('Stop', self)
        self.open_button = QPushButton('Open', self)

        # Layout
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.title_label)
        vbox.addWidget(self.subtitle_label)
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.subtitle2_label)
        vbox.addWidget(self.slider)
        vbox.addWidget(self.next_button)
        vbox.addWidget(self.previous_button)
        vbox.addWidget(self.play_button)
        vbox.addWidget(self.stop_button)
        vbox.addWidget(self.open_button)

        # Initialize
        self.frame_files = []
        self.current_index = 0

        # Timer for play functionality
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)

        # Event handlers
        self.slider.valueChanged.connect(self.slider_changed)
        self.next_button.clicked.connect(self.next_frame)
        self.previous_button.clicked.connect(self.previous_frame)
        self.play_button.clicked.connect(self.play)
        self.stop_button.clicked.connect(self.stop)
        self.open_button.clicked.connect(self.open)
        # Next Button Shortcut
        next_shortcut = QShortcut(QKeySequence(Qt.Key_Right), self)
        next_shortcut.activated.connect(self.next_frame)
        # Previous Button Shortcut
        prev_shortcut = QShortcut(QKeySequence(Qt.Key_Left), self)
        prev_shortcut.activated.connect(self.previous_frame)
        # Play Button Shortcut
        play_shortcut = QShortcut(QKeySequence(Qt.Key_Space), self)
        play_shortcut.activated.connect(self.play)
        # Stop Button Shortcut
        stop_shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        stop_shortcut.activated.connect(self.stop)
        # Open Button Shortcut
        open_shortcut = QShortcut(QKeySequence('O'), self)
        open_shortcut.activated.connect(self.open)

    def load_image(self, path):
        # Load the image using OpenCV
        image = cv2.imread(path)

        # Check if the image was loaded successfully
        if image is None:
            print(f"Failed to load image at {path}")
            return None

        # Convert the image from BGR to RGB (because OpenCV uses BGR by default)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        return image


    def load_annotation(self, path):
        boxes = []

        # Check if annotation file exists
        if not os.path.exists(path):
            print(f"Annotation file not found at {path}")
            return boxes

        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                tokens = line.split()
                class_id = int(tokens[0])
                x_center = float(tokens[1])
                y_center = float(tokens[2])
                width = float(tokens[3])
                height = float(tokens[4])
                box = {'class_id': class_id, 'x_center': x_center, 'y_center': y_center, 'width': width, 'height': height}
                boxes.append(box)
        return boxes

    def load_prediction(self, path):
        boxes = []

        # Check if prediction file exists
        if not os.path.exists(path):
            # print(f"Prediction file not found at {path}")
            return boxes

        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                tokens = line.split()
                class_id = int(tokens[0])
                x_center = float(tokens[1])
                y_center = float(tokens[2])
                width = float(tokens[3])
                height = float(tokens[4])
                box = {'class_id': class_id, 'x_center': x_center, 'y_center': y_center, 'width': width, 'height': height}
                boxes.append(box)
        return boxes


    def draw_boxes_on_image(self, image, boxes, color=None):
        # Get the image dimensions
        height, width = image.shape[:2]

        for box in boxes:
            class_id = box['class_id']

            # Convert the bounding box coordinates from normalized to actual values
            x_center = int(box['x_center'] * width)
            y_center = int(box['y_center'] * height)
            box_width = int(box['width'] * width)
            box_height = int(box['height'] * height)

            # Convert the center-based bounding box coordinates to corner-based
            x_min = int(x_center - box_width / 2)
            y_min = int(y_center - box_height / 2)
            x_max = int(x_center + box_width / 2)
            y_max = int(y_center + box_height / 2)

            color_rgb = colorsl[color] if color is not None else colorsl[class_id]

            # Draw the bounding box on the image
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color_rgb[::-1], 2)

            # Optionally, draw the class_id near the bounding box
            if color is None:
                cv2.putText(image, classes_id[class_id], (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_rgb[::-1], 2)

        if not boxes:
            return image, False
        
        if color is not None:
            # Draw a border around the image
            class_id = boxes[0]['class_id']
            cv2.rectangle(image, (0, 0), (width - 1, height - 1), colorsl[class_id][::-1], thickness=20)  # adjust thickness as needed

        return image, True

    def open(self):
        # TODO: Open a dialog to select a video folder, load frame files and annotations, update slider range
        dir_path = QFileDialog.getExistingDirectory(self, 'YOUR_DIALOG_TITLE')
        if dir_path:
            # Use glob to get all .jpg files
            self.frame_files = sorted(glob.glob(os.path.join(dir_path, '*.jpg')))

            if len(self.frame_files) > 0:
                # Get the parent directory
                grandparent_dir = os.path.dirname(os.path.dirname(dir_path))

                # Replace the './' in annot_folder and pred_folder with grandparent_dir in update_frame
                self.annot_folder = os.path.join(grandparent_dir, folder_names[0])
                self.pred_folder = os.path.join(grandparent_dir, folder_names[1])

                # Set up the slider
                self.slider.setMinimum(0)
                self.slider.setMaximum(len(self.frame_files) - 1)
                self.slider.setValue(0)

                # Set the current index to 0 and update the frame
                self.current_index = 0
                self.update_frame()
            else:
                # Error handling if there are no .jpg files
                print(f"No .jpg files found in the directory: {dir_path}")

    def update_frame(self):
        frame_path = self.frame_files[self.current_index]
        image = self.load_image(frame_path)

        # Update the title label with the frame name
        base_name = os.path.splitext(os.path.basename(frame_path))[0]  # remove '.jpg'
        self.title_label.setText(f"<h2><b><center>{base_name}</center></b></h2>")

        # Generate paths for annotation and prediction files
        annot_folder = os.path.join(self.annot_folder, os.path.basename(os.path.dirname(frame_path)))
        pred_folder = os.path.join(self.pred_folder, os.path.basename(os.path.dirname(frame_path)))
        file_name = os.path.basename(frame_path).replace('.jpg', '.txt')
        annot_path = os.path.join(annot_folder, file_name)
        pred_path = os.path.join(pred_folder, file_name)

        annot_boxes = self.load_annotation(annot_path)
        pred_boxes = self.load_prediction(pred_path)        

        # Display the class name based on the first annotation box (if any)
        if annot_boxes:
            class_id = annot_boxes[0]['class_id']  # Use the first box's class_id
            class_name = classes_id[class_id]  # Use your classes_id list to get the class name
            color_rgb = colorsl[class_id]
            # Set the subtitle label text and color
            color_rgb = color_rgb[::-1]  # Convert BGR to RGB
            self.subtitle_label.setText(f"<h1><b><center>{class_name}</center></b></h1>")
            self.subtitle_label.setStyleSheet(f"color: rgb({color_rgb[0]}, {color_rgb[1]}, {color_rgb[2]})")

        image, _ = self.draw_boxes_on_image(image, annot_boxes, color=-1)  # annotation boxes in yellow
        image, flag = self.draw_boxes_on_image(image, pred_boxes)  # predicted boxes with respective colors

        if not flag:  
            # If no prediction boxes were drawn, update the subtitle2_label
            self.subtitle2_label.setText("<h2><b><center>No predictions found for this frame</center></b></h2>")
            self.subtitle2_label.setStyleSheet("color: red")  # Set the color to red
        else:
            # If predictions were found, clear the subtitle2_label
            self.subtitle2_label.setText("")

        # Convert image to QPixmap and show it
        qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)

    def slider_changed(self):
        self.current_index = self.slider.value()
        self.update_frame()

    def next_frame(self):
        if self.current_index < len(self.frame_files) - 1:
            self.current_index += 1
            self.slider.setValue(self.current_index)
            self.update_frame()

    def previous_frame(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.slider.setValue(self.current_index)
            self.update_frame()

    def play(self):
        self.timer.start(3)  # play next frame every 1000 ms

    def stop(self):
        self.timer.stop()


app = QApplication([])
viewer = ImageViewer()
viewer.show()
app.exec_()
