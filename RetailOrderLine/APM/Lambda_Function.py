import signalfx_lambda
import opentracing
from opentracing.ext import tags
from opentracing.propagation import Format


import json
import uuid
import os
APM_ENVIRONMENT = os.environ['SIGNALFX_APM_ENVIRONMENT']
LAMBDA_FUNCTION = os.environ['AWS_LAMBDA_FUNCTION_NAME']

@signalfx_lambda.is_traced(with_span=False)
def lambda_handler(event, context):
    # Setup tracer so we can create span and set the B3 Headers
    print ('event:')
    print (event)
    tracer = opentracing.tracer
    TraceHeaders =  event ['TraceHeaders']  # Value passed in from  calling app
    print ('TraceHeaders:')
    print (TraceHeaders)
    span_ctx = tracer.extract(Format.HTTP_HEADERS, TraceHeaders)
    print("span_ctx:")
    print (span_ctx)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER, "environment" : APM_ENVIRONMENT}
    with tracer.start_active_span(LAMBDA_FUNCTION , child_of=span_ctx, tags=span_tags):
        span = tracer.active_span #grabing the active span for Custom Tags
        print (span)
        with tracer.start_active_span(LAMBDA_FUNCTION+"_input", tags=span_tags) as scope:
            scopespan = scope.span
        
            #1 Read the input parameters
            productName = event['ProductName']
            quantity    = event['Quantity']
            unitPrice   = event['UnitPrice']
        
            #send tags and close span
            scopespan.set_tag("ProductName",productName)
            scopespan.set_tag("Quantity", quantity)
            scopespan.set_tag("UnitPrice", unitPrice)
            
         
        with tracer.start_active_span(LAMBDA_FUNCTION+"_transaction", tags=span_tags) as scope:
            scopespan = scope.span
         
            #2 Generate the Order Transaction ID
            transactionId   = str(uuid.uuid1())
    
            #send tags and close span
            scopespan.set_tag("TransactionId",transactionId)
            scope.close()
       
        with tracer.start_active_span(LAMBDA_FUNCTION+"_Logic", tags=span_tags) as scope:
            scopespan = scope.span
         
            #3 Implement Business Logic
            amount      = quantity * unitPrice
            
            #send tags and close span
            scopespan.set_tag("Amount",amount)
            scope.close()
            
        #optionally close the span
        span.finish()
        #4 Format and return the result
        return {
            'TransactionID' :   transactionId,
            'ProductName'   :   productName,
            'Amount'        :   amount
            
            }