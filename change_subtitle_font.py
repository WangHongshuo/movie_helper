
from fileinput import filename
import os
import sys
import shutil

from util import detect_file_encoding

HELP_INFO = '''"-p=[Path]", "-ss=[Src String]", "-ds=[Dst String]"'''

src_path = str()
src_str = str()
dst_str = str()

if len(sys.argv) <= 1:
        print(HELP_INFO)
        exit()

for i in range(1, len(sys.argv)):
    if sys.argv[i].startswith("-p="):
        src_path = sys.argv[i].removeprefix("-p=")
    elif sys.argv[i].startswith("-ss="):
        src_str = sys.argv[i].removeprefix("-ss=")
    elif sys.argv[i].startswith("-ds="):
        dst_str = sys.argv[i].removeprefix("-ds=")
    else:
        print("unsupport argv:" + sys.argv[i])
        print(HELP_INFO)
        exit()

src_strs = src_str.split(",")

# 过滤器
SUBTITLE_FORMAT = ".ass"
# 字幕复制
for root, dirs, files in os.walk(src_path, topdown=True):
    for name in files:
        if (os.path.splitext(name)[1] == SUBTITLE_FORMAT):
            old_file_path = os.path.join(root, name)
            file_encoding = detect_file_encoding(old_file_path)
            old_file = open(old_file_path, "r", encoding=file_encoding)
            lines = old_file.readlines()
            old_file.close()
            is_need_new_file = False
            print("[Checking]: ", old_file_path)
            for i in range(0, len(lines)):

                for s in src_strs:
                    if lines[i].find(s) != -1:
                        is_need_new_file = True
                        lines[i] = lines[i].replace(s, dst_str)
                        print("[Changing]: line ", i, " From: ", s, " To: ", dst_str)
                        is_need_new_file = True
                        break

            if is_need_new_file:
                new_file_path = os.path.join(root, name+"tmp")
                new_file = open(new_file_path, "w", encoding=file_encoding)
                new_file.writelines(lines)
                new_file.close()
                os.remove(old_file_path)
                os.rename(new_file_path, old_file_path)
    
    break
