$(document).ready(function() {

    $("#search-button").click(function() {
        $.get( "analyze/" + $("#query-input").val())
          .done(function( status ) {
             console.log( "Status: " + status );
             start_fetching();
          });
    });

    function start_fetching() {
            setTimeout(function() {
                do_fetch();
            }, 1000);
    }

    function do_fetch() {
        $.get( "fetch" )
          .done(function( json ) {
             console.log( json );
             var obj = JSON.parse(json);

             if (obj.error != undefined) {
                console.log("Error: empty list");
                return;
             }

             $("#pos").html(obj.pos.toFixed(2) + " %");
             $("#neg").html(obj.neg.toFixed(2) + " %");
          })
          .always(function() {
            start_fetching();
          });
    }

    $(document).on("keypress", "#query-input", function(e) {
     if (e.which == 13) {
        $("#search-button").click()
     }});
});