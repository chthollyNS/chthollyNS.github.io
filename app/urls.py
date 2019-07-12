from django.urls import path

from app.views import *

urlpatterns = [
    path('login/', login,name='login'),
    path('register/', register,name='register'),
    path('logout/<str:username>/<str:username1>/',logout,name='logout'),
    path('index/<str:username>/',index,name='index'),
    path('cancel/<str:username>/',cancel,name='cancel'),
    path('del/<str:id>/<str:username>/',cancel2),
    path('upload/<str:name>/', upload, name='upload'),
    path('admin/<str:username>/', admin, name='admin'),
    path('balance/<str:name>/<str:name1>/', balance, name='balance'),
    path('search/<str:name>/<str:name1>/', search, name='search'),
    path('title/<str:name>/<str:name1>/',title, name='title'),
    path('title_search/<str:name>/', title_search, name='title_search'),
    path('title_search1/<str:name>/<str:name1>/', title_search1,name='title_search1'),
    path('personal/<str:name>/', personal),
    path('<str:name>/<str:name1>/shop/', shop),
    path('<str:name>/<str:name1>/now/', now),
    path('trolley/<str:name>/', trolley),
    path('del_id/<str:name>/<str:name1>/', del_id),
    path('consumes/<str:name>/<str:name1>/<str:name2>/',consume),
    path('details/<str:name>/<str:name1>/',details),
    path('alter/<str:name>/<str:name1>/', alter),
    path('revise/<str:name>/<str:name1>/<str:name2>/', revise),
    path('consume/<str:name>/<str:name1>/<str:name2>/',consume_updata),
    path('all/<str:name>/',all_shop),
]
