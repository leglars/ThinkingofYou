var sendMessage = require('./sendMessage');

var q1 = "This is a test response from Leglars."


var twilio = require('twilio');
var resp = new twilio.TwimlResponse();

var express = require('express'),
	bodyParser = require('body-parser');


var app = express();

app.use(bodyParser.urlencoded({
	extended: true
}));

app.get('/', function(req, res){
	res.send('Hello world!');
});

app.get('/send', function(req, res){
	var to = "+61478417108";
	var q2 = "Hello world";
	sendMessage(to, q2);

	res.send('the message should be sent to' + to);
});

app.post('/incoming', function(req, res){
	sendMessage(req.body.From, q1);
	res.end();
});

// app.listen(3000, function(){
// 	console.log('Example app listening on port 3000!');
// });