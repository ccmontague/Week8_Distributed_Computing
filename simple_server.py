#!/usr/bin/env python3
"""
This code is a simple HTTP server in python for serving static files and POST requests. 
This server will receive get and post requests from the user_interface_client.py inputs. The get request will send back a reponse with json attached that the client can parse.
The post request will be parsed and then sent to the credit_card_processor_client.py that acts as the authorizing body for the payment request. This script will return appended 
json to the server, which will then send that repsonse to the user_interface.

Based on:
Author: Rob Judd
File:   simple_server.py

Edited by:
Author: Courtney Montague
Date: 10/2/20
"""

from http.server import SimpleHTTPRequestHandler, HTTPServer
import logging
import urllib.parse
import os.path
import json
from credit_card_processor_client import *

class HTTPRequestHandler(SimpleHTTPRequestHandler):
    """ HTTP request handler """

    def _set_response(self):
        """Sends additional headers and marks the response as ready to send the body."""
        self.send_response(200)    # <-- 200 status code means success
        self.send_header('Content-type', 'application/json')   # <-- marks the content type to be sent as json
        self.send_header('Accept', 'application/json')         # <-- marks the accept type as json
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        request = urllib.parse.urlparse(self.path)
        file = self.directory + request.path

        if os.path.exists(file):
            # Log the request
            logging.info("GET request,\nPath: %s\nHeaders:\n%s\n",
            str(self.path), str(self.headers))
            # Create the json data to send back
            get_data_json = json.dumps({"Get Request": "Successful"})
            # Set the headers and status
            self._set_response()
            # Send the response
            self.wfile.write(get_data_json.encode('utf-8'))
        else:
            logging.info("GET request,\nPath: %s\nHeaders:\n%s\n",
                         str(self.path), str(self.headers))
            logging.info("File %s not found.", file)
            self._set_response()
            self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):

        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))
        
        """
        Read the Path name and make sure that it is equal to make-payment. 
        If it is, continue with processing the payment. If it is not, give error.
        """

        if self.path == "/make-payment":
            """
            Send the json to the credit card processor client, who will determine whether the payment is accepted or declined. 
            To see the credit card processor client logic, see the Credit_Card_Processor_Client.py script. This script will
            send back an appended json message with accept or decline and a comfirmation number or error.
            """
            # Parse json to a python dictionary that the program can use
            post_data = json.loads(post_data)
        
            # Send json to the credit card processor and get back appended json response
            authorization_response = authorize_payment(post_data)

            # Encode the returned data
            data = authorization_response.encode('utf-8')
            # Call the set_response function that sets the HTTP response headers
            self._set_response()
            # Write the body of the response in JSON and return to the user
            self.wfile.write(data)
        else:
            print("The Path was incorrect.")
        



def run(server_class=HTTPServer, handler_class=HTTPRequestHandler, port=8000):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
