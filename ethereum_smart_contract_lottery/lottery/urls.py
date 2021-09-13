from django.urls import path

from . import views

app_name = 'lottery'

urlpatterns = [
    path('', views.index, name='index'),
    path('createLottery/', views.createLottery, name='createLottery'),
    path('joinLottery/', views.joinLottery, name='joinLottery'),
    path('listLotteries/', views.listLotteries, name='listLotteries'),
    path('<int:lottery_id>/lotteryInfo/', views.lotteryInfo, name='lotteryInfo'),
    path('creating/', views.create_form_handling, name='create_form_handling'),
    path('joining/', views.join_form_handling, name='join_form_handling'),
    path('<int:status_id>/statusPage/', views.statusPage, name='statusPage'),
    path('checkIndex/', views.checkIndex, name='checkIndex'),
]
