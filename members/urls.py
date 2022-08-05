
from django.urls import path

from .views import *

app_name='members'
urlpatterns=[


    path('alumni/',alumni_view,name='alumni_view'),
    path('<slug:slug>/',simpleMembersView,name='members_list'),
    path('<slug:slug>/<slug:clubyear_slug>/',simpleMembersView,name='members_list'),

]