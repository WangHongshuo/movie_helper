from fileinput import filename
import os
import sys
import natsort

from util import detect_file_encoding

HELP_INFO = '''"-p=[Path]"'''

if len(sys.argv) <= 1:
        print(HELP_INFO)
        exit()

for i in range(1, len(sys.argv)):
    if sys.argv[i].startswith("-p="):
        curr_path = sys.argv[i].removeprefix("-p=")
    else:
        print("unsupport argv:" + sys.argv[i])
        print(HELP_INFO)
        exit()
    
print("[Start Check]")
# 过滤器
SUBTITLE_FORMAT = ".ass"
# 列表
subtitle_name_list = list()
# 读取所有.ass文件
for root, dirs, files in os.walk(curr_path, topdown=True):
    for name in files:
        if os.path.splitext(name)[1] == SUBTITLE_FORMAT:
            subtitle_name_list.append(name)
    
    break


subtitle_name_list = natsort.natsorted(subtitle_name_list)

for i in range(len(subtitle_name_list)):
    file_path = os.path.join(curr_path, subtitle_name_list[i])
    is_repeat = False
    file_encoding = detect_file_encoding(file_path)
    print("[Checking]: ", file_path)
    print("[Checking]: Encoding is ", file_encoding)
    file = open(file_path, "r", encoding=file_encoding)
    lines = file.readlines()
    for j in range(0, len(lines)-1):
        if lines[j] == lines[j+1]:
            # 检查到可疑重复
            print("[Error]: line ", j, " and ", j+1, " is same.")
            is_repeat = True
    
    if is_repeat:
        new_file_path = os.path.join(curr_path, os.path.splitext(subtitle_name_list[i])[0] + "(1)" + os.path.splitext(subtitle_name_list[i])[1])
        new_file = open(new_file_path, "w", encoding=file_encoding)
        new_file.writelines(lines[0])
        for j in range(1, len(lines)):
            if lines[j] == lines[j-1]:
                continue
            new_file.writelines(lines[j])
        new_file.close()
        print("[Fix]: Create new file: ", new_file_path)
    
    file.close()


