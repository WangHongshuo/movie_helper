from fileinput import filename
import os
import sys
import natsort

HELP_INFO = '''"-op=[p(or s)]", "-p=[Path]", "-s=[Add String]"'''

if len(sys.argv) <= 1:
        print(HELP_INFO)
        exit()

curr_path = str()
add_str = str()
op = str()

for i in range(1, len(sys.argv)):
    if sys.argv[i].startswith("-p="):
        curr_path = sys.argv[i].removeprefix("-p=")
    elif sys.argv[i].startswith("-s="):
        add_str = sys.argv[i].removeprefix("-s=")
    elif sys.argv[i].startswith("-op="):
        op = sys.argv[i].removeprefix("-op=")
    else:
        print("unsupport argv:" + sys.argv[i])
        print(HELP_INFO)
        exit()
    
if op != "p" and op != "s":
    print("invalid op:", op)
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
            if op == "p":
                new_file_name = add_str + new_file_name
            if op == "s":
                new_file_name = new_file_name + add_str
            os.rename(os.path.join(curr_path, name), os.path.join(curr_path, new_file_name + MOVIE_FORMAT))
            print("[Video Renaming:]from: ", name, " to: ", new_file_name + MOVIE_FORMAT)
            movie_name_list.append(new_file_name)
        if os.path.splitext(name)[1] == SUBTITLE_FORMAT:
            subtitle_name_list.append(name)
    
    break


movie_name_list = natsort.natsorted(movie_name_list)
subtitle_name_list = natsort.natsorted(subtitle_name_list)

# 字幕重命名
if len(movie_name_list) == len(subtitle_name_list):
    for i in range(len(movie_name_list)):
        print("[Subtitle Renaming]from: ", subtitle_name_list[i], " to : ", movie_name_list[i] + SUBTITLE_FORMAT)
        os.rename(os.path.join(curr_path, subtitle_name_list[i]), os.path.join(curr_path, movie_name_list[i] + SUBTITLE_FORMAT))

