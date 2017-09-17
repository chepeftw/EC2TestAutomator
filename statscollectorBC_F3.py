#!/usr/bin/python

import argparse, glob, os, yaml
from datetime import datetime
from pymongo import MongoClient

__author__ = 'chepe'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, help="The number of nodes of the simulation")
    parser.add_argument("nodes", type=int, help="The number of nodes of the simulation")
    parser.add_argument("time", type=int, help="The time of the simulation")
    parser.add_argument("timeout", type=int, help="The timeout of the simulation")
    parser.add_argument("size", type=int, help="The size of the network in the simulation")
    parser.add_argument("-ns", "--nodespeed", action="store", help="The speed of the nodes expressed in m/s")
    parser.add_argument("-np", "--nodepause", action="store", help="The pause of the nodes expressed in s")
    parser.add_argument("-cp", "--cryptopiece", action="store", help="The piece of the crypto puzzle")
    parser.add_argument("-ct", "--count", action="store", help="The piece of the crypto puzzle")
    args = parser.parse_args()

    ###############################################################################
    # First we read all logs, collecting the important values
    ###############################################################################

    # print("Reading log files ...")

    folder = "/home/ubuntu/tap/var/log/"
    filepaths = glob.glob(os.path.join(folder, '**/monitor.log'), recursive=True)

    start_string = "QUERY_START="
    end_string = "QUERY_END="
    start_val = 0
    end_val = 0
    
    # iterate for each file path in the list
    for fp in filepaths:
        # Open the file in read mode
        with open(fp, 'r') as f:
            for line in f:
                if start_string in line:
                    start_val = int(line.split(start_string)[1].rstrip())
                elif end_string in line:
                    temp = int(line.split(end_string)[1].rstrip())

                    if end_val > temp or end_val == 0:
                        end_val = temp

    # Then we connect to MongoDB and store the values

    # print("Loading config.yml ...")
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

    # print("Connecting to mongo ...")
    connection = MongoClient(host, port)
    connection.admin.authenticate(user, pasw, mechanism='SCRAM-SHA-1')
    # print("Connected to mongo ...")

    # DATABASE selection
    db = connection.blockchain.full_convergence

    # create dictionary and place values in dictionary
    record = {

        'start': start_val,
        'end': end_val,
        'diff': end_val-start_val,

        'cryptopiece': args.cryptopiece,
        'count': args.count,

        'name': args.name,
        'nodes': int(args.nodes),
        'duration': int(args.time),
        'timeout': int(args.timeout),
        'size': int(args.size),

        'created': datetime.now(),
    }
    # insert the record
    print("Inserting record ...")

    # for x in record.keys():
    #     print("{0} => {1}".format(x, record[x]))

    db.insert_one(record)

    print("Closing ...")
    # close the connection to MongoDB
    connection.close()


if __name__ == '__main__':
    main()
