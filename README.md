# JenkinsUnityPyAutoMator
## 介绍
***通过Jenkins服务使用python语言来对Unity和周边进行构建和自动化操作***
## 说明
每个项目各不相同，可以参考我其中的具体实现，举一反三实现你的功能

~尽可能不使用python的库，大多数使用的命令行，避免Jenkins有多台节点机器时，复杂麻烦的python环境，docker暂时没去研究~
- - -
## 环境
+ Python 3.7+ [Python官网地址](https://www.python.org/)
+ Jenkins [Jenkins官网地址](https://www.jenkins.io/)下载Generic Java package (.war) 轻量包
+ Java [java官网下载地址](https://www.oracle.com/java/technologies/downloads/) 下载java并且配置环境变量
+ BundleTool [bundletool Github下载地址](https://github.com/google/bundletool/releases) 下载bundletool-all-x.x.jar 用于安装 [Google Android App Bundle](https://developer.android.com/guide/app-bundle) 到手机测试
## Jenkins使用
+ 如果是windows系统，使用`jenkins_win/jenkins.bat`运行jenkins主服务。如果是linux系统，使用`jenkins_mac/jenkins.sh`运行jenkins主服务。
+ 如果是分布jenkins服务，使用`jenkins_win/jenkins-salves.bat`或者`jenkins_mac/jenkins-salves.sh`运行jenkins子服务。
    - 关于子jenkins服务的`.jnlp`文件，在jenkins后台配置的时候自行查看下载。
## 脚本功能说明
### 主功能
<details>
<summary>auto_build.py</summary>
    
 - 从Unity构建Win包
 - 从Unity构建Android工程，在由Android工程构建相应的Apk或者AAB包
 - 从Unity构建Xcode工程
</details>

<details>
<summary>auto_build_ios.py</summary>
    
 - 构建ipa包
 - 上传符号表到firebase
</details>

<details>
<summary>auto_build_patch.py</summary>
    
 - 构建unity热更资源
</details>

<details>
<summary>aauto_flush.py</summary>
    
 - 刷新cdn资源
</details>

<details>
<summary>auto_upload2_cdn.py</summary>
    
 - 上传资源到ftp
 - 上传资源到sftp
</details>

<details>
<summary>auto_upload2_cos.py</summary>
    
 - 上传资源到腾讯云
</details>

### 配置
<details>
<summary>const.py</summary>
    
 - 静态数据信息
 - 公共枚举
</details>

<details>
<summary>params.py</summary>
    
 - Jenkins初始化参数
 - Jenkins脚本传入参数
 - 各种路径
 - Unity打包所需的自定义参数
 - 构建包体所需参数
 - 热更所需参数
 - 上传资源到cdn所需参数
 - 版本参数
 - xcode构建所需参数
 - 上传资源到腾讯云所需参数
</details>

<details>
<summary>func.py</summary>
    
 - 私有函数
</details>

### 工具
<details>
<summary>util.py</summary>
    
 - 公有工具函数
 - 各种工具的初始化函数
</details>

<details>
<summary>utils/cdn_flush_util.py</summary>
    
 - http请求刷新cdn资源
</details>

<details>
<summary>utils/ftp_util.py</summary>
    
 - ftp上传资源
</details>

<details>
<summary>utils/gradle_util.py</summary>
    
 - gradle进行android工程的构建，清理
</details>

<details>
<summary>utils/jar_util.py</summary>
    
 - jar进行符号表上传
 - android app bundle[^aab] 的安装
</details>

<details>
<summary>utils/ssh_util.py</summary>
    
 - sftp上传资源
</details>

<details>
<summary>utils/svn_util.py</summary>
    
 - svn更新清理还原上传等操作
</details>

<details>
<summary>utils/tail_util.py</summary>
    
 - tail工具
</details>

<details>
<summary>utils/unity_util.py</summary>
    
 - 切平台，前台或者后台执行方法
</details>

<details>
<summary>utils/xcode_util.py</summary>
    
 - 构建xcode工程
 - 修改plist文件
</details>

<details>
<summary>utils/vpn_util.py</summary>
    
 - mac机器上的vpn开启和关闭
</details>

<details>
<summary>utils/cos_util.py</summary>
    
 - 利用cosmod上传资源至腾讯云储存
</details>

<details>
<summary>utils/aws_util.py</summary>
    
 - 利用aws上传资源至亚马逊储存桶
</details>

### 引用
[^aab]:android app bundle - <https://developer.android.com/guide/app-bundle>
