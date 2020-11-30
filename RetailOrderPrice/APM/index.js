'use strict ';
const signalFxLambda = require('signalfx-lambda');
const tracing = require('signalfx-lambda/tracing'); // needed if we wish to set our own tags an/or wish to call other lambda's
const https = require('https');

// function to handle callback from HTTP call in Node JS
async function getDiscount(options) {
    return new Promise((resolve, reject) => {
        let body = "";
        const req = https.get(options, function(res) {
            console.log('statusCode: ' + res.statusCode);
            res.on('data', chunk => {
                body += chunk;
                console.log("body: "+ body);
            });
            res.on('error', error => {
                console.error(error);
                // If failed
                reject(error);
            });
            res.on('end', () => {
                resolve(JSON.parse(body).Discount);
        });
    
        });
    });
}

exports.handler = signalFxLambda.asyncWrapper(async(event, context) => {
    try {
        let response ="";
        const tracer = tracing.tracer(); // get the active tracer (only if you wish to use custom tags or call other lambda's)
        if (tracer) {
            console.log("We have a tracer")
        }
        else {
            console.error("No Tracer")
            response = {
                statusCode: 500,
                headers: {},
                body: "Tracer not available"
            };
            return response;
        }
        const span = tracer.scope().active(); // get the active span (only if you wish to use custom tags)
        if (span) {
            console.log("We have a span")
            //We now can use span.setTag("tag_label", value) to set your own tags
            span.setTag("Custom tag", "custom value")
        }
        else {
            console.error("No span")
            response = {
                statusCode: 500,
                headers: {},
                body: "Span not available"
            };
            return response;
        }
        //  Setting Price hardcoded .. could fetch it from DataBase if required
        var price = 499;
        
        /// Set option for an other HTTPS call to a LAMBDA
        var discount_Hostname = process.env.DISCOUNT_HOST;
        var discount_Path = process.env.DISCOUNT_PATH;
        var discount = 0; // No discount unless call returns it
        const options = {
            hostname:  discount_Hostname,
            port: 443,
            path: discount_Path,
            method: 'GET'
        };

        //Fetch discount
        discount = await getDiscount(options);
        
        // calc new price and send it back    
        var totalPrice = price - discount;
        var response = {
            statusCode: 200,
            body: JSON.stringify({'Price':totalPrice})
        };
        return response;
    }
    catch (err) {
        console.error(err);
    }
});