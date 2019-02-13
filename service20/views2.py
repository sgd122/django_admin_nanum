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
    ms_id = request.GET.get('ms_id_id', None)
    #l_key1 = ms_apl.objects.filter(ms_id_id=ms_id).values_list('apl_id', flat=True) 

    #print(l_key1);
    #queryset = self.get_queryset()
    #queryset = vm_nanum_stdt.objects.filter(apl_id__in=ms_id)
    queryset = ms_apl.objects.filter(ms_id_id=ms_id)

    queryset2 = cm_cnv_scr.objects.filter(eval_item='1')

    for val in queryset:
        print("1234")

        print(ms_id)
        print(val.apl_id)
        print(val.score1)
        print("0000")
        print(val.score2)  

        print("1111")
        vl_cscore1 = (val.score1 / 100) * 100
        print("2222")
        print(vl_cscore1)
        print("3333")
        queryset2 = queryset2.filter(eval_item=1,max_scr__lt=vl_cscore1)
        
        queryset2 = queryset2.filter(eval_item=1,max_scr__lt ='15')
        for val2 in queryset2:
            print(val2.max_scr)

        print(queryset2);
        queryset2 = queryset2.filter(max_scr__lt=vl_cscore1)
        print(queryset2);
        print("4444")
        print(queryset2[0].fin_scr)
        print("5555")
        



        """
        model_instance = ms_apl(
            ms_id_id=ms_id_id, 
            apl_no=apl_no, 
            apl_id=apl_id,
            score1=apl_id,
            score2=apl_id,
            score3=apl_id,
            score4=apl_id,
            score5=apl_id,
            )
        model_instance.save()
        """


    print(queryset[0].apl_id)
    print(queryset)

    message = "Ok"
     
    context = {'message': message,}
    

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})
