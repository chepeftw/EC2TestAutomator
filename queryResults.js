db.testcases.aggregate(
   [
    { $match: { name: { $regex: /Tmout_*/, $options: "si" }, computation: { $type: "int" }, nodes: { $type: "int" } } },
     {
       $group:
         {
           _id: "$name",
           minQuantity: { $min: "$convergence" },
           maxQuantity: { $max: "$convergence" },
           avgQuantity: { $avg: "$convergence" },
           avgComputations: { $avg: "$computation" },
           timeout: { $avg: "$timeout" },
           accuracy: { $avg: { $divide: [ "$computation", "$nodes" ] }},
           runs: { $sum: 1 }
         }
     },
     { $sort: { accuracy: -1 } }
   ]
)