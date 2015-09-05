import os
import sys
import math
import numpy as np
import glob
import shutil

# parse seeds file
seedsfname = sys.argv[1] + '/seeds.txt'
f = open(seedsfname,'r')
seeds = f.readline()
seeds = seeds[1:-2]
seeds = seeds.split('; ')
f.close()

# FITNESS1
# list report files correspoding to seeds
reportFolder = sys.argv[2]
reportFiles = []
for s in seeds:
    reportFiles += [glob.glob(reportFolder + '/' + '*-' + s + '_DeliveredMessagesReport*')]

# move report files to temp directory sys.argv[1]
for i,file in enumerate(reportFiles):
    if os.path.exists(sys.argv[1]+'/'+os.path.basename(file[0])):
        os.remove(sys.argv[1]+'/'+os.path.basename(file[0]))
    shutil.move(file[0], sys.argv[1])
