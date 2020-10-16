'strict';
exports.handler = async (event,contecxt,callback) => {
    try {
        var response= {}; 
        var discount= 99; // hardcoded.. could come from DB
        response = {
            statusCode: 200,
             body:JSON.stringify({'Discount': discount})
        };
        return response;
    }
    catch (err) {
        console.error(err);
    } 
};

