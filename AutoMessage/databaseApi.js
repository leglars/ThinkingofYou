/**
 * Created by llegl on 2016/5/12.
 */

//var dbAPI = function() {
    var bodyParser = require('body-parser');

    var mysql = require('mysql');
    var connection = mysql.createConnection({
        host: 'localhost',
        user: 'root',
        password: '1936887',
        database: 'thinkingofyou'
    });

    var getNameByNumber = function(number) {
        var name;

        var query = connection.query("SELECT * from contact where contactnumber=?", number, function(err, rows, field){
            console.log("connection");
            if (err) {
                console.error(err);
                return;
            }
            if(rows.length == 1) {
                for (var row in rows) {
                    name = row.name;
                    return name;
                }

            }else{
                console.log("can't find the contact");
            }
        });

        name = query;
        console.log("this is name" + name);
    };
//};


module.exports.getNameByNumber = getNameByNumber;

