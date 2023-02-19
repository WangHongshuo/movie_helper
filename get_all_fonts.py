import os
import sys

from pyparsing import line

from util import detect_file_encoding


HELP_INFO = '''"-p=[Path]""'''

src_path = str()

if len(sys.argv) <= 1:
    print(HELP_INFO)
    exit()

for i in range(1, len(sys.argv)):
    if sys.argv[i].startswith("-p="):
        src_path = sys.argv[i].removeprefix("-p=")
    else:
        print("unsupport argv:" + sys.argv[i])
        print(HELP_INFO)
        exit()

# 过滤器
SUBTITLE_FORMAT = ".ass"
fonts_set = set()
FN_TARGET = "\\fn"
# 字幕复制
for root, dirs, files in os.walk(src_path, topdown=True):
    for name in files:
        if (os.path.splitext(name)[1] == SUBTITLE_FORMAT):
            old_file_path = os.path.join(root, name)
            file_encoding = detect_file_encoding(old_file_path)
            old_file = open(old_file_path, "r", encoding=file_encoding)
            lines = old_file.readlines()
            old_file.close()
            print("[Checking]: ", old_file_path)
            for i in range(0, len(lines)):
                pos = lines[i].find(FN_TARGET)
                if pos != -1:
                    for j in range(pos+3, len(lines[i])):
                        if lines[i][j] == "\\" or lines[i][j] == "}":
                            fonts_set.add(lines[i][pos+3:j])
                            break
    
    break

output = str()
for i in fonts_set:
    output = output + i + ","

output = output.removesuffix(",")
print(output)

