// db.full_convergence.aggregate(
//    [
//    { $match: { name: { $regex: /BlockchainFULL1_.*_2/, $options: "si" }, diff: { $lt: 200758666636 } } },
//      {
//        $group:
//          {
//            _id: "$name",
//            diff: { $avg: "$diff" },
//            minff: { $min: "$diff" },
//            maxff: { $max: "$diff" },
//            runs: { $sum: 1 }
//          }
//      },
//      {
//          $project: {
//              "count":1,
//              "runs": "$runs",
//              "min":  { $divide: [ "$minff", 1000000000 ] },
//              "max":  { $divide: [ "$maxff", 1000000000 ] },
//              "diff_ms": { $divide: [ "$diff", 1000000000 ] }
//              }
//          },
//      { $sort: { diff_ms: -1 } }
//    ]
// )


Highcharts.chart('container', {

    title: {
        text: 'Figure'
    },

    yAxis: {
        title: {
            text: 'Time'
        }
    },
    xAxis: {
        labels: {
            rotation: -45,
            style: {
                fontSize: '13px',
                fontFamily: 'Verdana, sans-serif'
            }
        },
        categories: [
            '20 nodes',
            '30 nodes',
            '40 nodes',
            '50 nodes'

        ]
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

        credits: {
        enabled: false
    },


    series: [
    {
        name: '2 m/s',
        data: [46.4031578598182, 63.8251325844314, 57.7421096034571, 68.25412645622]
    }, {
        name: '5 m/s',
        data: [47.9931902599474, 84.1854839206981, 67.1236858196429, 69.6401852099592]
    }
    ],

    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom'
                }
            }
        }]
    }

});