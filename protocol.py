from distutils.command import build
import os
import random
import hill_climbing


#For each MDG, get the number of nodes and weighted_connections
num_of_nodes = []
num_of_weighted_connections_list = []

#Iterate through all files in 'dataset' directory
directory = 'dataset'

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

print(num_of_nodes) #The number of nodes for the bitchx, exim and lynx mdgs are different than the ones in the authors' results
print(num_of_weighted_connections_list) #The number of weighted_connections for the 'bunch' (364) and the 'bunchall' (1339) mdgs are different than the authors' results

hill_climbing.hill_climb(weighted_connections, nodes)