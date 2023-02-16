from django.urls import path, re_path
from django.views.generic.base import RedirectView
from . import views

app_name = 'webpage'

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    re_path(r'^favicon\.ico$', favicon_view),
    re_path(r'^imprint', views.ImprintView.as_view(), name="imprint"),
    re_path(r'^$', views.GenericWebpageView.as_view(), name="start"),
    re_path(r'^accounts/login/$', views.user_login, name='user_login'),
    re_path(r'^logout/$', views.user_logout, name='user_logout'),
    re_path(r'^set_user_settings/$', views.set_user_settings, name='set_user_settings'),
    re_path(r'^project-info/$', views.project_info, name='project_info'),
    re_path(r'^(?P<template>[\w-]+)/$', views.GenericWebpageView.as_view(), name='staticpage'),

]
