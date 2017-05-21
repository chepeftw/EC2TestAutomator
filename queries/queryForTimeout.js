db.testcases.aggregate(
   [
    { $match: { name: { $regex: /Tmout_20*/, $options: "si" }, computation: { $type: "int" }, nodes: { $type: "int" } } },
     {
       $group:
         {
           _id: "$name",
           timeout: { $avg: "$timeout" },
           accuracy: { $avg: { $divide: [ "$computation", "$nodes" ] }},
         }
     },
     { $sort: { timeout: 1 } },
   ]
)