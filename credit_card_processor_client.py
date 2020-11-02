"""
This code acts as the credit card processor client in the payment processing system.
When ther server receives json from the user interface, it will extract the json from the body of the post message and send it to the credit card processor.
The credit card processor will then determine whether the payment is accepted or declined, and send back a confirmation code. It will append this information
to the json request that arrived and send back json to the server. The server will then return the appended json package to the client.

Author: Courtney Montague
Date: 10/2/20
"""

from datetime import datetime
import json, random, string

def authorize_payment(post_data):
    # Call the check credentials script to make sure the payment details are correct
    allow_payment = check_credentials(post_data)

    # Determine whether the payment was accepted or not, and if it was create a confirmation number
    if allow_payment == True:
        # Call confirmation number function
        con = confirmation_number()
    # If the payment was declined, send the User back a message saying that it was declined.
    else:
        con = "Your Card was Declined. Please try again."

    # Append Confirmation Number to the JSON to be sent back to the user
    post_data['allow_payment'] = allow_payment
    post_data['confirmation_number'] = con
    return json.dumps(post_data)


def check_credentials(post_data):
    # Check that the payment is under "maximum_payment" dollars
    amount = float(post_data['paymentamount'])
    maximum_payment = float(350)
    # Check that the card is not expired
    expiration_month = post_data["expiremonth"]
    expiration_year = post_data["expireyear"]
    today = datetime.now()

    # Loop to check amount of the purchase
    if amount < maximum_payment:
        allowed = True
    else:
        allowed = False
    # if loop to check card expiration
    if allowed == True:
        # if the current year is less than the exp year and the expiration year is less than 25 (assuming there can be an expiration date out 5 years) give true
        if int(today.year) < int(expiration_year) and int(expiration_year) < 2025:
            return True
        # if the current year is equal to the expiration year and the current month is less than the expiration month and the month is valid give true
        elif int(today.year) == int(expiration_year) and int(today.month) <= int(expiration_month) and int(expiration_month) <= 12 and int(expiration_month) > 0:
            return True
        else:
            return False
    else:
        return False

# Here we'll make up some data to respond with and send it back to the caller.
def confirmation_number():
    size = 6
    letters = string.ascii_uppercase + string.digits
    confirmation_result =  ''.join(random.choice(letters) for i in range(size))
    return confirmation_result
    #print("Your Confirmation Number is:", confirmation_result)