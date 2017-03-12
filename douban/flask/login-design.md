# 用户登录流程图

## index界面：

```
首先：
  判断session是否存在:
      存在：  
        直接载入Dashboard
      不存在：
          跳转到登录界面()
```

## login界面:

```
选项：
    登录：
        ajax验证登录结果:
            post to 登录验证页面
            返回登录状态：
                    成功：
                        跳转到index界面
                    失败：
                        再次输入
    注册：
        成功后切换为登录
```
## mysql数据库表设计
      user 表
        字段：
          ID：自增  
              primary key
          username： unique
          email：unique
          password：

### PS:

```
  学到的其他技能。
  Atom装了一些牛逼的插件
  学了Atom的快捷键：
    command＋down： 到文件尾
    command+right:  到行尾
  ```
