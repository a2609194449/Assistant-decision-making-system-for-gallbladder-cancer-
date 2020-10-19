### 流程如下:

1. fork 上游仓库例如https://github.com/OHIF/Viewers

   fork至自己的github仓库https://github.com/ajn404/Viewers
   (前提是你已经注册并登录了自己的github,就像我的账号是[ajn404](https://github.com/ajn404))

2. git clone https://github.com/ajn404/Viewers,创建本地文件夹,称为本地库

3. 本地创建分支dev(该分支用于开发你的远程库):添加并切换到分支git checkout -b div;或者首先添加分支git branch dev 然后切换到分支git checkout dev

4. 创建upstream分支用于同步上游库,用来同步其他人对上游仓库的更改:git remote add upstream https://github.com/OHIF/Viewers

   注:可以使用git remote -v 查看具体关联库

5. 同步上游仓库:git remote update upstream

   ​						git rebase upstream/main

6. git add *

   git commit -m "你的修改内容记录"

   git push origin dev

   以上就是将你的更改同步到你自己fork的远程库的代码

7. 之后点击new pull request 就可以等待我review你的代码后merge入上游仓库了

8. 之后就是我的事情了

[git操作图解](https://github.com/ajn404/web_developer_daily/blob/main/git/gitcheatsheet.png?raw=true)	

**reference:**
[github:](https://docs.github.com/en)
知乎: [图文详解如何利用Git+Github进行团队协作开发](https://zhuanlan.zhihu.com/p/23478654)

- 关于第五步,也可以直接使用git pull upstream main
- 有什么不懂的可以在issues里讨论
- git command --help也不失为良策