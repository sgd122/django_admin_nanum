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

# api/moim 으로 get하면 이 listview로 연결

class Service20ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = msch
        fields = ('ms_id', 'ms_name','yr','yr_seq','sup_org','img_src','ins_dt','ins_id','apl_term','apl_fr_dt','apl_to_dt','trn_fr_dt','trn_to_dt','tot_apl','cnt_apl')

class Service20ListView(generics.ListAPIView):
    queryset = msch.objects.all()
    serializer_class = Service20ListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

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
    #created,created_flag = vm_nanum_stdt.apl_id.get_or_create(user=request.user)
    created_flag = vm_nanum_stdt.objects.filter(apl_id=ida).exists()
    #rows = vm_nanum_stdt.objects.filter(apl_id=ida)
    #rows2 = vm_nanum_stdt.objects.get("apl_nm")
    if not created_flag:
        message = "Fail"
        context = {'message': message}
    else:
        
        message = "Ok"
        rows = vm_nanum_stdt.objects.filter(apl_id=ida)[0]
        rows2 = mp_sub.objects.filter(ms_id=ms_ida)

        for val in rows2:
            key1 = val.att_id
            #key2 = val.att_cdd

        question01 = com_cdd.objects.filter(std_grp_code=key1)[0].rmrk
        question02 = com_cdd.objects.filter(std_grp_code=key1)[1].rmrk
        question03 = com_cdd.objects.filter(std_grp_code=key1)[2].rmrk
        question04 = com_cdd.objects.filter(std_grp_code=key1)[3].rmrk
        question05 = com_cdd.objects.filter(std_grp_code=key1)[4].rmrk




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
                    'question01' : question01,
                    'question02' : question02,
                    'question03' : question03,
                    'question04' : question04,
                    'question05' : question05
                    }
    

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})





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
    #created,created_flag = vm_nanum_stdt.apl_id.get_or_create(user=request.user)
    ms_id_id = programId
    ms_apl_max = ms_apl.objects.all().aggregate(vlMax=Max('apl_no'))
    #ms_apl_max = ms_apl.objects.all().last()
    #ms_apl_max = ms_apl_max + 1
    apl_no = ms_apl_max
    apl_id = ida
    apl_no = ms_apl_max['vlMax']
    apl_no = apl_no + 1;
    
    



    context = {'message': 'Ok'}
    
    model_instance = ms_apl(ms_id_id=ms_id_id, apl_no=apl_no, apl_id=apl_id,apl_nm=que1)
    model_instance.save()

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})
