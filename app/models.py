from django.db import models


# Create your models here.

from django.db import models


# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=1000)#账户
    password = models.CharField(max_length=1000)#密码
    balance=models.PositiveIntegerField()#余额
    path=models.CharField(max_length=1000)#头像路径
    admin=models.CharField(max_length=30)#权限
    text = models.TextField(default=None)  # 简介

class Wares(models.Model):
    username = models.CharField(max_length=1000,default=None)  # 账户
    path = models.CharField(max_length=1000,default=None)  # 产品图像路径
    name = models.CharField(max_length=300)#名称
    price = models.CharField(max_length=3000)#价格
    time = models.CharField(max_length=3000,default=None)  # 时间
    synopsis=models.TextField()#简介
    number=models.PositiveIntegerField()#数量
    category=models.CharField(max_length=3000)#类型
    Count=models.PositiveIntegerField(default=0)#购买数量




