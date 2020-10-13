## 简述

​	 开源中国社区中对于Orthanc有一段这样的描述：**Orthanc是一个轻量级的，基于REST的DICOM服务器，主要用于卫生保健和医疗研究**。Orthanc可将任意运行Windows和Linux的计算机编程DICOM存储（或者说是一个小型PACS系统），其架构是轻量级的，没有复杂的数据库管理，不依赖于第三方软件。除此以外，Orthanc官网（http://www.orthanc-server.com/about.php）对于Orthanc的描述着重提到：**Orthanc之所以与众不同是因为它提供RESTful API**。因此Orthanc可以使用任何计算机语言开发。Orthanc存储的DICOM图像的标签可以以JSON文件格式下载，此外，Orthanc对于存储的DICOM实例可以动态生成对应的PNG图像.Orthanc隐藏了复杂的DICOM文件格式和DICOM协议，使使用者只专注于DICOM文件内容。

[orthanc-book](https://book.orthanc-server.com/index.html)

### linux/云服务器体验

centos下使用docker将orthanc-web 运行再8042/4242端口

```bash
docker run -p 4242:4242 -p 8042:8042 --rm jodogne/orthanc
```

### 关于source

cmake编译,framework大部分是c和c++,server是js和html,

### 关于license

- Orthanc is licensed under the GPLv3 license
- The files of the "./OrthancFramework/Sources/" directory are
  licensed under the LGPLv3 (Lesser GPL) since Orthanc 1.7.2. 
- The files of the "./OrthancFramework/Sources/SQLite/" directory are
  licensed under the 3-clause BSD license, as they are derived from
  the Chromium project.