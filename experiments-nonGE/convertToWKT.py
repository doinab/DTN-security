# convert an n-attacker POIs list generated by uGP into n WKT files

import sys
import random
import pickle

sortAndRemoveDuplicates = False

# city name
cityname = sys.argv[1]

# parse input individual file
fname = sys.argv[2]
types = []
attackers = []
coordinates = []
with open(fname) as f:
    content = f.readlines()
    for c in content:
        c = c[:-1]
        if c.startswith('Type'):
            type_i = c.split('=')[1]
            types += [type_i]
            coordinates_i = []
            coordinates += [coordinates_i]
        elif c.startswith('Attacker'):
            attacker_i = c.split('=')[1]
            attackers += [attacker_i]
        else:
            if c:
                coordinates[-1] += [c]
    f.close()

for ind in range(len(types)):
    type_i = types[ind]
    attacker_i = attackers[ind]
    coordinates_i = coordinates[ind]

    # convert it into a LINESTRING
    ncoordinates = len(coordinates_i)
    n = 0
    string = 'LINESTRING ('
    for c in coordinates_i:
        coord = c.replace(',',' ')
        
        if n == 0:
            if type_i == 'pedestrian' or type_i == 'vehicle':
                picklefile = cityname + '-' + type_i + '-points-uniq-sorted_mapping.pickle'
            else:
                sys.exit('ERROR: Unknown type of attacker!')
            
            d = pickle.load(open(picklefile,'r'))

        ij = coord.split(' ')
        i = int(ij[0])
        j = int(ij[1])
        nPOIincell = len(d[i][j])
        if nPOIincell == 0:
            coord = 'INVALID_POI'
        elif nPOIincell == 1:
            coord = str(d[i][j][0][0]) + ' ' + str(d[i][j][0][1])
        else:
            '''
            # pick a random POI in the grid cell
            r = random.randint(0, nPOIincell-1)
            coord = str(d[i][j][r][0]) + ' ' + str(d[i][j][r][1])
            '''
            # visit all POIs in the grid cell
            coord = ''
            for k in range(nPOIincell):
                coord += str(d[i][j][k][0]) + ' ' + str(d[i][j][k][1])
                if k < nPOIincell-1:
                    coord += ', '

        string += coord
        if n < ncoordinates-1:
            string += ', '
        n += 1
    string += ')'

    # convert the LINESTRING to a list of POINTs
    points = string[12:-1].split(', ')
    # (optional) sort and remove duplicate POINTs
    if sortAndRemoveDuplicates:
        points = list(set(points))
        points.sort()
    string = ''
    for p in points:
        string += 'POINT (' + p + ')' + '\n'

    # write it to a WKT file
    outputfile = fname.replace('.txt','_'+type_i+'_'+attacker_i+'_'+str(ind)+'.wkt')
    with open(outputfile, 'w') as f:
        f.write(string)
        f.close()