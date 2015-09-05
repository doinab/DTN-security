# replace the seed and attacker file into the settings file of The ONE

import sys
import time

def addPedestrianFlooder(index,protocol):
    attackConfigs = '# PEDESTRIAN FLOOD attacker specific settings' + '\n' + \
                    'Group' + str(index) + '.groupID = PF' + '\n' + \
                    'Group' + str(index) + '.router = ' + protocol + '\n' + \
                    'Group' + str(index) + '.okMaps = 1' + '\n' + \
                    'Group' + str(index) + '.bufferSize = 5M' + '\n' + \
                    'Group' + str(index) + '.speed = 0.5, 1.5' + '\n' + \
                    'Group' + str(index) + '.nrofHosts = 1' + '\n' + \
                    'Group' + str(index) + '.nrofInterfaces = 1' + '\n' + \
                    'Group' + str(index) + '.interface1 = btInterface'
    return attackConfigs

def addVehicleFlooder(index,protocol):
    attackConfigs = '# VEHICLE FLOOD attacker specific settings' + '\n' + \
                    'Group' + str(index) + '.groupID = VF' + '\n' + \
                    'Group' + str(index) + '.router = ' + protocol + '\n' + \
                    'Group' + str(index) + '.okMaps = 2' + '\n' + \
                    'Group' + str(index) + '.bufferSize = 50M' + '\n' + \
                    'Group' + str(index) + '.speed = 2.7, 13.9' + '\n' + \
                    'Group' + str(index) + '.nrofHosts = 1' + '\n' + \
                    'Group' + str(index) + '.nrofInterfaces = 2' + '\n' + \
                    'Group' + str(index) + '.interface1 = btInterface' + '\n' + \
                    'Group' + str(index) + '.interface2 = highspeedInterface'
    return attackConfigs

def addPedestrianBlackHole(index):
    attackConfigs = '# PEDESTRIAN BLACKHOLE attacker specific settings' + '\n' + \
                    'Group' + str(index) + '.groupID = PB' + '\n' + \
                    'Group' + str(index) + '.router = PassiveRouter' + '\n' + \
                    'Group' + str(index) + '.okMaps = 1' + '\n' + \
                    'Group' + str(index) + '.bufferSize = 5M' + '\n' + \
                    'Group' + str(index) + '.speed = 0.5, 1.5' + '\n' + \
                    'Group' + str(index) + '.nrofHosts = 1' + '\n' + \
                    'Group' + str(index) + '.nrofInterfaces = 1' + '\n' + \
                    'Group' + str(index) + '.interface1 = btInterface'
    return attackConfigs

def addVehicleBlackHole(index):
    attackConfigs = '# VEHICLE BLACKHOLE attacker specific settings' + '\n' + \
                    'Group' + str(index) + '.groupID = VB' + '\n' + \
                    'Group' + str(index) + '.router = PassiveRouter' + '\n' + \
                    'Group' + str(index) + '.okMaps = 2' + '\n' + \
                    'Group' + str(index) + '.bufferSize = 50M' + '\n' + \
                    'Group' + str(index) + '.speed = 2.7, 13.9' + '\n' + \
                    'Group' + str(index) + '.nrofHosts = 1' + '\n' + \
                    'Group' + str(index) + '.nrofInterfaces = 2' + '\n' + \
                    'Group' + str(index) + '.interface1 = btInterface' + '\n' + \
                    'Group' + str(index) + '.interface2 = highspeedInterface'
    return attackConfigs

# city name
cityname = sys.argv[1]

# parse template configuration file
optionsfname = sys.argv[2]
f = open(optionsfname,'r')
options = f.readlines()
f.close()

# number of attackers of both kinds/attack
nrhumanattackers = 0
nrvehicleattackers = 0
nrfloodattackers = 0
nrblackholeattackers = 0

# parse input individual file
individualfname = sys.argv[3]
f = open(individualfname,'r')
types = []
attackers = []
content = f.readlines()

for c in content:
    c = c[:-1]
    if c.startswith('Type'):
        type_i = c.split('=')[1]
        types += [type_i]
        if type_i == 'pedestrian':
            nrhumanattackers = nrhumanattackers+1
        elif type_i == 'vehicle':
            nrvehicleattackers = nrvehicleattackers+1
    elif c.startswith('Attacker'):
        attacker_i = c.split('=')[1]
        attackers += [attacker_i]
        if attacker_i == 'flooder':
            nrfloodattackers = nrfloodattackers+1
        elif attacker_i == 'black_hole':
            nrblackholeattackers = nrblackholeattackers+1
f.close()

# sort the attacker vector to put the flooders at the end
temp = [(v,i) for i,v in enumerate(attackers)]
temp.sort()
temp, indices = zip(*temp)

nrattackers=len(types)

# parse number of seeds used for repeated simulation
nseeds = int(sys.argv[4])

# parse individual repetition simulation duration
endTime = int(sys.argv[5])

# variable numbers of attackers
poishumanattackers = ['Group3.pois', 'Group4.pois', 'Group5.pois', 'Group6.pois']
poisvehicleattackers = ['Group7.pois', 'Group8.pois', 'Group9.pois', 'Group10.pois']

newoptions = []

for option in options:
    if option.startswith('MovementModel.rngSeed'):
        originalseeds = option.split(' = ')[1]
        seeds = originalseeds[1:-2].split('; ')
        newseeds = ''
        k = 0
        for s in range(nseeds):
            seed = seeds[s]
            if k == 0:
                # get the base seed (depending on individual id)
                individualid = individualfname[10:-4]
                baseseed=''
                for c in individualid:
                    baseseed += str(ord(c))
                baseseed = int(time.time()) + int(baseseed) + (int(baseseed)-ord('A'))*nseeds
            # shift the k-th repetition seed
            newseeds += str(baseseed+int(s))
            if k < nseeds-1:
                newseeds += '; '
            k += 1
        newseeds = '[' + newseeds + ']\n'
        print newseeds
        option = option.replace(originalseeds,newseeds)

    elif option.startswith('Scenario.endTime'):
        originalTime = option.split(' = ')[1]
        option = option.replace(originalTime,str(endTime))

    elif option.startswith('Scenario.nrofHostGroups'):
        originalnrofhostgroups = option.split(' = ')[1]
        newnrofhostgroups = int(originalnrofhostgroups)+nrattackers
        option = option.replace('= ' + originalnrofhostgroups,'= ' + str(newnrofhostgroups))

    elif option.startswith('Group1.router'):
        protocol = option[:-1].split(' = ')[1]

    elif option.startswith('Group1.nrofHosts'):
        originalnrhumanhonest = option[:-1].split(' = ')[1]
        newnrhumanhonest = int(originalnrhumanhonest)-nrhumanattackers
        option = option.replace('= ' + originalnrhumanhonest,'= ' + str(newnrhumanhonest))

    elif option.startswith('Group2.nrofHosts'):
        originalnrvehiclehonest = option[:-1].split(' = ')[1]
        newnrvehiclehonest = int(originalnrvehiclehonest)-nrvehicleattackers
        option = option.replace('= ' + originalnrvehiclehonest,'= ' + str(newnrvehiclehonest))

    elif option.startswith('Events1.hosts'):
        events = option[:-1].split(' = ')[1]
        originalnrevents = events.split(',')[1]
        newnrevents = int(originalnrevents)-nrattackers
        option = option.replace(',' + originalnrevents,',' + str(newnrevents))

    elif option.startswith('Events2.tohosts'):
        if nrfloodattackers == 0:
            option = 'Events2.tohosts = 0,0\n'
        else:
            events = option[:-1].split(' = ')[1]
            originalnrevents = events.split(',')[1]
            newnrevents = int(originalnrevents)-nrattackers
            option = option.replace(',' + originalnrevents,',' + str(newnrevents))

    elif option.startswith('Events2.hosts'):
        if nrfloodattackers == 0:
            option = 'Events2.hosts = 1,1\n'
        else:
            events = option[:-1].split(' = ')[1]
            originalnrevents = events.split(',')[0]
            newnrevents = int(originalnrevents)-nrfloodattackers
            option = option.replace(originalnrevents + ',',str(newnrevents) + ',')
            originalnrevents = events.split(',')[1]
            newnrevents = int(originalnrevents)
            option = option.replace(',' + originalnrevents,',' + str(newnrevents))

    #Events1.hosts = 0,no nodes minus no of all attackers
    #Events2.tohosts = 0,no nodes minus no of all attackers
    #Events2.hosts = no nodes minus no of flooders, no nodes

    elif option.startswith('#ATTACKERS'):
        attackerstring = ''
        for i in range(nrattackers):
            index = indices[i]
            if types[index] == 'pedestrian':
                if attackers[index] == 'flooder':
                    attackerstring += addPedestrianFlooder(3+i,protocol) + '\n'
                elif attackers[index] == 'black_hole':
                    attackerstring += addPedestrianBlackHole(3+i) + '\n'
            elif types[index] == 'vehicle':
                if attackers[index] == 'flooder':
                    attackerstring += addVehicleFlooder(3+i,protocol) + '\n'
                elif attackers[index] == 'black_hole':
                    attackerstring += addVehicleBlackHole(3+i) + '\n'
        option = attackerstring

    elif option.startswith('#POIS'):
        pois = ''
        for i in range(nrattackers):
            index = indices[i]
            individualwktfile=individualfname.replace('.txt','_'+types[index]+'_'+attackers[index]+'_'+str(index)+'.wkt')
            pois += 'PointsOfInterest.poiFile' + str(3+i) + ' = data/' + individualwktfile + '\n'
        option = pois

    elif option.startswith('#PROBABILITIES'):
        probabilities = ''
        for i in range(nrattackers):
            probabilities += 'Group' + str(3+i) + '.pois = ' + str(3+i) + ',1' + '\n'
        option = probabilities
    
    if nrfloodattackers == 0:
        if option.startswith('Events2'):
            option = option.replace('Events2','#Events2')
        elif option.startswith('Events.nrof'):
            originalnrevents = option[:-1].split(' = ')[1]
            newnrevents = int(originalnrevents)-1
            option = option.replace('= ' + originalnrevents,'= ' + str(newnrevents))

    newoptions += [option]

# replace transmit range (and speed) in the settings file
optionsindfname = optionsfname.replace('.txt','') + '_' + individualfname

# print to file
f = open(optionsindfname,'w')
f.writelines(newoptions)
f.close()
