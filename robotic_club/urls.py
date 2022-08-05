"""robotic_club URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.generic import TemplateView
from core import urls
from django.contrib.auth import views as auth_views #new
import os 

admin.site.site_header = "Admin"
admin.site.site_title = "admin"
admin.site.index_title = "WELCOME TO PORTAL"
urlpatterns=[
    path('admin/login/', auth_views.LoginView.as_view(template_name='admin/register.html'), name='login'), #new
    path('admin/logout/', auth_views.LogoutView.as_view(template_name='admin/logout.html'), name='logout'), #new
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path("select2/", include("django_select2.urls"))
    

]
if os.getenv('MAINTAINS','off') == "on" :
    urlpatterns=[
        *urlpatterns,
        # match any url link that don't start with admin
        re_path(r'^((?!admin).)*$',TemplateView.as_view(template_name="maintains.html"))
    ]
else:
    

    urlpatterns = [
        *urlpatterns,
        # path("m",TemplateView.as_view(template_name="maintains.html")),
        path('',include(urls)),
        path('members/',include('members.urls')),

    ]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
