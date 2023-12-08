import os

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

#Set climb = True

# MQ fitness function, where MQ is sum of all the Modularization Factors (MF) which is the ratio of inner to outer edges within each module or group