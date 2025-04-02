global.require = require;   // 正确处理 require

function rpc(port)
{
    const net = require('net');

    // 启动服务
    const server = net.createServer((socket) => {
        socket.on('data', (data) => {
            let { funcName, args } = JSON.parse(data.toString())
            let response = ""
    
            // 动态调用函数
            if (funcName != undefined)
            {
                let func = eval(funcName);
                const result = func.apply(null, args);
                response = JSON.stringify({ result });
            }

            const length = Buffer.byteLength(response);
            response = length.toString().padStart(4, '0') + response

            // console.log(funcName, args, response);
            socket.write(response);
        });
    });
    
    server.listen(port, '127.0.0.1');
}

rpc(+process.argv[2])
