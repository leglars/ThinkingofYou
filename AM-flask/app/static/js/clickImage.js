/**
 * Created by llegl on 2016/6/20.
 */

// Since ToY need to do DOM operation, popping up a feedback to tell user the message has been sent after clicking,
// using JS to init a HTTP request and get a response, sending successfully, then manipulate DOM is a better solution.

var POST_ERROR_TIME = 0;
var POST_ERROR_LIMIT = 2;


$(document).ready(function () {
    var photo = $(".img-thumbnail");

    photo.click(function () {
        maskStatus.disableClick();
        console.log("mask disabled");

        var name = $(this).attr("alt").split(" ");  // alt stores the note of photo
        var contact = name[0];
        var url = $(location).attr('href').split("/");
        var userName = url[url.length - 1];

        var query = {
            contact: contact,
            user: userName
        };

        // if post fail, app will tell user touch again
        // but if post fail several times, like 2, report the error:   systemError.postErrorReport
        $.post(
            "/thinkingofyou", query)
            .done(function (data) {
                console.log(data);
                if (data == "success") {
                    // toastNotification will release the mask
                    thinkingofyouMessageStatus.successNotification();
                } else {
                    thinkingofyouMessageStatus.failNotification();
                }
            })
            .fail(function(xhr, textStatus, errorThrown) {
                POST_ERROR_TIME ++;
                systemError.postErrorReport(query);
                thinkingofyouMessageStatus.failNotification();
            })

    });
});

var maskStatus = {
    disableClick: function () {
        $("#mask").show()
    },
    enableClick: function () {
        $("#mask").hide()
    }
};

var thinkingofyouMessageStatus = {

    pending: function () {
        console.log("wait response")
    },

    failNotification: function() {
        $("#successFeedback").hide();
        $("#failFeedback").show();
        this._toastNotification();
    },

    successNotification: function() {
        $("#successFeedback").show();
        $("#failFeedback").hide();
        this._toastNotification();
    },

    _toastNotification: function () {
        var notification = $("#notification");
        $(notification).animate(
            {
                opacity: 1,
                bottom: "36px"
            }, {
                duration: 500,
                easing: "easeInOutQuint",
                complete: fadeOut()
            });

        function fadeOut() {
            var delay = 2000;
            setTimeout(function () {
                $(notification).animate(
                    {
                        opacity: 0,
                        bottom: "10px"
                    }, {
                        duration: 500,
                        easing: "easeInOutQuint",
                        complete: maskStatus.enableClick(),
                        done: function() {
                            console.log("mask enabled")
                        }
                    })
            }, delay)
        }
    }
};


var systemError = {
    postErrorReport: function(query) {
        // if post error happened twice, fire the report
        if (POST_ERROR_TIME >= POST_ERROR_LIMIT) {
            $.post(
            "/thinkingofyou/error/report", query)
            .done(function (data) {
                POST_ERROR_TIME = 0;  // success report, clean the calculator.
            })
            .fail(function(xhr, textStatus, errorThrown) {
                // retry every 60s
                var timeInterval = 60000;
                setTimeout(function() {
                    this.postErrorReport(query)
                }, timeInterval)
            })
        }
    },


};
