#!/usr/bin/python

import argparse
import glob
import os
import sys
from datetime import datetime

import yaml
from pymongo import MongoClient

__author__ = 'chepe'


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
    args = parser.parse_args()

    ###############################################################################
    # First we read all logs, collecting the important values
    ###############################################################################

    # Set folder:
    folder = "/home/ubuntu/tap/var/log/"

    # Get filepaths for all files which end with ".txt" and start with "travel_times_to_ 59721":
    filepaths = glob.glob(os.path.join(folder, '**/*.log'), recursive=True)

    # log constants
    RESULT_STRING = " RESULT="
    CONVERGENCE_TIME_STRING = " CONVERGENCE_TIME="
    LEVEL_STRING = " LEVEL="

    # variables
    computation = ""
    convergence = ""
    level = 0

    # iterate for each file path in the list
    for fp in filepaths:
        # Open the file in read mode
        with open(fp, 'r') as f:
            for line in f:
                if RESULT_STRING in line:
                    computation = line.split(RESULT_STRING)[1].rstrip()
                elif CONVERGENCE_TIME_STRING in line:
                    convergence = line.split(CONVERGENCE_TIME_STRING)[1].rstrip()
                elif LEVEL_STRING in line:
                    levelTmp = int(line.split(LEVEL_STRING)[1].rstrip())
                    if level < levelTmp:
                        level = levelTmp

    ###############################################################################
    # Then we connect to MongoDB and store the values
    ###############################################################################

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

    connection = MongoClient(host, port)
    connection.admin.authenticate(user, pasw, mechanism='SCRAM-SHA-1')

    # connect to the treesip database and the testcases collection
    db = connection.treesip.testcases

    # create dictionary and place values in dictionary
    record = {
        'computation': int(computation),
        'level': int(level),
        'convergence': int(convergence),
        'time': datetime.now(),
        'name': args.name,
        'nodes': int(args.nodes),
        'duration': int(args.time)
    }
    # insert the record
    db.insert_one(record)

    # close the connection to MongoDB
    connection.close()


if __name__ == '__main__':
    main(sys.argv[1:])
