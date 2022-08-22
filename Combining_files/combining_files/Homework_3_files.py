import os
import glob

def list_name_files():
    files_list = []
    for i in glob.glob('*.txt'):
        files_list.append(i)
    return files_list

def files_path():
    current_path = os.getcwd()
    folder_name = 'result_file'
    file_name = '4.txt'
    file_path = os.path.join(os.getcwd(), folder_name, file_name)
    return file_path

def file_sorted():
    dictionary = {}
    for i in list_name_files():
        count = 0
        with open(i, encoding='utf-8') as f:
            for line in f:
                count += 1
        dictionary[f.name] = count
    files_names = dict(sorted(dictionary.items(), key=lambda x: x[1]))
    return files_names

def write_file():
    for i in file_sorted():
        with open(i, 'r', encoding='utf-8') as fr, open(files_path(), 'a', encoding='utf-8') as fw:
            fw.write(f'{i} \n')
            fw.write(f'{file_sorted()[i]} \n')
            for line in fr:
                fw.write(f'{line.strip()} \n')
    return


def read_new_file():
    with open(files_path(), 'r', encoding='utf-8') as f:
        for line in f:
            print(line.strip())


write_file()
read_new_file()
