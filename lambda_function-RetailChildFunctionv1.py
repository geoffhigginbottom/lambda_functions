import signalfx_lambda
import opentracing

import json
import uuid
import os
from opentracing.propagation import Format

APM_ENVIRONMENT = os.environ['SIGNALFX_APM_ENVIRONMENT'] # The Environment Tag is used by Splunk APM to filter Environments in UI
FUNCTION_NAME = os.environ['AWS_LAMBDA_FUNCTION_NAME'] # Stores the name of the Lambda Function for use later on

@signalfx_lambda.emits_metrics()
#@signalfx_lambda.is_traced()
@signalfx_lambda.is_traced(with_span=False) # Set to False as we will manually create a span in this Lambda Function

def lambda_handler(event, context):
    # Setup tracer so we can create span and set the B3 Headers
    tracer = opentracing.tracer
    parent = tracer.extract(Format.HTTP_HEADERS,event['TraceHeaders']) # Retrieve the trace headers for propagation from the calling Lambda Function

    with tracer.start_active_span(FUNCTION_NAME + "_sub",child_of=parent) as scope: # Start and name the span the same as the name of the Lambda Function
        span = scope.span
        span.set_tag("environment", APM_ENVIRONMENT)
        
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