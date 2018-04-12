import os
import sys
import json
import pymongo
from bson import BSON
from bson import json_util

import yaml
from pymongo import MongoClient

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
    for num in range(2, 7):
        db = connection.treesip.testcases

        regexEval = 'JulySingle_' + str(num*10) + '_10_.*' # This is for speed specific
        # regexEval = 'JulySingle_' + str(num*10) + '_.*'
        print(regexEval)
        result = db.aggregate(
           [
            { '$match': { 'name': { '$regex': regexEval, '$options': "si" }, 'computation': { '$gt': 4 }  } },
               {
                   '$group':
                       {
                           '_id': "$name",
                           'timeout': {'$avg': "$timeout"},
                           'accuracy': {'$avg': {'$divide': ["$computation", "$nodes"]}},
                       }
               },
               {'$sort': {'timeout': 1}},
           ]
        )

        filenameEval = 'graphs/nodes' + str(num * 10) + '.json'
        print("JSON ...")
        f = open(filenameEval, 'w')
        f.write(json.dumps(list(result), default=json_util.default))