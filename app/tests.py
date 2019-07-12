import pymysql
import json

from django.forms import models
from django.http import HttpResponse
from django.shortcuts import render
from django.test import TestCase
from django.utils.deprecation import MiddlewareMixin
# Create your tests here.
def conn_mysql():
    """
    数据库连接
    :return:连接数据库
    """
    return pymysql.connect(user='root',db='market',password='542191733wsj',host='127.0.0.1',port=3306,charset='utf8')

def input_make(name):
    """
    创建表
    :param name:输入想创建表的名字
    :return:数据库创建相应名称的表。
    """
    conn = conn_mysql()
    cursor = conn.cursor()
    sql=' CREATE TABLE %s(id INT(20),chapter VARCHAR(100),type VARCHAR(100),clicks LONGTEXT,username VARCHAR(100),text LONGTEXT,vip INT(100));'% (name)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
def input_save(name,id,chapter,type,clicks,username,text,vip):
    """
    存储数据
    :param name:表名
    :param id: 主键,随数据增加自增长
    :param chapter: 章节数
    :param type: 书籍类型
    :param clicks: 点击数(未使用)
    :param username: 用户名
    :param text: 正文
    :param vip: 是否为vip(未使用)
    :return: 将数据存入表名的表中
    """
    conn = conn_mysql()
    cursor = conn.cursor()
    sql='INSERT INTO %s(id,chapter,type,clicks,username,text,vip)VALUES(%s,%s,%s,%s,%s,%s,%s)'% (name,id,chapter,type,clicks,username,text,vip)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

# def user_exist(user_name,pass_word):
#     conn=conn_mysql()
#     cursor=conn.cursor()
#     try:
#         sql='select password from app_user where username=%s'%(str(user_name))
#         cursor.execute(sql)
#         pass_word_from_mysql=cursor.fetchone()
#         if pass_word_from_mysql[0]==str(pass_word):
#             return True
#     except Exception as e:
#         print(e)
#         return  False
def update_wares(name,name1,name2):
    conn = conn_mysql()
    cursor = conn.cursor()
    sql='UPDATE app_wares SET %s=%s WHERE id=%s'% (name,name1,name2)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def del_table(name):
    """
    删除表
    :param name: 删除表的名称
    :return: 删除相应的表
    """
    conn = conn_mysql()
    cursor = conn.cursor()
    sql='DROP TABLE %s'% (name)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def auth(func):
    """
    判断cookies
    :return:如果能拿到user则可继续浏览,否则返回login.html并显示请登陆.
    """
    def inner(request,*args,**kwargs):
        try:
            data_cookies=request.COOKIES.get('user')
            if data_cookies is None:
                return render(request,'login.html',{'data': '请登陆'})
        except:
            return render(request,'login.html',{'data': '请登陆'})
        return func(request,*args,**kwargs)
    return inner

def get_username(request):
    """
    拿username
    :return:拿到username
    """
    data_cookies = request.COOKIES.get('user')
    data_cookies_json = json.loads(data_cookies)
    username = data_cookies_json.get('un')
    return username


def get_content(name):
    """
    获取章节
    :param name:查询的表名
    :return: 返回此表的章节
    """
    conn = conn_mysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select chapter from %s "%name
    cursor.execute(sql)
    allmassage_user_information= cursor
    conn.close()
    return allmassage_user_information
def get_chapter(name,name1):
    """
    获取章节正文
    :param name: 查询的表名
    :param name1: 查询的章节
    :return: 返回正文的列表套字典
    """
    conn = conn_mysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select text from %s WHERE chapter=%s"%(name,name1)
    cursor.execute(sql)
    allmassage_user_information= cursor.fetchall()
    conn.close()
    return allmassage_user_information
def get_wares(name,name1):
    conn = conn_mysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from app_wares WHERE %s=%s"%(name,name1)
    cursor.execute(sql)
    allmassage_user_information= cursor.fetchall()
    conn.close()
    return allmassage_user_information


def get_search(name):
    """
    返回搜索结果
    :param name: 查询的字符串
    :return: 与字符串相似的数据
    """
    conn = conn_mysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from app_wares WHERE title LIKE %s"%(name)
    cursor.execute(sql)
    allmassage_user_information= cursor
    conn.close()
    return allmassage_user_information

def last_page(name):
    """
    获取最后一页
    :param name: 查询表的名字
    :return: 表最后一章的id
    """
    conn = conn_mysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select id from %s order by id DESC limit 1" % (name)
    cursor.execute(sql)
    allmassage_user_information = cursor.fetchall()
    conn.close()
    return allmassage_user_information

def ranking():
    """
    获取点击数最高3个
    :return:查询书表中点击数最高的3个
    """
    conn = conn_mysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select name,path from app_wares order by Count DESC limit 3"
    cursor.execute(sql)
    allmassage_user_information = cursor.fetchall()
    conn.close()
    return allmassage_user_information
def get_user(name):
    """
    获取用户名
    :param name:查询的图片路径
    :return: 该图片路径所属的用户名
    """
    conn = conn_mysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select username from app_title where path=%s"%name
    cursor.execute(sql)
    allmassage_user_information = cursor.fetchall()
    conn.close()
    return allmassage_user_information

def get_table(name):
    """
    获取表数据
    :param name:查询的表名
    :return: 是否存在这个表
    """
    conn = conn_mysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select TABLE_NAME from information_schema.TABLES where TABLE_SCHEMA=(select database()) and table_name =%s"%(name)
    cursor.execute(sql)
    allmassage_user_information= cursor.fetchall()
    conn.close()
    return allmassage_user_information

def get_page(name,name1):
    """
    获取页数
    :param name:表名
    :param name1: 章节数
    :return: 此章节数下的id,也就是页数
    """
    conn = conn_mysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select id from %s WHERE chapter=%s"%(name,name1)
    cursor.execute(sql)
    allmassage_user_information= cursor.fetchall()
    conn.close()
    return allmassage_user_information

def up_page(name,name1):
    """
    获取页数
    :param name:表名
    :param name1: id
    :return: 此章节的上一章
    """
    conn = conn_mysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql ="SELECT id FROM %s WHERE (id < %s) LIMIT 1"%(name,name1)
    cursor.execute(sql)
    allmassage_user_information= cursor.fetchall()
    conn.close()
    return allmassage_user_information
def down_page(name,name1):
    """
    获取页数
    :param name:表名
    :param name1: id
    :return: 此章节的下一章
    """
    conn = conn_mysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "SELECT id FROM %s WHERE (id > %s) LIMIT 1"%(name,name1)
    cursor.execute(sql)
    allmassage_user_information= cursor.fetchall()
    conn.close()
    return allmassage_user_information

