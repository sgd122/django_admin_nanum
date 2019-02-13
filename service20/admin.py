import datetime
import time
from django.contrib import admin
from django.conf.urls import url
from django.template.response import TemplateResponse
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from service20.models import *
from django.contrib.admin.views.main import ChangeList
from django.utils.html import format_html




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




class ms_ansAdmin(admin.ModelAdmin):
    pass

class ms_mrkAdmin(admin.ModelAdmin):
    pass    

class mpgmAdmin(admin.ModelAdmin):
    pass    

class mp_subAdmin(admin.ModelAdmin):
    pass    



class mentorAdmin(admin.ModelAdmin):
    pass

class menteeAdmin(admin.ModelAdmin):
    pass

class guardianAdmin(admin.ModelAdmin):
    pass

class teacherAdmin(admin.ModelAdmin):
    pass  

class cm_cnv_scrAdmin(admin.ModelAdmin):
    list_display = (
        'eval_item',
        'eval_seq',
        'min_scr',
        'max_scr',
        'eval_unit',
        'fin_scr',
    )


class service20_01_Admin(admin.ModelAdmin):
    change_list_template ="service20/Service20_msch.html"

    list_filter = (
        'ms_id',
        'ms_name',
    )


    list_display = (
        'ms_id',
        'ms_name',
        'status_def',
        'ins_dt',
        'ins_id',
        'apl_term',
        'apl_fr_dt',
        'apl_to_dt',
        'trn_fr_dt',
        'trn_to_dt',
        'tot_apl',
        'cnt_apl',
    )

    fieldsets = [
        #('기본 정보', { 'fields': ( ('ms_id', 'ms_name','apl_term','sup_org','yr_seq','apl_fr_dt','apl_to_dt','trn_fr_dt','trn_to_dt')) }),
        ('기본 정보', { 'fields': ['ms_id', 'ms_name','apl_term','sup_org','yr_seq','apl_fr_dt','apl_to_dt','trn_fr_dt','trn_to_dt'] }),
        ('서류전형', { 'fields': ['tot_apl','cnt_apl','cnt_doc_suc','cnt_doc_res','doc_dt','doc_mgr'] }),
        ('면접전형', { 'fields': ['cnt_intv_pl','cnt_intv_ac','intv_dt','cnt_intv_suc','cnt_iintv_res','intv_mgr'] }),
        ('교육', { 'fields': ['cnt_trn','cnt_mtr'] }),
        #('기본 정보', { 'fields': (('ms_id', 'ms_name','apl_term','sup_org','yr_seq','apl_fr_dt','apl_to_dt','trn_fr_dt','trn_to_dt')) }),
    ]


    """
    def get_queryset(self, request):
        qs = super(service20_01_Admin, self).get_queryset(request)
        s1 = request.GET.get('s1')
        if(s1!=None):
            print("1")
            print(s1)
            vlquery = qs.filter(yr=s1)
        else:
            print("2")
            print(s1)
            vlquery = qs.all()
        return vlquery
    """


    def status_def(self, obj):
        now = datetime.datetime.today()


        if obj.apl_fr_dt == None:
            return '개설중'
        elif now < obj.apl_fr_dt:
            return '개설중'
        elif obj.apl_fr_dt <= now < obj.apl_to_dt:
            return '모집중'
        elif now > obj.apl_to_dt:
            return '모집완료'
        else:
            return '개설중'
    status_def.short_description = '상태'


    """
    def changelist_view(self, request, extra_context=None):
        print("abdf111")

        if request.method == "POST":
            print("bbbb")
        else:
            print("cccc")
            print(request.method)

            a = request.GET.get('s1')

            print(a)


        
        my_context = None

        return super(service20_01_Admin, self).changelist_view(request,extra_context=my_context)

    def get_search_fields(self,request):
        print("ggggghh111")
        return self.search_fields


    def get_list_filter(self, request):
        print("ggggghh222")
        a = request.GET.get('s1')
        print(a)

        list_fil = self.list_filter
        
        list_fil.filter(yr='2018')
        return list_fil
    """

    """
    fields = [
        'ms_id',
        'ms_name',
        'img_src',
        'ins_dt',
        'ins_id',
        'apl_term',
        'apl_fr_dt',
        'apl_to_dt',
        'trn_fr_dt',
        'trn_to_dt',
        'tot_apl',
        'cnt_apl',
    ]
    """


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


#class FooChangeList(ChangeList):
#    def url_for_result(self, result):
        #pk = getattr(result, self.pk_attname)
        #return "<script>alert('1')</script>"

#멘토스쿨 전형
class ms_aplAdmin(admin.ModelAdmin):
    change_list_template ="service20/Service20_ms_apl.html"

    #def get_changelist(self, request, **kwargs):
       # return FooChangeList




    actions = ["persion_info"]

    def persion_info(self, request, queryset):
        print('aa')
        print(request.POST.get('ms_id_id'))
        print(request.POST.get('id'))
        print(request.POST.get('_selected_action'))
        print('bb')

        context = None
        return TemplateResponse(request, "admin/post_status.html", context)

        #queryset.update(is_immortal=True)   

        #for obj in queryset:

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


    persion_info.short_description = "서류전형 상세보기"

    def detail(self, obj):
        print(obj.apl_no)
        print(obj.apl_id)
        return format_html(
            "<a onClick='{}; return false;');>Click Here</a>","window.open('http://naver.com?apl_id="+ obj.apl_id +"','popUp','heigth=500','width=500','resizable=no','location=no','toolbar=no','menubar=no')"
            )


#onclick="window.open('https://www.quackit.com/javascript/examples/sample_popup.cfm','popUpWindow','height=500,width=400,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');"

    list_display = (
        'apl_no',
        'unv_nm',
        'dept_nm',
        'apl_id',
        'apl_nm',
        'gen',
        'score1',
        'score2',
        'score3',
        'score4',
        'detail',

    )

    list_filter = (
        MSSeasonFilter2,
    )

    def define01(self,obj):
        l_one_score1 = obj.score1

        return obj.score1
    define01.short_description = '성적(20)'

    def define02(self,obj):
        return obj.score1
    define02.short_description = '봉사(10)'

    def define03(self,obj):
        return '8'
    define03.short_description = '외국어(10)'

    def define04(self,obj):
        return '6.00'
    define04.short_description = '지원서(10)'   



class ms_subAdmin(admin.ModelAdmin):
    list_display = (
        'ms_id',
        'att_id',
        'att_cdd',
        'att_unit',
        'use_yn',
        'sort_seq',
    )

    fields = [
        'ms_id',
        'att_id',
        'att_cdd',
        'att_unit',
        'use_yn',
        'sort_seq',
    ]


admin.site.register(msch, service20_01_Admin)   
admin.site.register(ms_sub, ms_subAdmin)

admin.site.register(ms_apl, ms_aplAdmin)

#admin.site.register(ms_apl, service20_01_Admin)


admin.site.register(ms_ans, ms_ansAdmin)
admin.site.register(ms_mrk, ms_mrkAdmin)
admin.site.register(mentor, mentorAdmin)
admin.site.register(mentee, menteeAdmin)
admin.site.register(guardian, guardianAdmin)
admin.site.register(teacher, teacherAdmin)

admin.site.register(mpgm, mpgmAdmin)
admin.site.register(mp_sub, mp_subAdmin)

admin.site.register(cm_cnv_scr, cm_cnv_scrAdmin)  
# Register your models here.
