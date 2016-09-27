#!/usr/bin/env python
#_*_coding:utf-8_*_
from  Intrac.rabbit_mq_conn import Rab_conn_server
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect

from dao.Repository.UserinfoRepository import UserRpostry
from dao.Repository.WeiBo_Repository import WeiboRepo
import json
import time,os

from dao.Repository.TagR import Tags_handler



def dail_pic(request,pic_obj_list):
    timestamp = time.time()
    user_id = request.session['userinfo']['data'][0]["user_id__id"]
    pic_path = "statics/uploads/%s/%s" % (user_id, timestamp)

    all_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), pic_path)
    if not os.path.exists(all_path):
        os.mkdir(all_path)

    path_list = []

    for obj in pic_obj_list:
        prefix_pic =timestamp+1
        f = open(os.path.join(all_path, "%s_%s"%(prefix_pic,obj.name)), "wb")
        # print(obj.name, obj.chunks(), type(obj.chunks()))
        for chunk in obj.chunks():
            f.write(chunk)
        path_list.append(os.path.join("/%s" % pic_path, "%s_%s"%(prefix_pic,obj.name)))
        timestamp+=1
    print(path_list)
    return json.dumps(path_list)


def create_weibo(request):

    rep = {"status":True,"message":"","data":""}
    if request.method == "POST":
        timestamp = time.time()
        print(time.time())
        pic_data_list =  request.FILES.getlist("fff") # [<InMemoryUploadedFile: 7A57C9B7FE5EF5082F305EF5B72AF274.png (image/png)>, <InMemoryUploadedFile: 024B00103A7C6061429E5F1DB2913C74.png (image/png)>]
        user_id = request.session['userinfo']['data'][0]["user_id__id"]
        perm = 0
        wb_type = request.POST.get("wb_type")
        text = request.POST.get("text")
        pictures_link_id = dail_pic(request,pic_data_list)

        # test 数据
        # pic_path = "statics/%s/%s" %(user_id,timestamp)
        # if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)),pic_path))
        # form_data = request.POST.get("weibo_data")
        # form_data = {"text":"这是一条新的微博","perm":0,"wb_type":0,"pictures_link_id":json.dumps(['/statics/uploads/1/temp/563DE154F522BCEAF9C81A383396C066.jpg']),"user_id":user_id}

        form_data = {"text":text,"perm":perm,"wb_type":wb_type,"pictures_link_id":pictures_link_id,"user_id":user_id}
        print(form_data)
        que_name = "create_weibo_item"
        channel  = Rab_conn_server()

        channel.create_rab_queue(que_name,json.dumps(form_data))
        form_data = json.dumps(form_data)
        rep["data"] = form_data


    return HttpResponse(json.dumps(rep))


def get_new_message(request):

    if request.method == "GET":
        user_id = request.session['userinfo']['data'][0]["user_id__id"]
        channel = Rab_conn_server()

        new_weibo_count = channel.get_num_weibo("user_queue_%s" % str(user_id))

        print("get weibo item_counts",new_weibo_count)

        return HttpResponse(json.dumps({"new_weibo_count":new_weibo_count}))


def get_all_new_weibo(request):

    if request.method == "GET":
        user_id = request.session['userinfo']['data'][0]["user_id__id"]
        channel = Rab_conn_server()
        all_new_weibo = channel.get_all_new_weibo_from_que("user_queue_%s" % str(user_id))

        print("get weibo item_weibo_detail ", all_new_weibo)

        return HttpResponse(json.dumps({"all_new_weibo": all_new_weibo}))


def forward_weibo(request):
    rep = {"status": True, "message": "", "data": ""}
    if request.method == "POST":

        # test 数据
        # pic_path = "statics/%s/%s" %(user_id,timestamp)
        # if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)),pic_path))
        # form_data = request.POST.get("weibo_data")
        # form_data = {"text":"这是一条新的微博","perm":0,"wb_type":0,"pictures_link_id":json.dumps(['/statics/uploads/1/temp/563DE154F522BCEAF9C81A383396C066.jpg']),"user_id":user_id}

        # form_data = {"text": text, "perm": perm, "wb_type": wb_type, "pictures_link_id": pictures_link_id,
        #              "user_id": user_id}

        form_data = request.POST.get("forward_data")

        print(form_data)
        que_name = "create_weibo_item"
        channel = Rab_conn_server()

        channel.create_rab_queue(que_name, json.dumps(form_data))
        form_data = json.dumps(form_data)
        rep["data"] = form_data

    return HttpResponse(json.dumps(rep))
