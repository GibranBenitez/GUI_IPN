# utils.py
import os, pdb, glob
import random
import shutil
import cv2
import numpy as np
from natsort import natsorted, os_sorted

classes_id = ["D0X: No-gest", "B0A: Point-1f", "B0B: Point-2f", "G01: Click-1f", "G02: Click-2f", "G03: Th-up", "G04: Th-down", 
                "G05: Th-left", "G06: Th-right", "G07: Open-2", "G08: 2click-1f", "G09: 2click-2f", "G10: Zoom-in", "G11: Zoom-o", "G12: Grab"]
random.seed(42)

def calculate_iou_yolo(yolo_bbox1, yolo_bbox2, img_width, img_height):
    # Helper function to convert YOLO bbox to regular bbox
    def yolo_to_bbox(yolo, img_width, img_height):
        x_center, y_center, width, height = map(float, yolo.split()[1:])
        x1 = (x_center - width / 2) * img_width
        y1 = (y_center - height / 2) * img_height
        x2 = (x_center + width / 2) * img_width
        y2 = (y_center + height / 2) * img_height
        return [x1, y1, x2, y2]
    # Convert YOLO bboxes to regular format
    bbox1 = yolo_to_bbox(yolo_bbox1, img_width, img_height)
    bbox2 = yolo_to_bbox(yolo_bbox2, img_width, img_height)
    # Calculate IoU
    x1_max = max(bbox1[0], bbox2[0])
    y1_max = max(bbox1[1], bbox2[1])
    x2_min = min(bbox1[2], bbox2[2])
    y2_min = min(bbox1[3], bbox2[3])
    intersection = max(x2_min - x1_max, 0) * max(y2_min - y1_max, 0)
    area_box1 = (bbox1[2] - bbox1[0]) * (bbox1[3] - bbox1[1])
    area_box2 = (bbox2[2] - bbox2[0]) * (bbox2[3] - bbox2[1])
    union = area_box1 + area_box2 - intersection
    if union == 0:
        return 0
    return intersection / union

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
        colore_ = [57, 12, 140] if int(staff[0]) < 1 else color_
        plot_one_box([x1,y1,x2,y2], image, color=[s-(35*i) for s in colore_], label=lprin, line_thickness=None, textdow=textdow)
    if img_temp:
        cv2.imwrite(imname+".jpg",image) 
        return None
    else:
        return image

def draw_change_boxes(txt_file, index_=None, value_=0, xml_in=True):
    label_ = None
    color_ = [20, 255, 60]  # bright shade of green
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

def find_SE(txt_path_list, lenv = False):
    anot_list = glob.glob(txt_path_list + "/*.txt")
    list_ids = []
    frame_ids = []
    hands_list = []
    for anot_txt in anot_list:
        txt_l = read_txt(anot_txt)
        hands_list.append(1 if len(txt_l) > 1 else 0)
        frame_ids.append(int(anot_txt.split(".txt")[0].split("_")[-1]))
        list_ids.append(int(txt_l[0].split(" ")[0]))
    instances = []
    ids_all = []
    for i, idx in enumerate(list_ids):
        if i < 1:
            s = frame_ids[0]
            s_i = 0
            f = 1
            continue
        if idx != list_ids[i-1]:
            e = frame_ids[i-1]
            if lenv:
                s_i = len(anot_list)
            instances.append([list_ids[i-1], s, e, f, s_i, sum(hands_list[s_i:i-1])])
            ids_all.append(list_ids[i-1])
            s = frame_ids[i]
            s_i = i
            f = 1
        else:
            f += 1
    if f < 2:
        e = s
    else:
        e = frame_ids[i]
    if lenv:
        s_i = len(anot_list)
    instances.append([list_ids[i], s, e, f, s_i, sum(hands_list[s_i:i])])
    ids_all.append(list_ids[i])
    values, counts = np.unique(ids_all, return_counts=True)
    uniq_cnt = list(range(len(classes_id)))
    for idx, cnt in zip(values.tolist(), counts.tolist()):
        uniq_cnt[idx] = cnt
    return [instances, uniq_cnt]

def save_vid_lists(instances, folder_, list_path):
    class_segments = [ [] for _ in range(len(classes_id)) ]
    for segment_ in instances:
        segment_ = [str(s) for s in segment_]
        segment_.insert(0, folder_)
        for i, class_ in enumerate(classes_id):
            if i == int(segment_[1]):
                class_segments[i].append(" ".join(segment_))
    for i, c_seg_ in enumerate(class_segments):
        class_ = classes_id[i]
        write_txt(os.path.join(list_path, "vid_segments", "{}_{}.txt".format("_".join(class_.split(": ")), folder_)), c_seg_)
    return class_segments

def save_full_list(idc, list_path):
    class_ = classes_id[idc]
    class_list = glob.glob(os.path.join(list_path, "vid_segments") + "/{}*".format("_".join(class_.split(": "))))
    list_full = []
    for list_ in class_list:
        list_full = list_full + read_txt(list_)
    list_full = os_sorted(list_full)        
    write_txt(os.path.join(list_path, "{}.txt".format("_".join(class_.split(": ")))), list_full)
    return list_full

if __name__ == "__main__":

    sepOS = '\\'    # Windows
    # sepOS = '/'     # Ubuntu

    frames_path = "F:\\IPN_Hand\\frames"
    anot_path = 'C:\\Users\\Luis Bringas\\Desktop\\New_gt\\anotations'
    sele_path = 'C:\\Users\\Luis Bringas\\Desktop\\New_gt\\selected_boxes'
    fin_path = 'C:\\Users\\Luis Bringas\\Desktop\\New_gt\\final_annot'
    list_path = 'C:\\Users\\Luis Bringas\\Desktop\\New_gt\\segment_lists'
    # frames_path = "E:/datasets/IPN_hand/frames"
    # anot_path = 'D:/Pytorch/yolov5/runs/test_gordo/anotations'
    # sele_path = 'D:/Pytorch/yolov5/runs/test_gordo/selected_boxes'
    # fin_path = 'D:/Pytorch/yolov5/runs/test_gordo/final_annot'
    # list_path = 'D:/Pytorch/yolov5/runs/test_gordo/segment_lists'
    # frames_path = "D:/datasets/IPN_hand/frames"
    # anot_path = 'D:/Pytorch/YOLOv5/anotations'
    # sele_path = 'D:/Pytorch/YOLOv5/selected_boxes'
    # sele_path = 'D:/Pytorch/YOLOv5/ipn_gordo'
    # fin_path = 'D:/Pytorch/YOLOv5/final_annot'
    # list_path = 'D:/Pytorch/YOLOv5/segment_lists'

    # all_folders = glob.glob(anot_path + "/*")
    # for folder_a in all_folders:
    #     folder_ = folder_a.split(sepOS)[-1]
    #     print("  Generating final annots of {}...".format(folder_))
    #     if not os.path.exists(os.path.join(fin_path, folder_)):
    #         os.makedirs(os.path.join(fin_path, folder_))
    #     # anot_list = glob.glob(folder_a + "/*.txt")
    #     anot_list = glob.glob(frames_path + sepOS + folder_ + sepOS + "/*.jpg")
    #     cnt = 0
    #     cntf = 0

    #     for frame_ in anot_list:
    #         txt_ = frame_.split(sepOS)[-1].replace('.jpg', '.txt')
    #         anot_txt = os.path.join(folder_a, txt_)
    #         sele_txt = os.path.join(sele_path, folder_, txt_)
    #         fin_txt = os.path.join(fin_path, folder_, txt_)
    #         if os.path.exists(fin_txt):
    #             cntf += 1
    #             continue

    #         if os.path.exists(sele_txt) and os.path.exists(anot_txt):
    #             sele_box = read_txt(sele_txt)
    #             anot_box = read_txt(anot_txt)
    #             final_box = mix_box(anot_box, sele_box)
    #             write_txt(fin_txt, final_box)
    #             cnt += 1
    #             # pdb.set_trace()
    #         elif os.path.exists(anot_txt):
    #             shutil.copy(anot_txt, fin_txt)
    #             cnt += 1
    #         elif os.path.exists(sele_txt):
    #             shutil.copy(sele_txt, fin_txt)
    #             cnt += 1
    #         else:
    #             write_txt(fin_txt, ["0 0.0 0.0 0.0 0.0"])
    #     print("     {}/{} selected bboxes ({} there)".format(cnt, len(anot_list), cntf))



    all_videos = glob.glob(fin_path + "/*")
    print(fin_path)
    if not os.path.exists(list_path):
        os.makedirs(list_path)
    if not os.path.exists(os.path.join(list_path, "vid_segments")):
        os.makedirs(os.path.join(list_path, "vid_segments"))
        
    for i, vid_a in enumerate(all_videos):
        folder_ = vid_a.split(sepOS)[-1]
        print("   Genereting list of [{}] ".format(i)+folder_+"...")
        instances, uniq_cnt = find_SE(os.path.join(vid_a), True)
        save_vid_lists(instances, folder_, list_path)

    print("Saving full lists of {} videos...".format(len(all_videos)))
    full_segments = []
    for i, class_ in enumerate(classes_id):
        class_ = classes_id[i]
        list_ = save_full_list(i, list_path)
        full_segments += list_
        print("   {}: {} instances".format(class_, len(list_)))

    write_txt(os.path.join(list_path, "Z_Full.txt"), full_segments)
    print(" Total: {} instances".format(len(full_segments)))