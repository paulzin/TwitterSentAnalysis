$(document).ready(function() {
    var chart;
    var graph_is_shown = false;

    $("#graph").hide();
    $("#progressbar").hide();
    $("#tweet_container").hide();

    $("#search-button").click(function() {
        stop_fetching();
        $.get( "analyze/" + $("#query-input").val())
          .done(function( status ) {
             console.log( "Status: " + status );
             $("#graph").hide();
             $("#tweet_container").hide();
             $("#progressbar").show();
             start_fetching();
          });
    });

    function start_fetching() {
            setTimeout(function() {
                do_fetch();
            }, 1000);
    }

    function stop_fetching() {
        $.get( "stop" ).done(function( resp ) {
            console.log("STOPPING: " + resp);
        });
    }

    function do_fetch() {
        $.get( "fetch" )
          .done(function( json ) {
             console.log( json );
             var obj = JSON.parse(json);

             if (obj.error != undefined) {
                return;
             }

             $("#progressbar").hide();
             $("#graph").show();

             $("#tweet_container").show();

             $("#pos-tweet").text(obj.last_pos_tweet);
             $("#neg-tweet").text(obj.last_neg_tweet);

             if (!graph_is_shown) {
                init_graph();
             }

             console.log("pos " + obj.pos.toFixed(2) + " neg " + obj.neg.toFixed(2))

             chart.series[0].setData([
                             {
                                name: 'Positive',
                                y: obj.pos
                            }, {
                                name: 'Negative',
                                y: obj.neg
                            }
                         ]);
          })
          .always(function() {
            start_fetching();
          });
    }

    $(document).on("keypress", "#query-input", function(e) {
     if (e.which == 13) {
        $("#search-button").click()
     }});

    function init_graph() {
        graph_is_shown = true;
        chart = new Highcharts.Chart({
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie',
                renderTo: 'graph'
            },

            title: {
                text: 'Real-time Tweets Tonality Analysis'
            },

            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },

            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    colors: ["#009688", "#424242"],
                    chart: {
                       backgroundColor: null,
                       style: {
                          fontFamily: "Roboto"
                       }
                    },
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                        style: {
                            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                        }
                    }
                }
            },

            series: [{
                colorByPoint: true,
                data: [ {
                    name: 'Positive',
                    y: 0.6
                }, {
                    name: 'Negative',
                    y: 0.4
                }]
            }]
        });
    }

    $(window).bind('beforeunload', function() {
        stop_fetching();
        return 'Stop discovering new tweets about this brand?';
    });
});