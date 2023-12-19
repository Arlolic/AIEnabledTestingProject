from distutils.command import build
import os
import random
import hill_climbing
from operator import itemgetter


#For each MDG, get the number of nodes and weighted_connections
num_of_nodes = []
num_of_weighted_connections_list = []

#Iterate through all files in 'dataset' directory
directory = 'dataset'

bison_nodes = set()
bison_weighted_connections = []
for filename in os.scandir(directory):
    if filename.is_file():
        print(filename.path) #debugging
        print("==========") #debugging
        nodes = set()
        weighted_connections = []
        num_of_weighted_connections = 0
        
        #Need to read through all MDG files (possibly using BufferedReader)
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                info = line.split()
                nodes.add(info[0])
                nodes.add(info[1])
                if (len(info) == 3):
                    weighted_connections.append((info[0], info[1], int(info[2])))
                else:
                    weighted_connections.append((info[0], info[1], 1))
            if filename.path == 'dataset\\bison.mdg': #debugging
                for line in lines:
                    info = line.split()
                    bison_nodes.add(info[0])
                    bison_nodes.add(info[1])
                    if (len(info) == 3):
                        bison_weighted_connections.append((info[0], info[1], int(info[2])))
                    else:
                        bison_weighted_connections.append((info[0], info[1], 1))
                print(nodes)
                print(len(nodes))
                print(len(weighted_connections))
                #print(file.read())
            """
            if filename.path == 'dataset\\xntp.mdg': #debugging
                print(nodes)
                print(len(nodes))
            """
            num_of_nodes.append(len(nodes))
            num_of_weighted_connections_list.append(num_of_weighted_connections)
        print("==========") #debugging

resulting_clusterings = []
for i in range(10):
    y = hill_climbing.hill_climb(bison_weighted_connections, bison_nodes)
    resulting_clusterings.append((y, hill_climbing.fitness(y, bison_weighted_connections)))
    
sorted_clusterings = sorted(resulting_clusterings, key=itemgetter(1))

for clustering in sorted_clusterings:
    print(hill_climbing.fitness(clustering[0], bison_weighted_connections))

# keep the x% top and the clusters which are common
x = 0.1
start = (len(sorted_clusterings)-1) * (1-x)
sorted_clusterings = sorted_clusterings[int(start)::]

building_blocks = []
for cluster in sorted_clusterings[0][0]:
    exists_everywhere = True
    for (clustering, score) in sorted_clusterings:
        exists = False
        for other_cluster in clustering:
            if cluster.equals(other_cluster):
                exists = True
        if not exists:
            exists_everywhere = False
    if exists_everywhere:
        building_blocks.append(cluster)

                
for module in bison_nodes:
    exists = False
    for building_block in building_blocks:
        if module in building_block.list_of_modules:
            exists = True
    if exists == False:
        building_blocks.append(hill_climbing.Cluster(module))

for building_block in building_blocks:
    print("===========")
    for module in building_block.list_of_modules:
        print(module)