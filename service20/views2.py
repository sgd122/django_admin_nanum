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
class comboMpmgListSerializer(serializers.ModelSerializer):
    class Meta:
        model = msch
        fields = ('ms_id','ms_name')


class comboMpmgListView(generics.ListAPIView):
    queryset = msch.objects.all()
    serializer_class = comboMpmgListSerializer

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
class comboMpmgListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = msch
        fields = ('ms_id','ms_name')


class comboMpmgListViewDetail(generics.ListAPIView):
    queryset = msch.objects.all()
    serializer_class = comboMpmgListDetailSerializer

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
