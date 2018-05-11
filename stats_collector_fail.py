#!/usr/bin/python

import common

__author__ = 'chepe'


def failfunc():
    return {
        'fail': int(1),
    }


def main():
    parser = common.addArgumentsToParser()
    args = parser.parse_args()

    connection = common.getMongo()
    db = common.getDatabase(connection)
    base_record = common.getBaseRecord(args)

    # args.operation == "fail"
    common.insertonerecord(db.full_fails, failfunc(), base_record)

    print("Closing ...")
    # close the connection to MongoDB
    connection.close()


if __name__ == '__main__':
    main()
