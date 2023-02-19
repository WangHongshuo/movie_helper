from fileinput import filename
import os
import sys
import natsort
from operator import itemgetter
import re

HELP_INFO = '''"-p=[Path]", "-ss=(opt: -reg=[reg])[Src String]", "-ds=[Dst String]"'''

if len(sys.argv) <= 1:
        print(HELP_INFO)
        exit()

curr_path = str()
src_str = str()
dst_str = str()

for i in range(1, len(sys.argv)):
    if sys.argv[i].startswith("-p="):
        curr_path = sys.argv[i].removeprefix("-p=")
    elif sys.argv[i].startswith("-ss="):
        src_str = sys.argv[i].removeprefix("-ss=")
    elif sys.argv[i].startswith("-ds="):
        dst_str = sys.argv[i].removeprefix("-ds=")
    else:
        print("unsupport argv:" + sys.argv[i])
        print(HELP_INFO)
        exit()
    
# 过滤器
MOVIE_FORMAT = ".mkv"
SUBTITLE_FORMAT = ".ass"

print("Path={}".format(curr_path))

# 列表
movie_name_list = list()
subtitle_name_list = list()
# 视频重命名
for root, dirs, files in os.walk(curr_path, topdown=True):
    for name in files:
        if os.path.splitext(name)[1] == MOVIE_FORMAT:
            new_file_name = os.path.splitext(name)[0]

            if src_str != "":
                if src_str.count("-reg=") != 0:
                    new_file_name = re.sub(src_str.removeprefix("-reg="), dst_str, new_file_name)
                else:    
                    new_file_name = new_file_name.replace(src_str, dst_str)

            os.rename(os.path.join(curr_path, name), os.path.join(curr_path, new_file_name + MOVIE_FORMAT))
            print("[Video Renaming:]from: ", name, " to: ", new_file_name + MOVIE_FORMAT)
            movie_name_list.append(new_file_name)
            
        if os.path.splitext(name)[1] == SUBTITLE_FORMAT:
            pair = dict()
            pair["key"] = name.replace(" ", "")
            pair["value"] = name
            subtitle_name_list.append(pair)
    
    break


movie_name_list = natsort.natsorted(movie_name_list)
subtitle_name_list = natsort.natsorted(subtitle_name_list, key=itemgetter("key"))

# 字幕重命名
if len(movie_name_list) == len(subtitle_name_list):
    for i in range(len(movie_name_list)):
        print("[Subtitle Renaming]from: ", subtitle_name_list[i]["value"], " to : ", movie_name_list[i] + SUBTITLE_FORMAT)
        os.rename(os.path.join(curr_path, subtitle_name_list[i]["value"]), os.path.join(curr_path, movie_name_list[i] + SUBTITLE_FORMAT))

