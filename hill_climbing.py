import os
import random

#For each MDG, get the number of nodes and edges
num_of_nodes = []
num_of_edges_list = []

#Iterate through all files in 'dataset' directory
directory = 'dataset'

for filename in os.scandir(directory):
    if filename.is_file():
        print(filename.path) #debugging
        print("==========") #debugging
        nodes = set()
        num_of_edges = 0
        #Need to read through all MDG files (possibly using BufferedReader)
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                info = line.split()
                nodes.add(info[0])
                nodes.add(info[1])
                num_of_edges += 1
            if filename.path == 'dataset\\bison.mdg': #debugging
                print(nodes)
                print(len(nodes))
                print(num_of_edges)
                #print(file.read())
            """
            if filename.path == 'dataset\\xntp.mdg': #debugging
                print(nodes)
                print(len(nodes))
            """
            num_of_nodes.append(len(nodes))
            num_of_edges_list.append(num_of_edges)
        print("==========") #debugging

print(num_of_nodes) #The number of nodes for the bitchx, exim and lynx mdgs are different than the ones in the authors' results
print(num_of_edges_list) #The number of edges for the 'bunch' (364) and the 'bunchall' (1339) mdgs are different than the authors' results

#===============================================================

#Hill climbing algorithm takes Module Dependency Graphs as input

def hill_climb(weighted_connections, modules, num_of_modules):
    # Perform initial set of hill climbs

    #Assign each module to a building block (Note: A building block contains one or more modules fixed to be in a particular cluster, if and only if all the selected 
    # initial hill climbs agree that these modules were to be located within the same cluster)

    n = random.randint(1, num_of_modules)

    #Building block is going to be a list (or can it be a set?)
    list_of_building_blocks = [[] for x in range(n)] #Followed this site here: https://stackoverflow.com/questions/13520876/how-can-i-make-multiple-empty-lists-in-python

    for x in range(num_of_modules):
        #Assign each module to a building block


    #Larger edge weights indicate more dependency between modules and an increase in the likely hood that they should be placed in the same cluster

    #Set climb = True

        # MQ fitness function, where MQ is sum of all the Modularization Factors (MF) which is the ratio of inner to outer edges within each module or group (Evaluate the
        # fitness of the clustering)

        # Search ends when none of the nearest neighbours from a clustering can yield a better MQ value

    # Need to identify common features of each solution in best hill climb to form building blocks for subsequent hill climb

    # Perform final set of hill climbs, identical to that of initial set of hill climbs