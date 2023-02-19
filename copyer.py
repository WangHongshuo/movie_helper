
from fileinput import filename
import os
import sys
import shutil

HELP_INFO = '''"-sp=[Src Path]", "-dp=[Dst Path]", "-ms=[Matching String]"'''

if len(sys.argv) <= 1:
        print(HELP_INFO)
        exit()

src_path = str()
dst_path = str()
match_str = str()

for i in range(1, len(sys.argv)):
    if sys.argv[i].startswith("-sp="):
        src_path = sys.argv[i].removeprefix("-sp=")
    elif sys.argv[i].startswith("-dp="):
        dst_path = sys.argv[i].removeprefix("-dp=")
    elif sys.argv[i].startswith("-ms="):
        match_str = sys.argv[i].removeprefix("-ms=")
    else:
        print("unsupport argv:" + sys.argv[i])
        print(HELP_INFO)
        exit()

# 过滤器
SUBTITLE_FORMAT = ".ass"
cnt = 0
# 字幕复制
for root, dirs, files in os.walk(src_path, topdown=True):
    for name in files:
        if (os.path.splitext(name)[1] == SUBTITLE_FORMAT) and (name.find(match_str) != -1):
            src_file_path = os.path.join(root, name)
            print(src_file_path)
            cnt = cnt + 1
            shutil.copy(src_file_path, dst_path)
    
    break

print("Total: ", cnt)
