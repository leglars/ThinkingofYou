/**
 * Created by llegl on 2016/6/23.
 */

//  reload this page
var timeInterval = 8; // hours
var milliInterval = timeInterval * 3600 * 1000;
console.log(milliInterval);

setTimeout(function() {
    pageEventLogger.reloadLogger();
    location.reload(true);
}, 60000);

var pageEventLogger = {
    getUsername: function() {
        var url = $(location).attr('href').split("/");
        return url[url.length - 1]
    },

    getDatetime: function() {
        // Thu Jun 23 2016 16:37:49 GMT+1000 (东部澳大利亚标准时间)"
        return String(new Date()).split(" (")[0]
    },

    reloadLogger: function() {
        $.post("/device/report/page/reload", {
            username: this.getUsername(),
            datetime: this.getDatetime()})
            .done(function(data) {})
            .always()
    },

    pageStatusReporter: function() {
        $.post("/device/report/page/status", {
            username: this.getUsername(),
            visibilityStatus: document.visibilityState,
            datetime: this.getDatetime()})
            .done(function(data) {})
            .always()
    }
};


// the page is still working

// minimize or change tab
document.addEventListener("visibilitychange", function() {
    console.log(document.visibilityState);
    //if(document.hidden) {
    //    pageEventLogger.pageStatusReporter()
    //}else{
    //    pageEventLogger.pageStatusReporter()
    //}
    pageEventLogger.pageStatusReporter()
}, false);
