/**
 * Created by llegl on 2016/6/20.
 */

// Since ToY need to do DOM operation, popping up a feedback to tell user the message has been sent after clicking,
// using JS to init a HTTP request and get a response, sending successfully, then manipulate DOM is a better solution.

$(document).ready(function() {
    var photo = $(".img-thumbnail");
    photo.click(function() {
        var name = $(this).attr("alt").split(" ");  // alt stores the note of photo
        var contact = name[0];
        var url = $(location).attr('href').split("/");
        var userName = url[url.length - 1];
        var query = {
                        contact: contact,
                        user: userName
                    };

        $.post(
            "/thinkingofyou", query, function(data) {
                console.log(data)
            },
            "text"
        )

    })
});