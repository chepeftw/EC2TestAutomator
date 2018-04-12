db.testcases.aggregate(
   [
    { '$match': { name: { $regex: /JulySingle.*/, $options: "si" }, 'computation': { '$gt': 1 } } },
     {
       '$group':
         {
           '_id': "$timeout",
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
