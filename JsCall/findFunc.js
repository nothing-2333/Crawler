const process = require('process');
const fs = require('fs');
const parser = require('@babel/parser');
const traverse = require('@babel/traverse').default;
const generator = require('@babel/generator').default;

// 获取文件名
const args = process.argv.slice(2);
let fileName = args[0] 
// let fileName = "Encrypt/encrypt.js"

// 获取函数列表
const code = fs.readFileSync(fileName, 'utf8');
const ast = parser.parse(code, {
  sourceType: 'module',
});
const globalFunctions = {};

traverse(ast, {
  FunctionDeclaration(path) 
  {
    if (path.parent.type == 'Program')  // 全局作用域
    {    
        // // 剔除函数中的标准输出
        path.traverse({
          	CallExpression(childPath)
			{
				let node = childPath.node;
				if (node["callee"] == undefined || node["callee"].type != "MemberExpression") return;
				if (node["callee"]["object"]["name"] != "console") return;

				childPath.remove();
			}
        });

		let name = path.get("id").node.name;
        let content = generator(path.node, {comments: false, minified: true}).code
        globalFunctions[name] = content
    }
  }
});

// 标准输出
console.log(JSON.stringify(globalFunctions));
