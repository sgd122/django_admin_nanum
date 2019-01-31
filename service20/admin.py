import datetime
import time
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from service20.models import msch,ms_apl


class mschAdmin(admin.ModelAdmin):
    list_display = (
        'ms_id',
        'ms_name',
    )

class ms_aplAdmin(admin.ModelAdmin):
    list_display = (
        'apl_id',
        'apl_nm',
    )

admin.site.register(msch, mschAdmin)   
admin.site.register(ms_apl, ms_aplAdmin)   
# Register your models here.
