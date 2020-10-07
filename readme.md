# 第一周

###### 问题定义

- 图像JPEG和dicom格式在服务端的转换
- dockers以及项目的部署
- 实现的功能,以及其背后的原理,效仿OHIF

###### 任务分工

- 周和杨的前端react学习,我和唐的后端学习

# 第二周

###### 开会总结第一周(周有事请假)

唐docker学了点,杨react学了点,我买了半年的1核2G带宽1M的阿里云服务器,自己练了练linux常用命令.也部署了一些相关的东西,离完成项目还很远,大家加油

###### 新任务

杨和周要把react再学深一点,我和唐要把docker再多学一点,尝试把OHIF的项目部署在docker镜像中,并实现网页的浏览,后端本应是像前端提供算法等接口的API,但我们基础还很差,目标还很遥远

本周进度

1. 服务器使用OHIF-REACT

   - 首先将文件上传

     ![image-20200722114516581](%E9%A1%B9%E7%9B%AE%E5%8E%86%E7%A8%8B.assets/image-20200722114516581.png)

   - npm install

   - npm start

   - curl  http://localhost:3000

     ![image-20200722121846574](%E9%A1%B9%E7%9B%AE%E5%8E%86%E7%A8%8B.assets/image-20200722121846574.png)

   ```html
   <!doctype html>
   <html lang="en">
   
     <head>
       <meta charset="utf-8">
       <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
       <meta name="theme-color" content="#000000">
   
       <link rel="manifest" href="/manifest.json">
   
       <title>OHIF Viewer</title>
   
       <!-- Latest compiled and minified CSS -->
       <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
   
       <!-- WEB FONTS -->
       <link href="https://fonts.googleapis.com/css?family=Sanchez" rel="stylesheet">
       <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css" integrity="sha384-UHRtZLI+pbxtHCWp1t77Bi1L4ZtiqrqD80Kn4Z8NTSRyMA2Fd33n5dQ8lWUE00s/"
       crossorigin="anonymous">
     </head>
   
     <body>
       <noscript>
         You need to enable JavaScript to run this app.
       </noscript>
   
       <div id="root"></div>
     <script src="/static/js/bundle.js"></script><script src="/static/js/0.chunk.js"></script><script src="/static/js/main.chunk.js"></script></body>
   
   ```

   

2. node

