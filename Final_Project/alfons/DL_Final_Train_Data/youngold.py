from os import listdir
from os.path import isfile, isdir, join
import re
import shutil
old = "old_face/"
young = "young_face/"
for count in range(0,20):
    oldc = 0
    youc = 0
    path = str(count).zfill(2)
    files = listdir(path)
    for f in files:
        parse = re.split('_|-|.jpg', f)
        if len(parse) < 6:
            continue
        if (int(parse[5]) - int(parse[2]) >= 65) and oldc < 100:
            shutil.copy2(path + "/" + f, old)
            oldc+=1
        elif (int(parse[5]) - int(parse[2]) <= 30) and youc < 100:
            shutil.copy2(path + "/" + f, young)
            youc+=1
