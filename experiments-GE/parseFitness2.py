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

# FITNESS 2
# list report files correspoding to seeds
reportFolder = sys.argv[2]
reportFiles = []
for s in seeds:
    reportFiles += [glob.glob(reportFolder + '/' + '*-' + s + '_MessageStatsReport*')]

# fitness names
fitnessNames = sys.argv[3:]

# fitness for each repetition
fitnesses = np.empty([len(reportFiles),len(fitnessNames)])
for i,file in enumerate(reportFiles):
    with open(file[0],'r') as f:
        lines = f.readlines()
        for l in lines:
            for j,fitness in enumerate(fitnessNames):
                if l.startswith(fitness):
                    value = float(l.split(': ')[1])
                    if fitness == 'delivery_prob':
                        value = 1-value
                    fitnesses[i][j] = value

# move report files to temp directory
for i,file in enumerate(reportFiles):
    if os.path.exists(sys.argv[1]+'/'+os.path.basename(file[0])):
        os.remove(sys.argv[1]+'/'+os.path.basename(file[0]))
    shutil.move(file[0], sys.argv[1])

meanFitness = np.mean(fitnesses,0)
string = ''
for m in meanFitness:
    string += str(m) + ' '
print string