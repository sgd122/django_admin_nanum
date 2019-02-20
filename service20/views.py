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

from django.db import connection
from collections  import OrderedDict
import json
# api/moim 으로 get하면 이 listview로 연결


#####################################################################################
# 공통 - START
#####################################################################################

# 년도 콤보박스 ###################################################
class com_combo_yr_Serializer(serializers.ModelSerializer):

    code = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = com_cdd
        fields = ('code','name')

    def get_code(self, obj):
        return obj.code
    def get_name(self, obj):
        return obj.name

class com_combo_yr(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_yr_Serializer

    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_user_id = request.GET.get('user_id', "")
        

        queryset = self.get_queryset()
        
        query = " select '1'id,DATE_FORMAT(now(),'%Y')-1 as code,DATE_FORMAT(now(),'%Y')-1 as name ";
        query += " union ";
        query += " select '2'id,DATE_FORMAT(now(),'%Y') as code,DATE_FORMAT(now(),'%Y') as name ";
        query += " union ";
        query += " select '3'id,DATE_FORMAT(now(),'%Y')+1 as code,DATE_FORMAT(now(),'%Y')+1 as name ";

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class com_list_my_mentee_Serializer(serializers.ModelSerializer):

    mp_plc_nm = serializers.SerializerMethodField()
    grd_rel_nm = serializers.SerializerMethodField()
    class Meta:
        model = mp_mte
        fields = ('mp_id','mnte_no','mnte_id','mnte_nm','mnte_nm_e','apl_no','brth_dt','mp_hm','mp_plc','mp_addr','sch_grd','sch_cd','sch_nm','gen','yr','term_div','sch_yr','mob_no','tel_no','grd_id','grd_nm','grd_tel','grd_rel','prnt_nat_cd','prnt_nat_nm','tchr_id','tchr_nm','tchr_tel','area_city','area_gu','h_addr','h_post_no','s_addr','s_post_no','email_addr','apl_dt','status','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','mp_plc_nm','grd_rel_nm')
    
    def get_mp_plc_nm(self, obj):
        return obj.mp_plc_nm
    def get_grd_rel_nm(self, obj):
        return obj.grd_rel_nm
        
class com_list_my_mentee(generics.ListAPIView):
    queryset = mp_mte.objects.all()
    serializer_class = com_list_my_mentee_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_id = request.GET.get('apl_id', "")
        
        l_mp_id = "P182014"
        l_apl_id = "201610101"

        queryset = self.get_queryset()
        
        query = " select (select std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0052' and std_detl_code = S2.mp_plc) mp_plc_nm";
        query += " ,(select std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0047' and std_detl_code = S2.grd_rel) grd_rel_nm ";
        query += " , S2.* ";
        query += " FROM service20_mp_mtr S1 ";
        query += " LEFT JOIN service20_mp_mte S2  ON (S2.MP_ID  = S1.MP_ID ";
        query += " AND S2.APL_NO = S1.APL_NO) ";
        query += " LEFT JOIN service20_mp_plnh S3 ON (S3.MP_ID    = S1.MP_ID ";
        query += " AND S3.APL_NO   = S1.APL_NO) ";
        query += " WHERE 1=1 ";
        query += " AND S1.MP_ID      = '"+l_mp_id+"'     /* 멘토링 프로그램ID */ ";
        query += " AND S1.APL_ID    =  '"+l_apl_id+"' ";


        queryset = mp_mte.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)        

#####################################################################################
# 공통 - END
#####################################################################################


#####################################################################################
# MS0101M - START
#####################################################################################

class MS0101M_list_Serializer(serializers.ModelSerializer):



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
        

class MS0101M_list(generics.ListAPIView):



    queryset = msch.objects.all()
    serializer_class = MS0101M_list_Serializer

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


@csrf_exempt
def MS0101M_detail(request):
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



class MS0101M_quest_Serializer(serializers.ModelSerializer):

   
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

class MS0101M_quest(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = MS0101M_quest_Serializer
    def list(self, request):
        #ms_sub 테이블에서 질문내역 조회
        key1 = request.GET.get('ms_id', None)           
        l_exist = ms_sub.objects.filter(ms_id=key1).exists()
        
        query = "select B.std_detl_code,B.std_detl_code_nm,B.rmrk,A.* from service20_ms_sub A left outer join service20_com_cdd B on (A.att_id = B.std_grp_code and A.att_cdd = B.std_detl_code) where A.att_id = 'MS0014' and A.ms_id = '"+key1+"'"
        queryset = ms_sub.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)



# 멘토스쿨 신청
@csrf_exempt
def MS0101M_save(request):
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


class MS0101M_adm_list_Serializer(serializers.ModelSerializer):
    
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

class MS0101M_adm_list(generics.ListAPIView):
    queryset = ms_apl.objects.all()
    serializer_class = MS0101M_adm_list_Serializer
    
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


# 멘토스쿨(관리자) - 질문
class MS0101M_adm_quest_Serializer(serializers.ModelSerializer):

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
class MS0101M_adm_quest(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = MS0101M_adm_quest_Serializer
    def list(self, request):
        #ms_sub 테이블에서 질문내역 조회
        key1 = request.GET.get('ms_id', None) 
        l_user_id = request.GET.get('user_id', None)           
        
        query = "select B.std_detl_code_nm,B.rmrk,A.* from service20_ms_ans A, service20_com_cdd B where A.ques_no = B.std_detl_code and B.std_grp_code in (select att_cdh from service20_ms_sub where att_id = 'MS0014' and ms_id = '"+key1+"') and A.ms_id = '"+key1+"' and apl_id = '"+l_user_id+"'"
        queryset = ms_ans.objects.raw(query)


        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

#####################################################################################
# MS0101M - END
#####################################################################################




#####################################################################################
# MP0101M - START
#####################################################################################

class MP0101M_list_Serializer(serializers.ModelSerializer):

    applyFlag = serializers.SerializerMethodField()
    applyStatus = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    statusCode = serializers.SerializerMethodField()
    
    apl_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    apl_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mnt_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mnt_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = mpgm
        fields = ('mp_id','mp_name','status','statusCode','yr','yr_seq','sup_org','applyFlag','applyStatus','apl_fr_dt','apl_to_dt','mnt_fr_dt','mnt_to_dt','cnt_trn','status')

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

    def get_statusCode(self,obj):
        request = self.context['request']
        now = datetime.datetime.today()
        if obj.apl_fr_dt == None:
            # 개설중
            return '1'
        elif now < obj.apl_fr_dt:
            # 개설중
            return '1'
        elif obj.apl_fr_dt <= now < obj.apl_to_dt:
            # 모집중
            return '2'
        elif now > obj.apl_to_dt:
            # 모집완료
            return '3'  
        else:
            # 개설중
            return '1'
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
        query = "select ifnull((select 'Y' from service20_mp_mtr where yr = '"+str(l_yr)+"' and apl_id = '"+str(ida)+"' and mp_id = A.mp_id),'N') AS applyFlag,A.* from service20_mpgm A where A.yr='"+str(l_yr)+"' and A.apl_term='"+str(l_apl_term)+"' and (select count(1) from service20_mentor where apl_id = '"+ida+"') > 0 "

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
        
        query = "select B.std_detl_code,B.std_detl_code_nm,B.rmrk,A.* from service20_mp_sub A left outer join service20_com_cdd B on (A.att_id = B.std_grp_code and A.att_cdd = B.std_detl_code) where A.att_id='MS0014' and A.mp_id = '"+key1+"'"
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
        fields = ('mp_id','apl_no','mntr_id','indv_div','team_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','bank_acct','bank_cd','bank_nm','bank_dpsr','cnt_mp_a','cnt_mp_p','cnt_mp_c','cnt_mp_g','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','fnl_rslt','acpt_dt','acpt_div','acpt_cncl_rsn','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','mp_name','pr_yr','pr_sch_yr','pr_term_div')

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
        
        query = "select B.std_detl_code_nm,B.rmrk,A.* from service20_mp_ans A, service20_com_cdd B where A.ques_no = B.std_detl_code and B.std_grp_code in (select att_cdh from service20_mp_sub where att_id='MS0014' and mp_id = '"+str(key1)+"') and A.mp_id = '"+str(key1)+"' and apl_id = '"+str(l_user_id)+"'"
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




#####################################################################################
# MP0102M - START
#####################################################################################

# 학습외신청(멘토) 리스트 ###################################################
class MP0102M_list_Serializer(serializers.ModelSerializer):

    testField = serializers.SerializerMethodField()
    class Meta:
        model = mp_spc
        fields = ('id','mp_id','spc_no','spc_div','status','spc_name','spc_intro','yr','yr_seq','apl_ntc_fr_dt','apl_ntc_to_dt','apl_term','apl_fr_dt','apl_to_dt','mnt_term','mnt_fr_dt','mnt_to_dt','cnf_dt','appr_tm','tot_apl','cnt_apl','cnt_pln','cnt_att','use_div','pic_div','rep_div','ord_div','grd_appr_div','tch_appr_div')

    def get_testField(self, obj):
        return 'test'     


class MP0102M_list(generics.ListAPIView):
    queryset = mp_spc.objects.all()
    serializer_class = MP0102M_list_Serializer

    # mp_spc

    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_status = request.GET.get('status', "")
        ida = request.GET.get('user_id', "")
        
        queryset = self.get_queryset()
        
        query = "select * from service20_mp_spc where yr='"+l_yr+"' and apl_term='"+l_apl_term+"'";
        queryset = mp_spc.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

######################################################################

#####################################################################################
# MP0102M - END
#####################################################################################



#####################################################################################
# MP0103M - START
#####################################################################################

# 프로그램 수행계획서 리스트 ###################################################
class MP0103M_list_Serializer(serializers.ModelSerializer):

    mnte_nm = serializers.SerializerMethodField()
    sch_nm = serializers.SerializerMethodField()
    sch_yr = serializers.SerializerMethodField()
    pln_dt = serializers.SerializerMethodField()
    appr_nm = serializers.SerializerMethodField()
    appr_dt = serializers.SerializerMethodField()
    mgr_id = serializers.SerializerMethodField()
    mgr_dt = serializers.SerializerMethodField()
    apl_id = serializers.SerializerMethodField()
    apl_nm = serializers.SerializerMethodField()
    tchr_nm = serializers.SerializerMethodField()
    pln_dt = serializers.SerializerMethodField()
    mtr_sub = serializers.SerializerMethodField()
    pln_sedt = serializers.SerializerMethodField()
    
    mgr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    pln_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    appr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    pln_sedt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = mpgm
        fields = ('mp_id','mp_name','apl_term','yr_seq','mnte_nm','sch_nm','sch_yr','pln_dt','appr_nm','appr_dt','mgr_id','mgr_dt','apl_id','apl_nm','tchr_nm','pln_dt','mtr_sub','pln_sedt')
    
    def get_mnte_nm(self,obj):
        return obj.mnte_nm  
    def get_sch_nm(self,obj):
        return obj.sch_nm
    def get_sch_yr(self,obj):
        return obj.sch_yr
    def get_pln_dt(self,obj):
        return obj.pln_dt
    def get_appr_nm(self,obj):
        return obj.appr_nm
    def get_appr_dt(self,obj):
        return obj.appr_dt
    def get_mgr_id(self,obj):
        return obj.mgr_id
    def get_mgr_dt(self,obj):
        return obj.mgr_dt
    def get_apl_id(self,obj):
        return obj.apl_id
    def get_apl_nm(self,obj):
        return obj.apl_nm
    def get_tchr_nm(self,obj):
        return obj.tchr_nm
    def get_pln_dt(self,obj):
        return obj.pln_dt
    def get_mtr_sub(self,obj):
        return obj.mtr_sub
    def get_pln_sedt(self,obj):
        return obj.pln_sedt
    


class MP0103M_list(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0103M_list_Serializer

    # mp_mtr - 프로그램 지원자(멘토) => mp_id(멘토링ID), apl_id
    # mp_mte - 프로그램 지원자(멘티) => mp_id(멘토링ID)


    def list(self, request):
        l_user_id = request.GET.get('user_id', "")

        queryset = self.get_queryset()

        query = " select b.mp_id      AS mp_id ";
        query += " , b.mp_name    AS mp_name ";
        query += " , b.apl_term   AS apl_term ";
        query += " , b.yr_seq     AS yr_seq ";
        query += " , c.mnte_nm    AS mnte_nm ";
        query += " , c.sch_nm     AS sch_nm ";
        query += " , c.sch_yr     AS sch_yr ";
        query += " , a.pln_dt     AS pln_dt ";
        query += " , a.appr_nm    AS appr_nm ";
        query += " , a.appr_dt    AS appr_dt ";
        query += " , a.mgr_id     AS mgr_id ";
        query += " , a.mgr_dt     AS mgr_dt ";
        query += " , d.apl_id     AS apl_id ";
        query += " , d.apl_nm     AS apl_nm ";
        query += " , c.tchr_nm    AS tchr_nm ";
        query += " , a.mtr_sub     AS mtr_sub ";
        query += " , (SELECT concat(pln_sdt, CONCAT('~', pln_edt)) FROM service20_mp_plnd WHERE mp_id = a.mp_id AND apl_no = a.apl_no LIMIT 1) AS pln_sedt ";
        query += " from service20_mp_plnh a ";
        query += " , service20_mpgm b ";
        query += " , service20_mp_mte c ";
        query += " , (SELECT mp_id ";
        query += " , apl_no ";
        query += " , apl_id ";
        query += " , apl_nm ";
        query += " FROM service20_mp_mtr ";
        query += " WHERE mntr_id = '"+l_user_id+"' or apl_id = '"+l_user_id+"') d ";
        query += " WHERE a.mp_id = b.mp_id ";
        query += " AND a.mp_id = c.mp_id ";
        query += " AND a.mp_id = d.mp_id ";
        query += " AND a.apl_no = d.apl_no ";
        query += " AND d.apl_no = c.apl_no ";

        print(query)

        queryset = mpgm.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 프로그램 수행계획서 상세 ###################################################
class MP0103M_Detail_Serializer(serializers.ModelSerializer):

    testField = serializers.SerializerMethodField()
    class Meta:
        model = mp_plnd
        fields = ('mp_id','apl_no','pln_no','pln_sdt','pln_edt','mtr_desc','testField')

    def get_testField(self, obj):
        return 'test'     


class MP0103M_Detail(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0103M_Detail_Serializer

    # mp_mtr - 프로그램 지원자(멘토) => mp_id(멘토링ID), apl_id
    # mp_mte - 프로그램 지원자(멘티) => mp_id(멘토링ID)


    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_user_id = request.GET.get('user_id', "")
        

        queryset = self.get_queryset()
        

        query = " select b.*";
        query += " from service20_mp_plnh a";
        query += " , service20_mp_plnd b";
        query += " , (SELECT mp_id";
        query += " , apl_no";
        query += " FROM service20_mp_mtr";
        query += " WHERE mp_id = '"+l_mp_id+"'";
        query += " AND ( apl_id = '"+l_user_id+"') ) c";
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

# 계획서 최초 작성 시 주차 수를 셋팅
class MP0103M_list_v1_Serializer(serializers.ModelSerializer):

    
    class Meta:
        model = mp_sub
        fields = ('id','mp_id','att_id','att_seq','att_cdh','att_cdd','att_val','use_yn','sort_seq')
    

class MP0103M_list_v1(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0103M_list_v1_Serializer

    # mp_mtr - 프로그램 지원자(멘토) => mp_id(멘토링ID), apl_id
    # mp_mte - 프로그램 지원자(멘티) => mp_id(멘토링ID)


    def list(self, request):
        l_user_id = request.GET.get('user_id', "")
        l_apl_id = request.GET.get('apl_id', "")
        l_mp_id = request.GET.get('mp_id', "")

        queryset = self.get_queryset()

        query = " select t2.id,t2.att_val AS att_val ";
        query += " FROM service20_mp_mtr t1 ";
        query += " LEFT JOIN service20_mp_sub t2 ON (t2.mp_id = t1.mp_id ";
        query += " AND t2.att_id= 'MP0013' ";
        query += " AND t2.att_cdh = 'MP0013' ";
        query += " AND t2.att_cdd = '20') ";
        query += " WHERE t1.mp_id = '"+l_mp_id+"' ";
        query += " AND t1.apl_id='"+l_apl_id+"' ";

        print(query)

        queryset = mp_sub.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 프로그램 수행계획서 Insert
@csrf_exempt
def MP0103M_Insert(request):
    mp_id = request.POST.get('mp_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")
    pln_no = request.POST.get('pln_no', 0)
    pln_sdt = request.POST.get('pln_sdt', "")
    pln_edt = request.POST.get('pln_edt', "")
    mtr_desc = request.POST.get('mtr_desc', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    maxRow = request.POST.get('maxRow', 0)


    row_max = int(maxRow)
    for i in range(0,row_max):
    
        mp_plnd_max = mp_plnd.objects.all().aggregate(vlMax=Max('apl_no'))
        
        apl_no = 0;
        
        max_no = mp_plnd_max['vlMax']    

        if max_no == None:
            apl_no = 0;
        else:
            apl_no = mp_plnd_max['vlMax']
            apl_no = apl_no + 1;

        mtr_desc = request.POST.get('mtr_desc'+str(i), "")
        pln_no = request.POST.get('pln_no'+str(i+1), "")

        insert_text = " insert into service20_mp_plnd ( ";
        insert_text += " mp_id ";
        insert_text += " , apl_no ";
        insert_text += " , pln_no ";
        insert_text += " , pln_sdt ";
        insert_text += " , pln_edt ";
        insert_text += " , mtr_desc ";
        insert_text += " , ins_id ";
        insert_text += " , ins_ip ";
        insert_text += " , ins_dt ";
        insert_text += " , ins_pgm ";
        insert_text += " , upd_id ";
        insert_text += " , upd_ip ";
        insert_text += " , upd_dt ";
        insert_text += " , upd_pgm ";
        insert_text += " ) ";
        insert_text += "  ( select ";
        insert_text += " '"+str(mp_id)+"' ";
        insert_text += " , (SELECT COALESCE(MAX(apl_no)+1, 1) AS apl_no FROM service20_mp_plnd WHERE mp_id = '"+str(mp_id)+"') ";
        insert_text += " , '"+str(pln_no)+"' ";
        insert_text += " , adddate(t2.mnt_fr_dt, 7*('"+str(pln_no)+"'*1-1) + 0) pln_sdt ";
        insert_text += " , adddate(t2.mnt_fr_dt, 7*('"+str(pln_no)+"'*1-1) + 6) pln_edt ";
        insert_text += " , '"+str(mtr_desc)+"' ";
        insert_text += " , '"+str(ins_id)+"' ";
        insert_text += " , '"+str(ins_ip)+"' ";
        insert_text += " , now() ";
        insert_text += " , '"+str(ins_pgm)+"' ";
        insert_text += " , '"+str(upd_id)+"' ";
        insert_text += " , '"+str(upd_ip)+"' ";
        insert_text += " , now() ";
        insert_text += " , '"+str(upd_pgm)+"' ";
        insert_text += " from service20_mp_mtr t1 ";
        insert_text += " left join service20_mpgm t2 on (t2.mp_id = t1.mp_id) ";
        insert_text += " where mntr_id = '"+str(mp_id)+"' ";
        insert_text += " and apl_id = '"+str(apl_id)+"' ";
        insert_text += " )";

        print(insert_text)
        cursor = connection.cursor()
        query_result = cursor.execute(insert_text)    
        print(query_result)
        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


# 프로그램 수행계획서 Update
@csrf_exempt
def MP0103M_Update(request):
    mp_id = request.POST.get('mp_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")
    pln_no = request.POST.get('pln_no', 0)
    mtr_pln_sdt = request.POST.get('mtr_pln_sdt', "")
    mtr_pln_edt = request.POST.get('mtr_pln_edt', "")
    mtr_desc = request.POST.get('mtr_desc', "")
    mtr_sub = request.POST.get('mtr_sub', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")
    

    maxRow = request.POST.get('maxRow', 0)
    print("::maxRow::")
    print(maxRow)

    row_max = int(maxRow)


    ####################################
    # 1번쿼리
    ####################################
    update_text = " update service20_mp_plnh ";
    update_text += " SET mtr_sub = '"+str(mtr_sub)+"' ";
    # update_text += " , pln_sdt = ifnull(trim(NULLIF('"+str(mtr_pln_sdt)+"','')),DATE_FORMAT(now(),'%Y-%m-%d')) ";
    # update_text += " , pln_edt = ifnull(trim(NULLIF('"+str(mtr_pln_edt)+"','')),DATE_FORMAT(now(),'%Y-%m-%d')) ";
    update_text += " , upd_id = '"+str(upd_id)+"' ";
    update_text += " , upd_ip = '"+str(upd_ip)+"' ";
    update_text += " , upd_dt = now() ";
    update_text += " , upd_pgm = '"+str(upd_pgm)+"' ";
    update_text += " WHERE mp_id = '"+str(mp_id)+"' ";
    # update_text += " AND apl_no = '"+str(apl_no)+"' ";
    update_text += " AND apl_no IN (SELECT apl_no FROM service20_mp_mtr WHERE apl_id = '"+str(apl_id)+"') ";

    print(update_text)
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)    
    print(query_result)
    ####################################
    # 1번쿼리
    ####################################


    for i in range(0,row_max):

        mtr_desc = request.POST.get('mtr_desc'+str(i), "")
        pln_no = request.POST.get('pln_no'+str(i+1), "")

        ####################################
        # 2번쿼리
        ####################################
        update_text = " update service20_mp_plnd ";
        update_text += " SET mtr_desc = '"+str(mtr_desc)+"' ";
        # update_text += " , pln_sdt = ifnull(trim(NULLIF('"+str(mtr_pln_sdt)+"','')),DATE_FORMAT(now(),'%Y-%m-%d')) ";
        # update_text += " , pln_edt = ifnull(trim(NULLIF('"+str(mtr_pln_edt)+"','')),DATE_FORMAT(now(),'%Y-%m-%d')) ";
        update_text += " , upd_id = '"+str(upd_id)+"' ";
        update_text += " , upd_ip = '"+str(upd_ip)+"' ";
        update_text += " , upd_dt = now() ";
        update_text += " , upd_pgm = '"+str(upd_pgm)+"' ";
        update_text += " WHERE mp_id = '"+str(mp_id)+"' ";
        # update_text += " AND apl_no = '"+str(apl_no)+"' ";
        update_text += " AND apl_no IN (SELECT apl_no FROM service20_mp_mtr WHERE apl_id = '"+str(apl_id)+"') ";
        update_text += " AND pln_no = '"+str(pln_no)+"' ";

        print(update_text)
        cursor = connection.cursor()
        query_result = cursor.execute(update_text)    
        print(query_result)
        ####################################
        # 2번쿼리
        ####################################

    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})
######################################################################

#####################################################################################
# MP0103M - END 
#####################################################################################



#####################################################################################
# MP0105M - START
#####################################################################################

# 보고서 현황 리스트 ###################################################
class MP0105M_combo_1_Serializer(serializers.ModelSerializer):

    # testField = serializers.SerializerMethodField()
    mp_name = serializers.SerializerMethodField()
    

    class Meta:
        model = mp_mtr
        fields = ('mp_id','apl_no','mntr_id','indv_div','team_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','bank_acct','bank_cd','bank_nm','bank_dpsr','cnt_mp_a','cnt_mp_p','cnt_mp_c','cnt_mp_g','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','mp_name','pr_yr','pr_sch_yr','pr_term_div','mp_name')

    def get_mp_name(self,obj):
        return obj.mp_name

class MP0105M_combo_1(generics.ListAPIView):
    queryset = mp_rep.objects.all()
    serializer_class = MP0105M_combo_1_Serializer


    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_id = request.GET.get('apl_id', "")


        queryset = self.get_queryset()

        query = " select A.id ";
        query += " , A.mp_id ";
        query += " , A.apl_no ";
        query += " , B.mp_name ";
        query += " FROM service20_mp_mtr A ";
        query += " , service20_mpgm B ";
        query += " WHERE apl_id = '"+l_apl_id+"' ";
        query += " AND mntr_id IS NOT null ";
        query += " AND A.mp_id = B.mp_id ";

        queryset = mp_mtr.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 보고서 현황 콤보1 ###################################################
class MP0105M_list_Serializer(serializers.ModelSerializer):

    # testField = serializers.SerializerMethodField()
    unv_nm = serializers.SerializerMethodField()
    cllg_nm = serializers.SerializerMethodField()
    dept_nm = serializers.SerializerMethodField()
    apl_id = serializers.SerializerMethodField()
    apl_nm = serializers.SerializerMethodField()
    rep_div_nm = serializers.SerializerMethodField()
    status_nm = serializers.SerializerMethodField()
    req_dt_sub = serializers.SerializerMethodField()
    appr_dt_sub = serializers.SerializerMethodField()
    mgr_dt_sub = serializers.SerializerMethodField()

    req_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    appr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mgr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = mp_rep
        fields = ('mp_id','apl_no','rep_no','rep_div','rep_ttl','mtr_obj','rep_dt','req_dt','mtr_desc','coatching','spcl_note','mtr_revw','appr_id','appr_nm','appr_dt','mgr_id','mgr_dt','status','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','unv_nm','cllg_nm','dept_nm','apl_id','apl_nm','rep_div_nm','status_nm','req_dt_sub','appr_dt_sub','mgr_dt_sub')
    
    def get_unv_nm(self,obj):
        return obj.unv_nm  
    def get_cllg_nm(self,obj):
        return obj.cllg_nm
    def get_dept_nm(self,obj):
        return obj.dept_nm
    def get_apl_id(self,obj):
        return obj.apl_id
    def get_appr_id(self,obj):
        return obj.appr_id
    def get_apl_nm(self,obj):
        return obj.apl_nm
    def get_rep_div_nm(self,obj):
        return obj.rep_div_nm
    def get_status_nm(self,obj):
        return obj.status_nm
    def get_req_dt_sub(self,obj):
        return obj.req_dt_sub
    def get_appr_dt_sub(self,obj):
        return obj.appr_dt_sub
    def get_mgr_dt_sub(self,obj):
        return obj.mgr_dt_sub


class MP0105M_list(generics.ListAPIView):
    queryset = mp_rep.objects.all()
    serializer_class = MP0105M_list_Serializer


    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_id = request.GET.get('apl_id', "")




        queryset = self.get_queryset()

        query = " select t1.id ";
        query += " , t1.mp_id     /* 멘토링 프로그램id */ ";
        query += " , t2.unv_nm          /* 지원자 대학교 명 */ ";
        query += " , t2.cllg_nm         /* 지원자 대학 명 */ ";
        query += " , t2.dept_nm         /* 지원자 학부/학과 명 */ ";
        query += " , t2.apl_id          /* 지원자(멘토,학생) 학번 */ ";
        query += " , t2.apl_nm          /* 지원자(멘토,학생) 명 */ ";
        query += " , t1.rep_div         /* 보고서 구분(mp0062) */ ";
        query += " , c2.std_detl_code_nm   as rep_div_nm ";
        query += " , t1.status          /* 상태(mp0070) */ ";
        query += " , c1.std_detl_code_nm   as status_nm ";
        query += " , substring(t1.req_dt,  1, 10) req_dt_sub    /* 승인요청일 */ ";
        query += " , substring(t1.appr_dt, 1, 10) appr_dt_sub   /* 보호자 승인일시 */ ";
        query += " , substring(t1.mgr_dt,  1, 10) mgr_dt_sub   /* 관리자 승인일시 */ ";
        query += " , t1.rep_ttl   /* 보고서 제목 : 내용 */ ";
        query += " , t1.apl_no    /* 멘토 지원 no */ ";
        query += " , t1.rep_no    /* 보고서 no */ ";
        query += " , t1.rep_div   /* 보고서 구분(mp0062) */ ";
        query += " , t1.rep_ttl   /* 보고서 제목 */ ";
        query += " , t1.mtr_obj   /* 학습목표 */ ";
        query += " , t1.rep_dt    /* 보고서작성일 */ ";
        query += " , t1.req_dt    /* 승인요청일 */ ";
        query += " , t1.mtr_desc  /* 학습내용 */ ";
        query += " , t1.coatching /* 학습외 지도(상담) */ ";
        query += " , t1.spcl_note /* 특이사항 */ ";
        query += " , t1.mtr_revw  /* 소감문 */ ";
        query += " , t1.appr_id   /* 승인자id */ ";
        query += " , t1.appr_nm   /* 승인자명 */ ";
        query += " , t1.appr_dt   /* 보호자 승인일시 */ ";
        query += " , t1.mgr_id    /* 관리자id */ ";
        query += " , t1.mgr_dt    /* 관리자 승인일시 */ ";
        query += " from service20_mp_rep t1     /* 프로그램 보고서 */ ";
        query += " left join service20_mp_mtr t2 on (t2.mp_id   = t1.mp_id ";
        query += " and t2.apl_no = t1.apl_no)       /* 지원 멘토 */ ";
        query += " left join service20_com_cdd c1 on (c1.std_grp_code  = 'MP0070'  /* 상태(mp0070) */ ";
        query += " and c1.std_detl_code = t1.status) ";
        query += " left join service20_com_cdd c2 on (c2.std_grp_code  = 'MP0062'  /* 보고서 구분(mp0062) */ ";
        query += " and c2.std_detl_code = t1.rep_div) ";
        query += " where 1=1 ";
        query += " and t1.mp_id     = '"+l_mp_id+"'     /* 멘토링 프로그램id */ ";
        # query += " and t1.rep_div   = 'M' ";
        # query += " and t1.status    =  '20' /* 제출, 40 완료 */ ";
        query += " and t2.apl_id    =  '"+l_apl_id+"' ";


        queryset = mp_rep.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)      

class MP0105M_detail_Serializer(serializers.ModelSerializer):

    # testField = serializers.SerializerMethodField()
    rep_div_nm  = serializers.SerializerMethodField()  
    apl_m  = serializers.SerializerMethodField()
    teacher  = serializers.SerializerMethodField()     
    mte_nm  = serializers.SerializerMethodField()     
    sch_yr  = serializers.SerializerMethodField()     
    obj_sub  = serializers.SerializerMethodField()     
    aaa  = serializers.SerializerMethodField()        
    status_nm  = serializers.SerializerMethodField() 
    unv_nm  = serializers.SerializerMethodField()
    cllg_nm = serializers.SerializerMethodField()
    dept_nm = serializers.SerializerMethodField()
    mgr_nm = serializers.SerializerMethodField()

    req_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    appr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mgr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = mp_rep
        fields = ('mp_id','apl_no','rep_no','rep_div','rep_ttl','mtr_obj','rep_dt','req_dt','mtr_desc','coatching','spcl_note','mtr_revw','appr_id','appr_nm','appr_dt','mgr_id','mgr_dt','status','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','rep_div_nm','apl_m','teacher','mte_nm','sch_yr','obj_sub','aaa','status_nm','unv_nm','cllg_nm','dept_nm','mgr_nm')
    
    def get_rep_div_nm(self,obj):
        return obj.rep_div_nm   
    def get_apl_m(self,obj):
        return obj.apl_m
    def get_teacher(self,obj):      
        return obj.teacher
    def get_mte_nm(self,obj):      
        return obj.mte_nm
    def get_sch_yr(self,obj):      
        return obj.sch_yr
    def get_obj_sub(self,obj):      
        return obj.obj_sub
    def get_aaa(self,obj):         
        return obj.aaa
    def get_status_nm(self,obj):   
        return obj.status_nm
    def get_unv_nm(self,obj):
        return obj.unv_nm
    def get_cllg_nm(self,obj):
        return obj.cllg_nm
    def get_dept_nm(self,obj):
        return obj.dept_nm
    def get_mgr_nm(self,obj):
        return obj.mgr_nm

class MP0105M_detail(generics.ListAPIView):
    queryset = mp_rep.objects.all()
    serializer_class = MP0105M_detail_Serializer


    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_id = request.GET.get('apl_id', "")
        l_apl_no = request.GET.get('apl_no', "")
        l_rep_no = request.GET.get('rep_no', "")

        queryset = self.get_queryset()

        # /*보고서 상세*/
        query = " select t1.id,t1.mp_id                                         /* 멘토링 프로그램id   */ "
        query += " , t1.rep_div                                       /* 보고서 구분(mp0062) */ "
        query += " , t1.rep_ttl                                       /* 보고서 제목 : 내용  */ "
        query += " , c2.std_detl_code_nm               as rep_div_nm    "
        query += " , concat(t2.apl_id, '/', t2.apl_nm) as apl_m       /* 지원자(멘토,학생) 명*/ "
        query += " , '교사'                            as teacher       "
        query += " , '멘티'                            as mte_nm       "
        query += " , '교/학년'                         as sch_yr       "
        query += " , '지도과목'                        as obj_sub       "
        query += " , '출석현황'                        as aaa          "
        query += " , substring(t1.rep_dt,  1, 10)      as rep_dt      /* 보고서작성일         */ "
        query += " , substring(t1.req_dt,  1, 10)      as req_dt      /* 승인요청일         */ "
        query += " , t1.appr_nm                                       /* 승인자명            */ "
        query += " , substring(t1.appr_dt,  1, 10)     as appr_dt     /* 보호자 승인일시      */ "
        query += " , t1.mgr_id                         as mgr_nm      /* 관리자id            */ "
        query += " , substring(t1.mgr_dt,  1, 10)      as mgr_dt      /* 관리자 승인일시      */ "
        query += " , t1.status                                        /* 상태(mp0070)         */ "
        query += " , c1.std_detl_code_nm               as status_nm    "
        query += " , t1.mtr_obj                                       /* 학습목표            */ "
        query += " , t1.mtr_desc                                      /* 학습내용            */ "
        query += " , t1.coatching                                     /* 학습외 지도(상담)   */ "
        query += " , t1.spcl_note                                     /* 특이사항            */ "
        query += " , t1.mtr_revw                                      /* 소감문            */ "
        query += " , t2.unv_nm                                        /* 지원자 대학교 명      */ "
        query += " , t2.cllg_nm                                       /* 지원자 대학 명      */ "
        query += " , t2.dept_nm                                       /* 지원자 학부/학과 명 */       "                                    
        query += " , t1.apl_no                                        /* 멘토 지원 no         */ "
        query += " , t1.rep_no                                        /* 보고서 no         */ "
        query += " , t1.rep_div                                       /* 보고서 구분(mp0062) */ "
        query += " , t1.rep_ttl                                       /* 보고서 제목         */ "
        query += " , t1.appr_id                                       /* 승인자id            */ "
        query += " from service20_mp_rep t1                              /* 프로그램 보고서      */ "
        query += " left join service20_mp_mtr t2  on (t2.mp_id   = t1.mp_id and t2.apl_no = t1.apl_no) "
        query += " left join service20_com_cdd c1 on (c1.std_grp_code  = 'MP0070'  and c1.std_detl_code = t1.status)  "
        query += " left join service20_com_cdd c2 on (c2.std_grp_code  = 'MP0062'  and c2.std_detl_code = t1.rep_div)  "
        query += " where 1=1 "
        query += " and t1.mp_id     = '"+l_mp_id+"'     "
        query += " and t2.apl_id    =  '"+l_apl_id+"' "
        query += " and t1.apl_no    = '"+l_apl_no+"' "
        query += " and t1.rep_no    = '"+l_rep_no+"' "

        queryset = mp_rep.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)                

#####################################################################################
# MP0105M - END
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



def stdApplyStdView(request):
    ms_aplAll = ms_apl.objects.all()
    context = None
    return render(request, 'stdApply/submit.html', context)


def Service20_01_View(request):
    ms_aplAll = ms_apl.objects.all()
    context = None
    return render(request, 'service20/Service20_01.html', context)    


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