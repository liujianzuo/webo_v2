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

import time,os

import json
from datetime import date
from datetime import datetime
from decimal import Decimal

class JsonCustomEncoder(json.JSONEncoder):  # 序列化时候json处理不了的我们需要自己做转换为json可以转换的数据类型

    def default(self, field):

        if isinstance(field, datetime):  # 如果字段是时间类型
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field, date):  #
            return field.strftime('%Y-%m-%d')
        elif isinstance(field, Decimal):  # 如果是小数类型
            return str(field)
        else:
            return json.JSONEncoder.default(self, field)



def wrapper(func):
    def inner(request):
        if not request.session.get("is_login", None):
            return redirect("/login")

        print(func)
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
            print(user_nid,"user_nid____++++++")
            view_model = obj_user.select_follow_list_and_num(user_nid) #{'data': {'followed_num': 1, 'data': [{'age': 23, 'email': '1223995142@qq.com', 'sex': 1, 'name': '刘健佐', 'user_id__id': 1, 'follow_list__user_id': 2, 'head_img': 'statics/head_img/024B00103A7C6061429E5F1DB2913C74.png', 'brief': '一江春水向东流', 'tags__name': 'test'}], 'my_fans_num': 2}, 'message': '', 'status': True}

            wei_user = WeiboRepo()
            webo_count = wei_user.count_user_num_weibo(user_nid)
            print(webo_count)

            weibo_detail_ = wei_user.get_new_ten_weibo_item(user_nid)
            # if weibo_detail_['status']:
            weibo_detail_data = weibo_detail_['data']
            print(1111,weibo_detail_data)

            for i in weibo_detail_data["weibo_detail_item"]:
                #     print(type(i))
                index_num = weibo_detail_data["weibo_detail_item"].index(i)
                weibo_detail_data["weibo_detail_item"][index_num]["pictures_link_id"] = json.loads(
                    weibo_detail_data["weibo_detail_item"][index_num]["pictures_link_id"])


            infomation  = {}
            if view_model["status"]:
                infomation["followed_num"] = view_model['data']['followed_num']
                infomation['my_fans_num'] = view_model['data']['my_fans_num']
                infomation['userinfo'] = request.session['userinfo']['data'][0]
                infomation["webo_count"] = webo_count['data']['count_user_weibo']
                infomation["username"] = username
                infomation["weibo_detail_data"] = weibo_detail_data


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



# @wrapper
def change_userprofile_name(request):
    rep = {"status":True,"message":""}

    if not request.session.get("is_login", None):
        return redirect("/login")

    if request.method == "POST":
    # if request.method == "GET":
        nid = request.session['userinfo']['data'][0]['id']
        print(request.POST)
        data_dict = request.POST.get("data_tag")
        print(nid,data_dict)
        # data_dict = {"name":'玄霸天下2'}
        data_list = json.loads(data_dict)
        data_dict = {data_list[0]:data_list[1]}
        print(data_dict)
        obj_user = UserRpostry()
        change_name = obj_user.change_colume(nid,data_dict)
        request.session['userinfo']['data'][0][data_list[0]]=data_list[1]
        request.session['userinfo'] = request.session['userinfo']
        if not change_name['status']:
            rep['status'] = False
            rep['message'] = "昵称修改失败"
    print('123123的说法是对方是否',rep)
    return HttpResponse(json.dumps(rep))

def personal(request):
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

            return render(request,"personal/personal.html",{'is_login':True,'infomation':infomation})

        return render(request, 'personal/personal.html',{'is_login': False,})


def pic_handle(request):

    timestamp = time.time()
    user_id = request.session['userinfo']['data'][0]["user_id__id"]
    pic_path = "statics/uploads/%s/%s" % (user_id, timestamp)

    if request.method == "POST":

        all_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), pic_path)
        if not os.path.exists(all_path):
            os.mkdir(all_path)
        print(request)
        print(request.FILES.getlist("fff"))
        files_obj = request.FILES.getlist("fff")
        # print(obj.name, obj.chunks(), type(obj.chunks()))
        path_list = []
        for obj in files_obj:
            f = open(os.path.join(all_path, obj.name), "wb")
            for chunk in obj.chunks():
                f.write(chunk)
            path_list.append(os.path.join("/%s" % pic_path, obj.name))

        return HttpResponse(json.dumps(path_list))

    return render(request,"test/test.html")


def search(request):

    rep = {"status":True,"message":"","searhch_length":0}

    username = request.session['username']
    obj_user = UserRpostry()
    user_nid = obj_user.select_nid(username)
    user_nid = user_nid['data']

    view_model = obj_user.select_follow_list_and_num(
        user_nid)  # {'data': {'followed_num': 1, 'data': [{'age': 23, 'email': '1223995142@qq.com', 'sex': 1, 'name': '刘健佐', 'user_id__id': 1, 'follow_list__user_id': 2, 'head_img': 'statics/head_img/024B00103A7C6061429E5F1DB2913C74.png', 'brief': '一江春水向东流', 'tags__name': 'test'}], 'my_fans_num': 2}, 'message': '', 'status': True}

    wei_user = WeiboRepo()
    webo_count = wei_user.count_user_num_weibo(user_nid)
    # print(webo_count)


    # print(request,request.method,request.POST.get("search_data",None))
    # if request.method == "POST":
    # if request.method == "GET":



    infomation = {}
    if view_model["status"]:
        infomation["followed_num"] = view_model['data']['followed_num']
        infomation['my_fans_num'] = view_model['data']['my_fans_num']
        infomation['userinfo'] = request.session['userinfo']['data'][0]
        infomation["webo_count"] = webo_count['data']['count_user_weibo']
        infomation["username"] = username
        infomation["lenth"] = False # if request.method == "POST":

    search_data = request.GET.get("search_data", None)
    infomation["search_data"] = search_data

    if search_data:
        print(search_data)
        wei_user = WeiboRepo()
        weibo_detail_ = wei_user.search_weibo_item(search_data)
        weibo_detail_data = weibo_detail_['data']['weibo_search_content']
        print(1111, weibo_detail_data) # 1111 {'weibo_search_content': [{'user__user__username': 'lilu', 'user__name': '李露', 'perm': 0, 'video_link_id': None, 'wb_type': 0, 'id': 5, 'user_id': 3, 'date': datetime.datetime(2016, 9, 26, 8, 2, 4, 41588, tzinfo=<UTC>), 'pictures_link_id': '["/statics/uploads/1/temp/563DE154F522BCEAF9C81A383396C066.png"]', 'text': '这是一条新的微博'}, {'user__user__username': 'lilu', 'user__name': '李露', 'perm': 0, 'video_link_id': None, 'wb_type': 0, 'id': 4, 'user_id': 3, 'date': datetime.datetime(2016, 9, 26, 8, 0, 3, 635208, tzinfo=<UTC>), 'pictures_link_id': '["/statics/uploads/1/temp/563DE154F522BCEAF9C81A383396C066.png"]', 'text': '这是一条新sss的微博'}, {'user__user__username': 'hefei', 'user__name': '何菲', 'perm': 0, 'video_link_id': None, 'wb_type': 0, 'id': 3, 'user_id': 2, 'date': datetime.datetime(2016, 9, 26, 7, 58, 57, 256159, tzinfo=<UTC>), 'pictures_link_id': '["/statics/uploads/1/temp/563DE154F522BCEAF9C81A383396C066.png"]', 'text': '这是一条dsf新的微博'}, {'user__user__username': 'liu', 'user__name': '玄霸天', 'perm': 0, 'video_link_id': None, 'wb_type': 0, 'id': 2, 'user_id': 1, 'date': datetime.datetime(2016, 9, 26, 7, 54, 39, 28646, tzinfo=<UTC>), 'pictures_link_id': '["/statics/uploads/1/temp/563DE154F522BCEAF9C81A383396C066.png"]', 'text': '这是一条sdf新的微博'}, {'user__user__username': 'liu', 'user__name': '玄霸天', 'perm': 0, 'video_link_id': None, 'wb_type': 0, 'id': 1, 'user_id': 1, 'date': datetime.datetime(2016, 9, 26, 7, 49, 48, 80055, tzinfo=<UTC>), 'pictures_link_id': '["/statics/uploads/1/temp/563DE154F522BCEAF9C81A383396C066.png"]', 'text': '这是一sdfas条新的微博'}]}


        for i in weibo_detail_data:
            #     print(type(i))
            index_num = weibo_detail_data.index(i)
            print(index_num)
            weibo_detail_data[index_num]["pictures_link_id"] = json.loads(
                weibo_detail_data[index_num]["pictures_link_id"])

        infomation["lenth"] = len(weibo_detail_["data"]['weibo_search_content'])
        print(123123, weibo_detail_, )  # {'status': True, 'data': {'weibo_search_content': []}, 'message': ''}
        # 123123 {'status': True, 'data': {'weibo_search_content': [{'user__user__username': 'lilu', 'pictures_link_id': '["/statics/uploads/1/temp/563DE154F522BCEAF9C81A383396C066.png"]', 'video_link_id': None, 'id': 5, 'date': datetime.datetime(2016, 9, 26, 8, 2, 4, 41588, tzinfo=<UTC>), 'user_id': 3, 'wb_type': 0, 'perm': 0, 'text': '这是一条新的微博', 'user__name': '李露'}, {'user__user__username': 'lilu', 'pictures_link_id': '["/statics/uploads/1/temp/563DE154F522BCEAF9C81A383396C066.png"]', 'video_link_id': None, 'id': 4, 'date': datetime.datetime(2016, 9, 26, 8, 0, 3, 635208, tzinfo=<UTC>), 'user_id': 3, 'wb_type': 0, 'perm': 0, 'text': '这是一条新sss的微博', 'user__name': '李露'}]}, 'message': ''}

        infomation["weibo_detail_data"] = weibo_detail_data

    return render(request,"search/search.html",{"infomation":infomation})



