function test(data)
{
    const crypto = require('crypto');
    console.log(crypto.randomBytes(1)[0]);
    
    return JSON.stringify(data)
}


