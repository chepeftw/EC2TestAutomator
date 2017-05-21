db.testcases.aggregate(
   [
    { $match: { computation: { $type: "int" }, nodes: { $type: "int" } } },
     {
       $group:
         {
           _id: "$name",
           minConvergence: { $min: "$convergence" },
           maxQuantity: { $max: "$convergence" },
           avgQuantity: { $avg: "$convergence" },
           avgComputations: { $avg: "$computation" },
           minQuantity2: { $min: "$convergence2" },
           maxQuantity2: { $max: "$convergence2" },
           avgQuantity2: { $avg: "$convergence2" },
           avgComputations2: { $avg: "$computation2" },
           timeout: { $avg: "$timeout" },
           accuracy1: { $avg: { $divide: [ "$computation", "$nodes" ] }},
           accuracy2: { $avg: { $divide: [ "$computation2", "$nodes" ] }},
           total_arithmetic_acuracy: 
              { $avg: { 
                $divide: [ 
                { $sum: [ { $divide: [ "$computation", "$nodes" ] }, { $divide: [ "$computation", "$nodes" ] }] },
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
     { $sort: { acuracy: -1 } }
   ]
)