#!/usr/bin/env python
#_*_coding:utf-8_*_
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect

from dao.Repository.UserinfoRepository import UserRpostry
from dao.Repository.WeiBo_Repository import WeiboRepo
import json

from dao.Repository.TagR import Tags_handler

def wrapper(func):
    def inner(request):
        if not request.session.get("is_login", None):
            return redirect("/login")
        else:
            func(request)

    return inner


def index(request):
    if request.session.get("is_login",None):
        print(request.session['userinfo']) #{'data': [{'email': '1223995142@qq.com', 'head_img': 'statics/head_img/024B00103A7C6061429E5F1DB2913C74.png', 'follow_list__user_id': 2, 'id': 1, 'user_id__id': 1, 'age': 23, 'sex': 1, 'brief': '一江春水向东流', 'name': '刘健佐', 'tags__name': 'test'}], 'message': '', 'status': True}

        if request.method == "POST":

            pass
        else:
            username = request.session['username']
            obj_user = UserRpostry()
            user_nid = obj_user.select_nid(username)
            user_nid = user_nid['data']

            view_model = obj_user.select_follow_list_and_num(user_nid) #{'data': {'followed_num': 1, 'data': [{'age': 23, 'email': '1223995142@qq.com', 'sex': 1, 'name': '刘健佐', 'user_id__id': 1, 'follow_list__user_id': 2, 'head_img': 'statics/head_img/024B00103A7C6061429E5F1DB2913C74.png', 'brief': '一江春水向东流', 'tags__name': 'test'}], 'my_fans_num': 2}, 'message': '', 'status': True}

            wei_user = WeiboRepo()
            webo_count = wei_user.count_user_num_weibo(user_nid)
            print(webo_count)


            infomation  = {}
            if view_model["status"]:
                infomation["followed_num"] = view_model['data']['followed_num']
                infomation['my_fans_num'] = view_model['data']['my_fans_num']
                infomation['userinfo'] = request.session['userinfo']['data'][0]
                infomation["webo_count"] = webo_count['data']['count_user_weibo']
                infomation["username"] = username


            # ret = json.dumps(infomation)

        return render(request,"index/index.html",{'is_login':True,'infomation':infomation})

    return render(request, "index/index.html", {'is_login': False,})


def lay_out(request):
    infomation ={}
    if not request.session.get("is_login", None):
        return redirect("/login")

    if request.method == "POST":
        pass

    else:
        nid = request.session['userinfo']['data'][0]['id']
        data_list = get_all_tags(nid)  # 数据库关联账户的所有标签
        infomation['userinfo'] = request.session['userinfo']['data'][0]
        infomation['username'] = request.session['username']
        infomation['tag_list'] = data_list #返回渲染的
        pass
    return render(request,"lay_out/lay_out.html",{'is_login': False,'infomation':infomation})

def test_lay_out(request):
    if request.session.get("is_login", None):
        print("首页测试")
        return render(request, "index/index.html", {'is_login': True,})
    return render(request,"_lay_mu_out/_layout.html",{'is_login': False,})


def get_all_tags(nid):
    obj_tag = Tags_handler()
    view_model = obj_tag.get_user_about_tag(
        nid)  # {'name': '刘健佐', 'tags__name': 'test'}{'name': '刘健佐', 'tags__name': 'dsfasdf'}

    print(view_model)  # {'message': '', 'data': [{'name': '刘健佐', 'tags__name': 'test'}, {'name': '刘健佐', 'tags__name': 'dsfasdf'}], 'status': True}

    data_list = []
    if view_model['status']:
        data_dict = view_model['data']
        for lis_item in data_dict:
            for k, v in lis_item.items():
                if k == 'tags__name':
                    data_list.append(v)

    else:
        pass
    return data_list

# @wrapper
def add_tags(request):

    rep = {"status":True,"message":""}
    if not request.session.get("is_login", None):
        return redirect("/login")

    if request.method == "POST":
    # if request.method == "GET":
        nid = request.session['userinfo']['data'][0]['id']
        data_list = get_all_tags(nid) # 数据库关联账户的所有标签
        print(data_list)

        print(request.POST) # <QueryDict: {'data_tag': ['["sdfdsfsdfas"]']}>

        data_from_web = request.POST["data_tag"]
        print(data_from_web) #["sdfdsfsdfas"]  需要再load一次

        data_from_web = json.loads(data_from_web)

        # data_from_web = ['宅控','是打发']
        # fromweb_tags_list = data_from_web
        print(data_from_web)

        if not data_from_web:
            rep['status']= False
            rep['message']="nodata get 数据未获取到"
            return HttpResponse(json.dumps(rep))

        fromweb_tags_list = data_from_web

        print(fromweb_tags_list,12312312312)
        li=[]
        for item in  fromweb_tags_list:
            if item in data_list:
                continue
            else:
                li.append(item)
                print(li,"li")
                print(item)
                # 开始插入新标签和多对多关系表数据
                obj_tag = Tags_handler()
                modle_view = obj_tag.insert_tags(item)
                print(modle_view)

        # 插入profile——tag关系表
        user_obj = UserRpostry()
        mod__d = user_obj.insert_tag_from_profile(nid,li)
        print(mod__d)
        return HttpResponse(json.dumps(data_list))




def change_userprofile_name(request):



    pass