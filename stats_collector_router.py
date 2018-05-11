#!/usr/bin/python

import os
import glob
import common

__author__ = 'chepe'


def msgcountfunc():
    folder = "/home/ubuntu/tap/var/log/"
    filesets = glob.glob(os.path.join(folder, '**/router.data'), recursive=True)

    sending_message_string = "SENDING_MESSAGE=1"
    messages_sent = 0

    sending_ping_string = "RE_SEND_MESSAGE=1"
    re_send = 0

    message_size_string = "MESSAGE_SIZE="
    messages_size = 0

    # iterate for each file path in the list
    for fp in filesets:
        # Open the file in read mode
        with open(fp, 'r') as f:
            for line in f:
                if sending_message_string in line:
                    messages_sent += 1
                elif sending_ping_string in line:
                    re_send += 1
                elif message_size_string in line:
                    messages_size += int(line.split(message_size_string)[1].rstrip())

    messages_size_total = int(messages_size / messages_sent)

    return {
        'messages_count': int(messages_sent),
        're_messages_count': int(re_send),
        'messages_size': int(messages_size),
        'messages_size_total': int(messages_size_total),
    }


def msgcountpqueryfunc():
    folder = "/home/ubuntu/tap/var/log/"
    filesets = glob.glob(os.path.join(folder, '**/router.data'), recursive=True)

    sending_message_string = "QUERY_MESSAGES_SEND="

    message_size_string = "QUERY_MESSAGES_SIZE="

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


def propagationfunc():
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

    items = []

    for i in range(len(ids)):
        qid = ids[i]

        query_sent_string = "QUERY_TIME_SENT_" + qid + "="
        query_sent = 0

        query_received_string = "QUERY_TIME_RECEIVED_" + qid + "="
        query_received = 0

        query_hops_string = "QUERY_HOPS_COUNT_" + qid + "="
        query_hops = 0

        # iterate for each file path in the list
        for fp in filesets:
            # Open the file in read mode
            with open(fp, 'r') as f:
                for line in f:
                    if query_sent_string in line:
                        query_sent = int(line.split(query_sent_string)[1].rstrip())
                    elif query_received_string in line:
                        query_received = max(query_received, int(line.split(query_received_string)[1].rstrip()))
                    elif query_hops_string in line:
                        query_hops = max(query_hops, int(line.split(query_hops_string)[1].rstrip()))

        time_total = int(query_received - query_sent)

        items.append({'query_hops': int(query_hops),
                      'query_sent_ns': int(query_sent), 'query_sent_ms': int(query_sent / 1000000),
                      'query_received_ns': int(query_received), 'query_received_ms': int(query_received / 1000000),
                      'query_propagation_ns': int(time_total), 'query_propagation_ms': int(time_total / 1000000), })

    return items


def main():
    parser = common.addArgumentsToParser()
    args = parser.parse_args()

    connection = common.getMongo()
    db = common.getDatabase(connection)
    base_record = common.getBaseRecord(args)

    # args.operation == "fail"
    common.insertonerecord(db.router_sent_messages, msgcountfunc(), base_record)

    # args.operation == "multiplemessageperquery"
    common.insertmultirecord(db.router_sent_messages_pquery, msgcountpqueryfunc(), base_record)

    # args.operation == "querypropagation"
    common.insertmultirecord(db.router_query_propagation, propagationfunc(), base_record)

    print("Closing ...")
    # close the connection to MongoDB
    connection.close()


if __name__ == '__main__':
    main()
