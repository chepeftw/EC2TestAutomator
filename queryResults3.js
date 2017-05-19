db.testcases.aggregate(
   [
    { $match: { name: { $regex: /MultiN_*/, $options: "si" }, computation: { $type: "int" }, nodes: { $type: "int" } } },
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
           runs: { $sum: 1 }
         }
     },
     { $sort: { accuracy: -1 } }
   ]
)