
$(document).ready(function() {

    // Posting messages asynchronously
    $("#message-form").submit(function(event) {
        event.preventDefault();
        var form = $(this)
        $.post(form.attr("action"), form.serialize()).done(function() {
            form.find('#message-input').val("");
        });
    });

    // Listening to the publisher
    var stream = new EventSource('/stream');
    stream.onmessage = function(event) {
        var message = $("<li></li>");
        message.text(event.data);
        $("#messages").prepend(message);
    };

});

