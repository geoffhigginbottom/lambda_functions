import json
import uuid
import os
APM_ENVIRONMENT = os.environ['SIGNALFX_APM_ENVIRONMENT']
LAMBDA_FUNCTION = os.environ['LAMBDA_FUNCTION_NAME']

def lambda_handler(event, context):
    print ("event: " , event)
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