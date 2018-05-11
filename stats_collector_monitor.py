#!/usr/bin/python

import argparse
import os
import glob
import common

__author__ = 'chepe'


def querycompletefunc():
    folder = "/home/ubuntu/tap/var/log/"
    filesets = glob.glob(os.path.join(folder, '**/monitor.data'), recursive=True)

    query_complete_string = "QUERY_COMPLETE="
    query_complete = 0

    items = []

    # iterate for each file path in the list
    for fp in filesets:
        # Open the file in read mode
        with open(fp, 'r') as f:
            for line in f:
                if query_complete_string in line:
                    query_complete += int(line.split(query_complete_string)[1].rstrip())

                    items.append({'query_complete_ns': int(query_complete),
                                  'query_complete_ms': int(query_complete / 1000000), })

    return items


def accuracyfunc(nodes):
    folder = "/home/ubuntu/tap/var/log/"
    filesets = glob.glob(os.path.join(folder, '**/router.data'), recursive=True)

    query_id_string = "QUERY_ID="
    ids = []

    # iterate for each file path in the list
    for fp in filesets:
        # Open the file in read mode
        with open(fp, 'r') as f:
            for line in f:
                if query_id_string in line:
                    ids.append(line.split(query_id_string)[1].rstrip())

    filesets = glob.glob(os.path.join(folder, '**/monitor.data'), recursive=True)

    items = []

    for i in range(len(ids)):
        qid = ids[i]

        block_valid_string = "BLOCK_VALID_" + qid + "="
        block_valid = 0

        block_invalid_string = "BLOCK_INVALID_" + qid + "="
        block_invalid = 0

        # iterate for each file path in the list
        for fp in filesets:
            # Open the file in read mode
            with open(fp, 'r') as f:
                for line in f:
                    if block_valid_string in line:
                        block_valid += 1
                    elif block_invalid_string in line:
                        block_invalid += 1

        unitbs = float(1 / (block_valid + block_invalid))
        unit = float(1 / nodes)

        items.append({'block_valid': int(block_valid), 'block_invalid': int(block_invalid),
                      'block_valid_ratio': float(block_valid * unitbs),
                      'block_invalid_ratio': float(block_invalid * unitbs),
                      'block_valid_ratio_percentage': float(block_valid * unitbs * 100),
                      'block_invalid_ratio_percentage': float(block_invalid * unitbs * 100),
                      'block_valid_general_ratio': float(block_valid * unit),
                      'block_invalid_general_ratio': float(block_invalid * unit),
                      'block_valid_general_ratio_percentage': float(block_valid * unit * 100),
                      'block_invalid_general_ratio_percentage': float(block_invalid * unit * 100), })

    return items


def main():
    parser = common.addArgumentsToParser()
    args = parser.parse_args()

    connection = common.getMongo()
    db = common.getDatabase(connection)
    base_record = common.getBaseRecord(args)

    # args.operation == "complete"
    common.insertmultirecord(db.monitor_query_complete, querycompletefunc(), base_record)

    # args.operation == "accuracy"
    common.insertmultirecord(db.monitor_accuracy, accuracyfunc(int(args.nodes)), base_record)

    print("Closing ...")
    # close the connection to MongoDB
    connection.close()


if __name__ == '__main__':
    main()
