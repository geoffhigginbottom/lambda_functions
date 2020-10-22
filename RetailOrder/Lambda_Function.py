import os
import json
import boto3
import urllib3
import urllib.request

# Define the client to interact with AWS Lambda
client = boto3.client('lambda')

URL_STRING = os.environ['URL_STRING']
CHILD_FUNCTION_ARN = os.environ['CHILD_FUNCTION_ARN']

def lambda_handler(event,context):
    print(event)

    # Define / read input parameters from the event trigger
    Name         =  json.loads(event ['body']).get("ProductName")  # Value passed in from test case
    Quantity     =  json.loads(event ['body']).get("Quantity")     # Value passed in from test case
    CustomerType =  json.loads(event ['body']).get("CustomerType") # Value passed in from test case
  
    # Call Node-JS lambda via Api Gateway to get the Price
    http = urllib3.PoolManager()
    r = http.request('GET', URL_STRING +"/RetailOrderPrice?CustomerType="+CustomerType)
    
    #Get Price from response   
    Price = json.loads(r.data.decode('utf-8')).get("Price") # Get Value from the Price calculator
  
    # Define the input parameters that will be passed on to the child function
    inputParams = {
        "ProductName" : Name ,
        "Quantity"    : Quantity,
        "UnitPrice"   : Price
    }
    print (inputParams)
    # Invoking Lambda directly
    response = client.invoke(
        # FunctionName = 'RetailOrderLine', # This could be set as a Lambda Environment Variable
        # FunctionName = 'arn:aws:lambda:eu-west-3:527477237977:function:Retail_Order_Line_60241d24',
        FunctionName = CHILD_FUNCTION_ARN,
        InvocationType = 'RequestResponse',
        Payload = json.dumps(inputParams)
    )

    responseFromOrderLine = json.load(response['Payload'])
   
    return 
    {
        "isBase64Encoded": false,
        "statusCode": 200,
        "body": {
            'phoneType'     : Name,
            'quantity'      : Quantity,
            'customerType'  : CustomerType,
            'price'         : responseFromOrderLine.get('Amount'),
            'transaction' : responseFromOrderLine.get('TransactionID')
        },
        "headers": {
            "Content-Type": "application/json"
        }
    }
