# Programa para duplicar bboxes en un grupo de anotaciones
import os

bbox_file = "C:/Users/Luis Bringas/Desktop/NEW_IPN_annotations_txt/3BG32_9_R_37_#513/master.txt"
frames_path = "C:/Users/Luis Bringas/Desktop/NEW_IPN_annotations_txt/3BG32_9_R_37_#513"  
frame_range = [5316, 5415] #Ingresar el frame inicial y el final en enteros, no poner ceros a ;a izquierda.


def add_lines(file_path, bboxes):
	bb_size = len(bboxes)
	newline_flag = False
	if bb_size < 1:
		print(f"Error the bbox file is empty '{bboxes}'.")
		return
	try:
		with open(file_path, 'r') as file:
			contents = file.read()
			if not contents.endswith('\n'):
				newline_flag = True
		with open(file_path, 'a') as file:
			if newline_flag:
				file.write('\n')
			for i, line in enumerate(bboxes):
				if i + 1 < bb_size:
					file.write(line + '\n')
				else:
					file.write(line)
		print(f"{os.path.basename(file_path)} ...DONE")
	except IOError:
		print(f"Error writing to file '{file_path}'.")

bboxes = []
try:
    with open(bbox_file, 'r') as file:
        print("Las siguientes bboxes van a ser copiadas: ")
        for line in file:
            line = line.strip() 
            bboxes.append(line)
            print(line)
        print("")
except FileNotFoundError:
    print(f"File '{bbox_file}' not found.")
except IOError:
    print(f"Error reading file '{bbox_file}'.")

for i in range(frame_range[0], frame_range[1]+1):
	frame_path = os.path.join(frames_path, os.path.basename(frames_path) + "_{:06d}.txt".format(i))
	add_lines(frame_path, bboxes)
