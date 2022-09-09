# git操作指南

## 一：建立自己的仓库指南

### 1. 下载git，用于管理本地的仓库

git仓库的地址：[Git (git-scm.com)](https://git-scm.com/)

### 2.配置自己的本机（使用的是ssh链接）

```
git config --global user.name "这里输入你在GitHub的账户名"
git config --global user.email "这里输入你在GitHub的注册邮箱名"
```

这里主要配置的git仓库账号信息，方便之后和github关联

接下来配置ssh，方便和github上面的仓库连接

```
cd ~/.ssh 
ls
```

查看是否存在id_rsa 和 id_rsa.pub两个文件，该文件在用户/administrator/.ssh文件下面

如果没有，就需要创建一个这样的文件

```
ssh-keygen -t rsa -C "这里输入你在 GitHub 的注册邮箱"
```

之后再执行这样的命令查看是否存在这样的文件

```
cat id_rsa.pub
```

该命令会显示公钥，需要将公钥和github的自己账号进行配置，在github中选择setting/SSH and GPG keys/new SSH key将公钥复制粘贴到里面，名字随意

```
ssh -T git@github.com
```

测试一下SSH是否安装成功

```
Hi Juliecodestack! You've successfully authenticated, but GitHub does not provide shell access.
```

显示上面表示安装成功

### 3.上传自己项目

首先在github中建立一个仓库

在打开git base

```
git clone ssh地址（这里面不是http的地址）
```

```
cd 文件目录
```

进入自己的文件目录

```
git add 加上自己需要提交的文件名字
git add . //表示提交所有的文件
git commit -m '写上自己的提交记录'
git push //就直接推送到github中
```

