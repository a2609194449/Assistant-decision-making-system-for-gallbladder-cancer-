var fs = require("fs");
fs.readFile("file.txt", "utf-8", function (err, data) {
  if (err) console.error(err);
  else console.log(data);
});

console.log("end");


// fs.readFile()函数第三个参数是回调函数,异步IO就是通过回调函数来实现的

// fs.readFile()的作用只是将异步IO请求发送给操作系统,然后立即返回并执行后面的语句,执行完以后进入事件循环监听事件
// nodejs并不是所有的API都同时提供异步和同步版本,不鼓励使用同步
