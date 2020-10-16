import json
import uuid
import os

def lambda_handler(event, context):
    # Setup tracer so we can create span and set the B3 Headers

        #1 Read the input parameters
        productName = event['ProductName']
        quantity    = event['Quantity']
        unitPrice   = event['UnitPrice']
        
        #2 Generate the Order Transaction ID
        transactionId   = str(uuid.uuid1())

        #3 Implement Business Logic
        amount      = quantity * unitPrice
     
        #4 Format and return the result
        return {
            'TransactionID' :   transactionId,
            'ProductName'   :   productName,
            'Amount'        :   amount
        }