from django.contrib import admin
from .models import Entry, APIData, EntryFilter

class MyAdminSite(admin.AdminSite):
    def each_context(self, request):
        context = super(MyAdminSite, self).each_context(request)
        context['accessTokenExpireDate'] = getattr(APIData.objects.last(), "accessTokenExpireDate", "None")
        return context

admin.site = MyAdminSite(name='my_custom_admin')
#admin_site.register(Entry)
#admin_site.register(APIData)
admin.site.register(Entry)
admin.site.register(APIData)
admin.site.register(EntryFilter)


