from django.urls import path, re_path
from django.views.generic.base import RedirectView
from . import views

app_name = 'webpage'

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    path('favicon.ico', favicon_view),
    path(r'imprint', views.ImprintView.as_view(), name="imprint"),
    path('', views.GenericWebpageView.as_view(), name="start"),
    path('accounts/login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('set_user_settings/', views.set_user_settings, name='set_user_settings'),
    path('project-info/', views.project_info, name='project_info'),
    re_path(r'^(?P<template>[\w-]+)/$', views.GenericWebpageView.as_view(), name='staticpage'),

]
