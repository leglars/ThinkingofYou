/**
 * Created by llegl on 2016/5/13.
 */

$(document).ready( function() {
    $.ajax({
        type:"GET",
        url:"http://localhost:3000/contact",
        dataType: "json",
        success: function(data) {
            console.log(data);
        }
    })
});