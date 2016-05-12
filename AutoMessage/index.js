

var sendMessage = require('./sendMessage');
var dbAPI = require('./databaseApi');
var twilio = require('twilio');

var firebase = require('firebase');
var myFirebaseRef = new firebase("https://burning-heat-7654.firebaseio.com/");

var express = require('express'),
	bodyParser = require('body-parser');


var app = express();

var server =  app.listen(3000, function(){
    var host = server.address().address;
    var port = server.address().port;
 	console.log('Example app listening at http://%s:%s', host, port);
 });

app.use(bodyParser.urlencoded({
	extended: true
}));
app.use(bodyParser.json());

app.get('/', function(req, res){
	res.render('index');
});

app.get('/send', function(req, res){
	var to = "+61478417108";
	var q2 = "Hello world";
	sendMessage(to, q2);

	res.send('the message should be sent to' + to);
});

app.get('/contact', function(req, res){
	var query = 'contact/' + "+61478416802" + '/name';
	myFirebaseRef.child(query).on('value', function (name) {
		res.send(name.val());
	});
});

app.post('/incoming', function(req, res){
    var q1 = "This is a test response from Leglars.";
	sendMessage(req.body.From, q1);
	res.end();
});

