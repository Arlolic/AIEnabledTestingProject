from distutils.command import build
import os
import random

class Building_Block:
    
    list_of_modules = []

    def __init__(self, module):
        self.list_of_modules.append(module)

    def add_module(self, module): #Method for adding module onto building block
        self.list_of_modules.append(module)
    
    def remove_module(self, module): #Method for removing module from list_of_modules
        self.list_of_modules.remove(module)

    def contains(self, module): #Method that checks if Building Block already contains a module
        if module in self.list_of_modules:
            return True
        else:
            return False
        
    def is_empty(self):
        if not self.list_of_modules:
            return True
        else:
            return False

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

def hill_climb(weighted_connections, modules):
    # Perform initial set of hill climbs

    #Assign each module to it's own building block (Note: A building block contains one or more modules fixed to be in a particular cluster, if and only if all the selected 
    # initial hill climbs agree that these modules were to be located within the same cluster)

    n = len(modules) # Number of modules

    list_of_building_blocks = []

    for m in modules:
        list_of_building_blocks.append(Building_Block(m)) #Assign each module to a building block

    s = list_of_building_blocks
    s_fitness = fitness(list_of_building_blocks, weighted_connections)

    #Building block is going to be a list (or can it be a set?)
    #list_of_building_blocks = [[] for x in range(n)] #This is a list comprehension. Followed this site here: https://stackoverflow.com/questions/13520876/how-can-i-make-multiple-empty-lists-in-python

    #***"The nearest neighbours from each clustering are formed by moving a single module from one building block to another building block"***

    #Larger edge weights indicate more dependency between modules and an increase in the likely hood that they should be placed in the same cluster

    #Set climb = True (?)

    while True: #Random Ascent Hill Climbing Algorithm
        for bb in list_of_building_blocks: #check each building block
            #list_of_modules_to_remove = []
            for m in bb.list_of_modules: #check each module
                bb_contains_m = False
                search_ends = True
                for bb2 in list_of_building_blocks: #move the clustering
                    if not bb2.contains(m):
                        n_fitness = fitness(list_of_building_blocks, weighted_connections, bb2, m) #Then calculate MQ
                        if n_fitness > s_fitness:
                            bb2.add_module(m) #Do the clustering
                            s = list_of_building_blocks
                            s_fitness = n_fitness
                            #list_of_modules_to_remove.append(m)
                            bb_contains_m = True
                            search_ends = False
                if bb_contains_m: #TODO: Remove any modules from bb if necessary
                    bb.remove_module(m)

                if search_ends: # Search ends when none of the nearest neighbours from a clustering can yield a better MQ value
                    break #Used this as a reference: https://note.nkmk.me/en/python-break-nested-loops/
            else:
                continue
            break
        else:
            continue
        break

    # remove any empty lists in list_of_building_blocks
    s = [bb for bb in s if bb.is_empty() == False]

    # Need to identify common features of each solution in best hill climb to form building blocks for subsequent hill climb

    # Perform final set of hill climbs, identical to that of initial set of hill climbs
    while True:
        #TODO

        #Should fine new peaks using the building blocks, which are used as nodes here

# Below is MQ fitness function, where MQ is sum of all the Modularization Factors (MF) which is the ratio of inner to outer edges within each module or group (Evaluates 
# the fitness of the clustering)
def fitness(clusters, weighted_connections, building_block, module): #weighted_connections is a list of lists. Each sublist is a weighted connection and is of length 3 (including the weight!)
    mq = 0

    bb_module = building_block.list_of_modules[0]
    
    for c in clusters:
        if c.contains(module):
            c.remove_module(module) # remove 'module' out of the current cluster

    clusters = [c for c in clusters if c.is_empty() == False] #TODO: remove any empty building blocks

    for c in clusters:
        if c.contains(bb_module): # if c.list_of_modules contains bb_module
            c.add_module(module)

    # Need to check ALL clusters
    for c in clusters:
        i = 0 #sum of inner edge weights
        j = 0 #sum of outer edge weights
        for m in c.list_of_modules: #Check all modules in cluster
            for wc in weighted_connections: #Check for all possible weighted connections
                if m in wc:
                    if wc[0] in c.list_of_modules and wc[1] in c.list_of_modules: # if other module in 'wc' is in the same cluster as 'm'
                        i += wc[2] # add onto the sum of inner edge weights
                    else:
                        j += wc[2] # add onto the sum of outer edge weights
        mf = i / (i + j / 2)
        mq += mf
    
    return mq