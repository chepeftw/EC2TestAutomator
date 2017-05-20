db.testcases.aggregate(
   [
    { $match: { name: { $regex: /MultiN4.*/, $options: "si" }, computation: { $type: "int" }, nodes: { $type: "int" } } },
     {
       $group:
         {
           _id: "$name",
           minConvergence: { $min: "$convergence" },
           maxConvergence: { $max: "$convergence" },
           avgConvergence: { $avg: "$convergence" },
           avgComputations: { $avg: "$computation" },
           minConvergence2: { $min: "$convergence2" },
           maxConvergence2: { $max: "$convergence2" },
           avgConvergence2: { $avg: "$convergence2" },
           avgComputations2: { $avg: "$computation2" },
           timeout: { $avg: "$timeout" },
           speed: { $avg: "$node_speed" },
           accuracy: { $avg: { $divide: [ "$computation", "$nodes" ] }},
           accuracy2: { $avg: { $divide: [ "$computation2", "$nodes" ] }},
                      total_arithmetic_acuracy: 
              { $avg: { 
                $divide: [ 
                { $sum: [ { $divide: [ "$computation", "$nodes" ] }, { $divide: [ "$computation2", "$nodes" ] }] },
                 2 
                 ] }},
            total_weighted_acuracy: 
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