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
from collections import namedtuple

from django.db import connection
from collections  import OrderedDict
import json
#import csv

import unicodecsv as csv
import time
from django import forms
import django_excel as excel
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


##멘토스쿨 사정 버튼 클릭
@csrf_exempt
def msFn2(request):
    ms_id = request.GET.get('ms_id', None)  
    
    queryset2 = cm_cnv_scr.objects.all()
    query = "select * from service20_ms_apl where ms_id = '" +str(ms_id)+"' order by (cscore1+cscore2+cscore3+cscore4+cscore5+cscore5) desc"
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


    cursor = connection.cursor()
    query_doc1 = "select cnt_doc_suc from service20_mpgm where mp_id = '" +str(mp_id)+ "'"
    cursor.execute(query_doc1)
    results_doc1 = namedtuplefetchall(cursor)   
    val_doc1 = results_doc1[0].cnt_doc_suc


    #
    i = 0
    for val in queryset:
        if int(i) < int(val_doc1):
            mp_mtr.objects.filter(id=val.id,mp_id=val.mp_id).update(doc_rank=rank)
            mp_mtr.objects.filter(id=val.id,mp_id=val.mp_id).update(doc_rslt='P')

        rank = rank + 1
        i= i + 1

    message = "Ok" 
    context = {'message': message,}
    

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})



@csrf_exempt
def mpFn3(request):
    mp_id = request.GET.get('mp_id', None)  
    query = "select * from service20_mp_mtr where mp_id = '" +str(mp_id)+"'"
    queryset = mp_mtr.objects.raw(query)

    response = HttpResponse(content_type='text/csv;encoding=UTF-8"') 
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

 
    writer = csv.writer(response,encoding='euc-kr')
    writer.writerow(['apl_no', 'unv_nm', 'dept_nm', 'apl_id', 'apl_nm', 'gen', 'cscore1', 'cscore2', 'cscore3', 'cscore4', 'cscore5', 'doc_rslt', 'doc_rank', 'intv_team', 'intv_dt', 'intv_part_pl','intv_part_ac'])

    if mp_id == None:
        users = mp_mtr.objects.all().values_list('apl_no', 'unv_nm', 'dept_nm', 'apl_id', 'apl_nm', 'gen', 'cscore1', 'cscore2', 'cscore3', 'cscore4', 'cscore5', 'doc_rslt', 'doc_rank', 'intv_team', 'intv_dt', 'intv_part_pl','intv_part_ac')
    else:
        users = mp_mtr.objects.filter(mp_id=mp_id).values_list('apl_no', 'unv_nm', 'dept_nm', 'apl_id', 'apl_nm', 'gen', 'cscore1', 'cscore2', 'cscore3', 'cscore4', 'cscore5', 'doc_rslt', 'doc_rank', 'intv_team', 'intv_dt', 'intv_part_pl','intv_part_ac')

    for user in users:
        writer.writerow(user)
    return response




#면접 구성
@csrf_exempt
def mpFn4(request):

    mp_id = request.GET.get('mp_id', None)
    cursor = connection.cursor()

    query_a = "select intv_dt from service20_mpgm where mp_id = '"+ mp_id + "'"
    cursor.execute(query_a)
    results_a = namedtuplefetchall(cursor)  

    query_b = "select * from service20_mp_mtr where doc_rslt = 'P' and mp_id = '"+ mp_id + "'order by id"

    cursor.execute(query_b)
    results_b = namedtuplefetchall(cursor)  

     

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

    l_data = str(results_a[0].intv_dt) +" " + str(val_02) + ":00"
    l_data2 = datetime.datetime.strptime(l_data,"%Y-%m-%d %H:%M:%S")
    for var in results_b:
        
        insert_sql = "update service20_mp_mtr set "
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



@csrf_exempt
def mpPop1(request):
    posts = None
    return render(request, 'popup/mento/mpPop1.html', { 'posts': posts })


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


class mpPop1_Det1Serializer(serializers.ModelSerializer):
    class Meta:
        model = mp_mtr
        fields = ('mp_id','apl_no','mntr_id','indv_div','team_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','bank_acct','bank_cd','bank_nm','bank_dpsr','cnt_mp_a','cnt_mp_p','cnt_mp_c','cnt_mp_g','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm')        
        #fields = ('mp_id','apl_no','mntr_id','indv_div','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr')

class mpPop1_Det1(generics.ListAPIView):

 
    queryset = mp_mtr.objects.all()
    serializer_class = mpPop1_Det1Serializer

    def list(self, request):

  
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



@csrf_exempt
def sms(request):

    vlSelectNo = request.POST.get('_selected_action')
    vlSelectVar = request.POST.getlist('_selected_action')
    print("제발되라")
    print(vlSelectNo)
    print(vlSelectVar)
    posts = None
    return render(request, 'popup/sms/sms.html', { 'posts': posts })


@csrf_exempt
def sms_result(request):
    vlSelectNo = request.GET.get('id')
    vlFlag = request.GET.get('flag')
    ms_id = ''
    apl_no = ''
    print(vlSelectNo)
    print(vlFlag)
    print("시작000")
    if vlFlag == 'mp':
        print("시작000111")
        cursor = connection.cursor()
        query_b = "select mp_id, apl_no from service20_mp_mtr where id = '"+ vlSelectNo +"'"
        print(query_b)
        cursor.execute(query_b)
        results_b = namedtuplefetchall(cursor)  
        ms_id = results_b[0].mp_id
        apl_no = results_b[0].apl_no
        
        query = "SELECT CASE A.DOC_RSLT WHEN 'P' THEN   CONCAT(   A.APL_NM, '님 ', CHAR(10)"
        query +=  "                       , (SELECT MP_NAME" 
        query +=  "                       FROM service20_mpgm B" 
        query += "                      WHERE B.MP_ID    = '"+ str(ms_id) +"'), ' 서류젼형 합격을 축하합니다.', CHAR(10)" 
        query += "                  , '면접 일시 : ', SUBSTRING(A.INTV_DT, 1, 16), '(', A.INTV_TEAM, '팀)', CHAR(10)"
        query += "                  , '장소 :',    (SELECT B.ATT_VAL"
        query += "                          FROM service20_mp_sub B"
        query += "                          WHERE B.MP_ID  = A.MP_ID"
        query += "                           AND B.ATT_ID = 'MS0019'" 
        query += "                           AND B.ATT_CDH = 'MS0019'"
        query += "                           AND B.ATT_CDD = '06'), CHAR(10)" 
        query += "                  , '면접시간 15분전 대기 바랍니다.' )"
        query += "         WHEN 'N' THEN    CONCAT(   A.APL_NM, '님', CHAR(10)"
        query += "                  , (SELECT MP_NAME"
        query += "                       FROM service20_mpgm B"
        query += "                      WHERE B.MP_ID    = '"+ ms_id +"'), ' 서류젼형에 불합격 했습니다.', CHAR(10)"
        query += "                  , '다음 기회에 도전 부탁드립니다.' )"
        query += "         ELSE 'NO MESSAGE' END MSG"
        query += "  FROM service20_mp_mtr A"
        query += " WHERE A.MP_ID    = '"+ str(ms_id) +"'"
        query += "   AND A.APL_NO   = '"+ str(apl_no) +"'"

        
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

        query = "SELECT CASE A.DOC_RSLT WHEN 'P' THEN   CONCAT(   A.APL_NM, '님 ', CHAR(10)"
        query +=  "                       , (SELECT MS_NAME" 
        query +=  "                       FROM service20_msch B" 
        query += "                      WHERE B.MS_ID    = '"+ str(ms_id) +"'), ' 서류젼형 합격을 축하합니다.', CHAR(10)" 
        query += "                  , '면접 일시 : ', SUBSTRING(A.INTV_DT, 1, 16), '(', A.INTV_TEAM, '팀)', CHAR(10)"
        query += "                  , '장소 :',    (SELECT B.ATT_VAL"
        query += "                          FROM service20_ms_sub B"
        query += "                          WHERE B.MS_ID  = A.MS_ID"
        query += "                           AND B.ATT_ID = 'MS0019'" 
        query += "                           AND B.ATT_CDH = 'MS0019'"
        query += "                           AND B.ATT_CDD = '06'), CHAR(10)" 
        query += "                  , '면접시간 15분전 대기 바랍니다.' )"
        query += "         WHEN 'N' THEN    CONCAT(   A.APL_NM, '님', CHAR(10)"
        query += "                  , (SELECT MS_NAME"
        query += "                       FROM service20_msch B"
        query += "                      WHERE B.MS_ID    = '"+ ms_id +"'), ' 서류젼형에 불합격 했습니다.', CHAR(10)"
        query += "                  , '다음 기회에 도전 부탁드립니다.' )"
        query += "         ELSE 'NO MESSAGE' END MSG"
        query += "  FROM service20_ms_apl A"
        query += " WHERE A.MS_ID    = '"+ str(ms_id) +"'"
        query += "   AND A.APL_NO   = '"+ str(apl_no) +"'"

        
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
def returnsso(request,response):
        message = "Ok"
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
