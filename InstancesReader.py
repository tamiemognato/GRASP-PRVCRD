
import os
import re


def insert_solutution_in_the_dictionary(parameter):
    filekeep = open(parameter, "r")
    contentkeep = filekeep.readlines() #Guardar o conteúdo do arquivo da instância em uma lista
    input = parameter
    filekeep.close()
    contentkeep1 = contentkeep[0]

    # Avalie o conteúdo do arquivo como uma expressão Python
    dic_solution = eval(contentkeep1)
    if dic_solution['TYPE'] == 'CRVP':
        dic_solution['SAFETY_STOCK'] = ""
        dic_solution['MAXTIME'] = ""

    return dic_solution


def insert_instance_in_the_dictionary(parameter):
    # This function reads the instance input file in and fills, variable by variable, the dic_instance defined in "DictionaryDefinition.py".

    # PARAMETERS

    # name = string
    # dimension = integer
    # capacity = integer
    # distance = float
    # node_coord = []
    # demand = []

    maxtime = -1   #CMT instances
    node_coord = []
    demand = []

    filekeep = open(parameter, "r")
    contentkeep = filekeep.readlines()  #Guardar o conteúdo do arquivo da instância em uma lista
    input = parameter
    filekeep.close()
    # print(contentkeep)

    maincount = 0
    while maincount < len(contentkeep):     #Loop for read all the lines of the file

        if contentkeep[maincount].startswith("NAME"):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" : ")
            mainlistaux = mainlistaux[1].split("\n")
            name = mainlistaux[0]

            # print(name)
            # print(type(name))

        if contentkeep[maincount].startswith("DIMENSION"):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" : ")
            mainlistaux = mainlistaux[1].split("\n")
            dimension = int(mainlistaux[0])

            # print(dimension)
            # print(type(dimension))

        if contentkeep[maincount].startswith("CAPACITY"):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" : ")
            mainlistaux = mainlistaux[1].split("\n")
            capacity = int(mainlistaux[0])

            # print(capacity)
            # print(type(capacity))

        if contentkeep[maincount].startswith("DISTANCE"):
            mainaux = contentkeep[maincount]
            mainlistaux = mainaux.split(" : ")
            mainlistaux = mainlistaux[1].split("\n")
            maxtime = float(mainlistaux[0])

            # print(distance)
            # print(type(distance))

        if contentkeep[maincount].startswith("NODE_COORD_SECTION\n"):
            auxcount = maincount + 1
            while auxcount <= (maincount + dimension):
                mainaux = contentkeep[auxcount]
                mainlistaux = mainaux.split(" ")
                secondlistaux = mainlistaux[2].split("\n")
                auxtuple = (float(mainlistaux[1]), float(secondlistaux[0]))
                node_coord.append(auxtuple)
                auxcount = auxcount + 1

            # print(node_coord)
            # print(type(node_coord))
            # print(len(node_coord))
            # print(type(node_coord[0]))
            # print(type(node_coord[0][0]))

        if contentkeep[maincount].startswith("DEMAND_SECTION\n"):
            auxcount = maincount + 1
            while auxcount <= (maincount + dimension):
                mainaux = contentkeep[auxcount]
                mainlistaux = mainaux.split(" ")
                secondlistaux = mainlistaux[1].split("\n")
                demand.append(int(secondlistaux[0]))
                auxcount = auxcount + 1

            # print(demand)
            # print(type(demand))
            # print(len(demand))
            # print(type(demand[0]))

        maincount = maincount + 1


    dic_instance = {
        'NAME'          : name,             # string                         # Identifies the data file
        'DIMENSION'     : dimension,        # int                            # Total number of nodes and depots
        'CAPACITY'      : capacity,         # int                            # Specifies the vehicle capacity in a CVRP
        'MAXTIME'       : maxtime,          # float                          # A maximum distance per route -> i.e. A maximum travel time per route
        'NODE_COORD'    : node_coord,       # list[tuple (float, float)]     # Coordinates
        'DEMAND'        : demand,           # list [integer]                 # Demands
                   }

    # print(dic_instance)

    return dic_instance
