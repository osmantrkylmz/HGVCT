from django.conf.urls import url

from index import views



urlpatterns = [

    
        url(r'^delete/.*/$', views.delete,name = "del"),
        url(r'login/$', views.login, name='login'),
		url(r'logout/$', views.logout, name='logout'),

        ]
