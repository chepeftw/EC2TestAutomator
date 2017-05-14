#!/usr/bin/python

import os
import sys
import glob
import time
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
    computation = ""
    convergence = ""

    # iterate for each file path in the list
    for fp in filepaths:
        # Open the file in read mode
        with open(fp, 'r') as f:
            for line in f:
                if RESULT_STRING in line :
                    computation = line.split( RESULT_STRING )[1].rstrip()
                elif CONVERGENCE_TIME_STRING in line :
                    convergence = line.split(CONVERGENCE_TIME_STRING)[1].rstrip()


    ###############################################################################
    # Then we connect to MongoDB and store the values
    ###############################################################################

    # connection.admin.authenticate('chepeftw', '<nope>', mechanism='SCRAM-SHA-1')
    connection = MongoClient('10.0.0.54', 27017)
    time.sleep(2)

    # connect to the students database and the ctec121 collection
    db = connection.students.test

    # create a dictionary to hold student documents

    # create dictionary
    student_record = {}

    # set flag variable
    flag = True

    # loop for data input
    while (flag):
        # ask for input
        # student_name,student_grade = input("Enter student name and grade: ").split(',')
        student_name = 'chepe'
        student_grade = 90
        # place values in dictionary
        student_record = {'name': student_name, 'grade': student_grade}
        # insert the record
        db.insert(student_record)
        flag = False




    # connect to the treesip database and the testcases collection
    db = connection.treesip.testcases


    # find all documents
    results = db.find()

    print()
    print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-')

    # display documents from collection
    for record in results:
        # print out the document
        print(record['name'] + ',',record['grade'])

    print()

     
    # create dictionary and place values in dictionary
    record = {'computation': computation, 'convergence': convergence, 'time': datetime.now()}
    # insert the record
    db.insert_one(record)
     
    # close the connection to MongoDB
    connection.close()


if __name__ == '__main__':
    main(sys.argv[1:])