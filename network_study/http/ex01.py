#!/usr/bin/python
#%%
from http.server import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    
    
	#Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        
        self.wfile.write(bytes("Title goes here. <br>", "utf-8"))
        self.wfile.write(bytes("This is a test. <br>", "utf-8"))
        self.wfile.write(bytes("You accessed path: %s" % self.path, "utf-8"))
        self.wfile.write(bytes("<br>", "utf-8"))
    
        self.wfile.write("Hello World !<br>".encode())
		
        # Send the html message
		# self.wfile.write("Hello World !".encode())
        
        return
    
#%%
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print('Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print( '^C received, shutting down the web server')
	server.socket.close()
# %%
