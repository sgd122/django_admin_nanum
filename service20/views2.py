from django.shortcuts import render
from rest_framework import generics, serializers
from django.http import HttpResponse,Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.shortcuts import get_object_or_404,render
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse,Http404, HttpResponseRedirect
from django.views import generic, View
from django.urls import reverse
from service10.models import *
from service20.models import *
from polls.models import Choice, Question
from django.db.models import Max
from collections import namedtuple

from django.db import connection
from collections  import OrderedDict
import json
#import csv
from django.conf import settings
import unicodecsv as csv
import time
from django import forms
import django_excel as excel
import os
import requests
from bs4 import BeautifulSoup as bs

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
        fields = ('ms_id','status','ms_name','ms_sname','ms_intro','mng_area','mgr_id','mgr_nm','mng_org','sup_org','yr','yr_seq','apl_ntc_fr_dt','apl_ntc_to_dt','apl_term','apl_fr_dt','apl_to_dt','trn_term','trn_fr_dt','trn_to_dt','tot_apl','cnt_apl','cnt_doc_suc','cnt_doc_res','cnt_intv_pl','cnt_intv_ac','intv_dt','cnt_intv_suc','cnt_iintv_res','cnt_trn','cnt_mtr','doc_dt','doc_in_dt','doc_in_mgr','intv_in_dt','intv_in_mgr','fin_dt','fin_in_dt','fin_in_mgr')

class msComboListViewDetail(generics.ListAPIView):
    queryset = msch.objects.all()
    serializer_class = msComboListViewDetailSerializer

    def list(self, request):
        print("a1")
        l_ms_id = request.GET.get('ms_id', None)
        print(l_ms_id)
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

        query2 = "select id, eval_item, fin_scr from service20_cm_cnv_scr  where eval_item = '1'  and (min_scr < '" +str(vl_cscore1)+"' and  '" +str(vl_cscore1)+"' <= max_scr)"
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


##멘토스쿨 사정 버튼 클릭
@csrf_exempt
def msFn2(request):
    ms_id = request.GET.get('ms_id', None)  
    
    queryset2 = cm_cnv_scr.objects.all()
    query = "select * from service20_ms_apl where ms_id = '" +str(ms_id)+"' order by (cscore1+cscore2+cscore3+cscore4+cscore5) desc"
    rank = 1
    queryset = msch.objects.raw(query)
    
    cursor = connection.cursor()
    query_doc1 = "select tot_apl from service20_msch where ms_id = '" +str(ms_id)+ "'"
    cursor.execute(query_doc1)
    results_doc1 = namedtuplefetchall(cursor)   
    val_doc1 = results_doc1[0].tot_apl
    #
    i = 0
    for val in queryset:

        if val.cscore4 == None:
            message = "N4" #지원서 점수 값이 없을떄  
            break
        elif val.cscore4 == 0:
            message = "N4" #지원서 점수 값이 없을떄 
            break

        elif int(i) < int(val_doc1):
            ms_apl.objects.filter(id=val.id,ms_id=val.ms_id).update(doc_rank=rank)
            ms_apl.objects.filter(id=val.id,ms_id=val.ms_id).update(doc_rslt='P')
            message = "Ok" 

        rank = rank + 1
        i= i + 1

    context = {'message': message,}
    

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


##엑셀 다운로드 하기
@csrf_exempt
def msFn3(request):
    ms_id = request.GET.get('ms_id', None)  
    query = "select * from service20_ms_apl where ms_id = '" +str(ms_id)+"'"
    queryset = ms_apl.objects.raw(query)

    response = HttpResponse(content_type='text/csv;encoding=UTF-8"') 
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

 
    writer = csv.writer(response, encoding='euc-kr')
    writer.writerow(['apl_no', 'unv_nm', 'dept_nm', 'apl_id', 'apl_nm', 'gen', 'cscore1', 'cscore2', 'cscore3', 'cscore4', 'cscore5', 'doc_rslt', 'doc_rank', 'intv_team', 'intv_dt', 'intv_part_pl','intv_part_ac'])
    
    print(ms_id)
    if ms_id == None:
        users = ms_apl.objects.all().values_list('apl_no', 'unv_nm', 'dept_nm', 'apl_id', 'apl_nm', 'gen', 'cscore1', 'cscore2', 'cscore3', 'cscore4', 'cscore5', 'doc_rslt', 'doc_rank', 'intv_team', 'intv_dt', 'intv_part_pl','intv_part_ac')
    else:
        users = ms_apl.objects.filter(ms_id=ms_id).values_list('apl_no', 'unv_nm', 'dept_nm', 'apl_id', 'apl_nm', 'gen', 'cscore1', 'cscore2', 'cscore3', 'cscore4', 'cscore5', 'doc_rslt', 'doc_rank', 'intv_team', 'intv_dt', 'intv_part_pl','intv_part_ac')

    for user in users:
        writer.writerow(user)
    return response



#면접 구성
@csrf_exempt
def msFn4(request):

    ms_id = request.GET.get('ms_id', None)
    cursor = connection.cursor()

    query_a = "select intv_dt from service20_msch where ms_id = '"+ ms_id + "'"
    cursor.execute(query_a)
    results_a = namedtuplefetchall(cursor)  
    query_b = "select * from service20_ms_apl where doc_rslt = 'P' and ms_id = '"+ ms_id + "'order by id"
    cursor.execute(query_b)
    results_b = namedtuplefetchall(cursor)  

    print(query_b)
     

    #면접 그룹 인원수
    query_01 = "select att_val, att_unit from service20_ms_sub where ms_id =  '"+ ms_id + "' and att_id = 'MS0019' and att_cdd = '01' and use_yn = 'Y'"
    cursor.execute(query_01)
    results_01 = namedtuplefetchall(cursor) 
    val_01 = results_01[0].att_val
    val_01_copy = val_01

    #면접시작시간
    query_02 = "select att_val, att_unit from service20_ms_sub where ms_id =  '"+ ms_id + "' and att_id = 'MS0019' and att_cdd = '02' and use_yn = 'Y'"
    cursor.execute(query_02)
    results_02 = namedtuplefetchall(cursor) 
    val_02 = results_02[0].att_val
    val_02_copy = val_02

    #시간 간격
    query_03 = "select att_val, att_unit from service20_ms_sub where ms_id =  '"+ ms_id + "' and att_id = 'MS0019' and att_cdd = '03' and use_yn = 'Y'"
    cursor.execute(query_03)
    results_03 = namedtuplefetchall(cursor) 
    val_03 = results_03[0].att_val

    #휴식 가능 팀수
    query_04 = "select att_val, att_unit from service20_ms_sub where ms_id =  '"+ ms_id + "' and att_id = 'MS0019' and att_cdd = '04' and use_yn = 'Y'"
    cursor.execute(query_04)
    results_04 = namedtuplefetchall(cursor) 
    val_04 = results_04[0].att_val

    #휴식 시간
    query_05 = "select att_val, att_unit from service20_ms_sub where ms_id =  '"+ ms_id + "' and att_id = 'MS0019' and att_cdd = '05' and use_yn = 'Y'"
    cursor.execute(query_05)
    results_05 = namedtuplefetchall(cursor) 
    val_05 = results_05[0].att_val

    #면접 장소
    query_06 = "select att_val, att_unit from service20_ms_sub where ms_id =  '"+ ms_id + "' and att_id = 'MS0019' and att_cdd = '06' and use_yn = 'Y'"
    cursor.execute(query_06)
    results_06 = namedtuplefetchall(cursor) 
    val_06 = results_06[0].att_val
    print("bbbb")
    
    lv_intv_team = 1 #면접번호
    lv_cnt = 1

    l_data = str(results_a[0].intv_dt) +" " + str(val_02) + ":00"
    l_data2 = datetime.datetime.strptime(l_data,"%Y-%m-%d %H:%M:%S")
    for var in results_b:
        
        insert_sql = "update service20_ms_apl set "
        insert_sql += "intv_team='"+ str(lv_intv_team) +"'," 
        insert_sql += "intv_dt='"+ str(l_data2) +"'" 
        insert_sql += " where 1=1 " 
        insert_sql += " and id='"+ str(var.id) +"'" 

        print(insert_sql)

        cursor.execute(insert_sql)
        
        print("면접팀" + str(lv_intv_team))
        print("면접일" + str(results_a[0].intv_dt))
        print("면접시간" + str(l_data2))
        print("휴식가능" + str(val_04)) 
        #면접번호랑 카운트랑 같으면 하나 증가시켜준다
        if int(lv_cnt) == int(val_01):
            val_01 = int(val_01) + int(val_01_copy)

            #휴식시간 같으면 거시기한다
            if int(lv_intv_team) == int(val_04):
                l_data2 = l_data2 + datetime.timedelta(minutes=int(val_05))

            lv_intv_team = lv_intv_team +1

            #휴식가능 시간을 만들어준다.
            l_data2 = l_data2 + datetime.timedelta(minutes=int(val_03))
        lv_cnt = lv_cnt + 1

    message = "Ok" 
    context = {'message': message,}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


class UploadFileForm(forms.Form):
    file = forms.FileField()


#합격자 업로드.
@csrf_exempt
def msFn6(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(), "csv",
                                       file_name="download")
    else:
        form = UploadFileForm()
    return render(
        request,
        'popup/fileupload/upload_form.html',
        {
            'form': form,
            'title': '서류평가 엑셀 업로드',
            'header': ('업로드할 엑셀파일을 넣어주세요')
        })


#합격자 업로드.
@csrf_exempt
def msFn6_Submit(request):
    apl_id = request.GET.get('apl_id', None)
    ms_id = request.GET.get('ms_id', None)
    #print(apl_id)
    #print(ms_id)
    cursor = connection.cursor()
    insert_sql = "update service20_ms_apl set "
    insert_sql += "doc_rslt='P' "
    insert_sql += " where 1=1" 
    insert_sql += " and ms_id='"+ ms_id +"'" 
    insert_sql += " and apl_id='"+ apl_id +"'"
    cursor.execute(insert_sql)

    message = "Ok" 
    context = {'message': message,}
    
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


#합격자 업로드.
@csrf_exempt
def msFn6_Submit2(request):
    apl_id = request.GET.get('apl_id', None)
    ms_id = request.GET.get('ms_id', None)
    print(apl_id)
    print(ms_id)
    print("울트라 잘된다.............................................")
    cursor = connection.cursor()
    insert_sql = "update service20_ms_apl set "
    insert_sql += "doc_rslt='N' "
    insert_sql += " where doc_rslt<>'P'" 
    insert_sql += " and ms_id='"+ ms_id +"'" 

    print(insert_sql)
    cursor.execute(insert_sql)

    message = "Ok" 
    context = {'message': message,}
    
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})



#합격자 업로드.
@csrf_exempt
def msFn7(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(), "csv",
                                       file_name="download")
    else:
        form = UploadFileForm()
    return render(
        request,
        'popup/fileupload/upload_form2.html',
        {
            'form': form,
            'title': '서류평가 엑셀 업로드',
            'header': ('업로드할 엑셀파일을 넣어주세요')
        })


#최종 합격자 업로드.
@csrf_exempt
def msFn7_Submit(request):
    apl_id = request.GET.get('apl_id', None)
    ms_id = request.GET.get('ms_id', None)
    #print(apl_id)
    #print(ms_id)
    cursor = connection.cursor()
    
    print("되야함11")
    #멘토 ID
    query_01 = "select CONCAT('M',substr(DATE_FORMAT(now(), '%Y'),3,2),(select ifnull(lpad(max(right(mntr_id,2)) + 1,4,0),'0001')   from service20_mentor where substr(mntr_id,2,2)  = substr(DATE_FORMAT(now(), '%Y'),3,2))) as id from dual"
    cursor.execute(query_01)
    results_01 = namedtuplefetchall(cursor) 
    val_01 = results_01[0].id
    print("되야함22")
    
    insert_sql = "update service20_ms_apl set "
    insert_sql += "fnl_rslt='P',"
    insert_sql += "mntr_id='"+ str(results_01[0].id) +"'," 
    insert_sql += "mntr_dt=now()" 
    insert_sql += " where 1=1" 
    insert_sql += " and ms_id='"+ str(ms_id) +"'" 
    insert_sql += " and apl_id='"+ str(apl_id) +"'" 
    print("되야함33")
    print("시작")
    print(insert_sql)
    cursor.execute(insert_sql)

    print("한솔이는 E클래스 사줄꼐")
    instr_sql = "INSERT"
    instr_sql += " INTO   service20_mentor "  
    instr_sql += "       (                 "
    instr_sql += "              MNTR_ID ,  "
    instr_sql += "              MNTR_NM ,"
    instr_sql += "              MNTR_NM_E ,"
    instr_sql += "              MS_ID ,"
    instr_sql += "              APL_NO ,"
    instr_sql += "              APL_ID ,"
    instr_sql += "              MNTR_DT ,"
    instr_sql += "              UNV_CD ,"
    instr_sql += "              UNV_NM ,"
    instr_sql += "              CLLG_CD ,"
    instr_sql += "              CLLG_NM ,"
    instr_sql += "              DEPT_CD ,"
    instr_sql += "              DEPT_NM ,"
    instr_sql += "              BRTH_DT ,"
    instr_sql += "              GEN ,"
    instr_sql += "              YR ,"
    instr_sql += "              TERM_DIV ,"
    instr_sql += "              SCH_YR ,"
    instr_sql += "              EXP_DT ,"
    instr_sql += "              EXP_RSN ,"
    instr_sql += "              MOB_NO ,"
    instr_sql += "              TEL_NO ,"
    instr_sql += "              TEL_NO_G ,"
    instr_sql += "              H_ADDR ,"
    instr_sql += "              POST_NO ,"
    instr_sql += "              EMAIL_ADDR ,"
    instr_sql += "              BANK_ACCT ,"
    instr_sql += "              BANK_CD ,"
    instr_sql += "              BANK_NM ,"
    instr_sql += "              BANK_DPSR ,"
    instr_sql += "              CNT_MP_A ,"
    instr_sql += "              CNT_MP_P ,"
    instr_sql += "              CNT_MP_C ,"
    instr_sql += "              CNT_MP_G ,"
    instr_sql += "              INS_ID ,"
    instr_sql += "              INS_IP ,"
    instr_sql += "              INS_DT ,"
    instr_sql += "              INS_PGM ,"
    instr_sql += "              UPD_ID ,"
    instr_sql += "              UPD_IP ,"
    instr_sql += "              UPD_DT ,"
    instr_sql += "              UPD_PGM"
    instr_sql += "       )"
    instr_sql += "SELECT '"+  str(results_01[0].id) + "',"
    instr_sql += "       APL_NM ,"
    instr_sql += "       ' ',"
    instr_sql += "       MS_ID ,"
    instr_sql += "       APL_NO ,"
    instr_sql += "       APL_ID ,"
    instr_sql += "       MNTR_DT ,"
    instr_sql += "       UNV_CD ,"
    instr_sql += "       UNV_NM ,"
    instr_sql += "       CLLG_CD ,"
    instr_sql += "       CLLG_NM ,"
    instr_sql += "       DEPT_CD ,"
    instr_sql += "       DEPT_NM ,"
    instr_sql += "       BRTH_DT ,"
    instr_sql += "       GEN ,"
    instr_sql += "       YR ,"
    instr_sql += "       TERM_DIV ,"
    instr_sql += "       SCH_YR ,"
    instr_sql += "       NULL ,"
    instr_sql += "       NULL ,"
    instr_sql += "       MOB_NO ,"
    instr_sql += "       TEL_NO ,"
    instr_sql += "       TEL_NO_G ,"
    instr_sql += "       H_ADDR ,"
    instr_sql += "       POST_NO ,"
    instr_sql += "       EMAIL_ADDR ,"
    instr_sql += "       NULL ,"
    instr_sql += "       NULL ,"
    instr_sql += "       NULL ,"
    instr_sql += "       NULL ,"
    instr_sql += "       0 ,"
    instr_sql += "       0 ,"
    instr_sql += "       0 ,"
    instr_sql += "       0 ,"
    instr_sql += "       '5550541',"
    instr_sql += "       '0.0.0.1',"
    instr_sql += "       NOW() ,"
    instr_sql += "       'MySQL',"
    instr_sql += "       NULL ," 
    instr_sql += "       NULL ," 
    instr_sql += "       NULL ,"
    instr_sql += "       NULL" 
    instr_sql += " FROM   service20_ms_apl"
    instr_sql += " WHERE  MNTR_ID = '" + str(results_01[0].id) + "'"

    #print(instr_sql)
    cursor.execute(instr_sql)

    message = "Ok" 
    context = {'message': message,}
    
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

#불합격자 업로드.
@csrf_exempt
def msFn7_Submit2(request):
    apl_id = request.GET.get('apl_id', None)
    ms_id = request.GET.get('ms_id', None)
    print(apl_id)
    print(ms_id)
    print("울트라 잘된다.............................................")
    cursor = connection.cursor()
    insert_sql = "update service20_ms_apl set "
    insert_sql += "doc_rslt='N' "
    insert_sql += " where doc_rslt<>'P'" 
    insert_sql += " and ms_id='"+ ms_id +"'" 

    print(insert_sql)

    cursor.execute(insert_sql)

    message = "Ok" 
    context = {'message': message,}
    
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})



#멘토스쿨 리포트보기.
@csrf_exempt
def msFn8(request):
    print("aa")
    context = None
    return render(
        request,
        #'report/reportProgram.html',
        'report/reportProgram.html',
        context)




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
        fields = ('mp_id','status','mp_name','apl_term','yr_seq','mng_org','sup_org','tot_apl','apl_fr_dt','apl_to_dt','mnt_fr_dt','mnt_to_dt')



class mpComboListViewDetail(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = mpComboListDetailSerializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', None)
        queryset = self.get_queryset()
        #queryset = queryset.filter(mp_id=l_mp_id)  
        query = "select mp_id,status as status_code, base_div, apl_term as apl_term_code, mp_name,mp_sname,mng_area,mgr_id, mgr_nm, yr, yr_seq, mng_org as mng_org_code,sup_org as sup_org_nm,tot_apl,apl_fr_dt,apl_to_dt,mnt_fr_dt,mnt_to_dt, "
        query +="(SELECT  std_detl_code_nm from service20_com_cdd B WHERE std_grp_code = 'MS0022' AND B.std_detl_code = A.apl_term) AS apl_term, "
        query +="(SELECT  std_detl_code_nm from service20_com_cdd B WHERE std_grp_code = 'MP0003' AND B.std_detl_code = A.mng_org) AS mng_org, "
        query +="(SELECT  std_detl_code_nm from service20_com_cdd B WHERE std_grp_code = 'MP0004' AND B.std_detl_code = A.sup_org) AS sup_org, "
        query +="(SELECT  std_detl_code_nm from service20_com_cdd B WHERE std_grp_code = 'MP0001' AND B.std_detl_code = A.status) AS status "        
        query +="from service20_mpgm A where mp_id='"+l_mp_id+"'" 


        print(query)

        queryset = mpgm.objects.raw(query)   
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)    
#######################################################

@csrf_exempt
def msPop1(request):
    posts = None
    return render(request, 'popup/mento/msPop1.html', { 'posts': posts })      
#######################################################


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
#######################################################

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
        query = "select * from service20_ms_sub where ms_id='"+ms_id+"' and att_id = 'MS0016' and use_yn = 'Y' order by sort_seq"
        print("a333")
        queryset = ms_sub.objects.raw(query)        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)    
#######################################################

#멘토스쿨 핍압1_조회4_채점자 교수 조회
class msPop1_Det4Serializer(serializers.ModelSerializer):
    nm = serializers.SerializerMethodField()
    class Meta:
        model =ms_sub
        fields = ('ms_id','att_id','att_seq','att_cdh','att_cdd','att_val','att_unit','use_yn','sort_seq','nm')        

    def get_nm(self,obj):
        return obj.nm
#######################################################

class msPop1_Det4(generics.ListAPIView):

    queryset = ms_sub.objects.all()
    serializer_class = msPop1_Det4Serializer
    def list(self, request):
        ms_id = request.GET.get('ms_id', None)
        print("aaa1")
        print(ms_id)
        #query = "select * from service20_ms_sub where ms_id='"+ms_id+"' and att_id = 'MS0016' and use_yn = 'Y' order by sort_seq"
        query = "select (Select std_detl_code_nm from service20_com_cdd B where B.std_grp_code = A.att_id and B.std_detl_code = A.att_cdd) as nm, A.*   from service20_ms_sub A where A.att_id = 'MS0015' and A.ms_id ='"+ms_id+"' and use_yn = 'Y' order by sort_seq"
        print("a333")
        queryset = ms_sub.objects.raw(query)        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)    



#멘토스쿨 핍압1_조회5_채점 조회
class msPop1_Det5Serializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    class Meta:
        model =ms_sub
        fields = ('ms_id','att_id','att_seq','att_cdh','att_cdd','att_val','att_unit','use_yn','sort_seq','score')        

    def get_score(self,obj):
        return obj.score


class msPop1_Det5(generics.ListAPIView):

    queryset = ms_sub.objects.all()
    serializer_class = msPop1_Det5Serializer
    def list(self, request):
        ms_id = request.GET.get('ms_id', None)
        apl_no = request.GET.get('user_id', None)
        att_cdd_id = request.GET.get('att_cdd_id', None)
        nm_id = request.GET.get('nm_id', None)

        

        query = "select A.*, B.* from   service20_ms_sub A left outer join service20_ms_mrk B on     A.ms_id   = B.ms_id and    A.att_cdd = B.mrk_id where  A.att_id   = 'MS0016' and    B.apl_no         = '" + apl_no +"' and    A.att_cdd        = '"+att_cdd_id+"' and    B.item_cd = '"+nm_id+"' order by item_cd"
        
        print(query)
        queryset = ms_sub.objects.raw(query)        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)    


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]



#지원서 점수 저장하기
@csrf_exempt
def msPop1_Det5_Save(request):
    ms_id = request.GET.get('ms_id', None)  
    test_div = request.GET.get('test_div', None)  
    
    apl_no = request.GET.get('apl_no', None)
    mrk_id = request.GET.get('mrk_id', None)
    mrk_nm = request.GET.get('mrk_nm', None)
    score = request.GET.get('score', None)
    item_cd = request.GET.get('item_cd', None)
    item_nm = request.GET.get('item_nm', None)

    mrk_seq = request.GET.get('mrk_seq', None)
    mrk_no = request.GET.get('mrk_no', None)

    cursor = connection.cursor()
    query = "select count(1) as cnt  from service20_ms_mrk  where apl_no ='"+ apl_no +"' and ms_id='"+ ms_id +"' and mrk_id = '" +mrk_id + "' and item_cd = '" +item_cd + "' and test_div = '" +test_div +   "' and mrk_seq = '" +mrk_seq +    "' and mrk_no = '" +mrk_no +   "' "
    cursor.execute(query)
    results = namedtuplefetchall(cursor)    
    num = results[0].cnt


    if num > 0:
        print("건수가 있음")
        insert_sql = "update service20_ms_mrk set "

        insert_sql += "score='"+ score +"'," 
        insert_sql += "item_cd='"+ item_cd +"'," 
        insert_sql += "item_nm='"+ item_nm +"'" 

        insert_sql += " where 1=1" 
        insert_sql += " and ms_id='"+ ms_id +"'" 
        insert_sql += " and test_div='"+ test_div +"'" 
        insert_sql += " and apl_no='"+ apl_no +"'" 
        insert_sql += " and mrk_seq='"+ mrk_seq +"'" 
        insert_sql += " and mrk_no='"+ mrk_no +"'" 
        insert_sql += " and mrk_id='"+ mrk_id +"'" 
        #print(insert_sql)
        cursor.execute(insert_sql)


    else:
        
        print("건수가 없음")
        
        if score == None:
            score = '0'
        elif score == '':
            score = '0'

        insert_sql = "insert into service20_ms_mrk (ms_id, test_div, apl_no, mrk_seq, mrk_no, mrk_id, mak_nm, score, item_cd, item_nm)"
        insert_sql += "values("
        insert_sql += "'"+ ms_id +"'," 
        insert_sql += "'10'," 
        insert_sql += "'"+ apl_no +"'," 
        insert_sql += "'"+ mrk_seq +"',"  #mrk_id
        insert_sql += "'"+ mrk_no +"',"  #mrk_id
        insert_sql += "'"+ mrk_id +"',"  #mrk_id
        insert_sql += "'"+ mrk_nm +"',"  #mrk_nm
        insert_sql += "'"+ score +"',"  #score
        insert_sql += "'"+ item_cd +"',"  #item_cd
        insert_sql += "'"+ item_nm +"')"  #item_nm
        #print(insert_sql)

        cursor.execute(insert_sql)
        

    query = " select (sum(score) / 3) as res from service20_ms_mrk where apl_no = '" + apl_no + "' and ms_id = '" + ms_id +"'"

    print(query)

    cursor.execute(query)
    results = namedtuplefetchall(cursor)    
    score4 = results[0].res
    
    print("aaaa")
    insert_sql = "update service20_ms_apl set "
    insert_sql += "cscore4='"+ str(score4) +"'" 
    insert_sql += " where 1=1" 
    print("bbbb")
    insert_sql += " and ms_id='"+ str(ms_id) +"'" 
    insert_sql += " and apl_no='"+ str(apl_no) +"'" 
    print("cccc")
    
    print(insert_sql)

    #print(insert_sql)
    cursor.execute(insert_sql)

    
        

    message = "Ok" 
    context = {'message': message,}


    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


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
    cursor = connection.cursor()

    for val in queryset:

        if val.score1==None:
            vl_cscore1 = 0
        elif val.score2==None:
            vl_cscore1 = 0
        else:
            vl_cscore1 = (val.score1 / val.score2) * 100

        #query2 = "select id, eval_item, fin_scr from service20_cm_cnv_scr  where eval_item = '1'  and (min_scr <= '" +str(vl_cscore1)+"' and  '" +str(vl_cscore1)+"' < max_scr)"
        query2 = "select id, eval_item, fin_scr from service20_cm_cnv_scr  where eval_item = '1'  and (min_scr < '" +str(vl_cscore1)+"' and  '" +str(vl_cscore1)+"' <= max_scr)"
        queryset2 = cm_cnv_scr.objects.raw(query2)

        mp_mtr.objects.filter(id=val.id,mp_id=val.mp_id).update(cscore1=0)
        for var2 in queryset2:
            #print(var2.fin_scr)
            vl_cscore1 = var2.fin_scr
            #queryset1 = mp_mtr.objects.all()  
            mp_mtr.objects.filter(id=val.id,mp_id=val.mp_id).update(cscore1=vl_cscore1)

    for val in queryset:
        vl_cscore2 = val.score3


        #query2 = "select id, eval_item, fin_scr from service20_cm_cnv_scr  where eval_item = '2'  and (min_scr <= '" +str(vl_cscore2)+"' and  '" +str(vl_cscore2)+"' < max_scr)"
        query2 = "select id, eval_item, fin_scr from service20_cm_cnv_scr  where eval_item = '2'  and (min_scr < '" +str(vl_cscore2)+"' and  '" +str(vl_cscore2)+"' <= max_scr)"
        queryset2 = cm_cnv_scr.objects.raw(query2)

        for var2 in queryset2:
            #print(var2.fin_scr)
            vl_cscore2 = var2.fin_scr
            #mp_mtr.objects.filter(id=val.id,mp_id=val.mp_id).update(cscore2=vl_cscore2)

    #어학
    for val in queryset:
        vl_cscore2 = val.score3
        query3  = " SELECT   MAX(CASE WHEN t3.eval_div = 'S' AND t3.min_scr <= t1.score AND t1.score < t3.max_scr THEN t3.fin_scr "
        query3 += "                WHEN t3.eval_div = 'G' AND t3.grade = t1.grade THEN t3.fin_scr "
        query3 += "                ELSE 0 END ) AS cnv_scr "
        query3 += "  FROM service20_mp_mtr_fe t1 "
        query3 += "  LEFT JOIN service20_com_cdd    t2 ON (t2.std_detl_code_nm = t1.frexm_nm) "
        query3 += "  LEFT JOIN service20_cm_cnv_scr t3 ON (t3.eval_item = 3 "
        query3 += "                                    AND t3.eval_cd   = t2.std_detl_code) "
        query3 += " WHERE t1.apl_id = '"+ str(val.apl_id) +"' "
        query3 += "   AND t1.mp_id = '"+ str(val.mp_id) +"' "
                
        cursor.execute(query3)
        results = namedtuplefetchall(cursor)    
        
        query_cnt = len(list(results))

        print("print___")
        print(query_cnt)

        if query_cnt == '0':
           vl_cscore2 = '0'
        else:
           print("print222")
           print(results[0].cnv_scr)
           if results[0].cnv_scr == None:
              vl_cscore2 = '0'
           else:
              vl_cscore2 = results[0].cnv_scr
           

        mp_mtr.objects.filter(id=val.id,mp_id=val.mp_id).update(cscore2=vl_cscore2)


    #봉사
    for val in queryset:
        mp_mtr.objects.filter(id=val.id,mp_id=val.mp_id).update(cscore3=0)

        vl_cscore4 = val.score4
        query3 = "select id, eval_item, fin_scr from service20_cm_cnv_scr  where eval_item = '2'  and (min_scr <= '" +str(vl_cscore4)+"' and  '" +str(vl_cscore4)+"' < max_scr)"
        #query3 = "select id, eval_item, fin_scr from service20_cm_cnv_scr  where eval_item = '2'  and (min_scr < '" +str(vl_cscore4)+"' and  '" +str(vl_cscore4)+"' <= max_scr)"
        queryset2 = cm_cnv_scr.objects.raw(query3)
        for var2 in queryset2:
            #print(var2.fin_scr)
            vl_cscore3 = var2.fin_scr
            mp_mtr.objects.filter(id=val.id,mp_id=val.mp_id).update(cscore3=vl_cscore3)

    #지원서
    for val in queryset:
        mp_mtr.objects.filter(id=val.id,mp_id=val.mp_id).update(cscore4=0)

        vl_cscore4 = val.score4
        vl_apl_no = val.apl_no
        #query3 = "select max(id) AS id, (SUM(tot_score) / 3) AS ss from service20_mp_mrk_h WHERE mp_id = '"+ str(val.mp_id) +"' AND apl_no = '"+ str(vl_apl_no)+"'"
        query3 = "select max(id) AS id, (SUM(tot_score) / 3) AS ss from service20_mp_mrk_h WHERE mp_id = '"+ str(val.mp_id) +"' AND apl_no = '"+ str(vl_apl_no)+"'"
        queryset2 = cm_cnv_scr.objects.raw(query3)
        for var2 in queryset2:
            vl_cscore4 = var2.ss
            mp_mtr.objects.filter(id=val.id,mp_id=val.mp_id).update(cscore4=vl_cscore4)    

            #사범대학일경우 가산점 1이 더 붙는다.
            #query_ex1 = "select max(id) AS id, (SUM(score) / 3) AS ss from service20_mp_mrk WHERE mp_id = '"+ str(val.mp_id) +"' AND apl_no = '"+ str(vl_apl_no)+"'"


    #사범대학 업로드
    """
    query5  = " update service20_mp_mtr "
    query5 += "    SET CSCORE5 = (SELECT IFNULL(MAX(att_val),0) "
    query5 += "                  FROM service20_mp_sub t3 "
    query5 += "  WHERE t3.mp_id   = '"+ str(val.mp_id) +"' "
    query5 += "    AND t3.att_id  = 'MP0009' "
    query5 += "    AND t3.att_cdh = 'MP0009' "
    query5 += "    AND t3.att_cdd = '20'  "
    query5 += "    ) "
    query5 += " WHERE CLLG_NM LIKE CONCAT('%',  "
    query5 += "    (SELECT att_val "
    query5 += "    FROM service20_mp_sub t3 "
    query5 += "    WHERE t3.mp_id   = '"+ str(val.mp_id) +"' "
    query5 += "    AND t3.att_id  = 'MP0008' "
    query5 += "    AND t3.att_cdh = 'MP0008' "
    query5 += "    AND t3.att_cdd = '20'  "
    query5 += "    ), '%')  "
    print(query5)
    cursor.execute(query5)  

    #지역 업로드
    query5  = " update service20_mp_mtr "
    query5 += "    SET CSCORE6 = (SELECT IFNULL(MAX(att_val),0) "
    query5 += "                  FROM service20_mp_sub t3 "
    query5 += "  WHERE t3.mp_id   = '"+ str(val.mp_id) +"' "
    query5 += "    AND t3.att_id  = 'MP0009' "
    query5 += "    AND t3.att_cdh = 'MP0009' "
    query5 += "    AND t3.att_cdd = '10'  "
    query5 += "    ) "
    query5 += " WHERE H_ADDR LIKE CONCAT('%',  "
    query5 += "    (SELECT att_val "
    query5 += "    FROM service20_mp_sub t3 "
    query5 += "    WHERE t3.mp_id   = '"+ str(val.mp_id) +"' "
    query5 += "    AND t3.att_id  = 'MP0008' "
    query5 += "    AND t3.att_cdh = 'MP0008' "
    query5 += "    AND t3.att_cdd = '10'  "
    query5 += "    ), '%')  "
    print(query5)
    cursor.execute(query5)
    """

    #멘토스쿨 합격자 업로드
    #query_mento = f"""UPDATE service20_mp_mtr A SET ms_trn_yn = 'Y' WHERE apl_id = (SELECT apl_id from service20_mentor where apl_id = A.apl_id) AND mp_id = '{val.mp_id}'"""
    #cursor.execute(query_mento)    

    #멘토스쿨 합격자 업로드
    query_mento = f"""UPDATE service20_mp_mtr A SET ms_trn_yn = 'Y' WHERE apl_id = (SELECT apl_id from service20_mentor where apl_id = A.apl_id) and mp_id = '{val.mp_id}'"""
    cursor.execute(query_mento)    


  

    for val in queryset:
        insert_sql = "update service20_mp_mtr set "
        insert_sql += "tot_doc=(ifnull(cscore1,0)+ifnull(cscore2,0)+ifnull(cscore3,0)+ifnull(cscore4,0)+ifnull(cscore5,0)+ifnull(cscore6,0) ) "
        insert_sql += " where 1=1 "
        insert_sql += " and mp_id='"+ str(val.mp_id) +"'" 
        insert_sql += " and id='"+ str(val.id) +"'"  

        cursor.execute(insert_sql)
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

    cursor = connection.cursor()
    query_att_val = f"""SELECT att_val
           FROM service20_mp_sub t3
          WHERE t3.mp_id   = '{mp_id}'
            AND t3.att_id  = 'MS0013'
            AND t3.att_cdh = 'MS0013'
            AND t3.att_cdd = '60' """

    cursor.execute(query_att_val)
    results_att_val = namedtuplefetchall(cursor)
    att_val = results_att_val[0].att_val



    mp_mtr.objects.filter(mp_id=str(mp_id)).exclude(dept_appr_div='Y').update(doc_rslt='N') #합격이 아닌것들은 거른다

    insert_sql = "update service20_mp_mtr set "
    insert_sql += "doc_rslt='N' "
    insert_sql += " where 1=1 "
    insert_sql += " and mp_id='"+ str(mp_id) +"'" 
    insert_sql += " and dept_appr_div <> 'Y'" 

    print(insert_sql)
    cursor.execute(insert_sql)


    queryset2 = cm_cnv_scr.objects.all()    
    query = "select * from service20_mp_mtr where mp_id = '" +str(mp_id)+"' and dept_appr_div='Y'  order by ifnull(cscore1,0)+ifnull(cscore2,0)+ifnull(cscore3,0)+ifnull(cscore4,0)+ifnull(cscore5,0)+ifnull(cscore6,0) DESC"
    rank = 1
    queryset = mp_mtr.objects.raw(query)


    
    query_doc1 = "select cnt_doc_res from service20_mpgm where mp_id = '" +str(mp_id)+ "'"
    cursor.execute(query_doc1)
    results_doc1 = namedtuplefetchall(cursor)   
    #val_doc1 = results_doc1[0].cnt_doc_suc
    val_doc1 = results_doc1[0].cnt_doc_res #서류전형 예비인원(실제 없음) 실제 이 컬럼에서 데이터를 처리함.


    cursor = connection.cursor()
    mp_mtr.objects.filter(mp_id=str(mp_id)).exclude(dept_appr_div='Y').update(doc_rslt='N') #합격이 아닌것들은 거른다

    vl_cnt = 0
    for cnt in queryset:
        vl_cnt = vl_cnt + 1


    # (1) 석차를 구한다.
    for val in queryset:

        print("시작111")

        #queryset.filter(id=val.id,mp_id=val.mp_id).update(doc_rank=rank)
        insert_sql = "update service20_mp_mtr set "
        insert_sql += "doc_rank='" + str(rank) + "' "
        insert_sql += " where 1=1 "
        insert_sql += " and mp_id='"+ str(val.mp_id) +"'" 
        insert_sql += " and id='"+ str(val.id) +"'"  
        insert_sql += " and dept_appr_div = 'Y'" 

        cursor.execute(insert_sql)
        rank = rank + 1

    print("a2")
    #val_doc1 0이면 전체 합격
    if int(val_doc1) == 0:
        print(" ")
        val_doc2 = vl_cnt
        mp_mtr.objects.filter(mp_id=str(mp_id),dept_appr_div='Y').update(doc_rslt='P')
    else:
        val_doc2 = float(vl_cnt) - float(val_doc1)

    print("a3")
    i = 0
    l_doc_rslt = ''
    for val in queryset:
        if int(i) < int(val_doc2):            
            l_doc_rslt = 'P'
            #mp_mtr.objects.filter(id=val.id,mp_id=val.mp_id).update(doc_rslt='P')

        else:
            l_doc_rslt = 'N'


        

        #공통설정에 있는 10점 (디폴트) 이하인 애들은 탈락시켜야하는데....
        if att_val != None and float(att_val) != 0 :
            if float(val.tot_doc) <= float(att_val):
                if val.ms_trn_yn != 'Y':
                    l_doc_rslt = 'N'


        if not val.cscore4:
            l_doc_rslt = 'N'

        
        print("으하하")        
        print(val.apl_id)

        if val.id == '829':
            print("여기서 에러111")
            print(val.id)

        if val.cscore4 == None or int(val.cscore4) == 0:            
            l_doc_rslt = 'N'

        print("여기서 에러222")

        insert_sql = "update service20_mp_mtr set "
        insert_sql += "doc_rslt='" + l_doc_rslt + "'"
        insert_sql += " where 1=1 "
        insert_sql += " and mp_id='"+ str(val.mp_id) +"'" 
        insert_sql += " and id='"+ str(val.id) +"'"        
        insert_sql += " and dept_appr_div = 'Y'" 
        print(insert_sql) 
        cursor.execute(insert_sql)  

        #rank = rank + 1
        i= i + 1

    #val_doc2 는 전체 인원에서 cnt_doc_res 이 부분을 뺀 값이 된다.
    print("카운트")
    print("카운트2")


    message = "Ok" 
    context = {'message': message,}
    

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})



@csrf_exempt
def mpFn3(request):
    mp_id = request.GET.get('mp_id', None)  
    query = "select * from service20_mp_mtr where mp_id = '" +str(mp_id)+"' and doc_rslt = 'Y'"
    queryset = mp_mtr.objects.raw(query)

    response = HttpResponse(content_type='text/csv;encoding=UTF-8"') 
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response,encoding='euc-kr')
    writer.writerow(['대학', '학과', '학번', '이름', '성별', '성적', '어학', '봉사', '지원서', '대학','지역', '멘토스쿨이수여부', '총점', '면접팀', '면접시간', '면접장소'])

    if mp_id == None:
        users = mp_mtr.objects.all().values_list('cllg_nm', 'dept_nm', 'apl_id', 'apl_nm', 'gen', 'cscore1', 'cscore2', 'cscore3', 'cscore4', 'cscore5','cscore6', 'ms_trn_yn', 'tot_doc', 'intv_team', 'intv_dt', 'intv_part_pl')
    else:
        users = mp_mtr.objects.filter(mp_id=mp_id, doc_rslt='P').exclude(intv_team='0').values_list('cllg_nm', 'dept_nm', 'apl_id', 'apl_nm', 'gen', 'cscore1', 'cscore2', 'cscore3', 'cscore4', 'cscore5','cscore6', 'ms_trn_yn', 'tot_doc', 'intv_team', 'intv_dt', 'intv_part_pl')

    for user in users:
        writer.writerow(user)
    return response




#면접 구성
@csrf_exempt
def mpFn4(request):

    print("aaabbb")
    mp_id = request.GET.get('mp_id', None)
    cursor = connection.cursor()
    print("aa1")
    query_a = "select intv_dt from service20_mpgm where mp_id = '"+ mp_id + "'"
    cursor.execute(query_a)
    results_a = namedtuplefetchall(cursor)  

    #query_b = "select * from service20_mp_mtr where doc_rslt = 'P' and mp_id = '"+ mp_id + "' order by id"
    query_b = "select * from service20_mp_mtr a WHERE a.doc_rslt = 'P' AND a.mp_id = '"+ mp_id + "' and not EXISTS (SELECT * from service20_mentor c WHERE c.apl_id = a.apl_id ) order BY a.id"

    query_b = f""" 
                select   *
                from     service20_mp_mtr a
                WHERE    a.doc_rslt = 'P'
                AND      a.mp_id    = '{mp_id}'
                and      not EXISTS
                         (SELECT *
                         from    service20_mentor c
                         WHERE   c.apl_id = a.apl_id
                         )
                AND a.apl_id NOT IN (SELECT apl_id from service20_mp_mtr WHERE mp_id IN  ('P190001','P190002')  and intv_rslt = 'P')
                order BY a.id
    """

    query_b = f"""
        SELECT A.* FROM (
        SELECT *
        from     service20_mp_mtr a
        WHERE    a.doc_rslt = 'P'
        AND      a.mp_id    ='{mp_id}'
        and      not EXISTS
                 (SELECT *
                 from    service20_mentor c
                 WHERE   c.apl_id = a.apl_id
                 )
        order BY a.id
        LIMIT 70, 141
        ) A
    """ 

    

    cursor.execute(query_b)
    results_b = namedtuplefetchall(cursor)  

     
    print("aa2")
    #면접 그룹 인원수
    query_01 = "select att_val, att_unit from service20_mp_sub where mp_id =  '"+ mp_id + "' and att_id = 'MS0019' and att_cdd = '01' and use_yn = 'Y'"
    cursor.execute(query_01)
    results_01 = namedtuplefetchall(cursor) 
    val_01 = results_01[0].att_val
    val_01_copy = val_01

    #면접시작시간
    query_02 = "select att_val, att_unit from service20_mp_sub where mp_id =  '"+ mp_id + "' and att_id = 'MS0019' and att_cdd = '02' and use_yn = 'Y'"
    cursor.execute(query_02)
    results_02 = namedtuplefetchall(cursor) 
    val_02 = results_02[0].att_val
    val_02_copy = val_02

    #시간 간격
    query_03 = "select att_val, att_unit from service20_mp_sub where mp_id =  '"+ mp_id + "' and att_id = 'MS0019' and att_cdd = '03' and use_yn = 'Y'"
    cursor.execute(query_03)
    results_03 = namedtuplefetchall(cursor) 
    val_03 = results_03[0].att_val

    #휴식 가능 팀수
    query_04 = "select att_val, att_unit from service20_mp_sub where mp_id =  '"+ mp_id + "' and att_id = 'MS0019' and att_cdd = '04' and use_yn = 'Y'"
    cursor.execute(query_04)
    results_04 = namedtuplefetchall(cursor) 
    val_04 = results_04[0].att_val

    #휴식 시간
    query_05 = "select att_val, att_unit from service20_mp_sub where mp_id =  '"+ mp_id + "' and att_id = 'MS0019' and att_cdd = '05' and use_yn = 'Y'"
    cursor.execute(query_05)
    results_05 = namedtuplefetchall(cursor) 
    val_05 = results_05[0].att_val

    #면접 장소
    query_06 = "select att_val, att_unit from service20_mp_sub where mp_id =  '"+ mp_id + "' and att_id = 'MS0019' and att_cdd = '06' and use_yn = 'Y'"
    cursor.execute(query_06)
    results_06 = namedtuplefetchall(cursor) 
    val_06 = results_06[0].att_val
    print("bbbb")
    
    lv_intv_team = 1 #면접번호
    lv_cnt = 1
    print("aa3")

    l_data = str(results_a[0].intv_dt) +" " + str(val_02) + ":00"
    l_data2 = datetime.datetime.strptime(l_data,"%Y-%m-%d %H:%M:%S")

    """
    insert_sql = "update service20_mp_mtr set "
    insert_sql += "intv_team='0'," 
    insert_sql += "intv_dt=null " 
    insert_sql += " where 1=1 " 
    insert_sql += " and mp_id='"+ str(mp_id) +"'" 
    cursor.execute(insert_sql)
    """

    for var in results_b:
        """
        insert_sql = "update service20_mp_mtr set "
        insert_sql += "intv_team='0'," 
        insert_sql += "intv_dt=null " 
        insert_sql += " where 1=1 " 
        insert_sql += " and id='"+ str(var.id) +"'" 
        cursor.execute(insert_sql)
        """
        
        insert_sql = "update service20_mp_mtr set "
        insert_sql += "intv_team='"+ str(lv_intv_team) +"'," 
        insert_sql += "intv_dt='"+ str(l_data2) +"'" 
        insert_sql += " where 1=1 " 
        insert_sql += " and id='"+ str(var.id) +"'" 
        cursor.execute(insert_sql)
        
        print("면접팀" + str(lv_intv_team))
        print("면접일" + str(results_a[0].intv_dt))
        print("면접시간" + str(l_data2))
        print("휴식가능" + str(val_04)) 
        #면접번호랑 카운트랑 같으면 하나 증가시켜준다
        if int(lv_cnt) == int(val_01):
            val_01 = int(val_01) + int(val_01_copy)

            #휴식시간 같으면 거시기한다
            if int(lv_intv_team) == int(val_04):
                l_data2 = l_data2 + datetime.timedelta(minutes=int(val_05))

            lv_intv_team = lv_intv_team +1

            #휴식가능 시간을 만들어준다.
            l_data2 = l_data2 + datetime.timedelta(minutes=int(val_03))
        lv_cnt = lv_cnt + 1

    message = "Ok" 
    context = {'message': message,}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

#합격자 업로드.
@csrf_exempt
def mpFn6(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(), "csv",
                                       file_name="download")
    else:
        form = UploadFileForm()
    return render(
        request,
        'popup/fileupload/upload_form_mp.html',
        {
            'form': form,
            'title': '서류평가 엑셀 업로드',
            'header': ('업로드할 엑셀파일을 넣어주세요')
        })


#합격자 업로드.
@csrf_exempt
def mpFn6_Submit(request):
    apl_id = request.GET.get('apl_id', None)
    mp_id = request.GET.get('mp_id', None)
    #print(apl_id)
    #print(ms_id)
    cursor = connection.cursor()
    insert_sql = "update service20_mp_mtr set "
    insert_sql += "doc_rslt='P' "
    insert_sql += " where 1=1" 
    insert_sql += " and mp_id='"+ mp_id +"'" 
    insert_sql += " and apl_id='"+ apl_id +"'"
    cursor.execute(insert_sql)

    message = "Ok" 
    context = {'message': message,}
    
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

#합격자 업로드.
@csrf_exempt
def mpFn6_Submit2(request):
    apl_id = request.GET.get('apl_id', None)
    mp_id = request.GET.get('mp_id', None)

    cursor = connection.cursor()
    insert_sql = "update service20_mp_mtr set "
    insert_sql += "doc_rslt='N' "
    insert_sql += " where doc_rslt<>'P'" 
    insert_sql += " and mp_id='"+ mp_id +"'" 

    cursor.execute(insert_sql)

    message = "Ok" 
    context = {'message': message,}
    
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})



#합격자 업로드.
@csrf_exempt
def mpFn7(request): 
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(), "csv",
                                       file_name="download")
    else:
        form = UploadFileForm()
    return render(
        request,
        'popup/fileupload/upload_form2_mp.html',
        {
            'form': form,
            'title': '서류평가 엑셀 업로드',
            'header': ('업로드할 엑셀파일을 넣어주세요')
        })


#최종 합격자 업로드.
@csrf_exempt
def mpFn7_Submit(request):
    apl_id = request.GET.get('apl_id', None)
    mp_id = request.GET.get('mp_id', None)
    #print(apl_id)
    #print(ms_id)
    cursor = connection.cursor()

    #멘토 ID
    query_01 = "select CONCAT('M',substr(DATE_FORMAT(now(), '%Y'),3,2),(select ifnull(lpad(max(right(mntr_id,2)) + 1,4,0),'0001')   from service20_mentor where substr(mntr_id,2,2)  = substr(DATE_FORMAT(now(), '%Y'),3,2))) as id from dual"
    cursor.execute(query_01)
    results_01 = namedtuplefetchall(cursor) 
    val_01 = results_01[0].id

    
    insert_sql = "update service20_mp_mtr set "
    insert_sql += "fnl_rslt='P' "
    insert_sql += " where 1=1" 
    insert_sql += " and mp_id='"+ str(ms_id) +"'" 
    insert_sql += " and mntr_id='"+ str(results_01[0].id) +"'" 
    insert_sql += " and mntr_dt=now()"

    cursor.execute(insert_sql)

    message = "Ok" 
    context = {'message': message,}
    
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


#지원서 평가  업로드.
@csrf_exempt
def mpFn9(request): 
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(), "csv",
                                       file_name="download")
    else:
        form = UploadFileForm()
    return render(
        request,
        'popup/fileupload/upload_form3_mp.html',
        {
            'form': form,
            'title': '지원서 평가 엑셀 업로드',
            'header': ('업로드할 엑셀파일을 넣어주세요')
        })





#지원서 평가  업로드 확인버튼
@csrf_exempt
def mpFn9_Submit(request):
    apl_id = request.GET.get('apl_id', None)
    mp_id = request.GET.get('mp_id', None)
    pro_id = request.GET.get('pro_id', None)
    item_cd = request.GET.get('item_cd', None)
    score = request.GET.get('score', None)
    cursor = connection.cursor()

    mp_mtr.objects.filter(apl_id=apl_id,mp_id=mp_id).update(dept_appr_div='Y')

    print("aa1")
    l_apl_no_query = "select apl_no FROM service20_mp_mtr WHERE mp_id = '"+ str(mp_id) +"' AND apl_id = '"+ str(apl_id) +"'"
    print(l_apl_no_query)
    cursor.execute(l_apl_no_query)
    results = namedtuplefetchall(cursor)    
    l_apl_no = results[0].apl_no

    print("aa2")
    l_com_cdd_query = "select sort_seq_no,std_detl_code_nm FROM service20_com_cdd WHERE std_grp_code = 'MS0015' AND std_detl_code = '"+ str(item_cd) +"'"
    print(l_com_cdd_query)
    cursor.execute(l_com_cdd_query)
    results = namedtuplefetchall(cursor)    
    l_sort_seq_no = results[0].sort_seq_no
    
    
    print("aa3")
    l_mp_sub_query = "select att_cdd,att_unit,att_val FROM service20_mp_sub WHERE  mp_id = '"+ str(mp_id) +"' and att_cdh = 'MS0016' AND att_val ='"+ str(pro_id) +"'"
    print(l_mp_sub_query)
    cursor.execute(l_mp_sub_query)
    results = namedtuplefetchall(cursor)    
    l_mrk_no = results[0].att_cdd
    l_mrk_nm = results[0].att_unit



    l_mp_sub_query = "select att_cdd,att_unit,att_val FROM service20_mp_sub WHERE  mp_id = '"+ str(mp_id) +"' and att_cdh = 'MS0015' AND att_cdd ='"+ str(item_cd) +"'"
    print(l_mp_sub_query)
    cursor.execute(l_mp_sub_query)
    results = namedtuplefetchall(cursor)    
    l_item_nm = results[0].att_val
    l_att_cdd = results[0].att_cdd

    print("aa4")
    
    #print(apl_id)
    #print(ms_id)


    print("아이템")
    print(item_cd)
    if item_cd =='06':
        insert_sql = f"""delete from service20_mp_mrk_h where  mp_id = '{mp_id}' and test_div = '10' and apl_no = '{l_apl_no}' and mrk_seq = '8' and mrk_no = '{l_mrk_no}' """

        print(insert_sql)
        cursor.execute(insert_sql)      
        insert_sql = f"""insert into service20_mp_mrk_h (mp_id, test_div, apl_no, mrk_seq, mrk_no, mrk_id, mak_nm, grade) 
                         select '{mp_id}'
                               ,'10'
                               ,'{l_apl_no}' 
                               ,'8' 
                               ,'{l_mrk_no}'
                               ,'{pro_id}'
                               ,'{l_mrk_nm}'
                               ,'{score}'
                         from dual
        """
        print(insert_sql)
        cursor.execute(insert_sql)      
    elif item_cd =='07':
        insert_sql = f"""update service20_mp_mrk_h set tot_score  = '{score}' where mp_id = '{mp_id}' and test_div = '10' and apl_no = '{l_apl_no}' and mrk_seq = '8' and mrk_no = '{l_mrk_no}' 
        """
        print(insert_sql)
        cursor.execute(insert_sql)  
    else:

        insert_sql = "delete from service20_mp_mrk where  mp_id = '" + str(mp_id) + "' and test_div = '10' and apl_no = '"+ str(l_apl_no) + "' and mrk_seq = '" + str(l_sort_seq_no) + "' and item_cd = '" + str(item_cd) + "' and mrk_no = '" + str(l_mrk_no) + "'"
        print(insert_sql)
        cursor.execute(insert_sql)      

        insert_sql = "insert into service20_mp_mrk (mp_id, test_div, apl_no, mrk_seq, mrk_no, mrk_id, mak_nm, score, item_cd, item_nm) "
        insert_sql += "select '" + str(mp_id) + "'," 
        insert_sql += "'10'," 
        insert_sql += "'" + str(l_apl_no)  +"'," 
        insert_sql += "'" + str(l_sort_seq_no)  +"',"
        insert_sql += "'" + str(l_mrk_no)  +"',"
        insert_sql += "'" + str(pro_id)  +"',"  
        insert_sql += "'" + str(l_mrk_nm)  +"',"    
        insert_sql += "'" + str(score)  +"',"
        insert_sql += "'" + str(item_cd)  +"',"
        insert_sql += "'" + str(l_item_nm)  +"'"
        insert_sql += "from dual" 
        print(insert_sql)
    


    print("aa5")

    message = "Ok" 
    context = {'message': message,}
    
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

#가선점 평가  업로드.
@csrf_exempt
def mpFn10(request): 
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            return excel.make_response(filehandle.get_sheet(), "csv",
                                       file_name="download")
    else:
        form = UploadFileForm()
    return render(
        request,
        'popup/fileupload/upload_form4_mp.html',
        {
            'form': form,
            'title': '가산점 평가 엑셀 업로드',
            'header': ('업로드할 엑셀파일을 넣어주세요')
        })

#가산점 평가  업로드 확인버튼
@csrf_exempt
def mpFn10_Submit(request):
    apl_id = request.GET.get('apl_id', None)
    mp_id = request.GET.get('mp_id', None)
    score = request.GET.get('score', None)
    item_cd = request.GET.get('item_cd', None)
    
    cursor = connection.cursor()

    print(item_cd)

    if score != None:
        if item_cd=='01':
                print("01")
                insert_sql = f"""update service20_mp_mtr set cscore5 = '0' where mp_id = '{mp_id}' and apl_id = '{apl_id}'""" 
                cursor.execute(insert_sql)                              
                insert_sql = f"""update service20_mp_mtr set cscore5 = '{score}' where mp_id = '{mp_id}' and apl_id = '{apl_id}'""" 
                cursor.execute(insert_sql)
        elif item_cd=='02':
                print("02")
                insert_sql = f"""update service20_mp_mtr set cscore6 = '0' where mp_id = '{mp_id}' and apl_id = '{apl_id}'""" 
                print(insert_sql)               
                insert_sql = f"""update service20_mp_mtr set cscore6 = '{score}' where mp_id = '{mp_id}' and apl_id = '{apl_id}'""" 
                print(insert_sql)
                cursor.execute(insert_sql)          


    message = "Ok" 
    context = {'message': message,}
    
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})   



@csrf_exempt
def mpPop1(request):
    posts = None
    return render(request, 'popup/mento/mpPop1.html', { 'posts': posts })




class mpPop1_Det1Serializer(serializers.ModelSerializer):
    class Meta:
        model = mp_mtr
        #fields = ('mp_id','apl_no','mntr_id','indv_div','team_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','bank_acct','bank_cd','bank_nm','bank_dpsr','cnt_mp_a','cnt_mp_p','cnt_mp_c','cnt_mp_g','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm')        
        fields = '__all__'
        #fields = ('mp_id','apl_no','mntr_id','indv_div','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr')

class mpPop1_Det1(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = mpPop1_Det1Serializer
    print("aaa")
    def list(self, request):
        print("시작1")
        mp_id = request.GET.get('mp_id', None)
        apl_id = request.GET.get('apl_id', None)
        print("시작2")
        print(mp_id)
        print(apl_id)



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
    vm_nanum_flag = vw_nanum_stdt.objects.filter(apl_id=apl_id).exists()

    if not vm_nanum_flag:
        print("FFF")
        message = "Fail"
        context = {'message': message}
        print("aaaa")
    else:
        message = "Ok"
        rows = vw_nanum_stdt.objects.filter(apl_id=apl_id)[0]
        print("bbb")
        print(rows)
        context = {'message': message,
                    'apl_nm' : rows.apl_nm,
                    'univ_cd' : rows.unv_cd,
                    'univ_nm' : rows.unv_nm,
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
                    'stdt_div' : rows.stds_div,
                    'stdt_nm' : rows.stds_nm, 
                    'mob_nm' : rows.mob_no,
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
                    'score05' : rows.score05,
                    'dept_chr_id' : rows.dept_chr_id
                    }
    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


#멘토링 핍압1_조회3_채점자 교수 조회
class mpPop1_Det3Serializer(serializers.ModelSerializer):
    class Meta:
        model =mp_sub
        fields = ('mp_id','att_id','att_seq','att_cdh','att_cdd','att_val','att_unit','use_yn','sort_seq')        

class mpPop1_Det3(generics.ListAPIView):

    queryset = mp_sub.objects.all()
    serializer_class = mpPop1_Det3Serializer
    def list(self, request):
        mp_id = request.GET.get('mp_id', None)
        print("aaa1")
        print(mp_id)
        query = "select * from service20_mp_sub where mp_id='"+str(mp_id)+"' and att_id = 'MS0016' and use_yn = 'Y' order by sort_seq"
        print(query)
        print("a333")
        queryset = mp_sub.objects.raw(query)        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)  



#멘토링 핍압1_조회4_채점자 교수 조회
class mpPop1_Det4Serializer(serializers.ModelSerializer):
    nm = serializers.SerializerMethodField()
    class Meta:
        model =mp_sub
        fields = ('mp_id','att_id','att_seq','att_cdh','att_cdd','att_val','att_unit','use_yn','sort_seq','nm')        

    def get_nm(self,obj):
        return obj.nm


class mpPop1_Det4(generics.ListAPIView):
    queryset = mp_sub.objects.all()
    serializer_class = mpPop1_Det4Serializer
    def list(self, request):
        mp_id = request.GET.get('mp_id', None)
        print("aaa1")
        print(mp_id) 
        #query = "select * from service20_mp_sub where mp_id='"+mp_id+"' and att_id = 'MS0016' and use_yn = 'Y' order by sort_seq"
        query = "select (Select std_detl_code_nm from service20_com_cdd B where B.std_grp_code = A.att_id and B.std_detl_code = A.att_cdd) as nm, A.*   from service20_mp_sub A where A.att_id = 'MS0015' and A.mp_id ='"+mp_id+"' and use_yn = 'Y' order by sort_seq"
        print(query)
        print("a333")
        queryset = mp_sub.objects.raw(query)        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)  


#멘토스쿨 핍압1_조회5_채점 조회
class mpPop1_Det5Serializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    class Meta:
        model =mp_sub
        fields = ('mp_id','att_id','att_seq','att_cdh','att_cdd','att_val','att_unit','use_yn','sort_seq','score')        

    def get_score(self,obj):
        return obj.score

class mpPop1_Det5(generics.ListAPIView):
    queryset = mp_sub.objects.all()
    serializer_class = mpPop1_Det5Serializer
    def list(self, request):
        mp_id = request.GET.get('mp_id', None)
        apl_no = request.GET.get('user_id', None)
        att_cdd_id = request.GET.get('att_cdd_id', None)
        nm_id = request.GET.get('nm_id', None)

        query = "select A.*, B.* from   service20_mp_sub A left outer join service20_mp_mrk B on     A.mp_id   = B.mp_id and    A.att_cdd = B.mrk_id where  A.att_id   = 'MS0016' and    B.apl_no         = '" + apl_no +"' and    A.att_cdd        = '"+att_cdd_id+"' and    B.item_cd = '"+nm_id+"' order by item_cd"
        
        print(query)
        queryset = mp_sub.objects.raw(query)        
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)    




@csrf_exempt
def mpPop1_Det5_Save(request):
    mp_id = request.GET.get('mp_id', None)  
    test_div = request.GET.get('test_div', None)  
    
    apl_no = request.GET.get('apl_no', None)
    mrk_id = request.GET.get('mrk_id', None)
    mrk_nm = request.GET.get('mrk_nm', None)
    score = request.GET.get('score', None)
    item_cd = request.GET.get('item_cd', None)
    item_nm = request.GET.get('item_nm', None)

    mrk_seq = request.GET.get('mrk_seq', None)
    mrk_no = request.GET.get('mrk_no', None)

    cursor = connection.cursor()
    query = "select count(1) as cnt  from service20_mp_mrk  where apl_no ='"+ str(apl_no) +"' and mp_id='"+ str(mp_id) +"' and mrk_id = '" + str(mrk_id) + "' and item_cd = '" + str(item_cd) + "' and test_div = '" + str(test_div) +   "' and mrk_seq = '" + str(mrk_seq) +    "' and mrk_no = '" + str(mrk_no) +   "' "
    print(query)
    cursor.execute(query)
    results = namedtuplefetchall(cursor)    
    num = results[0].cnt


    if num > 0:
        print("건수가 있음")
        if score == '':
            score = '0'

        insert_sql = "update service20_mp_mrk set "

        insert_sql += "score='"+ score +"'," 
        insert_sql += "item_cd='"+ item_cd +"'," 
        insert_sql += "item_nm='"+ item_nm +"'" 

        insert_sql += " where 1=1" 
        insert_sql += " and mp_id='"+ mp_id +"'" 
        insert_sql += " and test_div='"+ test_div +"'" 
        insert_sql += " and apl_no='"+ apl_no +"'" 
        insert_sql += " and mrk_seq='"+ mrk_seq +"'" 
        insert_sql += " and mrk_no='"+ mrk_no +"'" 
        insert_sql += " and mrk_id='"+ mrk_id +"'" 
        print(insert_sql)
        cursor.execute(insert_sql)


    else:
        
        print("건수가 없음")
        
        if score == None:
            score = '0'
        elif score == '':
            score = '0'

        insert_sql = "insert into service20_mp_mrk (mp_id, test_div, apl_no, mrk_seq, mrk_no, mrk_id, mak_nm, score, item_cd, item_nm)"
        insert_sql += "values("
        insert_sql += "'"+ mp_id +"'," 
        insert_sql += "'10'," 
        insert_sql += "'"+ apl_no +"'," 
        insert_sql += "'"+ mrk_seq +"',"  #mrk_id
        insert_sql += "'"+ mrk_no +"',"  #mrk_id
        insert_sql += "'"+ mrk_id +"',"  #mrk_id
        insert_sql += "'"+ mrk_nm +"',"  #mrk_nm
        insert_sql += "'"+ score +"',"  #score
        insert_sql += "'"+ item_cd +"',"  #item_cd
        insert_sql += "'"+ item_nm +"')"  #item_nm
        #print(insert_sql)

        cursor.execute(insert_sql)
        

    message = "Ok" 
    context = {'message': message,}


    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


#멘토링 리포트보기.
@csrf_exempt
def mpFn8(request):
    context = None
    return render(
        request,
        #'report/reportProgram.html',
        'report/choice.html',
        context)

#멘토링 리포트보기.
@csrf_exempt
def mpFn8_2(request):
    context = None
    return render(
        request,
        'report/reportProgram.html',
        #'report/choice.html',
        context)    

#멘토링 리포트보기.
@csrf_exempt
def mpFn8_assist(request):
    context = None
    return render(
        request,
        'report/reportProgram_assistant.html',
        #'report/choice.html',
        context)



#학과장 일괄승인하기
@csrf_exempt
def mpFn8_assist_confirm_all(request):
    cursor = connection.cursor()
    key = request.GET.get('key', None)
    mp_id = request.GET.get('mp_id', None)

    login_id = request.session.get('user_id')

    query2 = f'''
        SELECT * from service20_dept_ast where ast_id = '{login_id}' or dean_emp_id = '{login_id}'
    ''' 
    queryset = dept_ast.objects.raw(query2)
    dept_cd = ''
    for q in queryset:
        dept_cd = q.dept_cd
        dean_emp_id = q.dean_emp_id
        dean_emp_nm = q.dean_emp_nm
        ast_id = q.ast_id
        ast_nm = q.ast_nm


    insert_sql = f"""update service20_mp_mtr set 
                              dept_appr_div = 'Y',
                              dept_chr_id = '{dean_emp_id}', 
                              dept_chr_nm = '{dean_emp_nm}', 
                              ast_id = '{ast_id}',
                              ast_nm = '{ast_nm}',
                              dept_retn_rsn = '', 
                              dept_appr_dt = DATE_FORMAT(now(),'%Y%m%d') 
                      where  dept_cd = '{dept_cd}'
                        and  id = '{key}'
                      """ 
    print(insert_sql)
    cursor.execute(insert_sql)

    message = "Ok" 
    context = {'message': message,}
    
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})   



#학과장 승인하기
@csrf_exempt
def mpFn8_assist_confirm(request):
    cursor = connection.cursor()
    apl_id = request.GET.get('apl_id', None)
    mp_id = request.GET.get('mp_id', None)

    login_id = request.session.get('user_id')

    query2 = f'''
        SELECT * from service20_dept_ast where ast_id = '{login_id}' or dean_emp_id = '{login_id}'
    ''' 
    queryset = dept_ast.objects.raw(query2)
    dept_cd = ''
    for q in queryset:
        dept_cd = q.dept_cd
        dean_emp_id = q.dean_emp_id
        dean_emp_nm = q.dean_emp_nm
        ast_id = q.ast_id
        ast_nm = q.ast_nm



    insert_sql = f"""update service20_mp_mtr set 
                              dept_appr_div = 'Y',
                              dept_chr_id = '{dean_emp_id}', 
                              dept_chr_nm = '{dean_emp_nm}', 
                              ast_id = '{ast_id}',
                              ast_nm = '{ast_nm}',
                              dept_retn_rsn = '', 
                              dept_appr_dt = DATE_FORMAT(now(),'%Y%m%d') 

                      where  dept_cd = '{dept_cd}' 
                       and apl_id = '{apl_id}' """

    #insert_sql = f"""update service20_mp_mtr set dept_appr_div = 'Y',dept_retn_rsn = '', dept_appr_dt = DATE_FORMAT(now(),'%Y%m%d') where mp_id = '{mp_id}' and apl_id = '{apl_id}'""" 

    cursor.execute(insert_sql)

    message = "Ok" 
    context = {'message': message,}
    
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})   

#학과장 반려
@csrf_exempt
def mpFn8_assist_cancle(request):
    cursor = connection.cursor()
    apl_id = request.GET.get('apl_id', None)
    mp_id = request.GET.get('mp_id', None)
    content = request.GET.get('content', None)

    insert_sql = f"""update service20_mp_mtr set 
                            dept_appr_div = 'N', 
                            dept_appr_dt = '',
                            dept_chr_id = '',
                            dept_chr_nm = '',
                            ast_id = '',
                            ast_nm = ''
                     where mp_id = '{mp_id}' and apl_id = '{apl_id}'""" 
    cursor.execute(insert_sql)

    message = "Ok" 
    context = {'message': message,} 
    
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})   


#면접 관리자 코멘트
@csrf_exempt
def mpFn8_gabu(request):
    cursor = connection.cursor()
    apl_id = request.GET.get('apl_id', None)
    mp_id = request.GET.get('mp_id', None)
    content = request.GET.get('commnet', None)
    intv_rslt = request.GET.get('gabu',None)

    insert_sql = f"""update service20_mp_mtr set 
                            intv_cmt = '{content}'
                     where mp_id = '{mp_id}' and apl_id = '{apl_id}'""" 

    print(insert_sql)
    
    cursor.execute(insert_sql)

    message = "Ok" 
    context = {'message': message,} 
    
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

#면접 심사위원 가부 및 코멘트
@csrf_exempt
def mpFn8_gabu2(request):
    cursor = connection.cursor()
    apl_id = request.GET.get('apl_id', None)
    mp_id = request.GET.get('mp_id', None)
    content = request.GET.get('commnet', None)
    intv_rslt = request.GET.get('gabu',None)
    pro_id = request.GET.get('pro_id',None)


    l_apl_no_query = f"""select apl_no FROM service20_mp_mtr WHERE mp_id = '{mp_id}' AND apl_id = '{apl_id}'"""

    print(l_apl_no_query)
    cursor.execute(l_apl_no_query)
    results = namedtuplefetchall(cursor)    
    l_apl_no = results[0].apl_no

    l_mp_sub_query = f""" SELECT * FROM service20_mp_sub WHERE mp_id = '{mp_id}' AND att_cdh = 'MS0020' and att_val = '{pro_id}'"""
    print(l_mp_sub_query)
    cursor.execute(l_mp_sub_query)
    results = namedtuplefetchall(cursor)    
    l_mrk_no = results[0].att_val
    l_mrk_nm = results[0].att_unit


    insert_sql = f"""delete from service20_mp_mrk where  mp_id = '{mp_id}' and test_div = '20' and apl_no = '{l_apl_no}' and mrk_id = '{pro_id}'"""
    print(insert_sql)
    cursor.execute(insert_sql)      

    insert_sql = f"""insert into service20_mp_mrk (mp_id, test_div, apl_no, mrk_seq, mrk_no, mrk_id, mak_nm, score, item_cd, item_nm,mrk_cmt) 
                     select '{mp_id}' ,
                            '20',
                            '{l_apl_no}',
                            '1',
                            (SELECT ifnull(max(mrk_no),0) + 1 from service20_mp_mrk a where a.mp_id = mp_id and a.test_div = '20' and a.apl_no = apl_no and a.mrk_seq = mrk_seq),
                            '{l_mrk_no}',
                            '{l_mrk_nm}',
                            '{intv_rslt}',
                            '10',
                            '면접',
                            '{content}'
                     from dual
                    """
    print(insert_sql)       
    
    cursor.execute(insert_sql)

    message = "Ok" 
    context = {'message': message,} 
    
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


#멘토링 리포트보기 상세 리스트
class mpFn8_Det1Serializer(serializers.ModelSerializer):

    mrkFlag = serializers.SerializerMethodField()
    mrkContent = serializers.SerializerMethodField()

    class Meta:
        model = mp_mtr
        fields = ('mp_id','apl_no','mntr_id','indv_div','team_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','bank_acct','bank_cd','bank_nm','bank_dpsr','cnt_mp_a','cnt_mp_p','cnt_mp_c','cnt_mp_g','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','fnl_rslt','acpt_dt','acpt_div','acpt_cncl_rsn','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','pr_yr','pr_sch_yr','pr_term_div','mrkFlag','mrkContent')    

    def get_mrkFlag(self,obj):
        return obj.mrkFlag

    def get_mrkContent(self,obj):
        return obj.mrkContent        

class mpFn8_Det1(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = mpFn8_Det1Serializer
    def list(self, request):
        mp_id = request.GET.get('mp_id', None)
        pro_id = request.GET.get('pro_id', None)

        #query_b = f"""select * from service20_mp_mtr a WHERE a.doc_rslt = 'P' AND a.mp_id = '{mp_id}' and not EXISTS (SELECT * from service20_mentor c WHERE c.apl_id = a.apl_id ) order BY a.id"""
        query_b = f"""select a.*, 
                               (SELECT score
                     FROM    service20_mp_mrk
                     WHERE   mp_id    = a.mp_id
                      AND     test_div = '20'
                      AND     apl_no   = a.apl_no
                      AND     mrk_id = '{pro_id}'
                               ) AS mrkFlag,
                               (SELECT mrk_cmt
                     FROM    service20_mp_mrk
                     WHERE   mp_id    = a.mp_id
                      AND     test_div = '20'
                      AND     apl_no   = a.apl_no
                      AND     mrk_id = '{pro_id}'
                               ) AS mrkContent                               
                      from service20_mp_mtr a WHERE a.doc_rslt = 'P' AND a.mp_id = '{mp_id}' and not EXISTS (SELECT * from service20_mentor c WHERE c.apl_id = a.apl_id ) AND (intv_team <> '0' OR intv_team IS NOT NULL)  order BY a.id"""
        
        queryset = mp_mtr.objects.raw(query_b)
        #queryset = self.get_queryset()
        #queryset = queryset.filter(mp_id=mp_id)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)  


#심사위원 상세 리스트
class mpFn8_Det2Serializer(serializers.ModelSerializer):
    class Meta:
        model = mp_sub
        fields = '__all__'       

class mpFn8_Det2(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = mpFn8_Det2Serializer
    def list(self, request):
        mp_id = request.GET.get('mp_id', None)


        #query_b = f"""select * from service20_mp_mtr a WHERE a.doc_rslt = 'P' AND a.mp_id = '{mp_id}' and not EXISTS (SELECT * from service20_mentor c WHERE c.apl_id = a.apl_id ) order BY a.id"""  
        query = f"""SELECT * from service20_mp_sub WHERE att_id = 'MS0020' AND mp_id = '{mp_id}'"""

        queryset = mp_sub.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)          


#MP_MTR 전체 보기
class mpFn8_Det3Serializer(serializers.ModelSerializer):
    class Meta:
        model = mp_mtr
        fields = '__all__'       

class mpFn8_Det3(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = mpFn8_Det3Serializer
    def list(self, request):
        mp_id = request.GET.get('mp_id', None)
        apl_id = request.GET.get('apl_id', None)

        print("aa")
        print("bb")


        query_b = f"""select * from service20_mp_mtr a WHERE  a.mp_id = '{mp_id}' and a.apl_id = '{apl_id}' order BY a.id"""

        
        queryset = mp_mtr.objects.raw(query_b)
        #queryset = self.get_queryset()
        #queryset = queryset.filter(mp_id=mp_id)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)  



@csrf_exempt
def sms(request):

    vlSelectNo = request.POST.get('_selected_action')
    vlSelectVar = request.POST.getlist('_selected_action')

    posts = None
    return render(request, 'popup/sms/sms.html', { 'posts': posts })


@csrf_exempt
def sms_result(request):
    vlSelectNo = request.GET.get('id')
    vlFlag = request.GET.get('flag')
    ms_id = ''
    apl_no = ''

    if vlFlag == 'mp':
        cursor = connection.cursor()
        query_b = "select mp_id, apl_no,ms_trn_yn from service20_mp_mtr where id = '"+ vlSelectNo +"'"
        print(query_b)
        cursor.execute(query_b)
        results_b = namedtuplefetchall(cursor)  
        ms_id = results_b[0].mp_id
        apl_no = results_b[0].apl_no

        ms_trn_yn = results_b[0].ms_trn_yn


        print("A1")

        if ms_trn_yn == 'Y' :
            query =  f"""SELECT CASE A.DOC_RSLT WHEN 'P' THEN   CONCAT(   A.APL_NM, '님 ', CHAR(10)
                                               , (SELECT MP_NAME 
                                               FROM service20_mpgm B
                                              WHERE B.MP_ID    = '{ms_id}'), ' 선발 면접 및 멘토스쿨 이수 대상에서 제외됩니다.', CHAR(10),
                                          '최종 합격발표는 3월 25일 전후 예정입니다.'
                                          )
                                 WHEN 'N' THEN    CONCAT(   A.APL_NM, '님', CHAR(10)
                                          , (SELECT MP_NAME
                                               FROM service20_mpgm B
                                              WHERE B.MP_ID    = '{ms_id}'), ' 서류젼형에 불합격 했습니다.', CHAR(10)
                                          , '다음 기회에 도전 부탁드립니다.' )
                                 ELSE 'NO MESSAGE' END MSG
                          FROM service20_mp_mtr A
                         WHERE A.MP_ID    = '{ms_id}'
                           AND A.APL_NO   = '{apl_no}'"""
        else:


            query =  f"""SELECT CASE A.DOC_RSLT WHEN 'P' THEN   CONCAT(   A.APL_NM, '님 ', CHAR(10)
                                               , (SELECT MP_NAME 
                                               FROM service20_mpgm B
                                              WHERE B.MP_ID    = '{ms_id}'), ' 서류젼형 합격을 축하합니다.', CHAR(10)
                                          , '면접 일시 : ', SUBSTRING(A.INTV_DT, 1, 16), '(', A.INTV_TEAM, '팀)', CHAR(10)
                                          , '장소 :',    (SELECT B.ATT_VAL
                                                  FROM service20_mp_sub B
                                                  WHERE B.MP_ID  = A.MP_ID
                                                   AND B.ATT_ID = 'MS0019' 
                                                   AND B.ATT_CDH = 'MS0019'
                                                   AND B.ATT_CDD = '06'), CHAR(10)
                                          , '면접시간 15분전 대기 바랍니다.' )
                                 WHEN 'N' THEN    CONCAT(   A.APL_NM, '님', CHAR(10)
                                          , (SELECT MP_NAME
                                               FROM service20_mpgm B
                                              WHERE B.MP_ID    = '{ms_id}'), ' 서류젼형에 불합격 했습니다.', CHAR(10)
                                          , '다음 기회에 도전 부탁드립니다.' )
                                 ELSE 'NO MESSAGE' END MSG
                          FROM service20_mp_mtr A
                         WHERE A.MP_ID    = '{ms_id}'
                           AND A.APL_NO   = '{apl_no}'"""

        
        print(query)

        
        cursor.execute(query)
        results = namedtuplefetchall(cursor)    
        msg = results[0].MSG



        print(msg)
        message = "Ok"
        context = {'message': message,
                         'msg' : msg,
        }
        return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

    else:

        cursor = connection.cursor()
        query_b = "select ms_id, apl_no from service20_ms_apl where id = '"+ vlSelectNo +"'"
        print(query_b)
        cursor.execute(query_b)
        results_b = namedtuplefetchall(cursor)  
        ms_id = results_b[0].ms_id
        apl_no = results_b[0].apl_no

        print("시작111")
        print(apl_no)

        query =  f"""SELECT CASE A.DOC_RSLT WHEN 'P' THEN   CONCAT(   A.APL_NM, '님 ', CHAR(10)
                                           , (SELECT MP_NAME 
                                           FROM service20_mpgm B
                                          WHERE B.MP_ID    = '{ms_id}'), ' 서류젼형 합격을 축하합니다.', CHAR(10)
                                      , '면접 일시 : ', SUBSTRING(A.INTV_DT, 1, 16), '(', A.INTV_TEAM, '팀)', CHAR(10)
                                      , '장소 :',    (SELECT B.ATT_VAL
                                              FROM service20_mp_sub B
                                              WHERE B.MP_ID  = A.MP_ID
                                               AND B.ATT_ID = 'MS0019' 
                                               AND B.ATT_CDH = 'MS0019'
                                               AND B.ATT_CDD = '06'), CHAR(10)
                                      , '면접시간 15분전 대기 바랍니다.' )
                             WHEN 'N' THEN    CONCAT(   A.APL_NM, '님', CHAR(10)
                                      , (SELECT MP_NAME
                                           FROM service20_mpgm B
                                          WHERE B.MP_ID    = '{ms_id}'), ' 서류젼형에 불합격 했습니다.', CHAR(10)
                                      , '다음 기회에 도전 부탁드립니다.' )
                             ELSE 'NO MESSAGE' END MSG
                      FROM service20_mp_mtr A
                     WHERE A.MP_ID    = '{ms_id}'
                       AND A.APL_NO   = '{apl_no}'"""

        
        print(query)

        
        cursor.execute(query)
        results = namedtuplefetchall(cursor)    
        msg = results[0].MSG


        print(msg)
        message = "Ok"
        context = {'message': message,
                         'msg' : msg,
        }
        return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

@csrf_exempt
def sms_send(request):


    print('문자문자문자111')
    key = request.GET.get('key')
    method = request.GET.get('method')
    msg = request.GET.get('msg')
    print('문자문자문자222')
    queryset = mp_mtr.objects.all()
    queryset = queryset.filter(id=key)[0]

    print('문자문자문자333')
    print(queryset.apl_id)
    push_userid = queryset.apl_id
    login_id = request.session.get('user_id')

    if login_id == 'admin':
        login_id = '515440'


    user_id = login_id

    print('문자문자문자222')
    print(user_id)

    push_chk = 'S'
    push_userid = push_userid
    #push_userid = '515440'
    push_title = '부산대학교 나눔입니다'
    push_content = msg
    tickerText = ' '
    push_time = '60'
    cdr_id = login_id
    sms_content = push_content
    sms_nb = '0515103322'
    client_ip = request.META['REMOTE_ADDR']
    data_info = {'user_id':user_id,'push_chk': push_chk,'push_userid': push_userid,'push_title': push_title,'push_content': push_content,'tickerText': tickerText,'push_time': push_time,'cdr_id': cdr_id,'sms_content': sms_content,'sms_nb': sms_nb}
    #print(data_info)
    with requests.Session() as s:
        first_page = s.post('http://msg.pusan.ac.kr/api/push.asp', data=data_info)
        html = first_page.text
        print(html)
        soup = bs(html, 'html.parser')

    message = html
    context = {'message': message
    }
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})



#학과장 조교한테 승인 push 날리는 부분
@csrf_exempt
def sms_send_assist(request):
    key = request.GET.get('key')
    method = request.GET.get('method')
    msg = request.GET.get('msg')

    queryset = mp_mtr.objects.all()
    #queryset = queryset.filter(id=key)[0]

    #print(queryset.apl_id)
    #push_userid = queryset.apl_id
    login_id = request.session.get('user_id', 'admin')

    if login_id == 'admin':
        login_id = '515440'


    user_id = login_id
    push_chk = 'PO'
    push_userid = '515440'
    #push_userid = '515440'
    push_title = '멘토링 지원서 학과장 승인 요청.'
    push_content = '멘토링 지원서 학과장 승인 요청.'
    tickerText = ' '
    push_time = '60'
    cdr_id = '515440'
    sms_content = push_content
    sms_nb = '0515103322'
    client_ip = request.META['REMOTE_ADDR']
    data_info = {'user_id':user_id,'push_chk': push_chk,'push_userid': push_userid,'push_title': push_title,'push_content': push_content,'tickerText': tickerText,'push_time': push_time,'cdr_id': cdr_id,'sms_content': sms_content,'sms_nb': sms_nb}
    #print(data_info)
    with requests.Session() as s:
        first_page = s.post('http://msg.pusan.ac.kr/api/push.asp', data=data_info)
        html = first_page.text
        #print(html)
        soup = bs(html, 'html.parser')

    message = "Ok"
    context = {'message': message
    }
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})




@csrf_exempt
def returnsso(request,response):
        message = "Ok"
        context = {'message': message,
    
        }
        return JsonResponse(context,json_dumps_params={'ensure_ascii': True})





@csrf_exempt
def mssql(request):
    vlSelectNo = request.GET.get('id')
    vlFlag = request.GET.get('flag')
    # MSSQL 접속
    conn = pymssql.connect(server='192.168.2.124', user='nanum', password='n@num*!@', database='hakjuk', port='1221')
    
    print("aaaaaaaaaaa1")
    cursor = conn.cursor()
    print("aaaaaaaaaaa22")

    query = "select apl_id,pr_yr,pr_sch_yr,pr_term_div from WM_HANUM_STDT where apl_id = '201470117'"

    cursor.execute(query)  
    
    print("aaaaaaaaaaaa33")
    row = cursor.fetchone()  
    print(row)
    message = 'Fail'
    i = 0
    while row:
        message = str(row) + str(row[0])  + " " + str(row[1])  +  " " + str(row[2])  +  " " + str(row[3])  
        row = cursor.fetchone() 
        i = i + 1

    context = {'message': message
                    
    }
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


@csrf_exempt
def mssql2(request):
    vlSelectNo = request.GET.get('id')
    vlFlag = request.GET.get('flag')
    # MSSQL 접속
    #conn = pymssql.connect(server='192.168.2.124', user='nanum', password='n@num*!@', database='HAKJUK', port='1221')
    print("a0")
    conn =  pyodbc.connect('driver={ODBC Driver 17 for SQL Server};server=192.168.2.124;database=HAKJUK;uid=nanum;pwd=n@num*!@,port=1221')

    print("a1")
    cursor = conn.cursor()
    print("a2")
    cursor.execute("select apl_id from WM_HANUM_STDT where apl_id = '201678120'")  
    print("a3")
    row = cursor.fetchone()  
    while row:
        print(str(row[0]) + " " + str(row[1]) + " " + str(row[2]))
        row = cursor.fetchone() 
    message = "Ok"
    context = {'message': message
                    
    }
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


@csrf_exempt
def mssql_export(request):
    vlSelectNo = request.GET.get('id')
    vlFlag = request.GET.get('flag')
    # MSSQL 접속


    conn = pymssql.connect(server='192.168.2.124', user='nanum', password='n@num*!@', database='hakjuk', port='1221')
    cursor = conn.cursor()
    #query = "select emp_id, emp_nm, dept_cd, dept_nm, jw_cd, jw_nm, mob_no, tel_no, email_addr, if_dt from vw_nanum_dept_dean where emp_id = '" +vlSelectNo +"'"
    query = "select emp_id, emp_nm, dept_cd, dept_nm, jw_cd, jw_nm, mob_no, tel_no, email_addr, if_dt from vw_nanum_dept_dean"
    cursor.execute(query)  
    row = cursor.fetchone()  
    
    print("aaaaaaaaa")
    message = 'Fail'
    i = 0
    while row:
        message = str(row[0])  + " || " + str(row[1])  +  " || " + str(row[2])  +  " || " + str(row[3]) +  " || " + str(row[4])  +  " || " + str(row[5])  +  " || " + str(row[6])  +  " || " + str(row[7]) +  " || " + str(row[8])  +  " || " + str(row[9]) 
        insert_sql = "insert into vm_nanum_dept_dean_osh(emp_id, emp_nm, dept_cd, dept_nm, jw_cd, jw_nm, mob_no, tel_no, email_addr,if_dt)"
        insert_sql += "values("
        insert_sql += "'"+ str(row[0]) +"'," 
        insert_sql += "'"+ str(row[1]) +"'," 
        insert_sql += "'"+ str(row[2]) +"'," 
        insert_sql += "'"+ str(row[3]) +"'," 
        insert_sql += "'"+ str(row[4]) +"'," 
        insert_sql += "'"+ str(row[5]) +"'," 
        insert_sql += "'"+ str(row[6]) +"'," 
        insert_sql += "'"+ str(row[7]) +"'," 
        insert_sql += "'"+ str(row[8]) +"'," 
        insert_sql += "now() )"  #item_nm
        cursor1 = connection.cursor()
        query_result = cursor1.execute(insert_sql)    
        print(insert_sql) 
        i = i + 1
        row = cursor.fetchone()  


    context = {'message': i
                    
    }
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


@csrf_exempt
def mssql_export2(request):
    vlSelectNo = request.GET.get('id')
    vlFlag = request.GET.get('flag')
    # MSSQL 접속


    conn = pymssql.connect(server='192.168.2.124', user='nanum', password='n@num*!@', database='hakjuk', port='1221')
    cursor = conn.cursor()
    #query = "select emp_id, emp_nm, dept_cd, dept_nm, jw_cd, jw_nm, mob_no, tel_no, email_addr, if_dt from vw_nanum_dept_dean where emp_id = '" +vlSelectNo +"'"
    query = "select emp_id, emp_nm, dept_cd, dept_nm, mob_no, tel_no, email_addr, if_dt from vw_nanum_dept_assistant"


    cursor.execute(query)  
    row = cursor.fetchone()  
    
    print("aaaaaaaaa")
    message = 'Fail'
    i = 0
    while row:
        message = str(row[0])  + " || " + str(row[1])  +  " || " + str(row[2])  +  " || " + str(row[3]) +  " || " + str(row[4])  +  " || " + str(row[5])  +  " || " + str(row[6]) 
        insert_sql = "insert into vm_nanum_dept_assistant_osh(emp_id, emp_nm, dept_cd, dept_nm, mob_no, tel_no, email_addr,if_dt)"
        insert_sql += "values("
        insert_sql += "'"+ str(row[0]) +"'," 
        insert_sql += "'"+ str(row[1]) +"'," 
        insert_sql += "'"+ str(row[2]) +"'," 
        insert_sql += "'"+ str(row[3]) +"'," 
        insert_sql += "'"+ str(row[4]) +"'," 
        insert_sql += "'"+ str(row[5]) +"'," 
        insert_sql += "'"+ str(row[6]) +"'," 
        insert_sql += "now() )"  #item_nm
        cursor1 = connection.cursor()
        query_result = cursor1.execute(insert_sql)    
        print(insert_sql) 
        i = i + 1
        row = cursor.fetchone()  


    context = {'message': i
                    
    }
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})



@csrf_exempt
def returnsso(request):
        a =  request.POST.get('gbn')
        b =  request.POST.get('sta')
        request.session['member_id'] = 'aaaaaasss'

        message = "Ok"
        context = {'message': message,
        }
        return JsonResponse(context,json_dumps_params={'ensure_ascii': True})



@csrf_exempt
def returnsso2(request):
        
        print(request.session['member_id'])

        if request.session['member_id'] == None:
            message = 'NoSession'
        else:
            message = request.session['member_id']
        
        context = {'message': message,
        }
        return JsonResponse(context,json_dumps_params={'ensure_ascii': True})





#회원가입개인정보
class agree_cont1Serializer(serializers.ModelSerializer):
    class Meta:
        model = agree_cont1
        fields = ('title','code','html','content1','content2','content3')

class agree_cont1(generics.ListAPIView):
    queryset = agree_cont1.objects.all()
    serializer_class = agree_cont1Serializer

    def list(self, request):   

        l_code = request.GET.get('code', None)
        queryset = self.get_queryset()
        queryset = queryset.filter(code=l_code)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)




#멘토스쿨공통코드학년가져오기
class ms_com_cd1Serializer(serializers.ModelSerializer):

    yn = serializers.SerializerMethodField()
    att_val = serializers.SerializerMethodField()
    att_cdd = serializers.SerializerMethodField()
    att_unit = serializers.SerializerMethodField()

    class Meta:
        model = com_cdd
        fields = ('id','std_grp_code','std_detl_code','std_detl_code_nm','sort_seq_no','yn','att_val','att_cdd','att_unit','rmrk')
    def get_yn(self,obj):
        return obj.yn
    def get_att_val(self,obj):
        return obj.att_val
    def get_att_cdd(self,obj):
        return obj.att_cdd
    def get_att_unit(self,obj):
        return obj.att_unit

class ms_com_cd1(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = ms_com_cd1Serializer

    def list(self, request):    
        queryset = self.get_queryset()

        l_ms_id = request.GET.get('ms_id',None)
        
        #queryset = queryset.filter(std_grp_code="MS0010")
        query  = "select (                                  "
        query += "       CASE                               "
        query += "              WHEN B.ID IS NULL           "
        query += "              THEN 'N'                    "
        query += "              ELSE 'Y'                    "
        query += "       END) as yn,                        "
        query += "       A.*,                               "
        query += "       B.*                                "
        query += "from   service20_com_cdd A                "
        query += "       LEFT OUTER JOIN service20_ms_sub B "
        query += "       ON     A.std_grp_code  = B.att_id  "
        query += "       and    A.std_detl_code = B.att_cdd "
        query += "       and    B.ms_id         = '" +l_ms_id +"' "
        query += "where  1                      =1          "
        query += "and    A.std_grp_code in ('MS0010',       "    
        query += "                          'MS0011',       "    
        query += "                          'MS0012',       "    
        query += "                          'MS0013',       "  
        query += "                          'MS0014',       "       
        query += "                          'MS0015',       "
        query += "                          'MS0016',       "
        query += "                          'MS0020')       "

        print(query)
        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)
        
#멘토스쿨공통코드학년가져오기
class mp_com_cd1Serializer(serializers.ModelSerializer):

    yn = serializers.SerializerMethodField()
    att_val = serializers.SerializerMethodField()
    att_cdd = serializers.SerializerMethodField()
    att_unit = serializers.SerializerMethodField()

    class Meta:
        model = com_cdd
        fields = ('id','std_grp_code','std_detl_code','std_detl_code_nm','sort_seq_no','yn','att_val','att_cdd','att_unit')
    def get_yn(self,obj):
        return obj.yn
    def get_att_val(self,obj):
        return obj.att_val
    def get_att_cdd(self,obj):
        return obj.att_cdd
    def get_att_unit(self,obj):
        return obj.att_unit

class mp_com_cd1(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = mp_com_cd1Serializer

    def list(self, request):    
        queryset = self.get_queryset()

        l_mp_id = request.GET.get('mp_id',None)

        #queryset = queryset.filter(std_grp_code="MS0010")


        query  = "select (                                  "
        query += "       CASE                               "
        query += "              WHEN B.ID IS NULL           "
        query += "              THEN 'N'                    "
        query += "              ELSE 'Y'                    "
        query += "       END) as yn,                        "
        query += "       A.*,                               "
        query += "       B.*                                "
        query += "from   service20_com_cdd A                "
        query += "       LEFT OUTER JOIN service20_mp_sub B "
        query += "       ON     A.std_grp_code  = B.att_id  "
        query += "       and    A.std_detl_code = B.att_cdd "
        query += "       and    B.mp_id         = '" +l_mp_id +"' "
        query += "where  1                      =1          "
        query += "and    A.std_grp_code in ('MS0010',       "    
        query += "                          'MS0011',       "    
        query += "                          'MS0012',       "    
        query += "                          'MS0013',       "    
        query += "                          'MS0014',       "
        query += "                          'MS0015',       "
        query += "                          'MS0016',       "
        query += "                          'MS0019',       "
        query += "                          'MS0020')       "
        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)      



#멘토스쿨 설정값 저장하기
@csrf_exempt
def ms_com_save1(request):
    l_id = request.GET.get('id', None)
    l_ms_id = request.GET.get('ms_id', None)
    l_std_grp_code = request.GET.get('std_grp_code', None)
    l_std_detl_code = request.GET.get('std_detl_code', None)
    l_tflag = request.GET.get('tflag', None)
    
    print(l_id)
    print(l_ms_id)
    print(l_std_detl_code)
    print(l_tflag)
    
    cursor = connection.cursor()
    if l_tflag=='d':
        insert_sql = "delete from service20_ms_sub where  ms_id = '" + str(l_ms_id) + "' and att_id = '"+ l_std_grp_code + "' and att_cdd = '"+ l_id+ "' "
        print(insert_sql)  

    if l_tflag=='i':
        insert_sql = "insert into service20_ms_sub(ms_id, att_id, att_seq, att_cdh, att_cdd, att_val, att_unit, use_yn, sort_seq) "
        insert_sql += "select '" + str(l_ms_id) + "'," 
        insert_sql += "'" + str(l_std_grp_code) +"'," 
        insert_sql += "(select COALESCE(max(att_seq),0) + 1 from service20_ms_sub where ms_id = '" + str(l_ms_id) +"') ," 
        insert_sql += "std_grp_code, std_detl_code, std_detl_code_nm, '', 'Y', sort_seq_no from service20_com_cdd where std_grp_code = '"+ str(l_std_grp_code) +"' and std_detl_code = '"+ str(l_std_detl_code)+ "'"
        print(insert_sql) 
    cursor.execute(insert_sql)
    message = "Ok" 
    context = {'message': message,}
    
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


#멘토스쿨 설정값 저장하기
@csrf_exempt
def ms_com_save2(request):
    l_ms_id = request.GET.get('ms_id', None)
    l_t4_1 = request.GET.get('l_t4_1', None)
    l_t4_2 = request.GET.get('l_t4_2', None)
    l_t4_3 = request.GET.get('l_t4_3', None)
    l_t4_4 = request.GET.get('l_t4_4', None)

    
    cursor = connection.cursor()
    insert_sql = "update service20_ms_sub set att_val = '" + str(l_t4_1) +"' where  ms_id = '" + str(l_ms_id) + "' and att_id = 'MS0013' and att_cdd = '10' "
    print(insert_sql)   
    cursor.execute(insert_sql)
    insert_sql = "update service20_ms_sub set att_val = '" + str(l_t4_2) +"' where  ms_id = '" + str(l_ms_id) + "' and att_id = 'MS0013' and att_cdd = '20' "
    cursor.execute(insert_sql)
    insert_sql = "update service20_ms_sub set att_val = '" + str(l_t4_3) +"' where  ms_id = '" + str(l_ms_id) + "' and att_id = 'MS0013' and att_cdd = '30' "
    cursor.execute(insert_sql)
    insert_sql = "update service20_ms_sub set att_val = '" + str(l_t4_4) +"' where  ms_id = '" + str(l_ms_id) + "' and att_id = 'MS0013' and att_cdd = '40' "
    cursor.execute(insert_sql)
    insert_sql = "update service20_ms_sub set att_val = '" + str(l_t4_4) +"' where  ms_id = '" + str(l_ms_id) + "' and att_id = 'MS0013' and att_cdd = '50' "
    cursor.execute(insert_sql)

    message = "Ok" 
    context = {'message': message,}
    
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


@csrf_exempt
def mp_com_save1(request):
    l_id = request.GET.get('id', None)
    l_mp_id = request.GET.get('mp_id', None)
    l_std_grp_code = request.GET.get('std_grp_code', None)
    l_std_detl_code = request.GET.get('std_detl_code', None)
    l_tflag = request.GET.get('tflag', None)
    
    print(l_id)
    print(l_mp_id)
    print(l_std_detl_code)
    print(l_tflag)
    
    cursor = connection.cursor()
    if l_tflag=='d':
        insert_sql = "delete from service20_mp_sub where  mp_id = '" + str(l_mp_id) + "' and att_id = '"+ l_std_grp_code + "' and att_cdd = '"+ l_id+ "' "
        print(insert_sql)  

    if l_tflag=='i':
        insert_sql = "insert into service20_mp_sub(mp_id, att_id, att_seq, att_cdh, att_cdd, att_val, att_unit, use_yn, sort_seq) "
        insert_sql += "select '" + str(l_mp_id) + "'," 
        insert_sql += "'" + str(l_std_grp_code) +"'," 
        insert_sql += "(select COALESCE(max(att_seq),0) + 1 from service20_mp_sub where mp_id = '" + str(l_mp_id) +"') ," 
        insert_sql += "std_grp_code, std_detl_code, std_detl_code_nm, '', 'Y', sort_seq_no from service20_com_cdd where std_grp_code = '"+ str(l_std_grp_code) +"' and std_detl_code = '"+ str(l_std_detl_code)+ "'"
        print(insert_sql) 
    cursor.execute(insert_sql)
    message = "Ok" 
    context = {'message': message,}
    
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})



#파일업로드 테스트
@csrf_exempt
def upload(request):

    req = request
    DIR = os.getcwd()
    UPLOAD_DIR = str(DIR) + '/media/mp_mtr/'
    if request.method == 'POST':
        l_user_id = request.POST.get("user_id")
        l_mp_id = request.POST.get("mp_id")

        print(l_user_id)
        print(l_mp_id)
        file = request.FILES['file']
        filename = file._name
        n_filename = str(l_user_id) + '_' + str(l_mp_id) + '' + os.path.splitext(filename)[1]
        print(n_filename)
        print (UPLOAD_DIR)
        
        fp = open('%s/%s' % (UPLOAD_DIR, n_filename) , 'wb')

        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

        cursor = connection.cursor()
        fullFile = str(UPLOAD_DIR) + str(n_filename)
        insert_sql = "update service20_mp_mtr set  id_pic = '" + str(fullFile) + "' where mp_id = '"+ str(l_mp_id) + "' and apl_id = '" +  str(l_user_id) +"' "
        print(insert_sql)
        cursor.execute(insert_sql)

        return HttpResponse('File Uploaded')

    return HttpResponse('Failed to Upload File')
        


#공지사항
class bbs1Serializer(serializers.ModelSerializer):
    class Meta:
        model = bbs1
        fields = ('subject','name','html','hits','ins_dt','ins_id')

class bbs1(generics.ListAPIView):
    queryset = bbs1.objects.all()
    serializer_class = bbs1Serializer

    def list(self, request):   
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)




#공통코드가져오기
class comcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = com_cdd
        fields = ('std_grp_code','std_detl_code','std_detl_code_nm')

class comcode(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = comcodeSerializer

    def list(self, request):   
        queryset = self.get_queryset()
        l_code = request.GET.get('code',None)

        print(l_code)
        print("aaa")
        queryset = queryset.filter(std_grp_code=l_code)


        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)






## 강주원 작업 시작


class MPAttView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        mp_id = request.GET.get('mp_id')
        apl_no = request.GET.get('apl_no')
        status_map = dict(
            A='진행',
            B='미승인',
            C='보호자승인',
            D='관리자승인',
            E='완료',
        )
        return JsonResponse(data=[
            {
                'id': a.id,
                'started_at': a.att_sdt,
                'ended_at': a.att_edt,
                'is_approved': True if a.appr_dt else False,
                'approved_hour': a.appr_tm,
                'status': status_map.get(a.att_sts, '기타'),
                'note': a.mtr_desc,
                'started_addr': a.att_saddr,
                'ended_addr': a.att_eaddr,
                'manager_name': manager.objects.filter(mgr_id=a.mgr_id).first(),
                'approved_at': a.appr_dt,
                'image': f'http://114.202.247.167:8888/media/{a.mtr_pic}',
            }
            for a in mp_att.objects.filter(apl_no=apl_no, mp_id=mp_id).order_by('-ins_dt')
            #for a in mp_att.objects.filter(apl_no=apl_no, mp_id=mp_id).order_by('-ins_dt') if a.id == 1    if문으로 조건까지 걸수 있음.
        ], safe=False)

    def save_image(self, file, path):
        f = open(path, 'wb')
        for chunk in file.chunks():
            f.write(chunk)
        f.close()

    def post(self, request):
        request._load_post_and_files()
        data = request.POST
        id = data.get('id')
        apl_no = data.get('apl_no')
        mp_id = data.get('mp_id')
        mnte_id = data.get('mnte_id')
        address = data.get('address')
        lat = data.get('lat')
        lng = data.get('lng')
        action = data.get('action')
        if action == 'START':
            total_count = mp_att.objects.filter(mp_id=mp_id, apl_no=apl_no).count()
            now = datetime.datetime.now()
            mp = mpgm.objects.get(mp_id=mp_id)
            mp_att.objects.create(
                apl_no=apl_no,
                mp_id=mp_id,
                att_saddr=address,
                att_sdt=now,
                att_no=total_count + 1,
                mp_div='A',
                spc_no=0,
                att_div='Y',
                att_sts='A',
                ins_dt=datetime.datetime.now(),
                att_slat=lat,
                att_slon=lng,
                mgr_id=mp.mgr_id,
            )
            mtrs = mp_mte.objects.filter(mp_id=mp_id, apl_no=apl_no)
            for m in mtrs:
                total = mp_att_mte.objects.filter(mp_id=mp_id, apl_no=apl_no, mnte_no=m.mnte_no).count()
                mp_att_mte.objects.create(
                    mp_id=mp_id,
                    apl_no=apl_no,
                    mnte_no=m.mnte_no,
                    att_no=total + 1,
                    att_div='Y',
                    att_sdt=now,
                )
        elif action == 'END':
            att = mp_att.objects.get(id=id)
            mtrs = mp_mte.objects.filter(mp_id=att.mp_id, apl_no=att.apl_no)
            print(mtrs)
            for m in mp_att_mte.objects.filter(
                    mp_id=att.mp_id,
                    apl_no=att.apl_no,
                    att_sdt=att.att_sdt,
                    att_edt__isnull=True,
                    mnte_no__in=[e.mnte_no for e in mtrs]
            ):
                m.att_edt = datetime.datetime.now()
                m.appr_tm = (datetime.datetime.now() - att.att_sdt).seconds // 3600
                m.elap_tm = f'{m.appr_tm}:00'
                m.save()
            if request.FILES.get('image'):
                file = request.FILES['image']
                self.save_image(file, f'{settings.MEDIA_ROOT}/{file.name}')
                att.mtr_pic = file.name
            att.att_eaddr = address
            att.appr_tm = (datetime.datetime.now() - att.att_sdt).seconds // 3600
            att.att_edt = datetime.datetime.now()
            att.mtr_desc = data.get('note')
            att.att_sts = 'B'
            att.att_elat = lat
            att.att_elon = lng
            att.save()
        elif action == 'GUARDIAN_APPROVE':
            att = mp_att.objects.get(id=id)
            att.appr_dt = datetime.datetime.now()
            att.att_sts = 'C'
            att.save()
        elif action == 'QRCODE_GEN':
            mte = mp_mte.objects.filter(mp_id=mp_id, apl_no=apl_no, mnte_id=mnte_id).first()
            if not mte:
                return JsonResponse(data={'code': 'NOT_FOUND'}, status=412)
            if not mte.day_rand:
                mte.day_rand = ''.join([str(random.randint(0, 9)) for _ in range(10)])
                mte.save()
            return JsonResponse(data={'code': mte.day_rand})
        elif action == 'QR_MENTEE_ATTEND':
            pass
        return JsonResponse(data={'code': 'OK'})


class TeacherMP0101MList(View):
    def get(self, request):
        teacher_id = request.GET.get('user_id')
        query = f'''
            SELECT mpgm.*, mp_mte.*, c1.std_detl_code_nm  AS sup_org_nm, c2.std_detl_code_nm AS mng_org_nm, mp_mte.apl_no AS apl_no,
                mp_mte.sch_nm AS mnte_sch, mp_mte.sch_yr AS mnte_sch_yr
                FROM service20_mpgm mpgm
            INNER JOIN (SELECT * from service20_mp_mte WHERE tchr_id = '{teacher_id}') mp_mte ON mp_mte.mp_id = mpgm.mp_id
            INNER JOIN service20_mp_mtr mp_mtr on mp_mte.mp_id = mp_mtr.mp_id and mp_mte.apl_no = mp_mtr.apl_no
            LEFT JOIN service20_com_cdd c1 ON (c1.std_grp_code  = 'MP0004' AND c1.std_detl_code = mpgm.sup_org)
            LEFT JOIN service20_com_cdd c2 ON (c2.std_grp_code = 'MP0003' AND c2.std_detl_code = mpgm.mng_org)
        '''
        queryset = mpgm.objects.raw(query)
        return JsonResponse(data=[
            {
                'apl_no': m.apl_no,
                'mp_id': m.mp_id,
                'mnt_fr_dt': m.mnt_fr_dt,
                'mnt_to_dt': m.mnt_to_dt,
                'mp_name': m.mp_name,
                'mnte_nm': m.mnte_nm,
                'mnte_id': m.mnte_id,
                'mnte_sch': m.mnte_sch,
                'mnte_sch_yr': m.mnte_sch_yr,
                'sup_org_nm': m.sup_org_nm,
                'mng_org_nm': m.mng_org_nm,
                'mgr_nm': m.mgr_nm,

            } for m in queryset
        ], safe=False)


class GuardianMP0101MList(View):
    def get(self, request):
        guardian_id = request.GET.get('user_id')
        query = f'''
            SELECT mpgm.*, mp_mte.mnte_nm AS mnte_nm, c1.std_detl_code_nm  AS sup_org_nm, c2.std_detl_code_nm AS mng_org_nm, mp_mte.apl_no As apl_no
                FROM service20_mpgm mpgm
            INNER JOIN (SELECT * from service20_mp_mte WHERE grd_id = '{guardian_id}') mp_mte ON mp_mte.mp_id = mpgm.mp_id
            LEFT JOIN service20_com_cdd c1 ON (c1.std_grp_code  = 'MP0004' AND c1.std_detl_code = mpgm.sup_org)
            LEFT JOIN service20_com_cdd c2 ON (c2.std_grp_code = 'MP0003' AND c2.std_detl_code = mpgm.mng_org)
        '''
        queryset = mpgm.objects.raw(query)
        return JsonResponse(data=[
            {
                'apl_no': m.apl_no,
                'mp_id': m.mp_id,
                'mnt_fr_dt': m.mnt_fr_dt,
                'mnt_to_dt': m.mnt_to_dt,
                'mp_name': m.mp_name,
                'sup_org_nm': m.sup_org_nm,
                'mng_org_nm': m.mng_org_nm,
                'mgr_nm': m.mgr_nm,
                'mnte_nm': m.mnte_nm,
            } for m in queryset
        ], safe=False)



class UserLoginView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    user_type_dict = dict(
        M=dict(
            model=vw_nanum_stdt, 
            id_field='apl_id',
            return_fields=['apl_id', 'apl_nm', 'unv_nm', 'cllg_nm', 'dept_nm']
        ),
        T=dict(
            model=teacher,
            id_field='tchr_id',
            return_fields=['tchr_id', 'tchr_nm', 'sch_nm']
        ),
        G=dict(
            model=guardian,
            id_field='grdn_id',
            return_fields=['grdn_id', 'grdn_nm']
        )
    )

    def post(self, request):
        db_cursor = connection.cursor()
        data = json.loads(request.body)
        db_cursor.execute(
            f"select * from vw_nanum_login where user_id ='{data['user_id']}' AND user_div IN ('M', 'T', 'G')")
        info = db_cursor.fetchone()
        if not info:
            return JsonResponse(data={'code': 'NOT FOUND'}, status=412)

        user_dict = self.user_type_dict[info[5]]
        user = user_dict['model'].objects.filter(**{user_dict['id_field']: data['user_id']}).first()
        data = {f: getattr(user, f) for f in user_dict['return_fields']}
        data.update({'user_type': info[5]})
        return JsonResponse(data=data)




class MoveQuestionView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        request._load_post_and_files()
        surv_t = cm_surv_t.objects.get(surv_id=request.POST['object_id'])
        action = request.POST.get('action')
        ids = json.loads(request.POST['ids']) if request.POST.get('ids') else None
        if action == 'IN':
            count = cm_surv_q.objects.filter(surv_id=surv_t.surv_id).count()
            for id in ids:
                cm_surv_q.objects.update_or_create(surv_id=surv_t.surv_id, ques_no=id, sort_seq=count + 1)
                count += 1
        elif action == 'OUT':
            cm_surv_q.objects.filter(surv_id=surv_t.surv_id, ques_no__in=ids).delete()
        elif action == 'UP':
            id = request.POST.get('id')
            current_q = cm_surv_q.objects.filter(surv_id=surv_t.surv_id, ques_no=id).first()
            prev_q = cm_surv_q.objects.filter(surv_id=surv_t.surv_id, sort_seq=current_q.sort_seq - 1).first()
            if prev_q:
                prev_q.sort_seq += 1
                current_q.sort_seq -= 1
                prev_q.save()
                current_q.save()
        elif action == 'DOWN':
            id = request.POST.get('id')
            current_q = cm_surv_q.objects.filter(surv_id=surv_t.surv_id, ques_no=id).first()
            next_q = cm_surv_q.objects.filter(surv_id=surv_t.surv_id, sort_seq=current_q.sort_seq + 1).first()
            if next_q:
                next_q.sort_seq -= 1
                current_q.sort_seq += 1
                next_q.save()
                current_q.save()

        return JsonResponse(data={'code': 'OK'})

#김한솔 난수생성 api
class RandomSerializer(serializers.ModelSerializer):
    class Meta:
        model = mp_mte
        fields = ('day_rand',)

class RandomViewSet(generics.ListAPIView):
    queryset = mp_mte.objects.all()
    serializer_class = RandomSerializer

# 강주원 작업 종료
