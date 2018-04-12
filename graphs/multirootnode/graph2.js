/**
 * Created by chepe on 5/18/17.
 */

var options = {

    title: {
        text: ''
    },

    credits: false,

    yAxis: {
        title: {
            text: 'Accuracy'
        },
        max: 1,
        min: 0.60
    },

    xAxis: {
        title: {
            text: 'Nodes'
        },
        categories: ['20', '30', '40', '50', '60'],
        labels: {
            step: 10
        },
        min: 20,
        max: 60
    },

    // legend: false,

    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    plotOptions: {
        series: {
            pointStart: 20
        }
    },
    exporting: {
        width: 3000
    },
  series: [
  {
    name: 'single, t: 200',
    color: 'rgba(223, 83, 83, .5)',
    data: []

  }, {
    name: 'multi,  t: 200',
    color: 'rgba(119, 152, 191, .5)',
    data: []
  }, {
    name: 'single, t: 400',
    color: 'rgba(119, 182, 191, .5)',
    data: []
  }, {
    name: 'multi,  t: 400',
    color: 'rgba(19, 182, 191, .5)',
    data: []
  }
  ]
};

function getData(i, id) {
    var url = "file:///Users/chepe/Sites/ec2testautomator/graphs/" + id + ".json";
    return $.getJSON(url, function (data) {
        var points = [];

        $.each(data, function (i, item) {
            var tmp = new Array();
            tmp.push(item.nodes);
            tmp.push(item.accuracy);
            points.push(tmp);
        });

        options.series[i].data = points;
    })
};

console.log("Hey");

// var ids = [ 'multi_s_2_200', 'multi_m_2_200', 'multi_s_2_400', 'multi_m_2_400' ];
// var ids = [ 'multi_s_4_200', 'multi_m_4_200', 'multi_s_4_400', 'multi_m_4_400' ];
// var ids = [ 'multi_s_6_200', 'multi_m_6_200', 'multi_s_6_400', 'multi_m_6_400' ];
// var ids = [ 'multi_s_8_200', 'multi_m_8_200', 'multi_s_8_400', 'multi_m_8_400' ];
var ids = [ 'multi_s_10_200', 'multi_m_10_200', 'multi_s_10_400', 'multi_m_10_400' ];
var AJAX = [];
for (i=0; i < ids.length; i++) {
    console.log(ids[i]);
    AJAX.push(getData(i,ids[i]));
}


$.when.apply($, AJAX).done(function(){
    var obj = [];
    for(var i = 0, len = arguments.length; i < len; i++){
        obj.push(arguments[i][0]);
    }

    Highcharts.chart('container', options);
});