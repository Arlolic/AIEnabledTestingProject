from distutils.command import build
import os
import random

class Cluster:
    def __init__(self, module):
        self.list_of_modules = []
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
        
    def __str__(self) -> str:
        return str(self.list_of_modules)
    
    def is_empty(self):
        if not self.list_of_modules:
            return True
        else:
            return False
    
    def equals(self, other_cluster):
        for module in self.list_of_modules:
            if module not in other_cluster.list_of_modules:
                return False
        for module in other_cluster.list_of_modules:
            if module not in self.list_of_modules:
                return False
        return True



# Below is MQ fitness function, where MQ is sum of all the Modularization Factors (MF) which is the ratio of inner to outer edges within each module or group (Evaluates 
# the fitness of the clustering)
def fitness(clusters, weighted_connections, Cluster_original = None, Cluster_new = None, module = None): #weighted_connections is a list of lists. Each sublist is a weighted connection and is of length 3 (including the weight!)
    mq = 0

    if(Cluster_original is not None and Cluster_new is not None and module is not None):
        Cluster_original.remove_module(module) # remove 'module' out of the current cluster
        Cluster_new.add_module(module) # remove 'module' out of the current cluster

    # Need to check ALL clusters
    for cluster in clusters:
        if(cluster.is_empty()):
            continue
        i = 0 #sum of inner edge weights
        j = 0 #sum of outer edge weights
        if not (type(cluster.list_of_modules[0]) is list):
            for m in cluster.list_of_modules: #Check all modules in cluster
                for wc in weighted_connections: #Check for all possible weighted connections
                    if m in wc:
                        if wc[0] in cluster.list_of_modules and wc[1] in cluster.list_of_modules: # if other module in 'wc' is in the same cluster as 'm'
                            i += wc[2] # add onto the sum of inner edge weights
                        else:
                            j += wc[2] # add onto the sum of outer edge weights
            mf = i / (i + j / 2)
            mq += mf
        else:
            megalist = []
            for block in cluster.list_of_modules:
                for module in block:
                    megalist.append(module)
            for building_block in cluster.list_of_modules: #Check all modules in cluster
                for wc in weighted_connections: #Check for all possible weighted connections
                    for m in building_block:
                        if m in wc:
                            if wc[0] in megalist and wc[1] in megalist: # if other module in 'wc' is in the same cluster as 'm'
                                i += wc[2] # add onto the sum of inner edge weights
                            else:
                                j += wc[2] # add onto the sum of outer edge weights
            mf = i / (i + j / 2)
            mq += mf

    
    if(Cluster_original is not None and Cluster_new is not None and module is not None):
        Cluster_new.remove_module(module) # remove 'module' out of the current cluster
        Cluster_original.add_module(module) # remove 'module' out of the current cluster

    return mq


#Hill climbing algorithm takes Module Dependency Graphs as input

def hill_climb(weighted_connections, modules):
    # Perform initial set of hill climbs

    #Assign each module to it's own building block (Note: A building block contains one or more modules fixed to be in a particular cluster, if and only if all the selected 
    # initial hill climbs agree that these modules were to be located within the same cluster)

    n = len(modules) # Number of modules

    list_of_clusters = []

    for m in modules:
        if(type(m) is Cluster):
            list_of_clusters = modules
            break
        list_of_clusters.append(Cluster(m)) #Assign each module to a building block 
        
    random.shuffle(list_of_clusters) #shuffle the clusters

    s_fitness = fitness(list_of_clusters, weighted_connections)
    #Building block is going to be a list (or can it be a set?)
    #list_of_clusters = [[] for x in range(n)] #This is a list comprehension. Followed this site here: https://stackoverflow.com/questions/13520876/how-can-i-make-multiple-empty-lists-in-python

    #***"The nearest neighbours from each clustering are formed by moving a single module from one building block to another building block"***

    #Larger edge weights indicate more dependency between modules and an increase in the likely hood that they should be placed in the same cluster

    #Set climb = True (?)

    
    search_ends = True

    while search_ends: #Random Ascent Hill Climbing Algorithm
        for cluster in list_of_clusters: #check each building block
            for module in cluster.list_of_modules: #check each module
                for cluster2 in list_of_clusters: #move the clustering
                    if not cluster2.contains(module):
                        n_fitness = fitness(list_of_clusters, weighted_connections, cluster, cluster2, module) #Then calculate MQ
                        if n_fitness > s_fitness:
                            cluster2.add_module(module) #Do the clustering
                            s_fitness = n_fitness
                            cluster.remove_module(module)
                            search_ends = False
                            break

    # remove any empty lists in list_of_clusters
    list_of_clusters = [cluster for cluster in list_of_clusters if cluster.is_empty() == False]

    s_fitness = fitness(list_of_clusters, weighted_connections)
    return list_of_clusters
    # Need to identify common features of each solution in best hill climb to form building blocks for subsequent hill climb

    # Perform final set of hill climbs, identical to that of initial set of hill climbs
    #while True:
        #TODO
        #Should fine new peaks using the building blocks, which are used as nodes here
