import datetime
import time
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from service20.models import *



class mschAdmin(admin.ModelAdmin):
    list_display = (
        'ms_id',
        'ms_name',
    )


class MSSeasonFilter2(SimpleListFilter):
    title = '학기(교육시기)'
    parameter_name = 'season'

    def lookups(self, request, model_admin):
        return [('before', '모집예정'), ('ongoing', '모집중'), ('after', '모집마감')]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(course_season=self.value())
        return queryset

class ms_aplAdmin(admin.ModelAdmin):
    change_list_template ="stdApply/submit.html"

    list_display = (
        'apl_no',
        'unv_nm',
        'dept_nm',
        'apl_id',
        'apl_nm',
        'gen',
        'define01',
        'define02',
        'define03',
        'define04',
    )

    list_filter = (
        MSSeasonFilter2,
    )

    def define01(self,obj):
    	return '16'
    define01.short_description = '성적(20)'

    def define02(self,obj):
    	return '6'
    define02.short_description = '봉사(10)'

    def define03(self,obj):
    	return '8'
    define03.short_description = '외국어(10)'

    def define04(self,obj):
    	return '6.00'
    define04.short_description = '지원서(10)'   

class ms_ansAdmin(admin.ModelAdmin):
    pass

class ms_mrkAdmin(admin.ModelAdmin):
    pass    

class mpgmAdmin(admin.ModelAdmin):
    pass    


class mentorAdmin(admin.ModelAdmin):
    pass

class cm_cnv_scrAdmin(admin.ModelAdmin):
    pass    

admin.site.register(msch, mschAdmin)   
admin.site.register(ms_apl, ms_aplAdmin)
admin.site.register(ms_ans, ms_ansAdmin)
admin.site.register(ms_mrk, ms_mrkAdmin)
admin.site.register(mentor, mentorAdmin)
admin.site.register(mpgm, mpgmAdmin)

admin.site.register(cm_cnv_scr, cm_cnv_scrAdmin)  
# Register your models here.
