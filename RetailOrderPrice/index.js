'use strict ';
const https = require('https');

// load environment variables
let API_URL = process.env.API_URL
let RETAIL_DISCOUNT_FUNCTION_NAME = process.env.RETAIL_DISCOUNT_FUNCTION_NAME
let STAGE = process.env.STAGE

// function to handle callback from HTTP call in Node JS
async function getDiscount(options) {
    return new Promise((resolve, reject) => {
        let body = "";
        const req = https.get(options, function(res) {
            res.on('data', chunk => {
                body += chunk;
                console.log("body: " + body);
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

exports.handler = async(event) => {
    try {
        let response = "";
        // Get Customer Type from  queryStringParameters
        let CustomerType = event.queryStringParameters.CustomerType;
        //  Setting Price hardcoded .. could fetch it from DataBase if required
        var price = 525;
        // give special customers a start discount
        if (CustomerType=="Gold" || CustomerType=="Platinum") {
            price = 499; 
        }
        
        /// Set option for an other HTTPS call top a LAMBDA
        var discount = 0; // No discount unless call returns it
        const options = {
            hostname: API_URL,
            port: 443,
            path: '/' + STAGE + '/' +  RETAIL_DISCOUNT_FUNCTION_NAME, // path is built from env vars and has / added between each paramater
            method: 'GET'
        };
        
        //Fetch discount
        discount = await getDiscount(options);
        
        // calc new price and send it back    
        var totalPrice = price - discount; // very complex Math taken place here
        
        response = {
            statusCode: 200,
            body: JSON.stringify({"Price": totalPrice })
            };
        return response;
    }
    catch (err) {
    console.error(err);
    }
};