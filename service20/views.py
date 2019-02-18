from django.shortcuts import render
from rest_framework import generics, serializers
from django.http import HttpResponse,Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.shortcuts import get_object_or_404,render
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse,Http404, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from service10.models import *
from service20.models import *
from polls.models import Choice, Question
from django.db.models import Max


from collections  import OrderedDict
import json
# api/moim 으로 get하면 이 listview로 연결

class Service20ListSerializer(serializers.ModelSerializer):



    status = serializers.SerializerMethodField()
    applyYn = serializers.SerializerMethodField()
    class Meta:
        model = msch
        fields = ('ms_id', 'ms_name','yr','yr_seq','sup_org','img_src','ins_dt','ins_id','apl_term','apl_fr_dt','apl_to_dt','trn_fr_dt','trn_to_dt','tot_apl','cnt_apl','status','applyYn')

    def get_status(self,obj):
        request = self.context['request']
        l_user_id = request.GET.get('user_id', None)
        
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
    get_status.short_description = '상태'        

    def get_applyYn(self,obj):
        request = self.context['request']
        l_user_id = request.GET.get('user_id', None)
        

class Service20ListView(generics.ListAPIView):



    queryset = msch.objects.all()
    serializer_class = Service20ListSerializer

    def list(self, request):
        l_yr = request.GET.get('yr', None)
        l_apl_term = request.GET.get('trn_term', None)
        l_user_id = request.GET.get('user_id', None)

        query = "select ifnull((select 'Y' from service20_ms_apl where yr = '"+str(l_yr)+"' and term_div = '"+str(l_apl_term)+"' and apl_id = '"+str(l_user_id)+"' and ms_id = A.ms_id),'N') AS applyFlag,A.* from service20_msch A where A.yr='"+str(l_yr)+"' and A.apl_term='"+str(l_apl_term)+"'"
        queryset = msch.objects.raw(query)

        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)


        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


        



def stdApplyStdView(request):
    ms_aplAll = ms_apl.objects.all()
    context = None
    return render(request, 'stdApply/submit.html', context)


def Service20_01_View(request):
    ms_aplAll = ms_apl.objects.all()
    context = None
    return render(request, 'service20/Service20_01.html', context)    



@csrf_exempt
def post_user_info(request):
    ida = request.POST.get('user_id', None)
    ms_ida = request.POST.get('ms_id', None)
    l_yr = request.POST.get('yr', None)
    
    
    #created,created_flag = vm_nanum_stdt.apl_id.get_or_create(user=request.user)
    created_flag = vm_nanum_stdt.objects.filter(apl_id=ida).exists()

    # ms_apl_flag = ms_apl.objects.filter(apl_id=ida,ms_id=ms_ida).exists()
    ms_apl_flag = ms_apl.objects.filter(apl_id=ida,yr=l_yr,ms_id=ms_ida).exists()

    if not ms_apl_flag:
        applyYn = 'N'
    else:
        applyYn = 'Y'

    #rows = vm_nanum_stdt.objects.filter(apl_id=ida)
    #rows2 = vm_nanum_stdt.objects.get("apl_nm")
    if not created_flag:
        message = "Fail"
        context = {'message': message}
    else:
        
        message = "Ok"
        rows = vm_nanum_stdt.objects.filter(apl_id=ida)[0]
        rows2 = mp_sub.objects.filter(mp_id=ms_ida)
        rows3 = msch.objects.filter(ms_id=ms_ida)[0]


        for val in rows2:
            key1 = val.att_id
            #key2 = val.att_cdd

        #question01 = com_cdd.objects.filter(std_grp_code=key1)[0].rmrk
        #question02 = com_cdd.objects.filter(std_grp_code=key1)[1].rmrk
        #question03 = com_cdd.objects.filter(std_grp_code=key1)[2].rmrk
        #question04 = com_cdd.objects.filter(std_grp_code=key1)[3].rmrk
        #question05 = com_cdd.objects.filter(std_grp_code=key1)[4].rmrk

        context = {'message': message,
                    'applyYn' : applyYn,
                    'apl_nm' : rows.apl_nm,
                    'univ_cd' : rows.univ_cd,
                    'univ_nm' : rows.univ_nm,
                    'grad_div_cd' : rows.grad_div_cd,
                    'grad_div_nm' : rows.grad_div_nm,
                    'cllg_cd' : rows.cllg_cd,
                    'cllg_nm' : rows.cllg_nm,
                    'dept_cd' : rows.dept_cd,
                    'dept_nm' : rows.dept_nm,
                    'mjr_cd' : rows.mjr_cd,
                    'mjr_nm' : rows.mjr_nm,
                    'brth_dt' : rows.brth_dt,
                    'gen_cd' : rows.gen_cd,
                    'gen_nm' : rows.gen_nm,
                    'yr' : rows.yr,
                    'sch_yr' : rows.sch_yr,
                    'term_div' : rows.term_div,
                    'term_nm' : rows.term_nm,
                    'stdt_div' : rows.stdt_div,
                    'stdt_nm' : rows.stdt_nm,
                    'mob_nm' : rows.mob_nm,
                    'tel_no' : rows.tel_no,
                    'tel_no_g' : rows.tel_no_g,
                    'h_addr' : rows.h_addr,
                    'post_no' : rows.post_no,
                    'email_addr' : rows.email_addr,
                    'bank_acct' : rows.bank_acct,
                    'bank_cd' : rows.bank_cd,
                    'bank_nm' : rows.bank_nm,
                    'bank_dpsr' : rows.bank_dpsr,
                    'pr_yr' : rows.pr_yr,
                    'pr_sch_yr' : rows.pr_sch_yr,
                    'pr_term_div' : rows.pr_term_div,
                    'score01' : rows.score01,
                    'score02' : rows.score02,
                    'score03' : rows.score03,
                    'score04' : rows.score04,
                    'score04_tp' : rows.score04_tp,
                    'score05' : rows.score05,
                    'ms_id' : rows3.ms_id,
                    'ms_name' : rows3.ms_name,
                    }
    

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


class post_user_info_Quest_Serializer(serializers.ModelSerializer):

   
    std_detl_code_nm = serializers.SerializerMethodField()
    std_detl_code = serializers.SerializerMethodField()
    rmrk = serializers.SerializerMethodField()

    class Meta:
        model = ms_sub
        fields = ('id','ms_id','att_id','att_cdh','att_cdd','att_val','att_unit','use_yn','sort_seq','std_detl_code','std_detl_code_nm','rmrk')        

    def get_std_detl_code(self,obj):
        return obj.std_detl_code

    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm

    def get_rmrk(self,obj):
        return obj.rmrk  

class post_user_info_Quest(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = post_user_info_Quest_Serializer
    def list(self, request):
        #ms_sub 테이블에서 질문내역 조회
        key1 = request.GET.get('ms_id', None)           
        l_exist = ms_sub.objects.filter(ms_id=key1).exists()
        
        query = "select B.std_detl_code,B.std_detl_code_nm,B.rmrk,A.* from service20_ms_sub A left outer join service20_com_cdd B on (A.att_id = B.std_grp_code and A.att_cdd = B.std_detl_code) where A.ms_id = '"+key1+"'"
        queryset = ms_sub.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토스쿨(관리자) - 질문
class post_user_info_view_Quest_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_grp_code','std_detl_code','std_detl_code_nm','rmrk','use_indc')
# 멘토스쿨(관리자) - 질문2
class post_user_info_view_Quest_Serializer2(serializers.ModelSerializer):

    std_detl_code_nm = serializers.SerializerMethodField()
    rmrk = serializers.SerializerMethodField()

    class Meta:
        model = ms_ans
        fields = ('id','ms_id','test_div','apl_no','ques_no','apl_id','apl_nm','sort_seq','ans_t1','ans_t2','ans_t3','score','std_detl_code_nm','rmrk')        

    
    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm

    def get_rmrk(self,obj):
        return obj.rmrk  


# 멘토스쿨(관리자) - 질문
class post_user_info_view_Quest(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = post_user_info_view_Quest_Serializer2
    def list(self, request):
        #ms_sub 테이블에서 질문내역 조회
        key1 = request.GET.get('ms_id', None) 
        l_user_id = request.GET.get('user_id', None)           
        
        query = "select B.std_detl_code_nm,B.rmrk,A.* from service20_ms_ans A, service20_com_cdd B where A.ques_no = B.std_detl_code and B.std_grp_code in (select att_cdh from service20_ms_sub where ms_id = '"+key1+"') and A.ms_id = '"+key1+"' and apl_id = '"+l_user_id+"'"
        queryset = ms_ans.objects.raw(query)


        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)








class post_user_info_adm_Serializer(serializers.ModelSerializer):
    
    ms_name = serializers.SerializerMethodField()
    pr_yr = serializers.SerializerMethodField()
    pr_sch_yr = serializers.SerializerMethodField()
    pr_term_div = serializers.SerializerMethodField()

    class Meta:
        model = ms_apl
        fields = ('ms_id','apl_no','mntr_id','indv_div','team_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','ms_name','pr_yr','pr_sch_yr','pr_term_div')

    def get_ms_name(self,obj):
        return obj.ms_name

    def get_pr_yr(self,obj):
        return obj.pr_yr

    def get_pr_sch_yr(self,obj):
        return obj.pr_sch_yr

    def get_pr_term_div(self,obj):
        return obj.pr_term_div    

class post_user_info_adm(generics.ListAPIView):
    queryset = ms_apl.objects.all()
    serializer_class = post_user_info_adm_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        ms_ida = request.GET.get('ms_id', None)
        l_yr = request.GET.get('yr', None)
        
        # ms_apl
        query = "select C.ms_name,B.pr_yr,B.pr_sch_yr,B.pr_term_div,A.* from service20_ms_apl A,service10_vm_nanum_stdt B,service20_msch C where A.apl_id=B.apl_id and A.ms_id = C.ms_id and A.yr='"+l_yr+"' and A.ms_id = '"+ms_ida+"' and A.apl_id='"+ida+"'"
        queryset = ms_apl.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)




# 멘토스쿨 신청
@csrf_exempt
def post_msApply(request):
    ida = request.POST.get('memberNo', None)
    programId = request.POST.get('programID', None)
    que1 = request.POST.get('que1', None)
    que2 = request.POST.get('que2', None)
    que3 = request.POST.get('que3', None)
    que4 = request.POST.get('que4', None)
    que5 = request.POST.get('que5', None)

    ms_ida = request.POST.get('ms_id', None)
    apl_max = request.POST.get('aplMax', 0)
    #created,created_flag = vm_nanum_stdt.apl_id.get_or_create(user=request.user)
    ms_id = programId
    ms_apl_max = ms_apl.objects.all().aggregate(vlMax=Max('apl_no'))
    rows = vm_nanum_stdt.objects.filter(apl_id=ida)[0]
    #ms_apl_max = ms_apl.objects.all().last()
    #ms_apl_max = ms_apl_max + 1
    apl_no = ms_apl_max
    apl_id = ida
    
    max_no = ms_apl_max['vlMax']    

    if max_no == None:
        apl_no = 0;
    else:
        apl_no = ms_apl_max['vlMax']
        apl_no = apl_no + 1;
    
    
    model_instance = ms_apl(
        ms_id=ms_id, 
        apl_no=apl_no, 
        apl_id=apl_id,
        apl_nm=rows.apl_nm,
        unv_cd=rows.univ_cd,
        unv_nm=rows.univ_nm,
        cllg_cd=rows.cllg_cd,
        cllg_nm=rows.cllg_nm,
        dept_cd=rows.dept_cd,
        dept_nm=rows.dept_nm,
        brth_dt=rows.brth_dt,
        gen=rows.gen_cd,
        yr=rows.yr,
        term_div=rows.term_div,
        sch_yr=rows.sch_yr,
        mob_no=rows.mob_nm,
        tel_no=rows.tel_no,
        tel_no_g=rows.tel_no_g,
        h_addr=rows.h_addr,
        score1=rows.score01,
        score2=rows.score02,
        score3=rows.score03,
        score4=rows.score04,
        score5=rows.score05,
        )
    model_instance.save()
    
    apl_max = int(apl_max)

    for i in range(0,apl_max):
        anst2 = request.POST.get('que'+str(i+1), None)
        ques_no = request.POST.get('ques_no'+str(i+1), None)

        model_instance2 = ms_ans(
            ms_id=ms_id, 
            test_div='10', 
            apl_no=apl_no,
            ques_no=ques_no,
            apl_id=apl_id,
            apl_nm=rows.apl_nm,
            sort_seq =i+1,
            ans_t2=anst2
            )
        model_instance2.save()
        
    context = {'message': 'Ok'}

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})




class mpmgListSerializer(serializers.ModelSerializer):

    testField = serializers.SerializerMethodField()
    class Meta:
        model = mpgm
        fields = ('mp_id','mp_name','status','img_src','testField')

    def get_testField(self, obj):
        return 'test'     


class mpmgListView(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = mpmgListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)





class MP0101M_list_Serializer(serializers.ModelSerializer):

    applyFlag = serializers.SerializerMethodField()
    applyStatus = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = mpgm
        fields = ('mp_id','mp_name','status','yr','yr_seq','sup_org','applyFlag','applyStatus','apl_fr_dt','apl_to_dt','mnt_fr_dt','mnt_to_dt','cnt_trn','status')

    def get_applyFlag(self, obj):
        # return 'Y'     
        return obj.applyFlag    
    def get_applyStatus(self, obj):
        if obj.applyFlag == 'Y':
            return '지원'
        elif obj.applyFlag == 'N':
            return '미지원'    
        # return obj.applyStatus    

    def get_status(self,obj):
        request = self.context['request']
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
    get_status.short_description = '상태'     



class MP0101M_list(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0101M_list_Serializer

    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_status = request.GET.get('status', "")
        ida = request.GET.get('user_id', "")

        query = "select ifnull((select 'Y' from service20_mp_mtr where yr = '"+str(l_yr)+"' and apl_id = '"+str(ida)+"' and mp_id = A.mp_id),'N') AS applyFlag,A.* from service20_mpgm A where A.yr='"+str(l_yr)+"' and A.apl_term='"+str(l_apl_term)+"'"
        
        # 멘토만 조회가능.
        # query = "select ifnull((select 'Y' from service20_mp_mtr where yr = '"+str(l_yr)+"' and apl_id = '"+str(ida)+"' and mp_id = A.mp_id),'N') AS applyFlag,A.* from service20_mpgm A where A.yr='"+str(l_yr)+"' and A.apl_term='"+str(l_apl_term)+"' and (select count(1) from service20_mentor where mntr_id = '"+ida+"') > 0 "

        queryset = mpgm.objects.raw(query)


        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 멘토링 프로그램 질문유형 가져오기
class MP0101M_quest_Serializer(serializers.ModelSerializer):

    std_detl_code_nm = serializers.SerializerMethodField()
    std_detl_code = serializers.SerializerMethodField()
    rmrk = serializers.SerializerMethodField()
    class Meta:
        model = mp_sub
        fields = ('id','mp_id','att_id','att_seq','att_cdh','att_cdd','att_val','use_yn','sort_seq','std_detl_code','std_detl_code_nm','rmrk')

        
    def get_std_detl_code(self,obj):
        return obj.std_detl_code
        
    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm

    def get_rmrk(self,obj):
        return obj.rmrk    

# 멘토링 프로그램 질문유형 가져오기
class MP0101M_quest(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = MP0101M_quest_Serializer
    def list(self, request):
        #mp_sub 테이블에서 질문내역 조회
        key1 = request.GET.get('mp_id', None)           
        
        query = "select B.std_detl_code,B.std_detl_code_nm,B.rmrk,A.* from service20_mp_sub A left outer join service20_com_cdd B on (A.att_id = B.std_grp_code and A.att_cdd = B.std_detl_code) where A.mp_id = '"+key1+"'"
        queryset = mp_sub.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 신청
@csrf_exempt
def MP0101M_save(request):
    ida = request.POST.get('memberNo', None)
    programId = request.POST.get('programID', None)
    que1 = request.POST.get('que1', None)
    que2 = request.POST.get('que2', None)
    que3 = request.POST.get('que3', None)
    que4 = request.POST.get('que4', None)
    que5 = request.POST.get('que5', None)

    ms_ida = request.POST.get('ms_id', None)
    apl_max = request.POST.get('aplMax', 0)
    
    #created,created_flag = vm_nanum_stdt.apl_id.get_or_create(user=request.user)
    ms_id = programId
    mp_mtr_max = mp_mtr.objects.all().aggregate(vlMax=Max('apl_no'))
    rows = vm_nanum_stdt.objects.filter(apl_id=ida)[0]
    #mp_mtr_max = mp_mtr.objects.all().last()
    #mp_mtr_max = mp_mtr_max + 1
    apl_no = mp_mtr_max
    apl_id = ida
    v_gen = ""
    if str(rows.gen_cd) == "1":
        v_gen = "M"
    else:
        v_gen = "F"
    
    max_no = mp_mtr_max['vlMax']    

    if max_no == None:
        apl_no = 0;
    else:
        apl_no = mp_mtr_max['vlMax']
        apl_no = apl_no + 1;
    
    
    model_instance = mp_mtr(
        mp_id=ms_id, 
        apl_no=apl_no, 
        mntr_id=ida,
        apl_id=apl_id,
        apl_nm=rows.apl_nm,
        unv_cd=rows.univ_cd,
        unv_nm=rows.univ_nm,
        cllg_cd=rows.cllg_cd,
        cllg_nm=rows.cllg_nm,
        dept_cd=rows.dept_cd,
        dept_nm=rows.dept_nm,
        brth_dt=rows.brth_dt,
        gen=v_gen,
        yr=rows.yr,
        term_div=rows.term_div,
        sch_yr=rows.sch_yr,
        mob_no=rows.mob_nm.replace('-', ''),
        tel_no=rows.tel_no.replace('-', ''),
        tel_no_g=rows.tel_no_g.replace('-', ''),
        h_addr=rows.h_addr,
        score1=rows.score01,
        score2=rows.score02,
        score3=rows.score03,
        score4=rows.score04,
        score5=rows.score05,
        )
    model_instance.save()
    
    apl_max = int(apl_max)

    for i in range(0,apl_max):
        anst2 = request.POST.get('que'+str(i+1), None)
        ques_no = request.POST.get('ques_no'+str(i+1), None)

        model_instance2 = mp_ans(
            mp_id=ms_id, 
            test_div='10', 
            apl_no=apl_no,
            ques_no=ques_no,
            apl_id=apl_id,
            apl_nm=rows.apl_nm,
            sort_seq =i+1,
            ans_t2=anst2
            )
        model_instance2.save()
        
    context = {'message': 'Ok'}

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

@csrf_exempt
def MP0101M_detail(request):    

    ida = request.POST.get('user_id', None)
    ms_ida = request.POST.get('ms_id', None)
    l_yr = request.POST.get('yr', None)

    created_flag = vm_nanum_stdt.objects.filter(apl_id=ida).exists()
    ms_apl_flag = mp_mtr.objects.filter(apl_id=ida,mp_id=ms_ida).exists()
    
    if not ms_apl_flag:
        applyYn = 'N'
    else:
        applyYn = 'Y'

    
    if not created_flag:
        message = "Fail"
        context = {'message': message}
    else:
        
        message = "Ok"
        rows = vm_nanum_stdt.objects.filter(apl_id=ida)[0]
        rows2 = mp_sub.objects.filter(mp_id=ms_ida)
        rows3 = mpgm.objects.filter(mp_id=ms_ida)[0]


        for val in rows2:
            key1 = val.att_id
            #key2 = val.att_cdd


        context = {'message': message,
                    'applyYn' : applyYn,
                    'apl_nm' : rows.apl_nm,
                    'univ_cd' : rows.univ_cd,
                    'univ_nm' : rows.univ_nm,
                    'grad_div_cd' : rows.grad_div_cd,
                    'grad_div_nm' : rows.grad_div_nm,
                    'cllg_cd' : rows.cllg_cd,
                    'cllg_nm' : rows.cllg_nm,
                    'dept_cd' : rows.dept_cd,
                    'dept_nm' : rows.dept_nm,
                    'mjr_cd' : rows.mjr_cd,
                    'mjr_nm' : rows.mjr_nm,
                    'brth_dt' : rows.brth_dt,
                    'gen_cd' : rows.gen_cd,
                    'gen_nm' : rows.gen_nm,
                    'yr' : rows.yr,
                    'sch_yr' : rows.sch_yr,
                    'term_div' : rows.term_div,
                    'term_nm' : rows.term_nm,
                    'stdt_div' : rows.stdt_div,
                    'stdt_nm' : rows.stdt_nm,
                    'mob_nm' : rows.mob_nm,
                    'tel_no' : rows.tel_no,
                    'tel_no_g' : rows.tel_no_g,
                    'h_addr' : rows.h_addr,
                    'post_no' : rows.post_no,
                    'email_addr' : rows.email_addr,
                    'bank_acct' : rows.bank_acct,
                    'bank_cd' : rows.bank_cd,
                    'bank_nm' : rows.bank_nm,
                    'bank_dpsr' : rows.bank_dpsr,
                    'pr_yr' : rows.pr_yr,
                    'pr_sch_yr' : rows.pr_sch_yr,
                    'pr_term_div' : rows.pr_term_div,
                    'score01' : rows.score01,
                    'score02' : rows.score02,
                    'score03' : rows.score03,
                    'score04' : rows.score04,
                    'score04_tp' : rows.score04_tp,
                    'score05' : rows.score05,
                    'ms_id' : rows3.mp_id,
                    'ms_name' : rows3.mp_name,
                    }
    

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

class MP0101M_adm_list_Serializer(serializers.ModelSerializer):
    
    mp_name = serializers.SerializerMethodField()
    pr_yr = serializers.SerializerMethodField()
    pr_sch_yr = serializers.SerializerMethodField()
    pr_term_div = serializers.SerializerMethodField()

    class Meta:
        model = mp_mtr
        fields = ('mp_id','apl_no','mntr_id','indv_div','team_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','bank_acct','bank_cd','bank_nm','bank_dpsr','cnt_mp_a','cnt_mp_p','cnt_mp_c','cnt_mp_g','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','mp_name','pr_yr','pr_sch_yr','pr_term_div')

    def get_mp_name(self,obj):
        return obj.mp_name

    def get_pr_yr(self,obj):
        return obj.pr_yr

    def get_pr_sch_yr(self,obj):
        return obj.pr_sch_yr

    def get_pr_term_div(self,obj):
        return obj.pr_term_div    

class MP0101M_adm_list(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MP0101M_adm_list_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        ms_ida = request.GET.get('ms_id', None)
        l_yr = request.GET.get('yr', None)
        
        # mpgm
        query = "select C.mp_name,B.pr_yr,B.pr_sch_yr,B.pr_term_div,A.* from service20_mp_mtr A,service10_vm_nanum_stdt B,service20_mpgm C where A.apl_id=B.apl_id and A.mp_id = C.mp_id and A.yr='"+l_yr+"' and A.mp_id = '"+ms_ida+"' and A.apl_id='"+ida+"'"
        queryset = mp_mtr.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램(관리자) - 질문2
class MP0101M_adm_quest_Serializer2(serializers.ModelSerializer):

    
    std_detl_code_nm = serializers.SerializerMethodField()
    rmrk = serializers.SerializerMethodField()

    class Meta:
        model = mp_ans
        fields = ('id','mp_id','test_div','apl_no','ques_no','apl_id','apl_nm','sort_seq','ans_t1','ans_t2','ans_t3','score','std_detl_code_nm','rmrk')

    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm

    def get_rmrk(self,obj):
        return obj.rmrk

# 멘토링 프로그램(관리자) - 질문
class MP0101M_adm_quest(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = MP0101M_adm_quest_Serializer2
    def list(self, request):
        #mp_sub 테이블에서 질문내역 조회
        key1 = request.GET.get('mp_id', None) 
        l_user_id = request.GET.get('user_id', None)           
        l_exist = mp_sub.objects.filter(mp_id=key1).exists()
        
        query = "select B.std_detl_code_nm,B.rmrk,A.* from service20_mp_ans A, service20_com_cdd B where A.ques_no = B.std_detl_code and B.std_grp_code in (select att_cdh from service20_mp_sub where mp_id = '"+str(key1)+"') and A.mp_id = '"+str(key1)+"' and apl_id = '"+str(l_user_id)+"'"
        queryset = mp_ans.objects.raw(query)

        print(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

#####################################################################################
# MP0101M - END 
#####################################################################################


@csrf_exempt
def post_user_info(request):
    ida = request.POST.get('user_id', None)
    ms_ida = request.POST.get('ms_id', None)
    
    created_flag = vm_nanum_stdt.objects.filter(apl_id=ida).exists()
    ms_apl_flag = ms_apl.objects.filter(apl_id=ida,ms_id=ms_ida).exists()
    if not ms_apl_flag:
        applyYn = 'N'
    else:
        applyYn = 'Y'

    if not created_flag:
        message = "Fail"
        context = {'message': message}
    else:
        
        message = "Ok"
        rows = vm_nanum_stdt.objects.filter(apl_id=ida)[0]
        rows2 = mp_sub.objects.filter(mp_id=ms_ida)
        rows3 = msch.objects.filter(ms_id=ms_ida)[0]


        for val in rows2:
            key1 = val.att_id

        context = {'message': message,
                    'applyYn' : applyYn,
                    'apl_nm' : rows.apl_nm,
                    'univ_cd' : rows.univ_cd,
                    'univ_nm' : rows.univ_nm,
                    'grad_div_cd' : rows.grad_div_cd,
                    'grad_div_nm' : rows.grad_div_nm,
                    'cllg_cd' : rows.cllg_cd,
                    'cllg_nm' : rows.cllg_nm,
                    'dept_cd' : rows.dept_cd,
                    'dept_nm' : rows.dept_nm,
                    'mjr_cd' : rows.mjr_cd,
                    'mjr_nm' : rows.mjr_nm,
                    'brth_dt' : rows.brth_dt,
                    'gen_cd' : rows.gen_cd,
                    'gen_nm' : rows.gen_nm,
                    'yr' : rows.yr,
                    'sch_yr' : rows.sch_yr,
                    'term_div' : rows.term_div,
                    'term_nm' : rows.term_nm,
                    'stdt_div' : rows.stdt_div,
                    'stdt_nm' : rows.stdt_nm,
                    'mob_nm' : rows.mob_nm,
                    'tel_no' : rows.tel_no,
                    'tel_no_g' : rows.tel_no_g,
                    'h_addr' : rows.h_addr,
                    'post_no' : rows.post_no,
                    'email_addr' : rows.email_addr,
                    'bank_acct' : rows.bank_acct,
                    'bank_cd' : rows.bank_cd,
                    'bank_nm' : rows.bank_nm,
                    'bank_dpsr' : rows.bank_dpsr,
                    'pr_yr' : rows.pr_yr,
                    'pr_sch_yr' : rows.pr_sch_yr,
                    'pr_term_div' : rows.pr_term_div,
                    'score01' : rows.score01,
                    'score02' : rows.score02,
                    'score03' : rows.score03,
                    'score04' : rows.score04,
                    'score04_tp' : rows.score04_tp,
                    'score05' : rows.score05,
                    'ms_id' : rows3.ms_id,
                    'ms_name' : rows3.ms_name,
                    }
    

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})



#멘토링 질문 List######################################################################
@csrf_exempt
def post_mt_quest(request):
    l_ms_id = request.GET.get('ms_id', None)
    r_mp_sub = mp_sub.objects.filter(mp_id=l_ms_id)
    r_mp_sub = r_mp_sub.filter(use_yn='Y')

    response_json = OrderedDict()

    res = []
    for val in r_mp_sub:
        key1 = val.att_id
        key2 = val.att_cdd
        r_com_cdd = com_cdd.objects.filter(std_grp_code=key1,std_detl_code=key2)

    
    context = {'message': 'Ok'}


    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})
####################################################################################




# 프로그램 수행계획서 리스트 ###################################################
class mpPlnh_mpgmListSerializer(serializers.ModelSerializer):

    testField = serializers.SerializerMethodField()
    class Meta:
        model = mpgm
        fields = ('mp_id','status','mp_name','mp_sname','base_div','mp_intro','mng_area','mgr_id','mgr_nm','mng_org','sup_org','yr','yr_seq','apl_ntc_fr_dt','apl_ntc_to_dt','apl_term','apl_fr_dt','apl_to_dt','mnt_term','mnt_fr_dt','mnt_to_dt','tot_apl','cnt_apl','cnt_doc_suc','cnt_doc_res','cnt_intv_pl','cnt_intv_ac','intv_dt','cnt_intv_suc','cnt_iintv_res','cnt_trn','cnt_mtr','doc_dt','doc_mgr','intv_in_dt','intv_in_mgr','fin_dt','fin_mgr','use_div','img_src','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','testField')

    def get_testField(self, obj):
        return 'test'     


class mpPlnh_mpgmListView(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = mpPlnh_mpgmListSerializer

    # mp_mtr - 프로그램 지원자(멘토) => mp_id(멘토링ID), apl_id
    # mp_mte - 프로그램 지원자(멘티) => mp_id(멘토링ID)


    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_status = request.GET.get('status', "")
        ida = request.GET.get('user_id', "")

        queryset = self.get_queryset()
        
        query = "select * from service20_mpgm";
        queryset = mpgm.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 프로그램 수행계획서 상 ###################################################
class mpPlnh_mpgmDetailViewSerializer(serializers.ModelSerializer):

    testField = serializers.SerializerMethodField()
    class Meta:
        model = mp_plnd
        fields = ('mp_id','apl_no','pln_no','pln_sdt','pln_edt','mtr_desc','testField')

    def get_testField(self, obj):
        return 'test'     


class mpPlnh_mpgmDetailView(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = mpPlnh_mpgmListSerializer

    # mp_mtr - 프로그램 지원자(멘토) => mp_id(멘토링ID), apl_id
    # mp_mte - 프로그램 지원자(멘티) => mp_id(멘토링ID)


    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_mntr_id = request.GET.get('mntr_id', "")
        ida = request.GET.get('user_id', "")

        queryset = self.get_queryset()
        

        query = " select b.*";
        query += " from service20_mp_plnh a";
        query += " , service20_mp_plnd b";
        query += " , (SELECT mp_id";
        query += " , apl_no";
        query += " FROM service20_mp_mtr";
        query += " WHERE mp_id = '"+l_mp_id+"'";
        query += " AND mntr_id = '"+l_mntr_id+"') c";
        query += " WHERE a.mp_id = b.mp_id";
        query += "    AND a.mp_id = c.mp_id";
        query += "    AND a.apl_no = b.apl_no";
        query += "    AND a.apl_no = c.apl_no";

        queryset = mp_plnd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

######################################################################

# 학습외신청(멘토) 리스트 ###################################################
class mpSpc_ListSerializer(serializers.ModelSerializer):

    testField = serializers.SerializerMethodField()
    class Meta:
        model = mp_spc
        fields = ('id','mp_id','spc_no','spc_div','status','spc_name','spc_intro','yr','yr_seq','apl_ntc_fr_dt','apl_ntc_to_dt','apl_term','apl_fr_dt','apl_to_dt','mnt_term','mnt_fr_dt','mnt_to_dt','cnf_dt','appr_tm','tot_apl','cnt_apl','cnt_pln','cnt_att','use_div','pic_div','rep_div','ord_div','grd_appr_div','tch_appr_div')

    def get_testField(self, obj):
        return 'test'     


class mpSpc_ListView(generics.ListAPIView):
    queryset = mp_spc.objects.all()
    serializer_class = mpPlnh_mpgmListSerializer

    # mp_spc

    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_status = request.GET.get('status', "")
        ida = request.GET.get('user_id', "")
        
        queryset = self.get_queryset()
        
        query = "select * from service20_mp_spc";
        queryset = mpgm.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

######################################################################