#!/usr/bin/python

import argparse
import os
import glob
import common

__author__ = 'chepe'


def msgcountfunc():
    folder = "/home/ubuntu/tap/var/log/"
    filesets = glob.glob(os.path.join(folder, '**/raft.data'), recursive=True)

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
        'messages_size': int(messages_size),
        'messages_size_total': int(messages_size_total),
    }


def msgcountpqueryfunc():
    folder = "/home/ubuntu/tap/var/log/"
    filesets = glob.glob(os.path.join(folder, '**/raft.data'), recursive=True)

    sending_message_string = "RAFT_ACC_SENDING_MESSAGE="

    message_size_string = "RAFT_ACC_MESSAGE_SIZE="

    items = []

    # iterate for each file path in the list
    for fp in filesets:
        # Open the file in read mode
        with open(fp, 'r') as f:
            for line in f:
                if message_size_string in line:
                    bothmsgs = line.split("||||")
                    messages_size = int(bothmsgs[0].split(message_size_string)[1].rstrip())
                    messages_sent = int(bothmsgs[1].split(sending_message_string)[1].rstrip())
                    messages_size_total = int(messages_size / messages_sent)

                    items.append({'messages_count': int(messages_sent), 'messages_size': int(messages_size),
                                  'messages_size_total': int(messages_size_total), })

    return items


def avgmediumtimefunc():
    folder = "/home/ubuntu/tap/var/log/"
    filesets = glob.glob(os.path.join(folder, '**/raft.data'), recursive=True)

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
    filesets = glob.glob(os.path.join(folder, '**/raft.data'), recursive=True)

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
        'winner_total': (int(winner_count) - int(reverse_count)),
        'election_time_ns': int(election_time_total),
        'election_time_ms': int(election_time_total / 1000000),
        'election_time_s': int((election_time_total / 1000000) / 1000),
    }


def channelfunc():
    folder = "/home/ubuntu/tap/var/log/"
    filesets = glob.glob(os.path.join(folder, '**/raft.data'), recursive=True)

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
    parser = common.addArgumentsToParser()
    args = parser.parse_args()

    connection = common.getMongo()
    db = common.getDatabase(connection)
    base_record = common.getBaseRecord(args)

    # args.operation == "messagecount"
    common.insertonerecord(db.raft_sent_messages, msgcountfunc(), base_record)

    # args.operation == "avgmediumtime"
    common.insertonerecord(db.raft_medium_time, avgmediumtimefunc(), base_record)

    # args.operation == "election"
    common.insertonerecord(db.raft_elections, electionfunc(), base_record)

    # args.operation == "bufferchannel"
    common.insertonerecord(db.raft_bufferchannel, channelfunc(), base_record)

    # args.operation == "messagesperquery"
    common.insertmultirecord(db.raft_sent_messages_pquery, msgcountpqueryfunc(), base_record)

    print("Closing ...")
    # close the connection to MongoDB
    connection.close()


if __name__ == '__main__':
    main()
