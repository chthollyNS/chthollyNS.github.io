import datetime
import os
import json
import redis
import ranking as ranking
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.
from django.urls import reverse

from app import models
from app.form import AddForm


# from app.until import
from app.tests import auth, input_make, input_save, get_username, get_content, get_chapter, get_search, last_page, \
    ranking, get_user, get_page, del_table, get_wares, update_wares

conn_r=redis.Redis(host='127.0.0.1',port=6379)
personal_page=0
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        UserName = request.POST.get("username")
        PassWord = request.POST.get("password")
        try:
            if models.Users.objects.get(username=UserName):
                data = models.Users.objects.get(username=UserName)
                if data.password == PassWord:
                    object = index(request,UserName)
                    dict_cookie = {'un': UserName, 'pw': PassWord}
                    dict_cookie = json.dumps(dict_cookie)
                    object.set_cookie(UserName, dict_cookie)
                    return object
                else:
                    return render(request, 'login.html', {'data': '登陆失败'})
        except:
            return render(request, 'login.html', {'data': '登陆失败'})

def index(request,username,*args):
    data2 = models.Users.objects.filter(username=username).values('path')[0].get('path')
    rank = ranking()
    date = (rank[0])['name']
    date1 = (rank[1])['name']
    date2 = (rank[2])['name']
    img_date = (rank[0])['path']
    img_date1 = (rank[1])['path']
    img_date2 = (rank[2])['path']
    try:
        err=args[0]
        return render(request, 'index.html',
                      {'data2': data2, 'data3': models.Users.objects.filter(username=username),'data5':models.Wares.objects.all().order_by('-Count')[:3],'data6':models.Wares.objects.all().order_by('-time')[:5],'date':date,'date1':date1,'date2':date2,'img':img_date,'img1':img_date1,'img2':img_date2,
                       'username':username,'err':err})
    except:
        return render(request, 'index.html',
                      {'data2': data2, 'data3': models.Users.objects.filter(username=username),
                       'data5': models.Wares.objects.all().order_by('-Count')[:3],
                       'data6': models.Wares.objects.all().order_by('-time')[:5], 'date': date, 'date1': date1,
                       'date2': date2, 'img': img_date, 'img1': img_date1, 'img2': img_date2,
                       'username': username})
def personal(request,name):
    data=models.Wares.objects.filter(username=name)
    paginator=Paginator(data,5)
    page=request.GET.get('page')
    try:
        data_page=paginator.page(page)
    except PageNotAnInteger:
        data_page=paginator.page(1)
    except EmptyPage:
        data_page=paginator.page(paginator.num_pages)
    return render(request, 'details.html', {'data':data_page,'username':name})
def alter(request,name,name1):
    return render(request, 'alter.html',{'name':name,'name1':name1,'data':models.Wares.objects.filter(id=name),'username':name1})
def revise(request,name,name1,name2):
    if request.method == 'GET':
        return render(request,'revise.html',{'type':name,'id':name1,'username':name2})
    else:
        text=request.POST.get('text')
        update_wares(name,text,name1)
        return index(request,name2)

def del_id(request,name,name1):
    conn_r.hdel(name1, name)
    return trolley(request,name1)
def shop(request,name,name1):
    username = name1
    name=str(name)
    try:
        old_num=conn_r.hget(username,name).decode(encoding = "utf-8")
        num = int(request.POST.get('num'))+int(old_num)
        conn_r.hset(username,name,num)
        print(conn_r.hgetall(name1))
        return index(request,username)
    except:
        num = int(request.POST.get('num'))
        conn_r.hset(username, name, num)
        print(conn_r.hgetall(name1))
        return index(request,username)

def now(request,name,name1):
    data = get_wares('id', name)
    number=models.Wares.objects.filter(id=name).values('number')[0].get('number')
    price = models.Wares.objects.filter(id=name).values('price')[0].get('price')
    Count = int(models.Wares.objects.filter(id=name).values('Count')[0].get('Count'))+int(request.POST.get('num'))
    if int(number)-int(request.POST.get('num'))>=0:
        number=int(number)-int(request.POST.get('num'))
        if int(models.Users.objects.filter(username=name1).values('balance')[0].get('balance'))-int(request.POST.get('num'))*int(price)>=0:
            balance=int(models.Users.objects.filter(username=name1).values('balance')[0].get('balance')) - int(request.POST.get('num')) * int(price)
            models.Wares.objects.filter(id=name).update(Count=Count)
            models.Wares.objects.filter(id=name).update(number=number)
            models.Users.objects.filter(username=name1).update(balance=balance)
            return index(request,name1)
        else:
            return render(request, 'title.html',
                          {'data': data, 'username': name1, 'data3': models.Users.objects.filter(username=name1),
                           'data4': models.Users.objects.filter(username=name1).values('path')[0].get('path'),'err':'您的余额不足'})
    else:
        return render(request, 'title.html',
                      {'data': data, 'username': name1, 'data3': models.Users.objects.filter(username=name1),
                       'data4': models.Users.objects.filter(username=name1).values('path')[0].get('path'),'err':'余量已不足'})
def admin(request,username):
    path=models.Users.objects.filter(username=username).values('path')[0].get('path')
    data2=path
    if models.Users.objects.filter(username=username).values('admin')[0].get('admin')=='1':
        return render(request, 'admin.html', {'data': models.Users.objects.filter(~Q(password='')).order_by("id"),'data1':username
                                              ,'data2':data2,'username':username})
    else:
        return index(request,username,'您不是管理员')

def upload(request,name):
    if request.method == 'GET':
        return render(request, 'Upload.html',{'username':name})
    else:
        button=request.POST.get('button')
        title=request.POST.get("title")
        text = request.POST.get("text")
        price=request.POST.get("price")
        number=request.POST.get("number")
        up_file = request.FILES.get('file', None)
        username=name
        time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if up_file != None:
            file_path = os.path.join('static/img', up_file.name)
            f = open(file_path, 'wb+')
            for chunk in up_file.chunks():
                f.write(chunk)
            f.close()
            obj = models.Wares(username=username,name=title, path=up_file.name,time=time,synopsis=text,price=price,number=number,category=button,Count=0)
            obj.save()
        return index(request,username)

def cancel2(request,id,username):
    """
    :param name: 得到书的id
    :return: 删除id为name的书
    """
    models.Wares.objects.filter(id=id).delete()
    return index(request,username)

def title(request,name,name1):
    data = get_wares('id', name)
    return render(request, 'title.html',
                  {'data': data, 'username': name1, 'data3': models.Users.objects.filter(username=name1),
                   'data4': models.Users.objects.filter(username=name1).values('path')[0].get('path')})

def title_search(request,name):
    search = request.GET.get("search")
    data1=models.Wares.objects.filter(name__contains=search)#搜索相似字符串的搜索结果
    return render(request, 'search.html',{'data1':data1,'username':name,'data3': models.Users.objects.filter(username=name),'data4':models.Users.objects.filter(username=name).values('path')[0].get('path')})

def title_search1(request,name,name1):
    data1=models.Wares.objects.filter(name=name1)
    return render(request, 'search.html',{'data1':data1,'username':name,'data3': models.Users.objects.filter(username=name),'data4':models.Users.objects.filter(username=name).values('path')[0].get('path')})

def all_shop(request,name):
    spam = conn_r.hgetall(name)
    for k in spam:
        id= k.decode(encoding="utf-8")
        number= spam[k].decode(encoding="utf-8")
        print(id,number)
        price= models.Wares.objects.filter(id=k.decode(encoding="utf-8")).values('price')[0].get('price')
        balance = int(models.Users.objects.filter(username=name).values('balance')[0].get('balance')) - int(number) * int(price)
        Count = int(models.Wares.objects.filter(id=id).values('Count')[0].get('Count')) + int(number)
        number = models.Wares.objects.filter(id=id).values('number')[0].get('number') - int(number)
        if number>=0:
            if balance>=0:
                models.Wares.objects.filter(id=id).update(Count=Count)
                models.Wares.objects.filter(id=id).update(number=number)
                models.Users.objects.filter(username=name).update(balance=balance)
                conn_r.hdel(name, id)
            else:
                trolley(request,name)
        else:
            trolley(request,name)
    return trolley(request, name)
def trolley(request,name):
    if request.method == 'GET':
        # conn_r.delete(name)
        spam=conn_r.hgetall(name)
        list = []
        for k in spam:
            dict = {}
            dict['id']=k.decode(encoding = "utf-8")
            dict['number']=spam[k].decode(encoding = "utf-8")
            dict['path']=models.Wares.objects.filter(id=k.decode(encoding = "utf-8")).values('path')[0].get('path')
            dict['price']=models.Wares.objects.filter(id=k.decode(encoding = "utf-8")).values('price')[0].get('price')
            dict['name']=models.Wares.objects.filter(id=k.decode(encoding = "utf-8")).values('name')[0].get('name')
            dict['surplus'] = models.Wares.objects.filter(id=k.decode(encoding="utf-8")).values('number')[0].get('number')
            list.append(dict)
        data = list
        paginator = Paginator(data, 4)
        page = request.GET.get('page')
        try:
            data_page = paginator.page(page)
        except PageNotAnInteger:
            data_page = paginator.page(1)
        except EmptyPage:
            data_page = paginator.page(paginator.num_pages)
        return render(request, 'trolley.html',{'data':data_page,'username':name,'data2':models.Users.objects.filter(username=name).values('path')[0].get('path'),'data3': models.Users.objects.filter(username=name)})
    else:
        return render(request,'trolley.html',{'username':name,'data2':models.Users.objects.filter(username=name).values('path')[0].get('path'),'data3': models.Users.objects.filter(username=name)})
def consume(request,name,name1,name2):
    username = name
    spam = conn_r.hgetall(username)
    list = []
    for k in spam:
        dict = {}
        dict['id'] = k.decode(encoding="utf-8")
        dict['number'] = spam[k].decode(encoding="utf-8")
        dict['path'] = models.Wares.objects.filter(id=k.decode(encoding="utf-8")).values('path')[0].get('path')
        dict['price'] = models.Wares.objects.filter(id=k.decode(encoding="utf-8")).values('price')[0].get('price')
        dict['name'] = models.Wares.objects.filter(id=k.decode(encoding="utf-8")).values('name')[0].get('name')
        dict['surplus'] = models.Wares.objects.filter(id=k.decode(encoding="utf-8")).values('number')[0].get(
            'number')
        list.append(dict)
    try:
        number=models.Wares.objects.filter(id=name1).values('number')[0].get('number')
        price = models.Wares.objects.filter(id=name1).values('price')[0].get('price')
        Count = int(models.Wares.objects.filter(id=name1).values('Count')[0].get('Count'))+int(name2)
        number=int(number)-int(name2)
        balance=int(models.Users.objects.filter(username=username).values('balance')[0].get('balance'))-int(name2)*int(price)
        print(balance,number)
        if balance>=0:
            models.Wares.objects.filter(id=name1).update(Count=Count)
            models.Wares.objects.filter(id=name1).update(number=number)
            models.Users.objects.filter(username=username).update(balance=balance)
            conn_r.hdel(username, name1)
            return trolley(request,username)
        else:
            data = list
            paginator = Paginator(data, 4)
            page = request.GET.get('page')
            try:
                data_page = paginator.page(page)
            except PageNotAnInteger:
                data_page = paginator.page(1)
            except EmptyPage:
                data_page = paginator.page(paginator.num_pages)
            return render(request, 'trolley.html', {'err': '你的余额不足', 'data': data_page,'username':username,'data2':models.Users.objects.filter(username=name).values('path')[0].get('path'),'data3': models.Users.objects.filter(username=name)})
    except:
        data = list
        paginator = Paginator(data, 4)
        page = request.GET.get('page')
        try:
            data_page = paginator.page(page)
        except PageNotAnInteger:
            data_page = paginator.page(1)
        except EmptyPage:
            data_page = paginator.page(paginator.num_pages)
        return render(request,'trolley.html',{'err':'该商品余量不足','data':data_page,'username':username,'data2':models.Users.objects.filter(username=name).values('path')[0].get('path'),'data3': models.Users.objects.filter(username=name)})
def consume_updata(request,name,name1,name2):
    if name2=='add':
        num=int(conn_r.hget(name, name1).decode(encoding="utf-8"))+1
        conn_r.hset(name, name1, num)
        return trolley(request,name)
    elif name2=='update':
        num=request.GET.get('num')
        conn_r.hset(name, name1, num)
        return trolley(request, name)
    else:
        num = int(conn_r.hget(name, name1).decode(encoding="utf-8")) - 1
        if num>=0:
            conn_r.hset(name, name1, num)
            return trolley(request, name)
        else:
            return trolley(request, name)
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        passwords = request.POST.get('passwords')
        text=request.POST.get('text')
        if password != passwords:
            return render(request, 'register.html', {'key1': '两次输入的密码不同'})
        else:
            try:
                a=models.Users.objects.get(username=username)
                print(a)
                return render(request, 'register.html', {'key': '用户名已存在'})
            except:
                if not text:
                    return HttpResponse('简介未填写')
                else:
                    up_file = request.FILES.get('myfile', None)
                    if not up_file:
                        return HttpResponse('没有选择文件')
                    else:
                        if str(up_file).split('.')[1] in ['jpg']:
                            up_file_name = username + '.' + 'jpg'
                        elif str(up_file).split('.')[1] in ['png']:
                            up_file_name = username + '.' + 'png'
                        else:
                            return render(request, 'register.html', {'key': '只允许格式为png或者jpg'})
                        file_path = os.path.join('static/img', up_file_name)
                        f = open(file_path, 'wb+')
                        for chunk in up_file.chunks():
                            f.write(chunk)
                        f.close()
                        obj = models.Users(username=username, password=password, path=up_file_name,text=text,balance=0,admin=0)
                        obj.save()
                        return render(request, 'login.html')


def search(request,name,name1):
    username = name1
    name = str(name)
    return render(request, 'search.html', {'data': models.Users.objects.filter(username=username),
                                           'data1': models.Wares.objects.filter(category=name), 'data2': name,'username':username,'data3': models.Users.objects.filter(username=username),'data4':models.Users.objects.filter(username=username).values('path')[0].get('path')})

def details(request,name,name1):
    data = models.Wares.objects.filter(username=name)
    paginator = Paginator(data, 5)
    page = request.GET.get('page')
    try:
        data_page = paginator.page(page)
    except PageNotAnInteger:
        data_page = paginator.page(1)
    except EmptyPage:
        data_page = paginator.page(paginator.num_pages)
    return render(request,'details.html',{'data':data_page,'username':name1})
def logout(request,username,username1):
    print(username,username1)
    if models.Users.objects.filter(username=username).values('admin')[0].get('admin')=='1':
        data2=models.Users.objects.filter(username=username1).values('path')[0].get('path')
        return render(request, 'admin.html', {'data': models.Users.objects.filter(~Q(password='')).order_by("id"),'data1':username1
                                                  ,'data2':data2,'key': '管理员不可被删除','username':username1})
    else:
        models.Users.objects.filter(username=username).update(password='')
        data2=models.Users.objects.filter(username=username1).values('path')[0].get('path')
        return render(request, 'admin.html',{'data': models.Users.objects.filter(~Q(password='')).order_by("id"),'data1':username1,'data2':data2,'username':username1})

def balance(request,name,name1):
    username = name1
    if request.method == 'GET':
        return render(request, 'recharger.html',{'data':models.Users.objects.filter(username=username),'username':username})#会员充值网站
    else:
        money = request.POST.get('money')
        money=int(money)+int(name)
        models.Users.objects.filter(username=username).update(balance=money)#更新充钱金额
        return index(request,username)


def cancel(request,username):
    response = render(request, 'login.html')
    response.delete_cookie(username)
    return response



