#!/usr/bin/env python
#_*_coding:utf-8_*_
'''
# >>> make_password(123, "salt", 'pbkdf2_sha256')
# 'pbkdf2_sha256$30000$salt$HqrtiEeP29fCF8lIOaHblAb+X4kOQdWqXgq1MIv8CGE='
# >>> a = make_password(123, "salt", 'pbkdf2_sha256')
# >>> b=123
# >>> check_password(b,a)
True
'''

import time
import os
import hashlib
import json
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from dao import models
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from weibo import settings
from dao.Repository.UserinfoRepository import UserRpostry


from service.home import account as sign

def login(request):
    ret = {"status":True,"message":""}

    if request.session.get("is_login",None):
        username = request.session['username']
    else:
        username = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        print(user)
        import os
        if user:
            django_login(request, user)
            path_dir = settings.FILE_CENTER_PATH
            user_dir = "%s/%s" % (path_dir, request.user.userprofile.id)
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)
                os.makedirs(user_dir + "/temp")

            obj_user = UserRpostry()
            user_info_dict = obj_user.select_all_one_user_msg(username)

            print(user_info_dict)
            #
            request.session['is_login'] = True
            request.session[
                "userinfo"] = user_info_dict  # {'data': [{'email': '1223995142@qq.com', 'head_img': 'statics/head_img/024B00103A7C6061429E5F1DB2913C74.png', 'follow_list__user_id': 2, 'id': 1, 'user_id__id': 1, 'age': 23, 'sex': 1, 'brief': '一江春水向东流', 'name': '刘健佐', 'tags__name': 'test'}], 'message': '', 'status': True}
            request.session["username"] = username

            # 设置活跃用户
            # redis_cccon.set("active_%s" % user.userprofile.id, True, ex=3600*12) #半天
            ret["message"] = "登录成功"
            return redirect("/index")
        else:
            ret["status"] = False
            ret["message"] = "登录失败"
            return redirect("/login")

    return render(request,"home/register.html")


def register(request):
    print(request.method)
    if request.method == "POST":
        ret = sign.register(request)
        if ret["status"]:

            return redirect("/login/")
        else:
            return render(request,"home/login.html",{"error":ret["error"]})
    return render(request,"home/login.html",{"error":None})


def logout(request):

    request.session['is_login'] = False
    request.session['username'] = None
    return redirect("/blog/")




