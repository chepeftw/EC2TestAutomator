// Sample query to get these values
// db.pow_time.aggregate(
//    [
//    { $match: { time_ms: { $lt: 1505000000000 }, nodes: 40, name: { $regex: /.*_(0000)_.*/, $options: "si" } } },
//      {
//        $group:
//          {
//            _id: "$name",
//            avgT: { $avg: "$time_ms" },
//            avgHashes: { $avg: "$hashes" },
//            minT: { $min: "$time_ms" },
//            maxT: { $max: "$time_ms" },
//            runs: { $sum: 1 }
//          }
//      },
//      {
//          $project: {
//              "count":1,
//              "runs": "$runs",
//              "hashes": "$avgHashes",
//              "seconds": { $divide: [ "$avgT", 1000 ] }
//              }
//          },
//      { $sort: { seconds: -1 } }
//    ]
// )


Highcharts.chart('container1', {
    chart: {
        type: 'area',
        spacingBottom: 30
    },
    title: {
        text: 'Time per crypto puzzle of length 2'
    },

    legend: {
        layout: 'vertical',
        align: 'left',
        verticalAlign: 'top',
        x: 150,
        y: 100,
        floating: true,
        borderWidth: 1,
        backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
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
            'P: 12, I: medium',
            'P: 00, I: medium',
            'P: 12, I: small',
            'P: 00, I: small',
            'P: 12, I: micro',
            'P: 00, I: micro'

        ]
    },
    yAxis: {
        title: {
            text: 'Time (s)'
        },
        labels: {
            formatter: function () {
                return this.value;
            }
        }
    },
    tooltip: {
        formatter: function () {
            return '<b>' + this.series.name + '</b><br/>' +
                this.x + ': ' + this.y;
        }
    },
    plotOptions: {
        area: {
            fillOpacity: 0.5
        }
    },
    credits: {
        enabled: false
    },
    series: [
    {
        name: '20 nodes',
        data: [
            0.0380086206896552,
            0.0288898305084746,

            0.0713285198555957,
            0.0725571428571429,

            0.0796109090909091,
            0.0784491228070175
        ]
    },
        {
        name: '30 nodes',
        data: [
            0.0330728744939271,
            0.0422561983471074,

            0.0808628762541806,
            0.076891975308642,

            0.0688910256410256,
            0.0841740506329114
        ]
    },
        {
        name: '40 nodes',
        data: [
            0.0319812030075188,
            0.0340077821011673,

            0.0697068493150685,
            0.0740888888888889,

            0.0841524390243902,
            0.0955632183908046
        ]
    }
    ]
});



Highcharts.chart('container2', {
    chart: {
        type: 'area',
        spacingBottom: 30
    },
    title: {
        text: 'Time per crypto puzzle of length 3'
    },

    legend: {
        layout: 'vertical',
        align: 'left',
        verticalAlign: 'top',
        x: 150,
        y: 100,
        floating: true,
        borderWidth: 1,
        backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
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
            'P: 123, I: medium',
            'P: 000, I: medium',
            'P: 123, I: small',
            'P: 000, I: small',
            'P: 123, I: micro',
            'P: 000, I: micro'

        ]
    },
    yAxis: {
        title: {
            text: 'Time (s)'
        },
        labels: {
            formatter: function () {
                return this.value;
            }
        }
    },
    tooltip: {
        formatter: function () {
            return '<b>' + this.series.name + '</b><br/>' +
                this.x + ': ' + this.y;
        }
    },
    plotOptions: {
        area: {
            fillOpacity: 0.5
        }
    },
    credits: {
        enabled: false
    },
    series: [
    {
        name: '20 nodes',
        data: [
            9.92771794871795,
            9.45166666666667,

            22.675783919598,
            28.2784646464646,

            95.1089644670051,
            95.1089644670051
        ]
    },
        {
        name: '30 nodes',
        data: [
            8.79636040609137,
            9.85967980295566,

            20.2199086294416,
            31.9465577889447,

            94.7017936507936,
            83.8025677083333
        ]
    },
        {
        name: '40 nodes',
        data: [
            10.64002,
            10.9222474747475,

            22.7931155778894,
            26.4125612244898,

            114.138278947368,
            96.3400947368421
        ]
    }
    ]
});


Highcharts.chart('container3', {
    chart: {
        type: 'area',
        spacingBottom: 30
    },
    title: {
        text: 'Time per crypto puzzle'
    },

    legend: {
        layout: 'vertical',
        align: 'left',
        verticalAlign: 'top',
        x: 150,
        y: 100,
        floating: true,
        borderWidth: 1,
        backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
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
            'P: 0000, I: medium',
            'P: 0000, I: small'

        ]
    },
    yAxis: {
        title: {
            text: 'Time (s)'
        },
        labels: {
            formatter: function () {
                return this.value;
            }
        }
    },
    tooltip: {
        formatter: function () {
            return '<b>' + this.series.name + '</b><br/>' +
                this.x + ': ' + this.y;
        }
    },
    plotOptions: {
        area: {
            fillOpacity: 0.5
        }
    },
    credits: {
        enabled: false
    },
    series: [
    {
        name: '20 nodes',
        data: [
            6261.74841666667,
            13130.962
        ]
    },
        {
        name: '30 nodes',
        data: [
            7412.452,
            14052.2456
        ]
    },
        {
        name: '40 nodes',
        data: [
            1114.2,
            7974.00811111111
        ]
    }
    ]
});