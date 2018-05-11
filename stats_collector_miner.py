#!/usr/bin/python

import os
import glob
import common

__author__ = 'chepe'


def miningtime1func():
    folder = "/home/ubuntu/tap/var/log/"
    filesets = glob.glob(os.path.join(folder, '**/miner.data'), recursive=True)

    mining_time_string = "MINING_TIME_1="

    items = []

    # iterate for each file path in the list
    for fp in filesets:
        # Open the file in read mode
        with open(fp, 'r') as f:
            for line in f:
                if mining_time_string in line:
                    mining_time = int(line.split(mining_time_string)[1].rstrip())

                    items.append(
                        {'mining_time_1_ns': int(mining_time), 'mining_time_1_ms': int(mining_time / 1000000), })

    return items


def miningtime2func():
    folder = "/home/ubuntu/tap/var/log/"
    filesets = glob.glob(os.path.join(folder, '**/miner.data'), recursive=True)

    mining_time_string = "MINING_TIME_2="

    items = []

    # iterate for each file path in the list
    for fp in filesets:
        # Open the file in read mode
        with open(fp, 'r') as f:
            for line in f:
                if mining_time_string in line:
                    mining_time = int(line.split(mining_time_string)[1].rstrip())

                    items.append(
                        {'mining_time_2_ns': int(mining_time), 'mining_time_2_ms': int(mining_time / 1000000), })

    return items


def main():
    parser = common.addArgumentsToParser()
    args = parser.parse_args()

    connection = common.getMongo()
    db = common.getDatabase(connection)
    base_record = common.getBaseRecord(args)

    # args.operation == "miningtime1"
    common.insertmultirecord(db.miner_time1, miningtime1func(), base_record)

    # args.operation == "miningtime2"
    common.insertmultirecord(db.miner_time2, miningtime2func(), base_record)

    print("Closing ...")
    # close the connection to MongoDB
    connection.close()


if __name__ == '__main__':
    main()
