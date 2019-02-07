import datetime
import time
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from service10.models import *

class com_cdhAdmin(admin.ModelAdmin):
    pass

class com_cddAdmin(admin.ModelAdmin):
	pass

class vm_nanum_stdt_Admin(admin.ModelAdmin):
	pass


class articleAdmin(admin.ModelAdmin):
	pass

admin.site.register(com_cdh, com_cdhAdmin)   
admin.site.register(com_cdd, com_cddAdmin)
admin.site.register(vm_nanum_stdt, vm_nanum_stdt_Admin)

admin.site.register(article, articleAdmin)