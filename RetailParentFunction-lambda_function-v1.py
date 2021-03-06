import signalfx_lambda
import opentracing
import os

import json
import boto3


# Define the client to interact with AWS Lambda
client = boto3.client('lambda')

APM_ENVIRONMENT = os.environ['SIGNALFX_APM_ENVIRONMENT'] # The Environment Tag is used by Splunk APM to filter Environments in UI
CHILD_FUNCTION_ARN = os.environ['CHILD_FUNCTION_ARN']

@signalfx_lambda.emits_metrics()
@signalfx_lambda.is_traced()

def lambda_handler(event,context):
    # Setup tracer so we can create spans and retrieve the B3 Headers
    tracer = opentracing.tracer
    TraceHeaders = {} # Here we will store the B3 Headers needed for manual Propagation if required    
    signalfx_lambda.tracing.inject(TraceHeaders) # Retrieving B3 Headers and injecting them into the trace header array
    
    # Define / read input parameters
    Name     = event['ProductName'] # Value passed in from test case
    Quantity = event['Quantity']    # Value passed in from test case
    Price    =  499                 # Value hard coded - just as an example

    span = tracer.active_span # Grabbing the active span so we can add tags to it
    
    # Adding tags
    span.set_tag("environment"          , APM_ENVIRONMENT)
    span.set_tag("ProductName"          , Name)
    span.set_tag("Quantity"             , Quantity)
    span.set_tag("UnitPrice"            , Price)
    span.set_tag("ChildFunction arn"    , CHILD_FUNCTION_ARN)
 
    # Define the input parameters that will be passed on to the child function
    inputParams = {
        "ProductName"   : Name ,
        "Quantity"      : Quantity,
        "UnitPrice"     : Price,
        "TraceHeaders"  : TraceHeaders # Add the TraceHeaders as an input parameter so it can be used by the Lambda being called
    }

    # Invoking Lambda directly
    response = client.invoke(
        #FunctionName = 'arn:aws:lambda:eu-west-1:527477237977:function:RetailChildFunction', # This could be set as a Lambda Environment Variable
        FunctionName = CHILD_FUNCTION_ARN,
        InvocationType = 'RequestResponse',
        Payload = json.dumps(inputParams)
    )

    responseFromChild = json.load(response['Payload'])
 
    print('\n')
    print(responseFromChild)