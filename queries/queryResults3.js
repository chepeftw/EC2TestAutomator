db.testcases.aggregate(
   [
    { $match: { name: { $regex: /MultiN9.*/, $options: "si" }, computation: { $type: "int" }, nodes: { $type: "int" }, computation: { $gt: 0 }, computation2: { $gt: 0 } } },
     {
       $group:
         {
           _id: "$name",
           avgConvergence: { $avg: "$convergence" },
           avgComputations: { $avg: "$computation" },
           avgConvergence2: { $avg: "$convergence2" },
           avgComputations2: { $avg: "$computation2" },
           nodes: { $avg: "$nodes" },
           a_computations: 
              { $avg: { 
                $divide: [ { $sum: [ "$computation", "$computation2"] }, 2 ] 
              } },
           a_convergence: 
              { $avg: { 
                $divide: [ { $sum: [ "$convergence", "$convergence2"] }, 2 ] 
              } },
           timeout: { $avg: "$timeout" },
           speed: { $avg: "$node_speed" },
           w_acuracy: 
              { $avg: { 
                $divide: [ 
                { $sum: [ 
                  { $multiply: [ "$computation", { $divide: [ "$computation", "$nodes" ] } ] }, 
                  { $multiply: [ "$computation2", { $divide: [ "$computation2", "$nodes" ] } ] } 
                ] }, 
                { $sum: [ "$computation", "$computation2" ] } 
                ] }},
           runs: { $sum: 1 }
         }
     },
     { $sort: { runs: -1 } }
   ]
)