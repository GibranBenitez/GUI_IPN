# utils.py
import os
import random
import shutil
import cv2


def xml_to_yolo_bbox(bbox, w, h):
    # xmin, ymin, xmax, ymax
    x_center = ((bbox[2] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[1]) / 2) / h
    width = (bbox[2] - bbox[0]) / w
    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]

def yolo_to_xml_bbox(bbox, w, h):
    # x_center, y_center width heigth
    w_half_len = (bbox[2] * w) / 2
    h_half_len = (bbox[3] * h) / 2
    xmin = int((bbox[0] * w) - w_half_len)
    ymin = int((bbox[1] * h) - h_half_len)
    xmax = int((bbox[0] * w) + w_half_len)
    ymax = int((bbox[1] * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]

def bbox_limits(bbox, w, h):
    for i, point in enumerate(bbox):
        if point < 1:
            bbox[i] = 0
    # width [0] [2]
    if bbox[0] > w-1:
        bbox[0] = w-1
    if bbox[2] > w-1:
        bbox[2] = w-1
    # height [1] [3]
    if bbox[1] > h-1:
        bbox[1] = h-1
    if bbox[3] > h-1:
        bbox[3] = h-1
    return bbox

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
        [x1,y1,x2,y2] = yolo_to_xml_bbox([float(staff[1]),float(staff[2]),float(staff[3]),float(staff[4])], width, height)
        plot_one_box([x1,y1,x2,y2], image, color=[s-(35*i) for s in color_], label=lprin, line_thickness=None, textdow=textdow)
    if img_temp:
        cv2.imwrite(imname+".jpg",image) 
        return None
    else:
        return image

def draw_change_boxes(txt_file, index_=None, value_=0, xml_in=True):
    label_ = None
    color_ = [20, 255, 60]
    image = cv2.imread("temp_img2.jpg")

    if xml_in:
    	xml_list = txt_file[0]
    	width = txt_file[1]
    	height = txt_file[2]
    	t_lbl = txt_file[3]
    else:
    	height, width, channels = image.shape
    	line = txt_file[0]
    	staff = line.split() 
    	t_lbl = staff[0]
    	[x1,y1,x2,y2] = yolo_to_xml_bbox([float(staff[1]),float(staff[2]),float(staff[3]),float(staff[4])], width, height)
    	xml_list = [x1,y1,x2,y2]
    if index_ is not None:
        xml_list[index_] = xml_list[index_] + value_
        xml_list = bbox_limits(xml_list, width, height)

    lprin = label_ 
    plot_one_box(xml_list, image, color=[s for s in color_], label=lprin, line_thickness=None, textdow=True)
    cv2.imwrite("temp_img3.jpg",image)

    return [xml_list, width, height, t_lbl]

def xml_to_yolo(xml_list):
	[x, y, w, h] = xml_to_yolo_bbox(xml_list[0], xml_list[1], xml_list[2])
	str_list = [xml_list[3], x, y, w, h]
	return ' '.join([str(s) for s in str_list])