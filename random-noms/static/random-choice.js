$(document).ready(function() {
    $("#rand_restaurant").click(function() {
        $.ajax("/random_restaurant/JSON/").done(function(rest_data) {
            rest_name = rest_data.name;
            rest_id = rest_data.id;
            rest_url = "/restaurant/" + rest_id + "/menu";
            rest_link = "<a href=" + rest_url + ">" + rest_name + "</a>";
            $("#random_choice").html(rest_link);
            $("#random_choice").addClass("random_choice");
            $("#rand_restaurant").html("Try again");
        });
    });
});
/*
(function($) {
})(jQuery);
*/
