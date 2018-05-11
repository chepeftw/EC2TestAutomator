import argparse
import yaml
from pymongo import MongoClient
from datetime import datetime


def insertonerecord(collection, record, base_record):
    # insert the record
    print("Inserting record ...")
    record.update(base_record)
    collection.insert_one(record)


def insertmultirecord(collection, records, base_record):
    # insert the record
    for i in range(len(records)):
        print("Inserting record " + str(i) + " ...")
        insertonerecord(collection.raft_sent_messages_pquery, records[i], base_record)

def getMongo():
    # print("Loading config.yml ...")
    with open('config.yml', 'r') as f:
        doc = yaml.load(f)

    host = '54.186.74.114'
    port = 27017

    if 'parameters' in doc:
        if 'host' in doc['parameters']:
            host = doc['parameters']['host']
        if 'port' in doc['parameters']:
            port = doc['parameters']['port']

    # print("Connecting to mongo ...")
    connection = MongoClient(host, port)

    # connection.admin.authenticate(user, pasw, mechanism='SCRAM-SHA-1')
    # print("Connected to mongo ...")

    return connection


def getDatabase(connection):
    return connection.blockchain0


def getBaseRecord(args):
    return {
        'count': args.count,
        'name': args.name,
        'nodes': int(args.nodes),
        'duration': int(args.time),
        'timeout': int(args.timeout),
        'size': int(args.size),
        'created': datetime.now(),
    }


def addArgumentsToParser():
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

    return parser