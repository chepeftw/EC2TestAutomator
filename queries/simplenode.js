db.testcases.aggregate(
   [
    { $match: { name: { $regex: /SimpleN1_.*/, $options: "si" }, computation: { $type: "int" }, nodes: { $type: "int" }, computation: { $gt: 0 }, nodes: { $lt: 60 } } },
     {
       $group:
         {
           _id: "$name",
           avgConvergence: { $avg: "$convergence" },
           avgComputations: { $avg: "$computation" },
           nodes: { $avg: "$nodes" },
           timeout: { $avg: "$timeout" },
           speed: { $avg: "$node_speed" },
           accuracy: { $avg: { $divide: [ "$computation", "$nodes" ] } },
           runs: { $sum: 1 }
         }
     },
     { $sort: { runs: -1 } }
   ]
)