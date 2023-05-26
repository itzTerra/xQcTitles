from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

class MyAdminConfig(AdminConfig):
    default_site = 'main.admin.MyAdminSite'

class MainConfig(AppConfig):
    name = 'main'
