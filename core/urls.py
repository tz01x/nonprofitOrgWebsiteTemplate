
from os import name
from django.urls import path,include
from .views import *
app_name="core"
urlpatterns = [

    # path('test/',testview,name='test'),
    path('termsandconditions/',termsAndConditions,name='termsandconditions'),
    
    path ("",index,name='index'),
    path('newsletter/subscribe/',subscribeToNewsLetter,name='newsletter_sub'),
    path('get-intouch/',getintouch,name='getintouch'),
    path ("registation/",signup_page,name='signup'),
    path('registation/complect/',reg_complect,name='reg_complect'),
    
    path ("publications/",publication,name='publications'),
    path ("articles/",articles,name='articles'),
  
    path ("article-and-publication/<slug:slug>/",BlogAndArticleDetails.as_view(),name='blogAndArticle'),
    path ("gallery/",gallaryView,name='gallery'),
    path ("gallery/<slug:curr_semester_slug>/",gallaryView,name='gallery'),

    # news
    
    path('news/',newsListView,name='news'),
    path('news/<slug:slug>/',NewsDetailsView.as_view(),name='news_details'),

    # event 


    path('event/details/<slug:slug>/',EventDetails.as_view(),name='event'),
    path('event/<slug:slug>/',eventView,name='event_list'),


    # comments 

    path('create/comment/<str:commentFor>/<slug:slug>/',createComment,name='createComment'),
    path('add_replay/<int:pk>/',addReplay,name='addReplay'),
    

    # api 
    path('api/gallery/',GalleryListAPIView.as_view(),name='api_gallery'),
    path('api/gallery/<slug:curr_semester_slug>/',GalleryListAPIView.as_view(),name='api_gallery')
    
    
]
