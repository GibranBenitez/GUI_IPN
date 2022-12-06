# utils.py
import os
import random
import shutil
import cv2


def plot_one_box(x, image, color=None, label=None, line_thickness=None, textdow=False):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (image.shape[0] + image.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(image, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        if textdow:
        	c1l = c1[0], c2[1]
        	c2l = c1[0] + t_size[0], c2[1] + t_size[1] + 3
        	lpos = t_size[1]
        else:
        	c1l = c1
        	c2l = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        	lpos = -2
        cv2.rectangle(image, c1l, c2l, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(image, label, (c1l[0], c1l[1] + lpos), 0, tl / 3, [0, 0, 0], thickness=tf, lineType=cv2.LINE_AA)

def draw_boxes(image_path, txt_file, color_, label_=None, img_temp=True, image=None, textdow=False, imname="temp_img"):
    image = image if image is not None else cv2.imread(image_path)
    single = len(txt_file) < 2
    single = single if label_ is not None else True
    height, width, channels = image.shape

    for i, line in enumerate(txt_file):
        staff = line.split() 
        if staff[0] == "NO":
        	break
        lprin = label_ if single else "{}({})".format(label_, i+1)
        x_center, y_center, w, h = float(staff[1])*width, float(staff[2])*height, float(staff[3])*width, float(staff[4])*height
        x1 = round(x_center-w/2)
        y1 = round(y_center-h/2)
        x2 = round(x_center+w/2)
        y2 = round(y_center+h/2)     
        plot_one_box([x1,y1,x2,y2], image, color=[s-(35*i) for s in color_], label=lprin, line_thickness=None, textdow=textdow)
    
    if img_temp:
        cv2.imwrite(imname+".jpg",image) 
        return None
    else:
        return image