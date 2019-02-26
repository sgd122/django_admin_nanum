from django.shortcuts import render
from rest_framework import generics, serializers
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.http import HttpResponse,Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404,render
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse,Http404, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from service10.models import *
from service20.models import *
from django.db import connection
# Create your views here.

class Service10AuthListSerializer(serializers.ModelSerializer):

    class Meta:
        model = vm_nanum_stdt
        fields = ('apl_id', 'apl_nm','apl_nm_e','univ_cd','univ_nm')



class Service10AuthListView(generics.ListAPIView):
    queryset = vm_nanum_stdt.objects.all()
    serializer_class = Service10AuthListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

@csrf_exempt
def post_login(request):
	ida = request.POST.get('user_id', None)
	passa = request.POST.get('user_pw', None)

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

		#mentor_query
		mentor_query = " select mntr_id from service20_mentor where apl_id = '"+str(ida)+"'"
		mentor_cursor = connection.cursor()
		query_result = mentor_cursor.execute(mentor_query)  


		if query_result == 0:
			v_mntr_id = ''
		else:
			#mentor_query
			rows_mentor = mentor.objects.filter(apl_id=str(ida))[0]
			v_mntr_id = str(rows_mentor.mntr_id)

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
					'mntr_id' : v_mntr_id
					}
	
		print(context)
	#return HttpResponse(json.dumps(context), content_type="application/json")
	return JsonResponse(context,json_dumps_params={'ensure_ascii': True})



def authView(request):
    context = None
    return render(request, 'service10/Service10Auth.html', context)
