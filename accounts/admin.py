from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *


class AnonymousUserResource(resources.ModelResource):
	fields = ('id','created_date','ip_address')
	class Meta:
		model = AnonymousUser


class AnonymousUserAdmin(ImportExportModelAdmin):
	list_display = ['created_date','id','ip_address']

class ProfileResource(resources.ModelResource):
	fields = ('id','user','phone','short_description')
	class Meta:
		model = Profile


class ProfileUserAdmin(ImportExportModelAdmin):
	list_display = ['id','user','phone','short_description']


admin.site.register(UserProfile)
admin.site.register(Profile, ProfileUserAdmin)
admin.site.register(AnonymousUser, AnonymousUserAdmin)

admin.site.register(Room)
