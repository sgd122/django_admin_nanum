import datetime
import time
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from service10.models import *

from service20.models import *

class com_cdhAdmin(admin.ModelAdmin):
	list_display = (
	        'std_grp_code',
	        'lang_key',
	        'std_grp_code_nm',
	        'rmrk',
	        'use_indc',
	        'cls_date',
	        'sys_id',
	        'grp_type',
	    )    


class com_cddAdmin(admin.ModelAdmin):
	list_display = (
	        'std_grp_code',
	        'std_detl_code',
	        'lang_key',
	        'std_detl_code_nm',
	        'rmrk',
	        'rmrk_2',
	        'up_std_detl_cd',
	        'use_indc',
	        'cls_date',
	        'sort_seq_no',
	        'co_code',
	        'plnt',
	        'sys_id',
	        'text1',
	        'text2',
	        'text3',
	        'text4',
	        'text5',
	    )    

class vm_nanum_stdt_Admin(admin.ModelAdmin):
	pass


class articleAdmin(admin.ModelAdmin):
	pass

admin.site.register(com_cdh, com_cdhAdmin)   
admin.site.register(com_cdd, com_cddAdmin)
admin.site.register(vm_nanum_stdt, vm_nanum_stdt_Admin)

admin.site.register(article, articleAdmin)