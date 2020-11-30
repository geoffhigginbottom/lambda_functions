import os
import json
import boto3
import requests


# The Environment Tag is used by Splunk APM to filter Environments in UI
APM_ENVIRONMENT = os.environ['SIGNALFX_APM_ENVIRONMENT']
PRICE_URL       = os.environ['PRICE_URL']
ORDER_LINE      = os.environ['ORDER_LINE']

# Define the client to interact with AWS Lambda
client = boto3.client('lambda')

def lambda_handler(event,context):
    print("event received :", event)
        
    # Define / read input parameters from the event trigger
    Name         =  json.loads(event ['body']).get("ProductName")  # Value passed in from test case
    Quantity     =  json.loads(event ['body']).get("Quantity")     # Value passed in from test case
    CustomerType =  json.loads(event ['body']).get("CustomerType") # Value passed in from test case
  
    # Call Node-JS lambda via Api Gateway to get the Price
       
    payload = {'CustomerType': CustomerType}
    r = requests.post(PRICE_URL,  params=payload)
    print( "Price Url: ",r.url)
    print( "Price Payload: ",r.text)  
    
    #Get Price from response   
    Price =  json.loads(r.text).get('Price') # Get Value from the Price calculator       
    print("Price: ",Price)
    
    # Define the input parameters that will be passed on to the child function
    inputParams = {
        "ProductName" : Name ,
        "Quantity"    : Quantity,
        "UnitPrice"   : Price
    }
    print (inputParams)
    # Invoking Lambda directly
    response = client.invoke(
        FunctionName = ORDER_LINE, # This could be set as a Lambda Environment Variable
        InvocationType = 'RequestResponse',
        Payload = json.dumps(inputParams)
    )

    responseFromOrderLine = json.load(response['Payload'])
    print (responseFromOrderLine)
    newPrice = responseFromOrderLine.get('Amount')
    print ("Price:" , newPrice)
    transactionID =  responseFromOrderLine.get('TransactionID')
    print ("transactions id:",  transactionID)
    retval={'phoneType'     : Name,
            'quantity'      : Quantity,
            'customerType'  : CustomerType,
            'price'         : newPrice,
            'transaction'   : transactionID
            }
    return {
            'statusCode': 200,
            'body': json.dumps(retval)
            
        }