/**
 * Created by chepe on 5/18/17.
 */

var options = {

    title: {
        text: 'Timeout vs Accuracy for different number of nodes (10m/s)'
    },

    yAxis: {
        title: {
            text: 'Accuracy'
        }
    },

    xAxis: {
        title: {
            text: 'Timeout (ms)'
        }
    },

    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    plotOptions: {
        series: {
            pointStart: 10
        }
    },
  series: [
  {
    name: '20 nodes',
    color: 'rgba(223, 83, 83, .5)',
    data: []

  }, {
    name: '30 nodes',
    color: 'rgba(119, 152, 191, .5)',
    data: []
  }, {
    name: '40 nodes',
    color: 'rgba(119, 182, 191, .5)',
    data: []
  }, {
    name: '50 nodes',
    color: 'rgba(19, 182, 191, .5)',
    data: []
  }, {
    name: '60 nodes',
    color: 'rgba(119, 182, 19, .5)',
    data: []
  }
  ]
};

function getData(i, id) {
    var url = "file:///Users/chepe/Sites/ec2testautomator/graphs/nodes" + id + ".json";
    return $.getJSON(url, function (data) {
        var points = [];

        $.each(data, function (i, item) {
            var tmp = new Array();
            tmp.push(item.timeout);
            tmp.push(item.accuracy);
            points.push(tmp);
        });

        options.series[i].data = points;
    })
};

console.log("Hey");

var ids = [ 20, 30, 40, 50, 60 ];
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