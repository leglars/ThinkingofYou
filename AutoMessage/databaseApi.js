/**
 * Created by llegl on 2016/5/12.
 */


var bodyParser = require('body-parser');
var firebase = require('firebase');
var myFirebaseRef = new firebase("https://burning-heat-7654.firebaseio.com/");

var mysql = require('mysql');
var connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '1936887',
    database: 'thinkingofyou'
});

var dbAPI = {
    getNameByNumberMysql: function (number) {
        var name;

        var query = connection.query("SELECT * from contact where contactnumber=?", number, function (err, rows, field) {
            console.log("connection");
            if (err) {
                console.error(err);
                return;
            }
            if (rows.length == 1) {
                console.log(rows);
                for (var row in rows) {
                    name = row.name;
                    return name;
                }

            } else {
                console.log("can't find the contact");
            }
        });

        console.log(query);
    },

    getNameByNumberFirebase: function (number) {
        var query = 'contact/' + number + '/name';
        myFirebaseRef.child(query).on('value', function (name) {
            console.log(name.val());
        })
    },

    whetherContactLogFirebase: function (name, replay) {

    }
};


module.exports = dbAPI;

