$("#category_select").change(function() {
    var categoryID = $(this).find(":selected").val();
    var request = $.ajax({
        type: 'GET',
        url: '/models/' + categoryID + '/',
    });
    request.done(function(data){
        var option_list = [["", "--- Select One ---"]].concat(data);

        $("#exercise_select").empty();
        for (var i = 0; i < option_list.length; i++) {
            $("#exercise_select").append(
                $("<option></option>").attr(
                    "value", option_list[i][0]).text(option_list[i][1])
            );
        }
    });
});
