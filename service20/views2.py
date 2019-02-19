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
import csv


# api/moim 으로 get하면 이 listview로 연결




#멘토스쿨 콤보박스
class msComboListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = msch
        fields = ('ms_id','ms_name')

class msComboListView(generics.ListAPIView):
    queryset = msch.objects.all()
    serializer_class = msComboListViewSerializer


    def list(self, request):   
        queryset = self.get_queryset()

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

#멘토스쿨 콤보박스Detail
class msComboListViewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = msch
        fields = ('ms_id','status','ms_name','ms_sname','ms_intro','mng_area','mgr_id','mgr_nm','mng_org','sup_org','yr','yr_seq','apl_ntc_fr_dt','apl_ntc_to_dt','apl_term','apl_fr_dt','apl_to_dt','trn_term','trn_fr_dt','trn_to_dt','tot_apl','cnt_apl','cnt_doc_suc','cnt_doc_res','cnt_intv_pl','cnt_intv_ac','intv_dt','cnt_intv_suc','cnt_iintv_res','cnt_trn','cnt_mtr','doc_dt','doc_mgr','intv_in_dt','intv_in_mgr','fin_dt','fin_mgr')

class msComboListViewDetail(generics.ListAPIView):
    queryset = msch.objects.all()
    serializer_class = msComboListViewDetailSerializer

    def list(self, request):
        l_ms_id = request.GET.get('ms_id', None)
        queryset = self.get_queryset()
        queryset = queryset.filter(ms_id=l_ms_id)        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)    



@csrf_exempt
def msFn1(request):
    ms_id = request.GET.get('ms_id', None)  

    
    queryset2 = cm_cnv_scr.objects.all()
    query = "select * from service20_ms_apl where ms_id = '" +str(ms_id)+"'"
    queryset = msch.objects.raw(query)

    
    vl_cscore1=''
    vl_cscore2=''
    vl_cscore3=''
    vl_cscore4=''
    #

    
    for val in queryset:

        if val.score1==None:
            vl_cscore1 = 0
        elif val.score2==None:
            vl_cscore1 = 0
        else:
            vl_cscore1 = (val.score1 / val.score2) * 100

        query2 = "select id, eval_item, fin_scr from service20_cm_cnv_scr  where eval_item = '1'  and (min_scr <= '" +str(vl_cscore1)+"' and  '" +str(vl_cscore1)+"' < max_scr)"
        queryset2 = cm_cnv_scr.objects.raw(query2)

        
        for var2 in queryset2:
            #print(var2.fin_scr)
            vl_cscore1 = var2.fin_scr
            #queryset1 = ms_apl.objects.all()  
            ms_apl.objects.filter(id=val.id,ms_id=val.ms_id).update(cscore1=vl_cscore1)

    for val in queryset:
        vl_cscore2 = val.score3


        query2 = "select id, eval_item, fin_scr from service20_cm_cnv_scr  where eval_item = '2'  and (min_scr <= '" +str(vl_cscore2)+"' and  '" +str(vl_cscore2)+"' < max_scr)"
        queryset2 = cm_cnv_scr.objects.raw(query2)

        for var2 in queryset2:
            #print(var2.fin_scr)
            vl_cscore2 = var2.fin_scr
            #ms_apl.objects.filter(id=val.id,ms_id=val.ms_id).update(cscore2=vl_cscore2)

    for val in queryset:
        vl_cscore2 = val.score3
        query3 = "select id, eval_item, fin_scr from service20_cm_cnv_scr  where eval_item = '3'  and (min_scr <= '" +str(vl_cscore3)+"' and  '" +str(vl_cscore3)+"' < max_scr)"
        queryset2 = cm_cnv_scr.objects.raw(query3)

        for var2 in queryset2:
            #print(var2.fin_scr)
            vl_cscore3 = var2.fin_scr

    #봉사

    for val in queryset:
        vl_cscore4 = val.score4
        query3 = "select id, eval_item, fin_scr from service20_cm_cnv_scr  where eval_item = '2'  and (min_scr <= '" +str(vl_cscore4)+"' and  '" +str(vl_cscore4)+"' < max_scr)"
        queryset2 = cm_cnv_scr.objects.raw(query3)

        for var2 in queryset2:
            #print(var2.fin_scr)
            vl_cscore3 = var2.fin_scr
            ms_apl.objects.filter(id=val.id,ms_id=val.ms_id).update(cscore3=vl_cscore3)


    message = "Ok" 
    context = {'message': message,}
    

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


@csrf_exempt
def msFn2(request):
    ms_id = request.GET.get('ms_id', None)  
    
    queryset2 = cm_cnv_scr.objects.all()
    query = "select * from service20_ms_apl where ms_id = '" +str(ms_id)+"' order by (cscore1+cscore2+cscore3+cscore4+cscore5+cscore5) desc"
    rank = 1
    queryset = msch.objects.raw(query)


    #
    for val in queryset:
        ms_apl.objects.filter(id=val.id,ms_id=val.ms_id).update(doc_rank=rank)
        rank = rank + 1


    message = "Ok" 
    context = {'message': message,}
    

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})



@csrf_exempt
def msFn3(request):
    ms_id = request.GET.get('ms_id', None)  
    query = "select * from service20_ms_apl where ms_id = '" +str(ms_id)+"'"
    queryset = ms_apl.objects.raw(query)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

 
    writer = csv.writer(response)
    writer.writerow(['apl_no', 'unv_nm', 'dept_nm', 'apl_id', 'apl_nm', 'gen', 'cscore1', 'cscore2', 'cscore3', 'cscore4', 'cscore5', 'doc_rslt', 'doc_rank', 'intv_team', 'intv_dt', 'intv_part_pl','intv_part_ac'])

    if ms_id == None:
        users = ms_apl.objects.all().values_list('apl_no', 'unv_nm', 'dept_nm', 'apl_id', 'apl_nm', 'gen', 'cscore1', 'cscore2', 'cscore3', 'cscore4', 'cscore5', 'doc_rslt', 'doc_rank', 'intv_team', 'intv_dt', 'intv_part_pl','intv_part_ac')
    else:
        users = ms_apl.objects.filter(ms_id=ms_id).values_list('apl_no', 'unv_nm', 'dept_nm', 'apl_id', 'apl_nm', 'gen', 'cscore1', 'cscore2', 'cscore3', 'cscore4', 'cscore5', 'doc_rslt', 'doc_rank', 'intv_team', 'intv_dt', 'intv_part_pl','intv_part_ac')

    for user in users:
        writer.writerow(user)
    return response


#멘토링 콤보박스
class mpComboListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = mpgm
        fields = ('mp_id','mp_name')

class mpComboListView(generics.ListAPIView):
   
    queryset = mpgm.objects.all()
    queryset = queryset.filter(use_div='Y')
    serializer_class = mpComboListViewSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)



#멘토스쿨 콤보박스Detail
class mpComboListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = mpgm
        fields = ('mp_id','mp_name','apl_term','yr_seq','mng_org','sup_org','tot_apl','apl_fr_dt','apl_to_dt','mnt_fr_dt','mnt_to_dt')


class mpComboListViewDetail(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = mpComboListDetailSerializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', None)
        queryset = self.get_queryset()
        queryset = queryset.filter(mp_id=l_mp_id)        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)    


@csrf_exempt
def msPop1(request):
    posts = None
    return render(request, 'popup/mento/msPop1.html', { 'posts': posts })      



class msPop1_Det1Serializer(serializers.ModelSerializer):
    class Meta:
        model = ms_apl
        fields = ('ms_id','apl_no','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm')        
        #fields = ('mp_id','apl_no','mntr_id','indv_div','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr')

class msPop1_Det1(generics.ListAPIView):

    queryset = ms_apl.objects.all()
    serializer_class = msPop1_Det1Serializer

    def list(self, request):

        print("aaa222")
        ms_id = request.GET.get('ms_id', None)
        apl_id = request.GET.get('apl_id', None)

        query = "select * from service20_ms_apl where ms_id='"+ms_id+"' and apl_id = '"+apl_id+"'"

        print(query)
        queryset = mp_mtr.objects.raw(query)        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)    


#멘토스쿨 핍압1_조회3_채점자 교수 조회
class msPop1_Det3Serializer(serializers.ModelSerializer):
    class Meta:
        model =ms_sub
        fields = ('ms_id','att_id','att_seq','att_cdh','att_cdd','att_val','att_unit','use_yn','sort_seq')        

class msPop1_Det3(generics.ListAPIView):

    queryset = ms_sub.objects.all()
    serializer_class = msPop1_Det3Serializer
    def list(self, request):
        ms_id = request.GET.get('ms_id', None)
        print("aaa1")
        print(ms_id)
        query = "select * from service20_ms_sub where ms_id='"+ms_id+"' and att_id = 'MS0016'"
        print("a333")
        queryset = ms_sub.objects.raw(query)        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)    






@csrf_exempt
def mpFn1(request):
    mp_id = request.GET.get('mp_id', None)  
    
    queryset2 = cm_cnv_scr.objects.all()
    query = "select * from service20_mp_mtr where mp_id = '" +str(mp_id)+"'"
    queryset = mpgm.objects.raw(query)

    vl_cscore1=''
    vl_cscore2=''
    vl_cscore3=''
    vl_cscore4=''
    #
    for val in queryset:

        if val.score1==None:
            vl_cscore1 = 0
        elif val.score2==None:
            vl_cscore1 = 0
        else:
            vl_cscore1 = (val.score1 / val.score2) * 100

        query2 = "select id, eval_item, fin_scr from service20_cm_cnv_scr  where eval_item = '1'  and (min_scr <= '" +str(vl_cscore1)+"' and  '" +str(vl_cscore1)+"' < max_scr)"
        queryset2 = cm_cnv_scr.objects.raw(query2)

        
        for var2 in queryset2:
            #print(var2.fin_scr)
            vl_cscore1 = var2.fin_scr
            #queryset1 = mp_mtr.objects.all()  
            mp_mtr.objects.filter(id=val.id,mp_id=val.mp_id).update(cscore1=vl_cscore1)

    for val in queryset:
        vl_cscore2 = val.score3


        query2 = "select id, eval_item, fin_scr from service20_cm_cnv_scr  where eval_item = '2'  and (min_scr <= '" +str(vl_cscore2)+"' and  '" +str(vl_cscore2)+"' < max_scr)"
        queryset2 = cm_cnv_scr.objects.raw(query2)

        for var2 in queryset2:
            #print(var2.fin_scr)
            vl_cscore2 = var2.fin_scr
            #mp_mtr.objects.filter(id=val.id,mp_id=val.mp_id).update(cscore2=vl_cscore2)

    for val in queryset:
        vl_cscore2 = val.score3
        query3 = "select id, eval_item, fin_scr from service20_cm_cnv_scr  where eval_item = '3'  and (min_scr <= '" +str(vl_cscore3)+"' and  '" +str(vl_cscore3)+"' < max_scr)"
        queryset2 = cm_cnv_scr.objects.raw(query3)

        for var2 in queryset2:
            #print(var2.fin_scr)
            vl_cscore3 = var2.fin_scr

    #봉사
    for val in queryset:
        vl_cscore4 = val.score4
        query3 = "select id, eval_item, fin_scr from service20_cm_cnv_scr  where eval_item = '2'  and (min_scr <= '" +str(vl_cscore4)+"' and  '" +str(vl_cscore4)+"' < max_scr)"
        queryset2 = cm_cnv_scr.objects.raw(query3)

        for var2 in queryset2:
            #print(var2.fin_scr)
            vl_cscore3 = var2.fin_scr
            mp_mtr.objects.filter(id=val.id,mp_id=val.mp_id).update(cscore3=vl_cscore3)




    #mp_mtr.objects.filter(id=val.id,mp_id=val.mp_id).update(cscore3=vl_cscore3)




        #query2 = "select * from service20_cm_cnv_scr where eval_item = '1'"
        #queryset2 = cm_cnv_scr.objects.raw(query2)     
        #queryset1 = mp_mtr.objects.all()  
        #queryset1.filter(id=val.id,mp_id=val.mp_id).update(cscore1=vl_cscore1)

        """
        model_instance = mp_mtr(
            id=val.id, 
            mp_id=val.mp_id, 
            apl_no=val.apl_no, 
            apl_id=val.apl_id,
            cscore1=vl_cscore1,
            cscore2=vl_cscore2,
            cscore3=vl_cscore3
            )
        model_instance.save()
        """
    message = "Ok" 
    context = {'message': message,}
    

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})




@csrf_exempt
def mpFn2(request):
    mp_id = request.GET.get('mp_id', None)  
    
    queryset2 = cm_cnv_scr.objects.all()
    query = "select * from service20_mp_mtr where mp_id = '" +str(mp_id)+"' order by (cscore1+cscore2+cscore3+cscore4+cscore5+cscore5) desc"
    rank = 1
    queryset = mpgm.objects.raw(query)


    #
    for val in queryset:
        mp_mtr.objects.filter(id=val.id,mp_id=val.mp_id).update(doc_rank=rank)
        rank = rank + 1


    message = "Ok" 
    context = {'message': message,}
    

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})



@csrf_exempt
def mpFn3(request):
    mp_id = request.GET.get('mp_id', None)  
    query = "select * from service20_mp_mtr where mp_id = '" +str(mp_id)+"'"
    queryset = mp_mtr.objects.raw(query)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

 
    writer = csv.writer(response)
    writer.writerow(['apl_no', 'unv_nm', 'dept_nm', 'apl_id', 'apl_nm', 'gen', 'cscore1', 'cscore2', 'cscore3', 'cscore4', 'cscore5', 'doc_rslt', 'doc_rank', 'intv_team', 'intv_dt', 'intv_part_pl','intv_part_ac'])

    if mp_id == None:
        users = mp_mtr.objects.all().values_list('apl_no', 'unv_nm', 'dept_nm', 'apl_id', 'apl_nm', 'gen', 'cscore1', 'cscore2', 'cscore3', 'cscore4', 'cscore5', 'doc_rslt', 'doc_rank', 'intv_team', 'intv_dt', 'intv_part_pl','intv_part_ac')
    else:
        users = mp_mtr.objects.filter(mp_id=mp_id).values_list('apl_no', 'unv_nm', 'dept_nm', 'apl_id', 'apl_nm', 'gen', 'cscore1', 'cscore2', 'cscore3', 'cscore4', 'cscore5', 'doc_rslt', 'doc_rank', 'intv_team', 'intv_dt', 'intv_part_pl','intv_part_ac')

    for user in users:
        writer.writerow(user)
    return response





@csrf_exempt
def mpPop1(request):
    posts = None
    return render(request, 'popup/mento/mpPop1.html', { 'posts': posts })



class mpPop1_Det1Serializer(serializers.ModelSerializer):
    class Meta:
        model = mp_mtr
        fields = ('mp_id','apl_no','mntr_id','indv_div','team_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','bank_acct','bank_cd','bank_nm','bank_dpsr','cnt_mp_a','cnt_mp_p','cnt_mp_c','cnt_mp_g','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm')        
        #fields = ('mp_id','apl_no','mntr_id','indv_div','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr')

class mpPop1_Det1(generics.ListAPIView):

    print("aaa111")

    queryset = mp_mtr.objects.all()
    serializer_class = mpPop1_Det1Serializer

    def list(self, request):

        print("aaa222")
        mp_id = request.GET.get('mp_id', None)
        apl_id = request.GET.get('apl_id', None)

        query = "select * from service20_mp_mtr where mp_id='"+mp_id+"' and apl_id = '"+apl_id+"'"

        print(query)
        queryset = mp_mtr.objects.raw(query)        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)    




@csrf_exempt
def mpPop1_Det2(request):

    print("start")
    apl_id = request.GET.get('apl_id', None)

    print(apl_id)
    vm_nanum_flag = vm_nanum_stdt.objects.filter(apl_id=apl_id).exists()

    if not vm_nanum_flag:
        message = "Fail"
        context = {'message': message}
        print("aaaa")
    else:
        message = "Ok"
        rows = vm_nanum_stdt.objects.filter(apl_id=apl_id)[0]
        print("bbb")
        print(rows)
        context = {'message': message,
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
                    }
    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})