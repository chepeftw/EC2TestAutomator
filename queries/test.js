db.testcases.aggregate(
    [
        {'$match': {name: {$regex: /JulySingle.*/, $options: "si"}, 'computation': {'$gt': 1}}},
        {
            '$group':
                {
                    '_id': "$timeout",
                    'minConver': {'$min': "$convergence"},
                    'maxConver': {'$max': "$convergence"},
                    'avgConver': {'$avg': "$convergence"},
                    'minLevel': {'$min': "$maxlevel"},
                    'maxLevel': {'$max': "$maxlevel"},
                    'avgLevel': {'$avg': "$maxlevel"},
                    'avgComputations': {'$avg': "$computation"},
                    'timeout': {'$avg': "$timeout"},
                    'speed': {'$avg': "$node_speed"},
                    'nodes': {'$avg': "$nodes"},
                    'automata': {'$avg': "$automata"},
                    'accuracy': {'$avg': {'$divide': ["$computation", "$nodes"]}},
                    'runs': {'$sum': 1}
                }
        },
        {'$sort': {'accuracy': -1}}
    ]
)


db.raft_sent_messages.aggregate(
    [
        {'$match': {name: {$regex: /Blockchain.*/, $options: "si"}, 'messages_count': {'$lt': 100000}}},
        {
            '$group':
                {
                    '_id': "$name",
                    'minComplete': {'$min': {'$divide': ["$messages_count", 4]}},
                    'maxComplete': {'$max': {'$divide': ["$messages_count", 4]}},
                    'avgComplete': {'$avg': {'$divide': ["$messages_count", 4]}},
                    'stdSVal': {'$stdDevSamp': {'$divide': ["$messages_count", 4]}},
                    'runs': {'$sum': 1}
                }
        },
        {'$sort': {'_id': 1}}
    ]
)


db.monitor_query_complete.aggregate(
    [
        {
            '$match': {
                name: {$regex: /^Blockchain_.*_2$/, $options: "si"},
                'query_complete_ms': {'$gt': 0, '$lt': 60000},
                'nodes': 20,
                'timeout': 200
            }
        },
        {
            '$group':
                {
                    '_id': "$name",
                    'minComplete': {'$min': "$query_complete_ms"},
                    'maxComplete': {'$max': "$query_complete_ms"},
                    'avgComplete': {'$avg': "$query_complete_ms"},
                    'stdSVal': {'$stdDevSamp': "$query_complete_ms"},
                    'runs': {'$sum': 1}
                }
        },
        {'$sort': {'_id': 1}}
    ]
)

﻿db.monitor_accuracy.aggregate(
    [
        {
            '$match': {
                name: {$regex: /^Blockchain_.*_2$/, $options: "si"},
                'block_valid_ratio_percentage': {'$gt': 10},
            }
        },
        {
            '$group':
                {
                    '_id': "$timeout",
                    'minComplete': {'$min': "$block_valid_ratio_percentage"},
                    'maxComplete': {'$max': "$block_valid_ratio_percentage"},
                    'avgComplete': {'$avg': "$block_valid_ratio_percentage"},
                    'stdSVal': {'$stdDevSamp': "$block_valid_ratio_percentage"},
                    'runs': {'$sum': 1}
                }
        },
        {'$sort': {'_id': 1}}
    ]
)

﻿db.monitor_query_complete.aggregate(
    [
        {
            '$match': {
                name: {$regex: /^Blockchain_.*_2$/, $options: "si"},
                'query_complete_ms': {'$gt': 0, '$lt': 60000},
                'nodes': 30,
                'timeout': 200
            }
        },
        {
            '$group':
                {
                    '_id': "$timeout",
                    'minComplete': {'$min': "$query_complete_ms"},
                    'maxComplete': {'$max': "$query_complete_ms"},
                    'avgComplete': {'$avg': "$query_complete_ms"},
                    'stdSVal': {'$stdDevSamp': "$query_complete_ms"},
                    'runs': {'$sum': 1}
                }
        },
        {'$sort': {'_id': 1}}
    ]
)

db.getCollection('monitor_accuracy').updateMany(
    {name: {$regex: /^Blockchain_.*_2$/, $options: "si"},
{
    $set: {
        "speed"
    :
        2
    }
,
    $currentDate: {
        lastModified: true
    }
}
)

﻿db.getCollection('raft_sent_messages').updateMany(
    {name: {$regex: /^Blockchain_.*_5$/, $options: "si"}},
    {
        $set: {"speed": 5},
        $currentDate: {lastModified: true}
    }
)