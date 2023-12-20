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
for i in range(20):
    y = hill_climbing.hill_climb(bison_weighted_connections, bison_nodes)
    resulting_clusterings.append((y, hill_climbing.fitness(y, bison_weighted_connections)))
    

final_clustering = []
print("==========") #debugging
print("==========") #debugging
print("==========") #debugging
for x in range(0, 101, 10):
    print("Testing for the top {0} %".format(x))
    sorted_clusterings = sorted(resulting_clusterings, key=itemgetter(1))

    #for clustering in sorted_clusterings:
        #print(clustering[1])

    # keep the x% top and the clusters which are common
    start = (len(sorted_clusterings)-1) * (100-x)/100
    sorted_clusterings = sorted_clusterings[int(start)::]

    building_blocks = []
    used_modules = []
    for cluster in sorted_clusterings[0][0]:
        for module in cluster.list_of_modules:
            if module not in used_modules:
                used_modules.append(module)
                building_blocks.append(hill_climbing.Cluster(module))
                for other_module in cluster.list_of_modules:
                    together_in_all_clusterings = True
                    for (clustering, score) in sorted_clusterings:
                        are_together = False
                        for other_cluster in clustering:
                            if other_module in other_cluster.list_of_modules: 
                                are_together = True
                                for presentcluster in building_blocks[-1].list_of_modules:
                                    if presentcluster not in other_cluster.list_of_modules:
                                        are_together = False
                                        break
                        if not are_together:
                            together_in_all_clusterings = False
                            break
                    if together_in_all_clusterings:
                        if other_module not in used_modules:
                            building_blocks[-1].add_module(other_module)
                            used_modules.append(other_module)
                

    #add any missed modules
    for module in bison_nodes:
        exists = False
        for building_block in building_blocks:
            if module in building_block.list_of_modules:
                exists = True
        if exists == False:
            building_blocks.append(hill_climbing.Cluster(module))

    print("Resulting clusters")
    for building_block in building_blocks:
        if len(building_block.list_of_modules)>1:
            print("----------")
            for module in building_block.list_of_modules:
                print(module)
    
    y = hill_climbing.hill_climb(bison_weighted_connections, building_blocks)
    final_clustering.append((y, hill_climbing.fitness(y, bison_weighted_connections)))
    
    print(final_clustering[-1][1])

    print()
    

print("Average MQ of initial hill climbs:")
avg = 0
for clustering in sorted_clusterings:
    avg += clustering[1]
avg = avg/len(sorted_clusterings)
print (avg)

print("Best MQ of initial hill climbs:")
print(sorted_clusterings[-1][1])

