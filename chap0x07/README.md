# CHAP0x07 Web 应用漏洞攻防
## 实验目的
- 了解常见 Web 漏洞训练平台；
- 了解常见 Web 漏洞的基本原理；
- 掌握 OWASP Top 10 及常见 Web 高危漏洞的漏洞检测、漏洞利用和漏洞修复方法；
## 实验环境
- WebGoat
- Juice Shop
## 实验要求
- [x] 每个实验环境完成不少于 5 种不同漏洞类型的漏洞利用练习；
- [x] （可选）使用不同于官方教程中的漏洞利用方法完成目标漏洞利用练习；
完成情况如下(有两个系统bug了好像，完成了但没有打勾)：
![webgoat7.1完成情况](./img/webgoat7.1.png)
![webgoat8.0完成情况](./img/webgoat8.0.png)
![juice shop完成情况](./img/juiceshop.png)
## 实验准备
### WebGoat 配置
- 根据`README.md`执行代码
    ```bash
    # 一次获取所有文件（包括所有子模块管理的文件）
    git clone https://github.com/c4pr1c3/ctf-games.git --recursive

    cd ctf-games

    # （可选）单独更新子模块
    git submodule init && git submodule update

    # 启动 webgoat 系列服务
    cd owasp/webgoat/ && sudo docker-compose up -d

    # 启动 juice-shop 及 shake-logger 服务
    cd ../../owasp/juice-shop/ && sudo docker-compose up -d
    ```
- 查看配置情况：状态为`healthy`，访问`127.0.0.1:8087/WebGoat/login`(WebGoat7.1)可以成功登录，访问`127.0.0.1:8088/WebGoat/login`(WebGoat8.0)可以成功登录，访问`127.0.0.1:3000`(Juice Shop)可以成功登录
  
  ![webgoat-success](./img/webgoat-set.png)
## 实验过程
### WebGoat 7.1
#### General
##### HTTP Basic
- 输入框输入`webgoat`点击`GO!`,发现输入框里的内容反序变成`taogbew`
- 输入框内为`taogbew`,再次点击`GO!`，成功
  
![httpbasic](./img/webgoat7.1/httpbasic.png)
#### Access Control Flaws
##### Using an Access Control Matrix
- 原理是不同的用户对数据拥有不同的权限，根据提示：
  >User Larry [User, Manager] did not have privilege to access resource Public Share Change user:	MoeLarryCurlyShemp
- 判断`Larry`具有`Account manager`权限，成功
  
  ![Access Control Flaws](./img/webgoat7.1/accesscontrolmatrix.png)
#### Authentication Flaws
##### Password Strength
- 在所给网站测试破解密码的时间，输入就可以
  
  ![password](./img/webgoat7.1/password.png)
- 但是我遇到的问题是，我测出来的和答案不一样，是不是算力提高了，答案没更新...？
  
  ![passwordstrength](./img/webgoat7.1/passwordstrength.png)
##### Forgot Password
- 输入用户名到下一个问题，问最喜欢的颜色是什么

  ![forgetpassword](./img/webgoat7.1/color.png)
- 题目示例是`webgoat-red`，那就猜一下红配绿，成功
  
  ![forgetpassword](./img/webgoat7.1/forgetpassword.png)
#### Code Quality
##### Discover Clues in the HTML
- 已经给了提示，网页源代码找线索，发现用户名密码，直接提交成功
  
  ![html](./img/webgoat7.1/html.png)
#### Concurrency
##### Thread Safety Problems
- 多线程安全问题，两个页面，一个输入`dave`，另一个`jeff`，并尽量同时提交
  
  ![davejeff](./img/webgoat7.1/davejeff.png)
- 发现两个页面的结果都是`dave`
  
  ![Dave](./img/webgoat7.1/dave.png)
##### Shopping Cart Concurrency Flaw
- 和上一题一样，并发问题，两页面提交不同的数据
  
  ![cart](./img/webgoat7.1/cart.png)
- 左侧进入`purchase`，右侧`update`，左侧再`confirm`，成功
  
  ![Cart Concurrency](./img/webgoat7.1/shoppingcart.png)
#### Insecure Storage
##### Encoding Basics
- 讲了常见的编码基础,以及是否可以被解密
  
  ![Encoding Basics](./img/webgoat7.1/encodingbasic.png)
### WebGoat 8.0
#### General
##### HTTP Basics
- 根据问题找答案，问题是`POST`还是`GET`报文，`F12`查看报文，发现`POST`
  
  ![报文](./img/webgoat8.0/post.png)
- 寻找`magic_num`，报文参数里没有找到，前端代码搜索`magic_num`直接找到
  
  ![magicnum](./img/webgoat8.0/magicnum.png)
- 输入报文类型和`magic_num`，任务完成
  
  ![success](./img/webgoat8.0/http.png)
#### Authentication Flaws
##### Secure Passwords
- 密码强度的问题，尝试复杂密码直到满足要求即可
  
  ![password](./img/webgoat8.0/securepassword.png)
#### Cross-Site Scripting(XSS)
##### Cross Site Scripting
- `Stage2`:`cookie`一个域是一样的吗，你可以使用`JavaScript：alert(document.cookie);`，发现是一样的，回答`yes`
  
  ![yes](./img/webgoat8.0/XSSs2.png)
- `Stage7`:信用卡处输入`"<script>alert('my javascript here')</script>"`(注意带引号，否则不成功)
- `Stage10`:前端源代码寻找路径并输入
  
  ![test](./img/webgoat8.0/test.png)
- `Stage11`:通过上一题的路径获得函数的正确路径并运行，通过`F12`获得代码的运行结果，输入输入框
  
  ![test](./img/webgoat8.0/phonehome.png)
- `Stage12`:答题就好，都对了就通过了
  
  ![answer](./img/webgoat8.0/answer.png)
##### Cross Site Scripting(stored)
- 评论中给出了提示`calling webgoat.customjs.phoneHome()`
- 再评论框输入代码，`F12`查看运行结果，将其输入`submit`，任务完成
  
  ![XSSstored](./img/webgoat8.0/stored.png)
#### Insecure Communication
##### Insecure Login
- `F12`检查源代码，发现提交时用了一个函数`submit_secret_credentials()`
  
  ![function](./img/webgoat8.0/func.png)
- 检查函数的源代码
  
  ![source](./img/webgoat8.0/source.png)
- 在线解码十六进制代码
  
  ![decode](./img/webgoat8.0/decode.png)

- 得到`usernamde:CaptainJack`和`password:BlackPearl`提交成功
### Juice Shop
#### Broken Access Control
##### Admin Section
- 进入商店的`administration`部分，查看网页源代码，根据`score-board`的思路，发现`path:administration`
  
  ![administration](./img/juiceshop/administration.png)
- 访问`http://127.0.0.1:3000/#/administration`，登陆成功
  
  ![访问成功](./img/juiceshop/administrations.png)
##### Five-Star Feedback
- 删除顾客的五星评价，前提是已经登陆了`administration`账户
- 在`administration`页面成功删除
  
  ![删除成功](./img/juiceshop/fivestars.png)
#### Cryptographic Issues
##### Weird Crypto
- 在页面内提交一个不安全的密码算法，猜想`md5`试一试
- 提交`md5`，成功
  
  ![md5成功](./img/juiceshop/md5.png)
#### Injection
##### Login Admin
- 以`admin`身份登录账户，用户名采用万能句`' or 1=1 --`，密码任意
  
  ![login](./img/juiceshop/adminlogin.png)
- `admin`管理员身份登陆成功
  
  ![admin](./img/juiceshop/adminaccount.png)
#### Miscellaneous
##### Bully Chatbot
- 采用暴力破解的办法，从`chatbot`处获得优惠券
- 和`chatbot`聊天，不断发送`coupon code`
  
  ![chatbot](./img/juiceshop/bullychatbot.png)
##### Privacy Policy
- 这个很简单，不再附图，直接阅读隐私政策就完成了
##### Score Board
- 查看网页源代码，发现`path:score-board`
  
  ![chatbot](./img/juiceshop/scoreboard.png)
- 访问`http://127.0.0.1:3000/#/score-board`，任务完成
#### Security Misconfiguration
##### Error Handing
- 错误的登陆框：点击登陆，电子邮箱前加一个 ’ (单引号) 就行了
  
  ![单引号](./img/juiceshop/adminlogin.png)
#### Sensitive Data Exposure
##### Confidential Document
- 访问路径`http://127.0.0.1:3000/ftp`
- 查看文件`acquisitions.md`，可以直接访问，没有权限保护
  
  ![acquisitions.md](./img/juiceshop/confidentialdocument.png)
#### XSS
##### Bonus Payload
- 搜索框直接搜索所给代码`<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>`
- 任务完成
  
  ![bonuspayload](./img/juiceshop/bonuspayload.png)
##### DOM XSS
- 同样的漏洞，搜索框直接搜索代码
- 任务完成
  
  ![DOM XSS](./img/juiceshop/XSS.png)
## 参考资料

[1] [WebGoat中文手册.pdf](https://max.book118.com/html/2017/1126/141622436.shtm)

[2] [kali linux Burp Suite极简使用教程](https://www.cnblogs.com/thechosenone95/p/10623462.html)

[3] [WebGoat8 M17 XSS 答案、题解](https://www.pianshen.com/article/1142906991/)

[4] [WebGoat系列实验Cross-Site Scripting (XSS)](https://www.cnblogs.com/yangmzh3/p/7542018.html)