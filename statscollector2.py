#!/usr/bin/python

import os
import sys
import glob
from pymongo import MongoClient
from datetime import datetime

__author__ = 'chepe'


###############################################################################
# main
###############################################################################

def main(args):

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

    # variables
    result = ""
    convergence = ""

    # iterate for each file path in the list
    for fp in filepaths:
        # Open the file in read mode
        with open(fp, 'r') as f:
            for line in f:
                if RESULT_STRING in line :
                    result = line.split( RESULT_STRING )[1]
                elif CONVERGENCE_TIME_STRING in line :
                    convergence = line.split(CONVERGENCE_TIME_STRING)[1]


    ###############################################################################
    # Then we connect to MongoDB and store the values
    ###############################################################################

    connection = MongoClient('54.186.74.114', 27017)
    # connection.admin.authenticate('chepeftw', '<nope>', mechanism='SCRAM-SHA-1')

    # connect to the students database and the ctec121 collection
    db = connection.treesip.results
     
    # create a dictionary to hold student documents
     
    # create dictionary and place values in dictionary
    record = {'result': result, 'convergence': convergence, 'time': datetime.datetime.now()}
    # insert the record
    db.insert(record)
     
    # find all documents
    # results = db.find()
    #
    # print()
    # print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-')
    #
    # # display documents from collection
    # for record in results:
    #     # print out the document
    #     print(record['name'] + ',',record['grade'])
    #
    # print()
     
    # close the connection to MongoDB
    connection.close()


if __name__ == '__main__':
    main(sys.argv[1:])