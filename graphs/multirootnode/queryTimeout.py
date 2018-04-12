import os
import sys
import json
import pymongo
from bson import BSON
from bson import json_util

import yaml
from pymongo import MongoClient

def assembleQuery( regex, timeout, speed ):
    return [
            { '$match': { 'name': { '$regex': regex, '$options': "si" }, 'timeout': timeout, 'node_speed': speed } },
               {
                   '$group':
                       {
                           '_id': "$name",
                           'nodes': {'$avg': "$nodes"},
                           'accuracy': {'$avg': {'$divide': ["$length_map_all", "$nodes"]}},
                       }
               },
               {'$sort': {'nodes': 1}},
           ]

def queryToJson( db, regex, timeout, speed, mode ):
    result = db.aggregate(assembleQuery(regex, timeout, speed))
    filenameEval = 'graphs/multi_' + str(mode) + '_' + str(speed) + '_' + str(timeout) + '.json'
    print("JSON ...")
    f = open(filenameEval, 'w')
    f.write(json.dumps(list(result), default=json_util.default))

if __name__ == '__main__':
  try:
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
  except:
    print('Error: Unable to Connect')
    connection = None

  if connection is not None:
    for num in range(1, 6):
        db = connection.treesip.testcases

        queryToJson( db, 'JulySingle.*', 200, num * 2, 's' )
        queryToJson( db, 'JulyMulti.*', 200, num * 2, 'm' )

        queryToJson(db, 'JulySingle.*', 400, num * 2, 's')
        queryToJson(db, 'JulyMulti.*', 400, num * 2, 'm')