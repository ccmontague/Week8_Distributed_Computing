This file will describe how the client-Server Architecture is set up and how to run the necessary files inside of it. For the purposes of the payment process system, my architecture is set up in the following way:

Merchant User Interface (Could be a Website): user_interface_client.py
	- Sends the GET and POST Request to the Server based on the input taken from the 		User

Merchant Server: simple_server.py
	- Receives the GET and POST Requests from the Client and sends the results to the 		credit card processor
	- Receives updated json information from the credit card processor and uses HTTP to 	respond to the 	Client.

Credit Card Processor: credit_card_processor_client.py
	- Receives the Request data from the Server and checks:
		1. If the payment amount is less than $350.
		2. If the expiration date is valid and not expired.
	- Based on these criteria, appends approval (True or False) and confirmation number 		to the json data
	- Sends new json body back to the server


To Run the Client-Server Architecture:
1. Ensure the three Python files described above are placed in the same directory.
2. Ensure all required libraries are installed.
3. Open a new terminal window and run the simple_server.py script in python from the directory where the files are located. (Ex: python -m simple_server)
4. In a second terminal window, run the user_interface_client.py script in python from the directory where the files are located. (Ex: python -m user_interface_client)
5. Fill out the inputs in the command line based on the requirements.
  - Name: N/A
  - Credit Card Number: Must be an integer of 16 digits (EX: 1234567890123456)
  - Expiration Date: MMYY Format. (Ex: 0221)
  - CVV: integer of 3 digits (Ex: 111)
  - Payment Amount: N/A  
4. You will receive a Successful GET Request and depending on your inputs, a Confirmation Number or Message telling you that the POST Request Failed.