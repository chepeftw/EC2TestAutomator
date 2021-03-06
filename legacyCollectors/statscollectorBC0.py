#!/usr/bin/python

import argparse, yaml
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

    print("Reading log files ...")
    # Then we connect to MongoDB and store the values

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

    # DATABASE selection
    db = connection.blockchain.pow_fails

    # create dictionary and place values in dictionary
    record = {
        'fail': int(1),

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

    for x in record.keys():
        print("{0} => {1}".format(x, record[x]))

    db.insert_one(record)

    print("Closing ...")
    # close the connection to MongoDB
    connection.close()


if __name__ == '__main__':
    main()
