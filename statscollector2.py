#!/usr/bin/python

# Copyright (c) 2017 ObjectLabs Corporation
# Distributed under the MIT license - http://opensource.org/licenses/MIT

__author__ = 'chepe'

# Written with pymongo-3.4
# Documentation: http://docs.mongodb.org/ecosystem/drivers/python/
# A python script connecting to a MongoDB given a MongoDB Connection URI.

import sys
import glob
from pymongo import MongoClient

###############################################################################
# main
###############################################################################

def main(args):

    ###############################################################################
    # First we read all logs, collecting the important values
    ###############################################################################

    # Set folder:
    folder = "/home/ubuntu/logs"

    # Get filepaths for all files which end with ".txt" and start with "travel_times_to_ 59721":
    filepaths = glob.glob(os.path.join(folder, '*.log'))

    # Create an empty list for collecting the headers
    headers = []

    # iterate for each file path in the list
    for fp in filepaths:
        # Open the file in read mode
        with open(fp, 'r') as f:
            for line in f:
                # Read the first line of the file
                print(line)
                # Append the first line into the headers-list
                # headers.append(first_line)

    # After going trough all the files, print the list of headers
    print(headers)

    ###############################################################################
    # Then we connect to MongoDB and store the values
    ###############################################################################

    connection = MongoClient('54.186.74.114', 27017)
    # connection.admin.authenticate('chepeftw', '<nope>', mechanism='SCRAM-SHA-1')

    # connect to the students database and the ctec121 collection
    db = connection.students.test
     
    # create a dictionary to hold student documents
     
    # create dictionary and place values in dictionary
    student_record = {'name':'chepe','grade':90}
    # insert the record
    db.insert(student_record)
     
    # find all documents
    results = db.find()
     
    print()
    print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-')
     
    # display documents from collection
    for record in results:
        # print out the document
        print(record['name'] + ',',record['grade'])
     
    print()
     
    # close the connection to MongoDB
    connection.close()


if __name__ == '__main__':
    main(sys.argv[1:])