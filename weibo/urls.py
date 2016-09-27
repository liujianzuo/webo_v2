"""weibo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from web.home import account,test
from web.controller import controller as cont
from web.main import index as weibo_index
from  web.controller import new_account as n_acc
from web.test import test as tt
from web.rab_que import queue_handle


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', account.login),
    url(r'^logout/', n_acc.logout),
    url(r'^register/', account.register),

    # url(r'^weibo_login/', cont.blog),
    url(r'^blog/', cont.blog),
    url(r'^tet/', test.test),
    url(r'^pub/', cont.pub),
    url(r'^article/', cont.article),
    url(r'^index/', weibo_index.index),
    url(r'^lay_out/', weibo_index.lay_out),
    url(r'^test_lay_out/', weibo_index.test_lay_out),
    url(r'^search/',weibo_index.search),
    url(r'^weibo_login/',n_acc.login),
    url(r'^add_tags/',weibo_index.add_tags),
    url(r'^personal/', weibo_index.personal),
    url(r'^change_userprofile_name/',weibo_index.change_userprofile_name),
    # url(r'^file_up/',tt.file_up),
    url(r'^file_up/',weibo_index.pic_handle),
    url(r'^create_weibo/',queue_handle.create_weibo),
    url(r'^get_num_weibo/',queue_handle.get_new_message),
    url(r'^get_all_new_weibo/',queue_handle.get_all_new_weibo),
    url(r'^wei_bo_detail_test/',tt.wei_bo_detail_test),
    # url(r'^post_search/',weibo_index.post_search),
]