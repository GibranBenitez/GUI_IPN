# utils.py
import os, pdb, glob
import random
import shutil
import cv2
import numpy as np


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

def read_txt(patho, namae=None):
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

def write_txt(txt_path, text_list=None):
    if text_list is not None:
        out_file = open(txt_path, 'w')
        out_file.write('\n'.join(text_list))    
    else:
        print("***ERROR writing the txt file***")
        return

def mix_box(anot_box, sele_box):
    if len(anot_box) < len(sele_box):
        anot_box = [anot_box[0]]*len(sele_box)
    fin_box = sele_box
    for i, sele_line in enumerate(sele_box):
        sele_vals = sele_line.split(" ")
        anot_line = anot_box[i]
        anot_vals = anot_line.split(" ")
        sele_vals[0] = anot_vals[0]
        fin_box[i] = ' '.join(sele_vals)
    return fin_box

def find_SE(txt_path_list):
    anot_list = glob.glob(txt_path_list + "/*.txt")
    list_ids = []
    for anot_txt in anot_list:
        txt_l = read_txt(anot_txt)
        list_ids.append(int(txt_l[0].split(" ")[0]))
    instances = []
    ids_all = []
    for i, idx in enumerate(list_ids):
        if i < 1:
            s = 0
            f = 1
            continue
        if idx != list_ids[i-1]:
            e = i-1
            instances.append([list_ids[i-1], s, e, f])
            ids_all.append(list_ids[i-1])
            s = i
            f = 1
        else:
            f += 1
    if f < 2:
        e = s
    else:
        e = i
    instances.append([list_ids[i], s, e, f])
    ids_all.append(list_ids[i-1])
    values, counts = np.unique(ids_all, return_counts=True)
    ids_unique = values.tolist()
    ids_counts = counts.tolist()
    # pdb.set_trace()

if __name__ == "__main__":

    sepOS = '\\'    # Windows
    # sepOS = '/'     # Ubuntu
    # anot_path = 'D:/Pytorch/yolov5/runs/test_gordo/anotations'
    # sele_path = 'D:/Pytorch/yolov5/runs/test_gordo/selected_boxes'
    # fin_path = 'D:/Pytorch/yolov5/runs/test_gordo/final_annot'
    # anot_path = 'D:/Pytorch/YOLOv5/anotations'
    # sele_path = 'D:/Pytorch/YOLOv5/selected_boxes'
    # fin_path = 'D:/Pytorch/YOLOv5/final_annot'
    anot_path = 'C:\\Users\\Luis Bringas\\Desktop\\New_gt\\anotations'
    sele_path = 'C:\\Users\\Luis Bringas\\Desktop\\New_gt\\selected_boxes'
    fin_path = 'C:\\Users\\Luis Bringas\\Desktop\\New_gt\\final_annot'

    all_folders = glob.glob(anot_path + "/*")
    for folder_a in all_folders:
        folder_ = folder_a.split(sepOS)[-1]
        print("  Generating final annots of {}...".format(folder_))
        if not os.path.exists(os.path.join(fin_path, folder_)):
            os.makedirs(os.path.join(fin_path, folder_))
        anot_list = glob.glob(folder_a + "/*.txt")
        cnt = 0
        cntf = 0

        for anot_txt in anot_list:
            txt_ = anot_txt.split(sepOS)[-1]
            sele_txt = os.path.join(sele_path, folder_, txt_)
            fin_txt = os.path.join(fin_path, folder_, txt_)
            if os.path.exists(fin_txt):
                cntf += 1
                continue

            if os.path.exists(sele_txt):
                sele_box = read_txt(sele_txt)
                anot_box = read_txt(anot_txt)
                final_box = mix_box(anot_box, sele_box)
                write_txt(fin_txt, final_box)
                cnt += 1
                # pdb.set_trace()
            else:
                shutil.copy(anot_txt, fin_txt)
        print("     {}/{} selected bboxes ({} there)".format(cnt, len(anot_list), cntf))
        # find_SE(os.path.join(fin_path, folder_))