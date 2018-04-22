#!/usr/bin/python

import argparse

import os
import glob
import yaml
from datetime import datetime
from pymongo import MongoClient

__author__ = 'chepe'


def failfunc():
    return {
        'fail': int(1),
    }


def msgcountfunc():
    folder = "/home/ubuntu/tap/var/log/"
    filesets = glob.glob(os.path.join(folder, '**/raft.log'), recursive=True)

    sending_message_string = "RAFT_SENDING_MESSAGE=1"
    messages_sent = 0

    sending_ping_string = "RAFT_SENDING_PING=1"
    ping_sent = 0

    message_size_string = "RAFT_MESSAGE_SIZE="
    messages_size = 0

    # iterate for each file path in the list
    for fp in filesets:
        # Open the file in read mode
        with open(fp, 'r') as f:
            for line in f:
                if sending_message_string in line:
                    messages_sent += 1
                elif sending_ping_string in line:
                    ping_sent += 1
                elif message_size_string in line:
                    messages_size += int(line.split(message_size_string)[1].rstrip())

    messages_size_total = int(messages_size / messages_sent)

    return {
        'messages_count': int(messages_sent),
        'ping_count': int(ping_sent),
        'messages_size': int(messages_size_total),
    }


def avgmediumtimefunc():
    folder = "/home/ubuntu/tap/var/log/"
    filesets = glob.glob(os.path.join(folder, '**/raft.log'), recursive=True)

    message_avgtime_string = "RAFT_AVG_TIME="
    message_avgtime = 0
    message_avgtime_count = 0

    # iterate for each file path in the list
    for fp in filesets:
        # Open the file in read mode
        with open(fp, 'r') as f:
            for line in f:
                if message_avgtime_string in line:
                    message_avgtime += int(line.split(message_avgtime_string)[1].rstrip())
                    message_avgtime_count += 1

    messages_avgtime_total = int(message_avgtime / message_avgtime_count)

    return {
        'average_medium_time': int(messages_avgtime_total),
    }


def electionfunc():
    folder = "/home/ubuntu/tap/var/log/"
    filesets = glob.glob(os.path.join(folder, '**/raft.log'), recursive=True)

    winner_string = "RAFT_WINNER="
    winner = ""
    winner_count = 0

    reverse_string = "RAFT_REVERSE_WINNER="
    reverse = ""
    reverse_count = 0

    election_time_string = "RAFT_ELECTION_TIME="
    election_time = 0
    election_time_count = 0

    # iterate for each file path in the list
    for fp in filesets:
        # Open the file in read mode
        with open(fp, 'r') as f:
            for line in f:
                if winner_string in line:
                    winner = line.split(winner_string)[1].rstrip()
                    winner_count += 1
                elif reverse_string in line:
                    reverse = line.split(reverse_string)[1].rstrip()
                    reverse_count += 1
                elif election_time_string in line:
                    election_time += int(line.split(election_time_string)[1].rstrip())
                    election_time_count += 1

    election_time_total = int(election_time / election_time_count)

    return {
        'winner': winner,
        'reverse': reverse,
        'winner_count': int(winner_count),
        'reverse_count': int(reverse_count),
        'winner_total': (int(winner_count)-int(reverse_count)),
        'election_time_ns': int(election_time_total),
        'election_time_ms': int(election_time_total/1000000),
        'election_time_s': int((election_time_total/1000000)/1000),
    }


def channelfunc():
    folder = "/home/ubuntu/tap/var/log/"
    filesets = glob.glob(os.path.join(folder, '**/raft.log'), recursive=True)

    buffer_channel_time_string = "RAFT_ATTEND_BUFFER_CHANNEL_START_TIME="
    buffer_channel_time = 0
    buffer_channel_time_count = 0

    # iterate for each file path in the list
    for fp in filesets:
        # Open the file in read mode
        with open(fp, 'r') as f:
            for line in f:
                if buffer_channel_time_string in line:
                    buffer_channel_time += int(line.split(buffer_channel_time_string)[1].rstrip())
                    buffer_channel_time_count += 1

    buffer_channel_time_total = int(buffer_channel_time / buffer_channel_time_count)

    return {
        'buffer_channel_time': int(buffer_channel_time_total),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, help="The number of nodes of the simulation")
    parser.add_argument("nodes", type=int, help="The number of nodes of the simulation")
    parser.add_argument("time", type=int, help="The time of the simulation")
    parser.add_argument("timeout", type=int, help="The timeout of the simulation")
    parser.add_argument("size", type=int, help="The size of the network in the simulation")
    parser.add_argument("operation", type=str, help="The operation or property to look in the logs")
    parser.add_argument("-ns", "--nodespeed", action="store", help="The speed of the nodes expressed in m/s")
    parser.add_argument("-np", "--nodepause", action="store", help="The pause of the nodes expressed in s")
    parser.add_argument("-cp", "--cryptopiece", action="store", help="The piece of the crypto puzzle")
    parser.add_argument("-ct", "--count", action="store", help="The piece of the crypto puzzle")
    args = parser.parse_args()

    ###############################################################################
    # First we read all logs, collecting the important values
    ###############################################################################

    # print("Reading log files ...")
    # Then we connect to MongoDB and store the values

    # print("Loading config.yml ...")
    with open('config.yml', 'r') as f:
        doc = yaml.load(f)

    host = '54.186.74.114'
    port = 27017
    # user = 'username'
    # pasw = 'password'

    if 'parameters' in doc:
        if 'host' in doc['parameters']:
            host = doc['parameters']['host']
        if 'port' in doc['parameters']:
            port = doc['parameters']['port']
        # if 'user' in doc['parameters']:
        #     user = doc['parameters']['user']
        # if 'pasw' in doc['parameters']:
        #     pasw = doc['parameters']['pasw']

    # print("Connecting to mongo ...")
    connection = MongoClient(host, port)
    db = connection.blockchain
    # connection.admin.authenticate(user, pasw, mechanism='SCRAM-SHA-1')
    # print("Connected to mongo ...")

    base_record = {
        'count': args.count,
        'name': args.name,
        'nodes': int(args.nodes),
        'duration': int(args.time),
        'timeout': int(args.timeout),
        'size': int(args.size),
        'created': datetime.now(),
    }

    if args.operation == "fail":
        collection = db.full_fails
        record = failfunc()
    elif args.operation == "messagecount":
        collection = db.sent_messages
        record = msgcountfunc()
    elif args.operation == "avgmediumtime":
        collection = db.medium_time
        record = avgmediumtimefunc()
    elif args.operation == "election":
        collection = db.elections
        record = electionfunc()
    elif args.operation == "bufferchannel":
        collection = db.bufferchannel
        record = channelfunc()

    # insert the record
    print("Inserting record ...")
    record.update(base_record)
    collection.insert_one(record)

    print("Closing ...")
    # close the connection to MongoDB
    connection.close()


if __name__ == '__main__':
    main()
