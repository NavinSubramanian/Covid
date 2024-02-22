from django.urls import path,include
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('home',home),
    path('login',login, name="login"),
    path('logout',logout, name="logout"),
    path('register',register, name="register"),
    path('adminpanel',adminpanel, name="adminpanel"),
    path('dashboard',dashboard, name="dashboard"),
    path('dashboard/<int:pk>',seperate, name="seperate"),
    path('delete_center/<int:center_id>', delete_center, name='delete_center'),
    path('addslot', addslot, name='addslot'),
]