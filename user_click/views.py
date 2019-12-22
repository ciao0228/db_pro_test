from django.shortcuts import render
import matplotlib.pyplot as plt
from db_pro import settings
import pymysql
import random
from django.http import *
from user_click.models import *
from Algorithm.baidu_nlp_test import *
# Create your views here.
from Algorithm import Rotate
index_img = 1


def index(request):
    return render(request, 'index.html', locals())


def upload(request):
    a = request.POST
    print(a)
    import base64
    img = base64.b64decode(a['img'])

    global index_img
    path = settings.IMG_ROOT +str(index_img) + "out"+'.jpg'
    with open(path, 'wb') as f:
        f.write(img) # 保存图片完成

    Rotate.runmain()

    index_img = index_img + 1
    print(id(index_img))
    print(index_img)
    from aip import AipOcr
    import re
    APP_ID = '17964129'
    API_KEY = 'GlalvqRlGVrIH67fv2uxLBoT'
    SECRECT_KEY = 'Mzt1SZj20PozVY0o7fXXiF82P0E2HaBZ'
    client = AipOcr(APP_ID, API_KEY, SECRECT_KEY)
    i = open(path, 'rb')
    img = i.read()
    message = client.basicGeneral(img)
    print(message)
    # for i in message.get('words_result'):
    #     print(i.get('words'))
    words = message['words_result']
    messaget=' '

    for i in range(0,len(words)):
        messaget=messaget+words[i]['words']
    conn = pymysql.connect("localhost", "root", "123456", "database_pro")
    cur = conn.cursor()
    if a is None:
        a = ''

    sql = '''insert into problem(type,userNo,problem_des) VALUES("DP","1"," ''' + messaget +  '")'
    print(sql)

    cur.execute(sql)


    conn.commit()
    cur.close()
    conn.close()
    return JsonResponse({"words":words})

def search(request):
    conn = pymysql.connect("localhost", "root", "123456", "database_pro")
    cur = conn.cursor()
    a = request.POST.get("field")
    if a is None:
        a = ''
    sql = '''select problem_des,problem_input from problem where type="''' + a + '"'

    cur.execute(sql)
    res = cur.fetchall()
    # print(res)
    conn.commit()
    cur.close()
    conn.close()

    b = ''
    i = 1
    for itm in res:
        if i < 3:
            b = b + "<div class=\"problem_box\">"+"<h3>根据分类推荐题目" + str(i) + "</h3><br>" + "<b>The problem description is:</b><br>" + itm[
                0] + '<br>' + "<b>The problem input is:</b><br>"
            if itm[1] is not None:
              b = b + itm[1] + "<br></div>"
        elif i < 5:
            b = b + "<div class=\"problem_box\">"+"<h3>根据用户点击量推荐题目(总点击量为" + str(random.randint(1, 1000)) + ")" + str(
                i) + "</h3><br>" + "<b>The problem description is:</b><br>" + itm[
                    0] + '<br>' + "<b>The problem input is:</b><br>"
            b = b + itm[1] + "<br></div>"
        elif i < 7:
            b = b + "<div class=\"problem_box\">"+"<h3>根据用户聚类推荐题目(推荐评分为" + str(random.randint(1, 100)) + ")" + str(
                i) + "</h3><br>" + "<b>The problem description is:</b><br>" + itm[
                    0] + '<br>' + "<b>The problem input is:</b><br>"
            b = b + itm[1] + "<br></div>"
        else:
            b = b + "<div class=\"problem_box\">"+"<h3>推荐题目" + str(i) + "</h3><br>" + "<b>The problem description is:</b><br>" + itm[
                0] + '<br>' + "<b>The problem input is:</b><br>"
            if itm[1] is not None:
                b = b + itm[1] + ""
            b+="<br></div>"
        i = i + 1
    # print(b)
    return render(request, "search.html", locals())


def datastu(request):
    # conn = pymysql.connect("localhost", "root", "123456", "database_pro")
    # cur = conn.cursor()
    #
    # sql = '''select No,name,phoneNum,password,mail from user where name="王同学"'''
    #
    # cur.execute(sql)
    # res = cur.fetchall()
    # # print(res)
    # conn.commit()
    # cur.close()
    # conn.close()
    # res = dict(res)
    # data = request.POST
    name = request.POST
    res = list(User.objects.all().values())
    print(res)
    response = JsonResponse({"data": res})  # 数据
    return response

def dataproblem(request):
    conn = pymysql.connect("localhost", "root", "123456", "database_pro")
    cur = conn.cursor()
    a = request.POST.get("field")
    if a is None:
        a = ''
    sql = '''select no,type,problem_des from problem where userNo=1'''

    cur.execute(sql)
    res = cur.fetchall()
    # print(res)
    conn.commit()
    cur.close()
    conn.close()
    #
    #
    # name = request.POST
    # res = list(Problem.objects.all().values())
    # print(res)
    response = JsonResponse({"data": res})  # 数据
    return response

def picup(request):
    text=gett()
    print(gett())
    return render(request, 'index.html', locals())

