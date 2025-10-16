from django.urls import path
from django.contrib import admin

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name="index"),
    path('stats/', views.statistics, name="stats"),
    # path('generator/', views.generator, name="generator"),
    path('duplicateFilter/', views.duplicate_filter, name="duplicateFilter"),
    path('AIFilter/', views.AI_filter, name="AIFilter"),
    path("admin/", admin.site.urls),
    path("accounts/", admin.site.urls),
    path('callback/', views.callback, name="callback"),
    path('subscribe/', views.subscribe, name="subscribe"),
    path('gettoken/', views.get_token, name="gettoken"),
    path("listsub/", views.list_subs, name="listsub"),
]
