#!/usr/bin/python

import argparse
import glob
import os
import sys
from datetime import datetime
from pathlib import Path

import yaml
from pymongo import MongoClient

__author__ = 'chepe'


# log.Info(" ||| " + myIP.String() + " ||| RemoveFromList ||| " + payload.Source.String() + " ||| ")

def createDictionaryFromFile(filepath):
    REMOVE_FROM_LIST = " ||| RemoveFromList ||| "
    dictionaryT = dict()

    # iterate for each file path in the list
    for fp in filepath:
        with open(fp, 'r') as f:
            for line in f:
                if REMOVE_FROM_LIST in line:
                    values = line.split(" ||| ")
                    parentNode = values[1].strip()
                    childNode = values[3].strip()

                    if parentNode not in dictionaryT:
                        dictionaryT[parentNode] = list()

                    dictionaryT[parentNode].append(childNode)

    return dictionaryT


def recursionDictionary(dict, node, result):
    if node in dict:
        for item in dict[node]:
            recursionDictionary(dict, item, result)
            result[item] = 1

    result[node] = 1


###############################################################################
# main
###############################################################################

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str,
                        help="The number of nodes of the simulation")
    parser.add_argument("nodes", type=int,
                        help="The number of nodes of the simulation")
    parser.add_argument("time", type=int,
                        help="The time of the simulation")
    parser.add_argument("timeout", type=int,
                        help="The timeout of the simulation")
    parser.add_argument("size", type=int,
                        help="The size of the network in the simulation")
    parser.add_argument("-ns", "--nodespeed", action="store",
                        help="The speed of the nodes expressed in m/s")
    parser.add_argument("-np", "--nodepause", action="store",
                        help="The pause of the nodes expressed in s")
    args = parser.parse_args()

    ###############################################################################
    # First we read all logs, collecting the important values
    ###############################################################################

    print("Reading log files ...")

    # Set folder:
    folder = "/home/ubuntu/tap/var/log/"

    # Get filepaths for all files which end with ".txt" and start with "travel_times_to_ 59721":
    filepaths = glob.glob(os.path.join(folder, '**/*.log'), recursive=True)

    filepathsT1 = glob.glob(os.path.join(folder, '**/treesip10001.log'), recursive=True)
    filepathsT2 = glob.glob(os.path.join(folder, '**/treesip10002.log'), recursive=True)

    # log constants
    RESULT_STRING = " RESULT="
    CONVERGENCE_TIME_STRING = " CONVERGENCE_TIME="
    LEVEL_STRING = " LEVEL="
    SIZE_STRING = " MESSAGE_SIZE="
    SENT_STRING = " SENDING_MESSAGE="
    SENT_I_STRING = " INTERNAL_MESSAGE="
    ROUTE_STRING = " SUCCESS_ROUTE="
    AUTOMATA_TIME = " ATTEND_BUFFER_CHANNEL_START_TIME="

    # variables
    computation = 0
    convergence = 0
    computation2 = 0
    convergence2 = 0
    level = 0
    size = 0
    sent = 0
    internal = 0
    routed = 0
    automata = 0
    automataC = 0

    nodeSpeed = 0
    nodePause = 0
    if args.nodespeed:
        nodeSpeed = int(args.nodespeed)
    if args.nodepause:
        nodePause = int(args.nodepause)

    rootNode1 = folder + "emu1/treesip10001.log"
    rootNode2 = folder + "emu10/treesip10002.log"

    node1Path = Path(rootNode1)
    if node1Path.is_file():
        with open(rootNode1, 'r') as f:
            for line in f:
                if RESULT_STRING in line:
                    computation = int(line.split(RESULT_STRING)[1].rstrip())
                elif CONVERGENCE_TIME_STRING in line:
                    convergence = int(line.split(CONVERGENCE_TIME_STRING)[1].rstrip())

    node2Path = Path(rootNode2)
    if node2Path.is_file():
        with open(rootNode2, 'r') as f:
            for line in f:
                if RESULT_STRING in line:
                    computation2 = int(line.split(RESULT_STRING)[1].rstrip())
                elif CONVERGENCE_TIME_STRING in line:
                    convergence2 = int(line.split(CONVERGENCE_TIME_STRING)[1].rstrip())

    # iterate for each file path in the list
    for fp in filepaths:
        # Open the file in read mode
        with open(fp, 'r') as f:
            for line in f:
                if LEVEL_STRING in line:
                    levelTmp = int(line.split(LEVEL_STRING)[1].rstrip())
                    if level < levelTmp:
                        level = levelTmp
                elif SIZE_STRING in line:
                    size += int(line.split(SIZE_STRING)[1].rstrip())
                elif SENT_STRING in line:
                    sent += int(line.split(SENT_STRING)[1].rstrip())
                elif SENT_I_STRING in line:
                    internal += int(line.split(SENT_I_STRING)[1].rstrip())
                elif ROUTE_STRING in line:
                    routed += int(line.split(ROUTE_STRING)[1].rstrip())
                elif AUTOMATA_TIME in line:
                    automata += int(line.split(AUTOMATA_TIME)[1].rstrip())
                    automataC += 1

    automata = int(automata/automataC)

    # log.Info(" ||| " + myIP.String() + " ||| RemoveFromList ||| " + payload.Source.String() + " ||| ")

    dictionaryT1 = createDictionaryFromFile(filepathsT1)
    dictionaryT2 = createDictionaryFromFile(filepathsT2)

    print("This is dictionaryT1 ...")
    for keys, values in dictionaryT1.items():
        print(keys)
        print(values)

    print("This is dictionaryT2 ...")
    for keys, values in dictionaryT2.items():
        print(keys)
        print(values)

    resultingMapOverall = dict()

    resultingMap1 = dict()
    recursionDictionary( dictionaryT1, '10.12.0.1', resultingMap1 )
    lengthMap1 = len( resultingMap1.items() )

    print("This is resultingMap1 ...")
    for keys, values in resultingMap1.items():
        print(keys)
        resultingMapOverall[keys] = 1

    resultingMap2 = dict()
    recursionDictionary( dictionaryT2, '10.12.0.10', resultingMap2 )
    lengthMap2 = len( resultingMap2.items() )

    print("This is resultingMap2 ...")
    for keys, values in resultingMap2.items():
        print(keys)
        resultingMapOverall[keys] = 1

    lengthMapOverall = len(resultingMapOverall.items())



    ###############################################################################
    # Then we connect to MongoDB and store the values
    ###############################################################################

    print("Loading config.yml ...")
    with open('config.yml', 'r') as f:
        doc = yaml.load(f)

    host = '54.186.74.114'
    port = 27017
    user = 'username'
    pasw = 'password'

    if 'parameters' in doc:
        if 'host' in doc['parameters']:
            host = doc['parameters']['host']
        if 'port' in doc['parameters']:
            port = doc['parameters']['port']
        if 'user' in doc['parameters']:
            user = doc['parameters']['user']
        if 'pasw' in doc['parameters']:
            pasw = doc['parameters']['pasw']

    print("Connecting to mongo ...")
    connection = MongoClient(host, port)
    connection.admin.authenticate(user, pasw, mechanism='SCRAM-SHA-1')
    print("Connected to mongo ...")

    # connect to the treesip database and the testcases collection
    db = connection.treesip.testcases

    # create dictionary and place values in dictionary
    record = {
        'computation': int(computation),
        'convergence': int(convergence),
        'computation2': int(computation2),
        'convergence2': int(convergence2),
        'maxlevel': int(level),

        'name': args.name,
        'nodes': int(args.nodes),
        'duration': int(args.time),
        'timeout': int(args.timeout),
        'size': int(args.size),
        'node_speed': int(nodeSpeed),
        'node_pause': int(nodePause),

        'msg_size': int(size),
        'msg_sent': int(sent),
        'msg_internal': int(internal),
        'msg_routed': int(routed),

        'automata': int(automata),

        'length_map1': int(lengthMap1),
        'length_map2': int(lengthMap2),
        'length_map_all': int(lengthMapOverall),

        'created': datetime.now(),
    }
    # insert the record
    print("Inserting record ...")

    for x in record.keys():
        print("{0} => {1}".format(x, record[x]))

    db.insert_one(record)

    print("Closing ...")
    # close the connection to MongoDB
    connection.close()


if __name__ == '__main__':
    main(sys.argv[1:])
