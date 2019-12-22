"""db_pro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls import url
from user_click import views
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='search')),
    url(r'^index/', views.index),
    url(r'^upload', views.upload),
    url(r'^search', views.search),
    url(r'^datastu/', views.datastu),
    url(r'^dataproblem/', views.dataproblem),
    url(r'^picup/', views.picup)
    # url(r"^",admin.site.urls)
    # url(r'^', include("user_click.urls"))
]

urlpatterns += static(settings.IMG_URL, document_root=settings.IMG_ROOT)
