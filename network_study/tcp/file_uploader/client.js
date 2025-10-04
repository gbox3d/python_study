var net = require('net');
const fs = require('fs');
const { EOF } = require('dns');

//var HOST = '127.0.0.1';
//var PORT = 8081;

var HOST = 'localhost';
var PORT = 8181;


var client = new net.Socket();
client.connect(PORT, HOST, function() {

    console.log('CONNECTED TO: ' + HOST + ':' + PORT);

    let upload_fn='Lenna.png'
    client.write(JSON.stringify({fn:upload_fn,th:0.5}));
    
    let data = fs.readFileSync(`../../../res/${upload_fn}`);
    
    client.write(data);
    client.end()
    // client.write(EOF)
    // client.destroy();
    // client.destroy()
});

// Add a 'data' event handler for the client socket
// data is what the server sent to this socket
client.on('data', function(data) {

    console.log('DATA: ' + data);
    // Close the client socket completely
    client.destroy();

});

// Add a 'close' event handler for the client socket
client.on('close', function() {
    console.log('Connection closed');
});