db.testcases.aggregate(
   [
    { $match: { computation: { $type: "int" }, nodes: { $type: "int" } } },
     {
       $group:
         {
           _id: "$name",
           minQuantity: { $min: "$convergence" },
           maxQuantity: { $max: "$convergence" },
           avgQuantity: { $avg: "$convergence" },
           avgComputations: { $avg: "$computation" },
           timeout: { $avg: "$timeout" },
           acuracy: { $avg: { $divide: [ "$computation", "$nodes" ] }},
           countNum: { $sum: 1 }
         }
     },
     { $sort: { acuracy: -1 } }
   ]
)