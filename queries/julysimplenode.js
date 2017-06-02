db.testcases.aggregate(
   [
    { '$match': { name: { $regex: /JulySingle.*/, $options: "si" }, 'computation': { '$type': "int" }, 'nodes': { '$type': "int" } } },
     {
       '$group':
         {
           '_id': "$name",
           'minConver': { '$min': "$convergence" },
           'maxConver': { '$max': "$convergence" },
           'avgConver': { '$avg': "$convergence" },
           'minLevel': { '$min': "$maxlevel" },
           'maxLevel': { '$max': "$maxlevel" },
           'avgLevel': { '$avg': "$maxlevel" },
           'avgComputations': { '$avg': "$computation" },
           'timeout': { '$avg': "$timeout" },
           'speed': { '$avg': "$node_speed" },
           'nodes': { '$avg': "$nodes" },
           'automata': { '$avg': "$automata" },
           'accuracy': { '$avg': { '$divide': [ "$computation", "$nodes" ] }},
           'runs': { '$sum': 1 }
         }
     },
     { '$sort': { 'accuracy': -1 } }
   ]
)
