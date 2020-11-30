'use strict ';
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

exports.handler = async function(event, context) {
    try {
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
};