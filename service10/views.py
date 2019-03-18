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
	chk_info = request.POST.get('chk_info', None)

	#created,created_flag = vm_nanum_stdt.apl_id.get_or_create(user=request.user)

	created_flag = vm_nanum_stdt.objects.filter(apl_id=ida).exists()
	#rows = vm_nanum_stdt.objects.filter(apl_id=ida)
	#rows2 = vm_nanum_stdt.objects.get("apl_nm")
	
	client_ip = request.META['REMOTE_ADDR']

	# /*********************
	# * 메뉴리스트(user_div)
	#     C   KO  공통
	#     D   KO  조교
	#     E   KO  멘티
	#     G   KO  학부모
	#     M   KO  멘토
	#     R   KO  담당자
	#     S   KO  학생
	#     T   KO  교사
	# *********************/
	query = " select distinct A.user_id,A.user_div,B.std_detl_code_nm from vw_nanum_login as A left join service20_com_cdd as B on (B.std_grp_code = 'CM0001' and A.user_div = B.std_detl_code) "
	query += " where user_id = '"+str(ida)+"'"
	cursor = connection.cursor()
	query_result = cursor.execute(query)  
	results = namedtuplefetchall(cursor)  
	if query_result == 0:
		v_login_gubun = ''
		v_user_div = ''
	else:
		v_login_gubun_code = str(results[0].user_div)
		v_login_gubun = str(results[0].std_detl_code_nm)
		v_user_div =  str(results[0].user_div)

	if v_user_div == "M" or v_user_div == "S":
		created_flag = "ok"
	elif v_user_div == "G":
		# 학부모
		created_flag = "ok"
	elif v_user_div == "T":
		# 교사
		created_flag = "ok"
	elif v_user_div == "R":
		# 담당자
		created_flag = "ok"

	if not created_flag:
		message = "Fail"
		context = {'message': message}
	else:
		message = "Ok"
		# rows = vm_nanum_stdt.objects.filter(apl_id=ida)[0]
		if v_user_div == "M" or v_user_div == "S":
			# 멘토/학생
			rows = vm_nanum_stdt.objects.filter(apl_id=ida)[0]
			v_apl_id = rows.apl_id
			v_apl_nm = rows.apl_nm.replace('\'','')
		elif v_user_div == "G":
			# 학부모
			created_flag2 = guardian.objects.filter(grdn_id=ida,pwd=passa).exists()
            if not created_flag2:
                message = "Fail"
                context = {'message': message}
            else:
				# select * from service20_guardian;
				rows = guardian.objects.filter(grdn_id=ida,pwd=passa)[0]
				v_apl_id = rows.grdn_id
				v_apl_nm = rows.grdn_nm.replace('\'','')
		elif v_user_div == "T":
			# 교사
			created_flag2 = teacher.objects.filter(tchr_id=ida,pwd=passa).exists()
            if not created_flag2:
                message = "Fail"
                context = {'message': message}
            else:
				# select * from service20_teacher;
				rows = teacher.objects.filter(tchr_id=ida,pwd=passa)[0]
				v_apl_id = rows.tchr_id
				v_apl_nm = rows.tchr_nm.replace('\'','')
		elif v_user_div == "R":
			# 담당자
			created_flag2 = manager.objects.filter(mgr_id=ida).exists()
            if not created_flag2:
                message = "Fail"
                context = {'message': message}
            else:
				# select * from service20_manager;
				rows = manager.objects.filter(mgr_id=ida)[0]
				v_apl_id = rows.mgr_id
				v_apl_nm = rows.mgr_nm.replace('\'','')		

		client_ip = request.META['REMOTE_ADDR']
		query = " insert into service20_com_evt     /* 이벤트로그 */ ";
		query += "      ( evt_gb     /* 이벤트구분 */ ";
		query += "     , evt_userid /* 이벤트사용자id */ ";
		query += "     , evt_ip     /* 이벤트발생 ip */ ";
		query += "     , evt_dat    /* 이벤트일시 */ ";
		query += "     , evt_desc   /* 이벤트 내용 */ ";
		query += "     , ins_id     /* 입력자id */ ";
		query += "     , ins_ip     /* 입력자ip */ ";
		query += "     , ins_dt     /* 입력일시 */ ";
		query += "     , ins_pgm    /* 입력프로그램id */ ";
		query += ") ";
		query += " select 'EVT001'  AS evt_gb     /* 이벤트구분 - 로그인 */ ";
		query += "     , '"+ida+"' AS evt_userid /* 이벤트사용자id */ ";
		query += "     , '"+str(client_ip)+"' AS evt_ip     /* 이벤트발생 ip */ ";
		query += "     , REPLACE(REPLACE(REPLACE(SUBSTRING(NOW(),1, 19), '-',''),':',''),' ', '')        AS evt_dat    /* 이벤트일시 */ ";
		query += "     , CONCAT('','로그인') evt_desc   /* 이벤트 내용 */ ";
		query += "     , '"+ida+"' AS ins_id     /* 입력자id */ ";
		query += "     , '"+str(client_ip)+"' AS ins_ip     /* 입력자ip */ ";
		query += "     , NOW()     AS ins_dt     /* 입력일시 */ ";
		query += "     , 'LOGIN'   AS ins_pgm    /* 입력프로그램id */ ";
		cursor_log = connection.cursor()
		query_result = cursor_log.execute(query)  

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


		query = " select distinct A.user_id,A.user_div,B.std_detl_code_nm from vw_nanum_login as A left join service20_com_cdd as B on (B.std_grp_code = 'CM0001' and A.user_div = B.std_detl_code) "
		query += " where user_id = '"+str(ida)+"'"
		cursor = connection.cursor()
		query_result = cursor.execute(query)  
		results = namedtuplefetchall(cursor)  
		v_login_gubun_code = ''
		
		if query_result == 0:
			v_login_gubun = ''
		else:
			v_login_gubun_code = str(results[0].user_div)
			v_login_gubun = str(results[0].std_detl_code_nm)
			v_user_div =  str(results[0].user_div)


		if v_user_div == "M" or v_user_div == "S":
			# 멘토/학생
			context = {'message': message,
					'apl_nm' : v_apl_nm,
					'apl_id' : v_apl_id,
					'univ_cd' : rows.univ_cd,
					'univ_nm' : rows.univ_nm,
					'grad_div_cd' : rows.grad_div_cd,
					'grad_div_nm' : rows.grad_div_nm,
					'cllg_cd' : rows.cllg_cd,
					'cllg_nm' : rows.cllg_nm,
					'dept_cd' : rows.dept_cd,
					'dept_nm' : rows.dept_nm.replace('\'',''),
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
					'mntr_id' : v_mntr_id,
                    'login_gubun_code' : v_login_gubun_code,
                    'login_gubun' : v_login_gubun
					}
		elif v_user_div == "G":
			# 학부모
			context = {'message': message,
					'apl_nm' : v_apl_nm,
					'apl_id' : v_apl_id,
					'rel_tp' : rows.rel_tp,
					'brth_dt' : rows.brth_dt,
					'mob_no' : rows.mob_no,
					'tel_no' : rows.tel_no,
					'moth_nat_cd' : rows.moth_nat_cd,
					'moth_nat_nm' : rows.moth_nat_nm,
					'tch_id' : rows.tch_id,
					'h_addr' : rows.h_addr,
					'post_no' : rows.h_post_no,
					'email_addr' : rows.email_addr,
                    'login_gubun_code' : v_login_gubun_code,
                    'login_gubun' : v_login_gubun
					}
		elif v_user_div == "T":
			# 교사
			context = {'message': message,
					'apl_nm' : v_apl_nm,
					'apl_id' : v_apl_id,
					'sch_grd' : rows.sch_grd,
					'sch_cd' : rows.sch_cd,
					'sch_nm' : rows.sch_nm,
					'mob_no' : rows.mob_no,
					'tel_no' : rows.tel_no,
					'area_city' : rows.area_city,
					'area_gu' : rows.area_gu,
					'h_addr' : rows.h_addr,
					'post_no' : rows.h_post_no,
					's_addr' : rows.s_addr,
					's_post_no' : rows.s_post_no,
					'email_addr' : rows.email_addr,
                    'login_gubun_code' : v_login_gubun_code,
                    'login_gubun' : v_login_gubun
					}
		elif v_user_div == "R":
			# 담당자
			context = {'message': message,
					'apl_nm' : v_apl_nm,
					'apl_id' : v_apl_id,
					'mng_area' : rows.mng_area,
					'mgr_div' : rows.mgr_div,
					'dept_cd' : rows.dept_cd,
					'dept_nm' : rows.dept_nm,
					'ofc_lvl_cd' : rows.ofc_lvl_cd,
					'ofc_lvl_nm' : rows.ofc_lvl_nm,
					'func_cd' : rows.func_cd,
					'func_nm' : rows.func_nm,
					'status' : rows.status,
					'mob_no' : rows.mob_no,
					'tel_no' : rows.tel_no,
					'h_addr' : rows.h_addr,
					'post_no' : rows.h_post_no,
					'email_addr' : rows.email_addr,
                    'login_gubun_code' : v_login_gubun_code,
                    'login_gubun' : v_login_gubun
					}

		# context = {'message': message,
		# 			'apl_nm' : v_apl_nm,
		# 			'apl_id' : v_apl_id,
		# 			'univ_cd' : rows.univ_cd,
		# 			'univ_nm' : rows.univ_nm,
		# 			'grad_div_cd' : rows.grad_div_cd,
		# 			'grad_div_nm' : rows.grad_div_nm,
		# 			'cllg_cd' : rows.cllg_cd,
		# 			'cllg_nm' : rows.cllg_nm,
		# 			'dept_cd' : rows.dept_cd,
		# 			'dept_nm' : rows.dept_nm.replace('\'',''),
		# 			'mjr_cd' : rows.mjr_cd,
		# 			'mjr_nm' : rows.mjr_nm,
		# 			'brth_dt' : rows.brth_dt,
		# 			'gen_cd' : rows.gen_cd,
		# 			'gen_nm' : rows.gen_nm,
		# 			'yr' : rows.yr,
		# 			'sch_yr' : rows.sch_yr,
		# 			'term_div' : rows.term_div,
		# 			'term_nm' : rows.term_nm,
		# 			'stdt_div' : rows.stdt_div,
		# 			'stdt_nm' : rows.stdt_nm,
		# 			'mob_nm' : rows.mob_nm,
		# 			'tel_no' : rows.tel_no,
		# 			'tel_no_g' : rows.tel_no_g,
		# 			'h_addr' : rows.h_addr,
		# 			'post_no' : rows.post_no,
		# 			'email_addr' : rows.email_addr,
		# 			'bank_acct' : rows.bank_acct,
		# 			'bank_cd' : rows.bank_cd,
		# 			'bank_nm' : rows.bank_nm,
		# 			'bank_dpsr' : rows.bank_dpsr,
		# 			'pr_yr' : rows.pr_yr,
		# 			'pr_sch_yr' : rows.pr_sch_yr,
		# 			'pr_term_div' : rows.pr_term_div,
		# 			'score01' : rows.score01,
		# 			'score02' : rows.score02,
		# 			'score03' : rows.score03,
		# 			'score04' : rows.score04,
		# 			'score04_tp' : rows.score04_tp,
		# 			'score05' : rows.score05,
		# 			'mntr_id' : v_mntr_id,
  #                   'login_gubun_code' : v_login_gubun_code,
  #                   'login_gubun' : v_login_gubun
		# 			}
	
		print(context)
	#return HttpResponse(json.dumps(context), content_type="application/json")
	return JsonResponse(context,json_dumps_params={'ensure_ascii': True})



def authView(request):
    context = None
    return render(request, 'service10/Service10Auth.html', context)
