import os

directory = 'C:/Users/Luis Bringas/Desktop/NEW_IPN_annotations_txt/3BG32_9_R_37_#513'  # Replace with the path to the directory containing the text files
start_number = 3544
end_number = 3831

for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        file_number = int(filename.split('_')[-1].split('.')[0])
        if start_number <= file_number <= end_number:
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            with open(file_path, 'w') as file:
                file.write(lines[0])