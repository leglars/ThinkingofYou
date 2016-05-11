var accountSid = 'ACd7a0898f812377ef06121f8611f11b1e';
var authToken = 'eaae9bf97f64e5d844d5c65247216220';

var client = require('twilio')(accountSid, authToken);


function sendMessage(to, question) {
	client.messages.create({
		to: to,
		from: "+61400357926",
		body: question,
	}, function(err, message) {
		console.log(err);
		console.log(message.sid);
	});
}

module.exports = sendMessage;