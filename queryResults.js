db.testcases.aggregate(
   [
     {
       $group:
         {
           _id: "$name",
           minQuantity: { $min: "$convergence" },
           maxQuantity: { $max: "$convergence" },
           avgQuantity: { $avg: "$convergence" },
           avgComputations: { $avg: "$computation" },
           countNum: { $sum: 1 }
         }
     }
   ]
)