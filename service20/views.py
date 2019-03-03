from django.shortcuts import render
from rest_framework import generics, serializers
from django.http import HttpResponse,Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.shortcuts import get_object_or_404,render,redirect
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
import requests
import pymssql
from bs4 import BeautifulSoup as bs
import os
# api/moim 으로 get하면 이 listview로 연결


#####################################################################################
# 공통 - START
#####################################################################################

@csrf_exempt
def login_login(request):

        id =  request.POST.get('user_id')
        pswd =  request.POST.get('user_pw')
        # 로그인할 유저정보를 넣어주자 (모두 문자열)
        print("login_start => " + str(id))
        print("login_start(pswd) => " + str(pswd))
        login_info = {'id':id,'pswd': pswd,'dest':'http://nanum.pusan.ac.kr:8000/service20/login/returnsso/'}
        # login_info = {'id':'514965','pswd': 'gks3089#','dest':'http://nanum.pusan.ac.kr:8000/service20/login/returnsso/'}
        # HTTP GET Request: requests대신 s 객체를 사용한다.
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
        query += "     , '"+id+"' AS evt_userid /* 이벤트사용자id */ ";
        query += "     , '"+str(client_ip)+"' AS evt_ip     /* 이벤트발생 ip */ ";
        query += "     , REPLACE(REPLACE(REPLACE(SUBSTRING(NOW(),1, 19), '-',''),':',''),' ', '')        AS evt_dat    /* 이벤트일시 */ ";
        query += "     , CONCAT('','로그인') evt_desc   /* 이벤트 내용 */ ";
        query += "     , '"+str(id)+"' AS ins_id     /* 입력자id */ ";
        query += "     , '"+str(client_ip)+"' AS ins_ip     /* 입력자ip */ ";
        query += "     , NOW()     AS ins_dt     /* 입력일시 */ ";
        query += "     , 'LOGIN'   AS ins_pgm    /* 입력프로그램id */ ";
        cursor_log = connection.cursor()
        query_result = cursor_log.execute(query)    

        with requests.Session() as s:
            first_page = s.post('https://onestop.pusan.ac.kr/new_pass/exorgan/exidentify.asp', data=login_info)
            html = first_page.text
            if first_page.status_code != 200:
                message = "login_fail"           
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
                query += "     , '"+id+"' AS evt_userid /* 이벤트사용자id */ ";
                query += "     , '"+str(client_ip)+"' AS evt_ip     /* 이벤트발생 ip */ ";
                query += "     , REPLACE(REPLACE(REPLACE(SUBSTRING(NOW(),1, 19), '-',''),':',''),' ', '')        AS evt_dat    /* 이벤트일시 */ ";
                query += "     , CONCAT('','200Error') evt_desc   /* 이벤트 내용 */ ";
                query += "     , '"+id+"' AS ins_id     /* 입력자id */ ";
                query += "     , '"+str(client_ip)+"' AS ins_ip     /* 입력자ip */ ";
                query += "     , NOW()     AS ins_dt     /* 입력일시 */ ";
                query += "     , 'LOGIN'   AS ins_pgm    /* 입력프로그램id */ ";
                cursor_log = connection.cursor()
                query_result = cursor_log.execute(query)           
                print("login_200_error => " + str(id))
            else:
                soup = bs(html, 'html.parser')
                gbn = soup.find('input', {'name': 'gbn'}) # input태그 중에서 name이 _csrf인 것을 찾습니다.
                print(gbn['value'])
                if gbn['value'] == 'False':
                    print("login_false => " + str(id))
                    message = "login_fail"
                    context = {'login': 'fail',}

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
                    query += "     , '"+id+"' AS evt_userid /* 이벤트사용자id */ ";
                    query += "     , '"+str(client_ip)+"' AS evt_ip     /* 이벤트발생 ip */ ";
                    query += "     , REPLACE(REPLACE(REPLACE(SUBSTRING(NOW(),1, 19), '-',''),':',''),' ', '')        AS evt_dat    /* 이벤트일시 */ ";
                    query += "     , CONCAT('','notPass') evt_desc   /* 이벤트 내용 */ ";
                    query += "     , '"+id+"' AS ins_id     /* 입력자id */ ";
                    query += "     , '"+str(client_ip)+"' AS ins_ip     /* 입력자ip */ ";
                    query += "     , NOW()     AS ins_dt     /* 입력일시 */ ";
                    query += "     , 'LOGIN'   AS ins_pgm    /* 입력프로그램id */ ";
                    cursor_log = connection.cursor()
                    query_result = cursor_log.execute(query)    
                elif gbn['value'] == 'True':
                    print("login_true => " + str(id))

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
                    query += "     , '"+id+"' AS evt_userid /* 이벤트사용자id */ ";
                    query += "     , '"+str(client_ip)+"' AS evt_ip     /* 이벤트발생 ip */ ";
                    query += "     , REPLACE(REPLACE(REPLACE(SUBSTRING(NOW(),1, 19), '-',''),':',''),' ', '')        AS evt_dat    /* 이벤트일시 */ ";
                    query += "     , CONCAT('','success') evt_desc   /* 이벤트 내용 */ ";
                    query += "     , '"+id+"' AS ins_id     /* 입력자id */ ";
                    query += "     , '"+str(client_ip)+"' AS ins_ip     /* 입력자ip */ ";
                    query += "     , NOW()     AS ins_dt     /* 입력일시 */ ";
                    query += "     , 'LOGIN'   AS ins_pgm    /* 입력프로그램id */ ";
                    cursor_log = connection.cursor()
                    query_result = cursor_log.execute(query)  

                    userid = soup.find('input', {'name': 'userid'})
                    v_userid = userid['value']              
                    # MSSQL 접속


                    ########################################################################
                    # 어학 - 시작
                    ########################################################################
                    query = "select t3.apl_id         /* 학번 */"
                    query += "     , t3.apl_nm         /* 성명 */"
                    query += "     , t3.lang_kind_cd   /* 어학종류코드 */"
                    query += "     , t3.lang_kind_nm   /* 어학종류명 */"
                    query += "     , t3.lang_cd        /* 어학상위코드 */"
                    query += "     , t3.lang_nm        /* 어학상위코드명 */"
                    query += "     , t3.lang_detail_cd /* 어학하위코드 */"
                    query += "     , t3.lang_detail_nm /* 어학하위코드명 */"
                    query += "     , t3.frexm_nm       /* 외국어시험명 */"
                    query += "     , t3.score          /* 시험점수 */"
                    query += "     , t3.grade          /* 시험등급 */"
                    query += "  from vw_nanum_foreign_exam t3     /* 유효한 외국어 성적 리스트 view(임시) */"
                    query += " where 1=1"
                    query += " and t3.apl_id='"+v_userid+"'" 
                    conn = pymssql.connect(server='192.168.2.124', user='nanum', password='n@num*!@', database='hakjuk', port='1221')
                    cursor = conn.cursor()   
                    cursor.execute(query)  
                    row = cursor.fetchone()  

                    # 삭제 (어학)
                    delete_query = " delete from service20_vw_nanum_foreign_exam where apl_id = '"+v_userid+"' "
                    cursor_delete = connection.cursor()
                    delete_query_result = cursor_delete.execute(delete_query)                       
                    # 삭제 (어학)

                    while row:
                    # for val in row:    
                        l_apl_id = str(row[0])
                        l_apl_nm = str(row[1])
                        l_lang_kind_cd = str(row[2])
                        l_lang_kind_nm = str(row[3])
                        l_lang_cd = str(row[4])
                        l_lang_nm = str(row[5])
                        l_lang_detail_cd = str(row[6])
                        l_lang_detail_nm = str(row[7])
                        l_frexm_nm = str(row[8])
                        l_score = str(row[9])
                        l_grade = str(row[10])   

                        # insert(어학)
                        query = "insert into service20_vw_nanum_foreign_exam     /* 유효한 외국어 성적 리스트 view(임시) */"
                        query += "   ( apl_id         /* 학번 */"
                        query += "     , apl_nm         /* 성명 */"
                        query += "     , lang_kind_cd   /* 어학종류코드 */"
                        query += "     , lang_kind_nm   /* 어학종류명 */"
                        query += "     , lang_cd        /* 어학상위코드 */"
                        query += "     , lang_nm        /* 어학상위코드명 */"
                        query += "     , lang_detail_cd /* 어학하위코드 */"
                        query += "     , lang_detail_nm /* 어학하위코드명 */"
                        query += "     , frexm_nm       /* 외국어시험명 */"
                        query += "     , score          /* 시험점수 */"
                        query += "     , grade          /* 시험등급 */"
                        query += ")"
                        query += "values"
                        query += "     ( CASE WHEN '"+str(l_apl_id)+"' =  'None' THEN NULL ELSE '"+str(l_apl_id)+"' END         /* 학번 */"
                        query += "     ,CASE WHEN '"+str(l_apl_nm)+"' =  'None' THEN NULL ELSE '"+str(l_apl_nm)+"' END         /* 성명 */"
                        query += "     ,CASE WHEN '"+str(l_lang_kind_cd)+"' =  'None' THEN ' ' ELSE '"+str(l_lang_kind_cd)+"' END   /* 어학종류코드 */"
                        query += "     ,CASE WHEN '"+str(l_lang_kind_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_lang_kind_nm)+"' END   /* 어학종류명 */"
                        query += "     ,CASE WHEN '"+str(l_lang_cd)+"' =  'None' THEN ' ' ELSE '"+str(l_lang_cd)+"' END        /* 어학상위코드 */"
                        query += "     ,CASE WHEN '"+str(l_lang_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_lang_nm)+"' END        /* 어학상위코드명 */"
                        query += "     ,CASE WHEN '"+str(l_lang_detail_cd)+"' =  'None' THEN ' ' ELSE '"+str(l_lang_detail_cd)+"' END /* 어학하위코드 */"
                        query += "     ,CASE WHEN '"+str(l_lang_detail_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_lang_detail_nm)+"' END /* 어학하위코드명 */"
                        query += "     ,CASE WHEN '"+str(l_frexm_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_frexm_nm)+"' END       /* 외국어시험명 */"
                        query += "     ,CASE WHEN '"+str(l_score)+"' =  'None' THEN '0' ELSE '"+str(l_score)+"' END          /* 시험점수 */"
                        query += "     ,CASE WHEN '"+str(l_grade)+"' =  'None' THEN '0' ELSE '"+str(l_grade)+"' END          /* 시험등급 */"
                        # query += "     ,CASE WHEN '"+str(l_apl_id)+"' =  'None' THEN NULL ELSE '"+str(l_apl_id)+"' END         /* 입력자id */"
                        # query += "     ,CASE WHEN '"+str(client_ip)+"' =  'None' THEN NULL ELSE '"+str(client_ip)+"' END         /* 입력자ip */"
                        # query += "     ,now()         /* 입력일시 */"
                        # query += "     ,CASE WHEN '"+str(l_ins_pgm)+"' =  'None' THEN NULL ELSE '"+str(l_ins_pgm)+"' END        /* 입력프로그램id */"
                        # query += "     ,CASE WHEN '"+str(l_upd_id)+"' =  'None' THEN NULL ELSE '"+str(l_upd_id)+"' END         /* 수정자id */"
                        # query += "     ,CASE WHEN '"+str(l_upd_ip)+"' =  'None' THEN NULL ELSE '"+str(l_upd_ip)+"' END         /* 수정자ip */"
                        # query += "     ,CASE WHEN '"+str(l_upd_dt)+"' =  'None' THEN NULL ELSE '"+str(l_upd_dt)+"' END         /* 수정일시 */"
                        # query += "     ,CASE WHEN '"+str(l_upd_pgm)+"' =  'None' THEN NULL ELSE '"+str(l_upd_pgm)+"' END        /* 수정프로그램id */"
                        query += ")"
                        cursor3 = connection.cursor()
                        query_result = cursor3.execute(query)    
                        # insert(어학)
                        row = cursor.fetchone()  
                    ########################################################################
                    # 어학 - 종료
                    ########################################################################

                    ########################################################################
                    # 봉사 - 시작
                    ########################################################################
                    query = "select t3.apl_id          /* 학번 */"
                    query += "     , t3.apl_nm          /* 성명 */"
                    query += "     , t3.nation_inout_cd /* 국내외구분코드 */"
                    query += "     , t3.nation_inout_nm /* 국내외구분명 */"
                    query += "     , t3.sch_inout_cd    /* 교내외구분코드 */"
                    query += "     , t3.sch_inout_nm    /* 교내외구분명 */"
                    query += "     , t3.activity_nm     /* 봉사명 */"
                    query += "     , t3.manage_org_nm   /* 주관기관명 */"
                    query += "     , t3.start_date      /* 시작일자 */"
                    query += "     , t3.start_time      /* 시작시간 */"
                    query += "     , t3.end_date        /* 종료일자 */"
                    query += "     , t3.end_time        /* 종료시간 */"
                    query += "     , t3.tot_time        /* 총시간 */"
                    query += "  from vw_nanum_service_activ t3     /* 학생 봉사 시간 view(임시) */"
                    query += " where 1=1"
                    query += " and t3.apl_id='"+v_userid+"'" 
                    conn = pymssql.connect(server='192.168.2.124', user='nanum', password='n@num*!@', database='hakjuk', port='1221')
                    cursor = conn.cursor()   
                    cursor.execute(query)  
                    row = cursor.fetchone()  

                    # 삭제 (봉사)
                    delete_query = " delete from service20_vw_nanum_service_activ where apl_id = '"+v_userid+"' "
                    cursor_delete = connection.cursor()
                    delete_query_result = cursor_delete.execute(delete_query)                       
                    # 삭제 (봉사)

                    while row:
                    # for val in row:        
                        l_apl_id = str(row[0])
                        l_apl_nm = str(row[1])
                        l_nation_inout_cd = str(row[2])
                        l_nation_inout_nm = str(row[3])
                        l_sch_inout_cd = str(row[4])
                        l_sch_inout_nm = str(row[5])
                        l_activity_nm = str(row[6])
                        l_manage_org_nm = str(row[7])
                        l_start_date = str(row[8])
                        l_start_time = str(row[9])
                        l_end_date = str(row[10])
                        l_end_time = str(row[11])
                        l_tot_time = str(row[12])    

                        # insert(봉사)
                        query = "insert into service20_vw_nanum_service_activ     /* 학생 봉사 시간 view(임시)*/ "
                        query += "   ( apl_id          /* 학번 */"
                        query += "     , apl_nm          /* 성명 */"
                        query += "     , nation_inout_cd /* 국내외구분코드 */"
                        query += "     , nation_inout_nm /* 국내외구분명 */"
                        query += "     , sch_inout_cd    /* 교내외구분코드 */"
                        query += "     , sch_inout_nm    /* 교내외구분명 */"
                        query += "     , activity_nm     /* 봉사명 */"
                        query += "     , manage_org_nm   /* 주관기관명 */"
                        query += "     , start_date      /* 시작일자 */"
                        query += "     , start_time      /* 시작시간 */"
                        query += "     , end_date        /* 종료일자 */"
                        query += "     , end_time        /* 종료시간 */"
                        query += "     , tot_time        /* 총시간 */"
                        # query += "     , ins_id          /* 입력자id */"
                        # query += "     , ins_ip          /* 입력자ip */"
                        # query += "     , ins_dt          /* 입력일시 */"
                        # query += "     , ins_pgm         /* 입력프로그램id */"
                        # query += "     , upd_id          /* 수정자id */"
                        # query += "     , upd_ip          /* 수정자ip */"
                        # query += "     , upd_dt          /* 수정일시 */"
                        # query += "     , upd_pgm         /* 수정프로그램id */"
                        query += ")"
                        query += "values"
                        query += "     ( CASE WHEN '"+str(l_apl_id)+"' =  'None' THEN NULL ELSE '"+str(l_apl_id)+"' END         /* 학번 */"
                        query += "     ,CASE WHEN '"+str(l_apl_nm)+"' =  'None' THEN NULL ELSE '"+str(l_apl_nm)+"' END         /* 성명 */"
                        query += "     , CASE WHEN '"+str(l_nation_inout_cd)+"' =  'None' THEN ' ' ELSE '"+str(l_nation_inout_cd)+"' END /* 국내외구분코드 */"
                        query += "     , CASE WHEN '"+str(l_nation_inout_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_nation_inout_nm)+"' END /* 국내외구분명 */"
                        query += "     , CASE WHEN '"+str(l_sch_inout_cd)+"' =  'None' THEN ' ' ELSE '"+str(l_sch_inout_cd)+"' END    /* 교내외구분코드 */"
                        query += "     , CASE WHEN '"+str(l_sch_inout_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_sch_inout_nm)+"' END    /* 교내외구분명 */"
                        query += "     , CASE WHEN '"+str(l_activity_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_activity_nm)+"'END     /* 봉사명 */"
                        query += "     , CASE WHEN '"+str(l_manage_org_nm)+"' =  'None' THEN ' ' ELSE '"+str(l_manage_org_nm)+"' END   /* 주관기관명 */"
                        query += "     , CASE WHEN '"+str(l_start_date)+"' =  'None' THEN ' ' ELSE '"+str(l_start_date)+"' END      /* 시작일자 */"
                        query += "     , CASE WHEN '"+str(l_start_time)+"' =  'None' THEN ' ' ELSE '"+str(l_start_time)+"' END      /* 시작시간 */"
                        query += "     , CASE WHEN '"+str(l_end_date)+"' =  'None' THEN ' ' ELSE '"+str(l_end_date)+"' END        /* 종료일자 */"
                        query += "     , CASE WHEN '"+str(l_end_time)+"' =  'None' THEN ' ' ELSE  '"+str(l_end_time)+"' END       /* 종료시간 */"
                        query += "     , CASE WHEN '"+str(l_tot_time)+"' =  'None' THEN ' ' ELSE '"+str(l_tot_time)+"' END        /* 총시간 */"
                        # query += "     ,CASE WHEN '"+str(l_apl_id)+"' =  'None' THEN NULL ELSE '"+str(l_apl_id)+"' END         /* 입력자id */"
                        # query += "     ,CASE WHEN '"+str(client_ip)+"' =  'None' THEN NULL ELSE '"+str(client_ip)+"' END         /* 입력자ip */"
                        # query += "     ,now()         /* 입력일시 */"
                        # query += "     , CASE WHEN '"+str(l_ins_pgm)+"' =  'None' THEN NULL ELSE '"+str(l_ins_pgm)+"' END         /* 입력프로그램id */"
                        # query += "     , CASE WHEN '"+str(l_upd_id)+"' =  'None' THEN NULL ELSE '"+str(l_upd_id)+"' END          /* 수정자id */"
                        # query += "     , CASE WHEN '"+str(l_upd_ip)+"' =  'None' THEN NULL ELSE '"+str(l_upd_ip)+"' END          /* 수정자ip */"
                        # query += "     , CASE WHEN '"+str(l_upd_dt)+"' =  'None' THEN NULL ELSE '"+str(l_upd_dt)+"' END          /* 수정일시 */"
                        # query += "     , CASE WHEN '"+str(l_upd_pgm)+"' =  'None' THEN NULL ELSE '"+str(l_upd_pgm)+"' END         /* 수정프로그램id */"
                        query += ")"
                        cursor4 = connection.cursor()
                        query_result = cursor4.execute(query)    
                        # insert(봉사)
                        row = cursor.fetchone()  
                    ########################################################################
                    # 봉사 - 종료
                    ########################################################################

                    # 로그인처리 - 시작                
                    query = "select t3.apl_id      /* 학번 */ "
                    query += "     , t3.apl_nm      /* 성명 */ "
                    query += "     , t3.apl_nm_e    /* 성명_영문 */ "
                    query += "     , t3.unv_cd      /* 대학교코드 */ "
                    query += "     , t3.unv_nm      /* 대학교명 */ "
                    query += "     , t3.grad_div_cd /* 대학원구분코드 */ "
                    query += "     , t3.grad_div_nm /* 대학원구분명 */ "
                    query += "     , t3.cllg_cd     /* 대학코드 */ "
                    query += "     , t3.cllg_nm     /* 대학명 */ "
                    query += "     , t3.dept_cd     /* 학과코드 */ "
                    query += "     , t3.dept_nm     /* 학과명 */ "
                    query += "     , t3.mjr_cd      /* 전공코드 */ "
                    query += "     , t3.mjr_nm      /* 전공명 */ "
                    query += "     , t3.brth_dt     /* 생년월일 */ "
                    query += "     , t3.gen_cd      /* 성별코드 */ "
                    query += "     , t3.gen_nm      /* 성별명 */ "
                    query += "     , t3.yr          /* 학년도 */ "
                    query += "     , t3.sch_yr      /* 학년 */ "
                    query += "     , t3.term_div    /* 학기코드 */ "
                    query += "     , t3.term_nm     /* 학기명 */ "
                    query += "     , t3.stds_div    /* 학적상태코드 */ "
                    query += "     , t3.stds_nm     /* 학적상태명 */ "
                    query += "     , t3.mob_no      /* 휴대전화번호 */ "
                    query += "     , t3.tel_no      /* 집전화 */ "
                    query += "     , t3.tel_no_g    /* 보호자연락처 */ "
                    query += "     , t3.h_addr      /* 집주소 */ "
                    query += "     , t3.post_no     /* 우편번호 */ "
                    query += "     , t3.email_addr  /* 이메일주소 */ "
                    query += "     , t3.bank_acct   /* 은행계좌번호 */ "
                    query += "     , t3.bank_cd     /* 은행코드 */ "
                    query += "     , t3.bank_nm     /* 은행명 */ "
                    query += "     , t3.bank_dpsr   /* 예금주 */ "
                    query += "     , t3.pr_yr       /* 직전 학년도 */ "
                    query += "     , t3.pr_sch_yr   /* 직전 학년 */ "
                    query += "     , t3.pr_term_div /* 직전학기코드 */ "
                    query += "     , t3.score01     /* 직전학기 석차 */ "
                    query += "     , t3.score02     /* 직전학기 총원 */ "
                    query += "     , t3.score03     /* 직전학기 학점 */ "
                    query += "     , t3.score04     /* 봉사점수합계 */ "
                    query += "     , t3.score05     /* 자격증 개수 */ "
                    query += " from vw_nanum_stdt t3     /* 부산대학교 학생 정보 */ "              
                    query += " where t3.apl_id='"+v_userid+"'" 
                    # query += " where t3.apl_id='201866148'"                 
                    conn = pymssql.connect(server='192.168.2.124', user='nanum', password='n@num*!@', database='hakjuk', port='1221')
                    cursor = conn.cursor()   
                    cursor.execute(query)  
                    row = cursor.fetchone()  
                    print(row)
                    if row == None:
                        context = {'loginStudent': 'fail',}
                    else:    
                        message = "login_notFound"
                        while row:
                            message = "Ok"
                            # 삭제
                            delete_query = " delete from service20_vw_nanum_stdt where apl_id = '"+str(row[0])+"' "
                            cursor_delete = connection.cursor()
                            delete_query_result = cursor_delete.execute(delete_query)                       
                            # 삭제
                            
                            # insert
                            insert_query = " insert into service20_vw_nanum_stdt (apl_id      /* 학번 */ "
                            insert_query += " , apl_nm      /* 성명 */ "
                            insert_query += " , apl_nm_e    /* 성명_영문 */ "
                            insert_query += " , unv_cd      /* 대학교코드 */ "
                            insert_query += " , unv_nm      /* 대학교명 */ "
                            insert_query += " , grad_div_cd /* 대학원구분코드 */ "
                            insert_query += " , grad_div_nm /* 대학원구분명 */ "
                            insert_query += " , cllg_cd     /* 대학코드 */ "
                            insert_query += " , cllg_nm     /* 대학명 */ "
                            insert_query += " , dept_cd     /* 학과코드 */ "
                            insert_query += " , dept_nm     /* 학과명 */ "
                            insert_query += " , mjr_cd      /* 전공코드 */ "
                            insert_query += " , mjr_nm      /* 전공명 */ "
                            insert_query += " , brth_dt     /* 생년월일 */ "
                            insert_query += " , gen_cd      /* 성별코드 */ "
                            insert_query += " , gen_nm      /* 성별명 */ "
                            insert_query += " , yr          /* 학년도 */ "
                            insert_query += " , sch_yr      /* 학년 */ "
                            insert_query += " , term_div    /* 학기코드 */ "
                            insert_query += " , term_nm     /* 학기명 */ "
                            insert_query += " , stds_div    /* 학적상태코드 */ "
                            insert_query += " , stds_nm     /* 학적상태명 */ "
                            insert_query += " , mob_no      /* 휴대전화번호 */ "
                            insert_query += " , tel_no      /* 집전화 */ "
                            insert_query += " , tel_no_g    /* 보호자연락처 */ "
                            insert_query += " , h_addr      /* 집주소 */ "
                            insert_query += " , post_no     /* 우편번호 */ "
                            insert_query += " , email_addr  /* 이메일주소 */ "
                            insert_query += " , bank_acct   /* 은행계좌번호 */ "
                            insert_query += " , bank_cd     /* 은행코드 */ "
                            insert_query += " , bank_nm     /* 은행명 */ "
                            insert_query += " , bank_dpsr   /* 예금주 */ "
                            insert_query += " , pr_yr       /* 직전 학년도 */ "
                            insert_query += " , pr_sch_yr   /* 직전 학년 */ "
                            insert_query += " , pr_term_div /* 직전학기코드 */ "
                            insert_query += " , score01     /* 직전학기 석차 */ "
                            insert_query += " , score02     /* 직전학기 총원 */ "
                            insert_query += " , score03     /* 직전학기 학점 */ "
                            insert_query += " , score04     /* 봉사점수합계 */ "
                            insert_query += " , score05     /* 자격증 개수 */ "
                            insert_query += " ) values ("
        #                   insert_query += " (select ifnull(max(id)+1,1) from service20_vw_nanum_stdt)  "
                            insert_query += " CASE WHEN '"+str(row[0])+"' =  'None' THEN NULL ELSE '"+str(row[0])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[1])+"' =  'None' THEN NULL ELSE '"+str(row[1])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[2])+"' =  'None' THEN NULL ELSE '"+str(row[2])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[3])+"' =  'None' THEN NULL ELSE '"+str(row[3])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[4])+"' =  'None' THEN NULL ELSE '"+str(row[4])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[5])+"' =  'None' THEN NULL ELSE '"+str(row[5])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[6])+"' =  'None' THEN NULL ELSE '"+str(row[6])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[7])+"' =  'None' THEN NULL ELSE '"+str(row[7])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[8])+"' =  'None' THEN NULL ELSE '"+str(row[8])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[9])+"' =  'None' THEN NULL ELSE '"+str(row[9])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[10])+"' =  'None' THEN NULL ELSE '"+str(row[10])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[11])+"' =  'None' THEN NULL ELSE '"+str(row[11])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[12])+"' =  'None' THEN NULL ELSE '"+str(row[12])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[13])+"' =  'None' THEN NULL ELSE '"+str(row[13])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[14])+"' =  'None' THEN NULL ELSE '"+str(row[14])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[15])+"' =  'None' THEN NULL ELSE '"+str(row[15])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[16])+"' =  'None' THEN NULL ELSE '"+str(row[16])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[17])+"' =  'None' THEN NULL ELSE '"+str(row[17])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[18])+"' =  'None' THEN NULL ELSE '"+str(row[18])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[19])+"' =  'None' THEN NULL ELSE '"+str(row[19])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[20])+"' =  'None' THEN NULL ELSE '"+str(row[20])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[21])+"' =  'None' THEN NULL ELSE '"+str(row[21])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[22])+"' =  'None' THEN NULL ELSE '"+str(row[22])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[23])+"' =  'None' THEN NULL ELSE '"+str(row[23])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[24])+"' =  'None' THEN NULL ELSE '"+str(row[24])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[25])+"' =  'None' THEN NULL ELSE '"+str(row[25])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[26])+"' =  'None' THEN NULL ELSE '"+str(row[26])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[27])+"' =  'None' THEN NULL ELSE '"+str(row[27])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[28])+"' =  'None' THEN NULL ELSE '"+str(row[28])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[29])+"' =  'None' THEN NULL ELSE '"+str(row[29])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[30])+"' =  'None' THEN NULL ELSE '"+str(row[30])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[31])+"' =  'None' THEN NULL ELSE '"+str(row[31])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[32])+"' =  'None' THEN NULL ELSE '"+str(row[32])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[33])+"' =  'None' THEN NULL ELSE '"+str(row[33])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[34])+"' =  'None' THEN NULL ELSE '"+str(row[34])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[35])+"' =  'None' THEN NULL ELSE '"+str(row[35])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[36])+"' =  'None' THEN NULL ELSE '"+str(row[36])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[37])+"' =  'None' THEN NULL ELSE '"+str(row[37])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[38])+"' =  'None' THEN NULL ELSE '"+str(row[38])+"' END"
                            insert_query += " , CASE WHEN '"+str(row[39])+"' =  'None' THEN NULL ELSE '"+str(row[39])+"' END"
                            insert_query += " )"                    
                            cursor2 = connection.cursor()
                            query_result = cursor2.execute(insert_query)    
                            # insert

                            mentor_query = " select mntr_id from service20_mentor where apl_id = '"+str(row[0])+"'"
                            mentor_cursor = connection.cursor()
                            query_result = mentor_cursor.execute(mentor_query)    

                            if query_result == 0:
                                v_mntr_id = ''
                            else:
                                #mentor_query
                                rows_mentor = mentor.objects.filter(apl_id=str(row[0]))[0]
                                
                                v_mntr_id = str(rows_mentor.mntr_id)                            
                                                
                            context = {'message': message,
                            'apl_id' : str(row[0]),
                            'apl_nm' : str(row[1]),
                            'univ_cd' : str(row[3]),
                            'univ_nm' : str(row[4]),
                            'grad_div_cd' : str(row[5]),
                            'grad_div_nm' : str(row[6]),
                            'cllg_cd' : str(row[7]),
                            'cllg_nm' : str(row[8]),
                            'dept_cd' : str(row[9]),
                            'dept_nm' : str(row[10]),
                            'mjr_cd' : str(row[11]),
                            'mjr_nm' : str(row[12]),
                            'brth_dt' : str(row[13]),
                            'gen_cd' : str(row[14]),
                            'gen_nm' : str(row[15]),
                            'yr' : str(row[16]),
                            'sch_yr' : str(row[17]),
                            'term_div' : str(row[18]),
                            'term_nm' : str(row[19]),
                            'stdt_div' : str(row[20]),
                            'stdt_nm' : str(row[21]),
                            'mob_nm' : str(row[22]),
                            'tel_no' : str(row[23]),
                            'tel_no_g' : str(row[24]),
                            'h_addr' : str(row[25]),
                            'post_no' : str(row[26]),
                            'email_addr' : str(row[27]),
                            'bank_acct' : str(row[28]),
                            'bank_cd' : str(row[29]),
                            'bank_nm' : str(row[30]),
                            'bank_dpsr' : str(row[31]),
                            'pr_yr' : str(row[32]),
                            'pr_sch_yr' : str(row[33]),
                            'pr_term_div' : str(row[34]),
                            'score01' : str(row[35]),
                            'score02' : str(row[36]),
                            'score03' : str(row[37]),
                            'score04' : str(row[38]),
                            'score05' : str(row[39]),
                            'mntr_id' : v_mntr_id
                            }
                            row = cursor.fetchone()                                                                     
                        # 로그인처리 - 종료   

        
#         context = {'message': message,'member_id':v_userid}

        return JsonResponse(context,json_dumps_params={'ensure_ascii': True})
                


@csrf_exempt
def login_returnsso(request):
        print("====login_returnsso====")
        a =  request.POST.get('gbn')
        request.session['member_id'] = 'test'
        print("====login_returnsso====")
        print(request.session['member_id'])
        
        message = "Ok"
        context = {'message': message,    }

        return redirect('http://nanum.pusan.ac.kr/login/success.html', { 'context': context })
                
@csrf_exempt
def login_session(request):
        v_member_id = request.session.get('member_id', None)
        if v_member_id == None:
            message = 'NoSession'       
        else:
            message = request.session['member_id']
        context = {'message': message,}
        return JsonResponse(context,json_dumps_params={'ensure_ascii': True})


# 년도 콤보박스 ###################################################
class com_combo_yr_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_detl_code','std_detl_code_nm')


class com_combo_yr(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_yr_Serializer

    def list(self, request):

        queryset = self.get_queryset()
        
        query = " select '1' id,DATE_FORMAT(now(),'%%Y')-1 as std_detl_code,DATE_FORMAT(now(),'%%Y')-1 as std_detl_code_nm "
        query += " union "
        query += " select '2' id,DATE_FORMAT(now(),'%%Y') as std_detl_code,DATE_FORMAT(now(),'%%Y') as std_detl_code_nm "
        query += " union "
        query += " select '3' id,DATE_FORMAT(now(),'%%Y')+1 as std_detl_code,DATE_FORMAT(now(),'%%Y')+1 as std_detl_code_nm "
        query += " union "
        query += " select '4' id,DATE_FORMAT(now(),'%%Y')+2 as std_detl_code,DATE_FORMAT(now(),'%%Y')+2 as std_detl_code_nm "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 학기 콤보박스 ###################################################
class com_combo_termdiv_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_detl_code','std_detl_code_nm')


class com_combo_termdiv(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_termdiv_Serializer

    def list(self, request):

        queryset = self.get_queryset()
        
        query = " select '1' id,'10' as std_detl_code,'1' as std_detl_code_nm "
        query += " union "
        query += " select '2' id,'20' as std_detl_code,'2' as std_detl_code_nm "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 취소사유 콤보박스
class com_combo_cnclRsn_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_grp_code','std_detl_code','std_detl_code_nm','rmrk','sort_seq_no')


class com_combo_cnclRsn(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_cnclRsn_Serializer

    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_user_id = request.GET.get('user_id', "")
        

        queryset = self.get_queryset()
        
        query = " select id,std_grp_code,std_detl_code,std_detl_code_nm,rmrk,sort_seq_no from service20_com_cdd where std_grp_code = 'MS0004' and use_indc = 'Y'"

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)        

class com_combo_repdiv_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_grp_code','std_detl_code','std_detl_code_nm','rmrk','sort_seq_no')


class com_combo_repdiv(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_repdiv_Serializer

    def list(self, request):
        

        queryset = self.get_queryset()
        
        
        query = "select id,std_detl_code";
        query += "     , std_detl_code_nm,sort_seq_no ";
        query += "  from service20_com_cdd";
        query += " where std_grp_code = 'mp0062'";
        query += " order by sort_seq_no "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)        

class com_combo_com_cdd_Serializer(serializers.ModelSerializer):

    class Meta:
        model = com_cdd
        fields = ('std_grp_code','std_detl_code','std_detl_code_nm','rmrk','sort_seq_no')


class com_combo_com_cdd(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_com_cdd_Serializer

    def list(self, request):
        l_code = request.GET.get('code', "")

        queryset = self.get_queryset()
        
        
        query = "select id,std_detl_code";
        query += "     , std_detl_code_nm, sort_seq_no";
        query += "  from service20_com_cdd";
        query += " where std_grp_code = '"+str(l_code)+"'";
        query += " order by sort_seq_no "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)        

class com_combo_program2_Serializer(serializers.ModelSerializer):

    class Meta:
        model = mpgm
        fields = ('mp_id','mp_name','status','yr','apl_term')


class com_combo_program2(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_program2_Serializer

    def list(self, request):
        yr = request.GET.get('yr', "")
        apl_term = request.GET.get('apl_term', "")
        status = request.GET.get('status', "")

        queryset = self.get_queryset()
        
        
        query = "select mp_id";
        query += ", mp_name";
        query += ", status";
        query += ", yr";
        query += ", apl_term";
        query += " from service20_mpgm";
        query += " where yr = '"+yr+"'";
        query += " and apl_term = '"+apl_term+"'";
        query += " order by mp_id "

        queryset = mpgm.objects.raw(query)

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
        
        # l_mp_id = "P182014"
        # l_apl_id = "201610101"

        queryset = self.get_queryset()
        
        query = " select (select std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0052' and std_detl_code = S2.mp_plc and use_indc = 'Y') mp_plc_nm"
        query += " ,(select std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0047' and std_detl_code = S2.grd_rel and use_indc = 'Y') grd_rel_nm "
        query += " , S2.* "
        query += " FROM service20_mp_mtr S1 "
        query += " LEFT JOIN service20_mp_mte S2  ON (S2.MP_ID  = S1.MP_ID "
        query += " AND S2.APL_NO = S1.APL_NO) "
        query += " LEFT JOIN service20_mp_plnh S3 ON (S3.MP_ID    = S1.MP_ID "
        query += " AND S3.APL_NO   = S1.APL_NO) "
        query += " WHERE 1=1 "
        query += " AND S1.MP_ID      = '"+l_mp_id+"'     /* 멘토링 프로그램ID */ "
        query += " AND S1.APL_ID    =  '"+l_apl_id+"' "


        queryset = mp_mte.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)        

# 취소사유 콤보박스
class com_combo_program_Serializer(serializers.ModelSerializer):

    mp_name = serializers.SerializerMethodField()
    apl_no = serializers.SerializerMethodField()
    class Meta:
        model = mpgm
        fields = ('mp_id','apl_no','mp_name')

    def get_mp_name(self, obj):
        return obj.mp_name
    def get_apl_no(self, obj):
        return obj.apl_no

class com_combo_program(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = com_combo_program_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")
        

        queryset = self.get_queryset()
        
        query = " select A.mp_id "
        query += " , A.apl_no "
        query += " , B.mp_name "
        query += " FROM service20_mp_mtr A "
        query += " , service20_mpgm B "
        query += " WHERE apl_id = '"+str(apl_id)+"' "
        query += " AND mntr_id IS NOT null "
        query += " AND A.mp_id = B.mp_id "

        queryset = mpgm.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data) 

# 모집상태 콤보박스
class com_combo_ms_status_Serializer(serializers.ModelSerializer):

    
    class Meta:
        model = com_cdd
        fields = ('std_detl_code','std_detl_code_nm')


class com_combo_ms_status(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_ms_status_Serializer

    def list(self, request):
        

        queryset = self.get_queryset()
        
        query = " select '0'id,''std_detl_code,'전체'std_detl_code_nm "
        query += " union  "
        query += " select id,std_detl_code,std_detl_code_nm from service20_com_cdd where std_grp_code = 'MS0001' "
        query += " union  "
        query += " select '','xx','모집완료'  "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)                

# 모집상태 콤보박스
class com_combo_mp_status_Serializer(serializers.ModelSerializer):

    
    class Meta:
        model = com_cdd
        fields = ('std_detl_code','std_detl_code_nm')


class com_combo_mp_status(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = com_combo_mp_status_Serializer

    def list(self, request):
        

        queryset = self.get_queryset()
        
        query = " select '0'id,''std_detl_code,'전체'std_detl_code_nm "
        query += " union  "
        query += " select id,std_detl_code,std_detl_code_nm from service20_com_cdd where std_grp_code = 'MP0001' "
        query += " union  "
        query += " select '','xx','모집완료'  "

        queryset = com_cdd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)                


# 어학점수
class com_user_fe_Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = vw_nanum_foreign_exam
        fields = ('apl_id','apl_nm','lang_kind_cd','lang_kind_nm','lang_cd','lang_nm','lang_detail_cd','lang_detail_nm','frexm_nm','score','grade')


class com_user_fe(generics.ListAPIView):
    queryset = ms_apl.objects.all()
    serializer_class = com_user_fe_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        
        query = "select t3.id,t3.apl_id         /* 학번 */"
        query += "     , t3.apl_nm         /* 성명 */"
        query += "     , t3.lang_kind_cd   /* 어학종류코드 */"
        query += "     , t3.lang_kind_nm   /* 어학종류명 */"
        query += "     , t3.lang_cd        /* 어학상위코드 */"
        query += "     , t3.lang_nm        /* 어학상위코드명 */"
        query += "     , t3.lang_detail_cd /* 어학하위코드 */"
        query += "     , t3.lang_detail_nm /* 어학하위코드명 */"
        query += "     , t3.frexm_nm       /* 외국어시험명 */"
        query += "     , t3.score          /* 시험점수 */"
        query += "     , t3.grade          /* 시험등급 */"
        query += "  from service20_vw_nanum_foreign_exam t3     /* 유효한 외국어 성적 리스트 view(임시) */"
        query += " where 1=1"
        query += " and t3.apl_id='"+str(ida)+"'" 

        queryset = vw_nanum_foreign_exam.objects.raw(query)
        print(query)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 봉사점수
class com_user_sa_Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = vw_nanum_service_activ
        fields = ('apl_id','apl_nm','nation_inout_cd','nation_inout_nm','sch_inout_cd','sch_inout_nm','activity_nm','manage_org_nm','start_date','start_time','end_date','end_time','tot_time')


class com_user_sa(generics.ListAPIView):
    queryset = ms_apl.objects.all()
    serializer_class = com_user_sa_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        

        query = "select t3.id,t3.apl_id          /* 학번 */"
        query += "     , t3.apl_nm          /* 성명 */"
        query += "     , t3.nation_inout_cd /* 국내외구분코드 */"
        query += "     , t3.nation_inout_nm /* 국내외구분명 */"
        query += "     , t3.sch_inout_cd    /* 교내외구분코드 */"
        query += "     , t3.sch_inout_nm    /* 교내외구분명 */"
        query += "     , t3.activity_nm     /* 봉사명 */"
        query += "     , t3.manage_org_nm   /* 주관기관명 */"
        query += "     , t3.start_date      /* 시작일자 */"
        query += "     , t3.start_time      /* 시작시간 */"
        query += "     , t3.end_date        /* 종료일자 */"
        query += "     , t3.end_time        /* 종료시간 */"
        query += "     , t3.tot_time        /* 총시간 */"
        query += "  from service20_vw_nanum_service_activ t3     /* 학생 봉사 시간 view(임시) */"
        query += " where 1=1"
        query += "   AND apl_id = '"+str(ida)+"' "

        queryset = vw_nanum_service_activ.objects.raw(query)
        print(query)
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

class MS0101M_list_chk_1_Serializer(serializers.ModelSerializer):

    en_cnt = serializers.SerializerMethodField()
    mp_select01 = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    class Meta:
        model = vw_nanum_stdt
        fields = ('sch_yr','en_cnt','mp_select01','name','code')

    def get_mp_select01(self, obj):
        return obj.mp_select01
    def get_name(self, obj):
        return obj.name    
    def get_code(self, obj):
        return obj.code
    def get_en_cnt(self, obj):
        return obj.en_cnt        

class MS0101M_list_chk_1(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MS0101M_list_chk_1_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")
        ms_id = request.GET.get('ms_id', "")


        # 학년체크
        query = " select t1.id,t1.sch_yr, IFNULL(t4.en_cnt,0) as en_cnt, fn_mp_sub_desc_select_01('"+ms_id+"','MS0010') as mp_select01"
        query += "     , CASE WHEN IFNULL(t4.en_cnt,0) > 0 THEN '신청' ELSE CONCAT('신청불가:', fn_mp_sub_desc_select_01('"+ms_id+"','MS0010'), '만 신청가능') END  as name "
        query += "     , CASE WHEN IFNULL(t4.en_cnt,0) > 0 THEN 'Y' ELSE 'N' END  as code "
        query += "  FROM service20_vw_nanum_stdt t1     /* 부산대학교 학생 정보 */ "
        query += " LEFT JOIN (SELECT t2.apl_id, COUNT(*) en_cnt "
        query += "              FROM service20_vw_nanum_stdt t2     /* 부산대학교 학생 정보 */ "
        query += "             WHERE t2.sch_yr IN  "
        query += "                   (SELECT t3.att_cdd "
        query += "                      FROM service20_ms_sub t3 "
        query += "                     WHERE t3.ms_id   = '"+ms_id+"' "
        query += "                       AND t3.att_id  = 'MS0010' "
        query += "                       AND t3.att_cdh = 'MS0010' "
        query += "                   ) "
        query += "             GROUP BY t2.apl_id "
        query += "            ) t4 ON (t4.apl_id = t1.apl_id) "
        query += " WHERE t1.apl_id = '"+apl_id+"' "

        print(query)
        queryset = vw_nanum_stdt.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class MS0101M_list_chk_2_Serializer(serializers.ModelSerializer):

    
    name = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    class Meta:
        model = vw_nanum_stdt
        fields = ('name','code')

    def get_name(self, obj):
        return obj.name    
    def get_code(self, obj):
        return obj.code

class MS0101M_list_chk_2(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MS0101M_list_chk_2_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")
        ms_id = request.GET.get('ms_id', "")


        # -- 직전학기 학점 제한
        query = " select t2.id,CASE WHEN t2.score03 >= t3.att_val THEN '신청' ELSE CONCAT('신청불가 : 학점', t3.att_val, '미만') END as name "
        query += "      , CASE WHEN t2.score03 >= t3.att_val THEN 'Y' ELSE 'N' END as code "
        query += "   FROM service20_vw_nanum_stdt t2     /* 부산대학교 학생 정보 */ "
        query += "      , (  /* 학점 제한 */ "
        query += "         select cast(att_val as unsigned) att_val "
        query += "           FROM service20_ms_sub t3 "
        query += "          WHERE t3.ms_id   = '"+ms_id+"' "
        query += "            AND t3.att_id  = 'MP0071' "
        query += "            AND t3.att_cdh = 'MP0071' "
        query += "            AND t3.att_cdd = '10' "
        query += "       ) t3 "
        query += "   WHERE t2.apl_id = '"+apl_id+"' "

        print(query)
        queryset = vw_nanum_stdt.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class MS0101M_list_Serializer(serializers.ModelSerializer):

    applyFlag = serializers.SerializerMethodField()
    applyFlagNm = serializers.SerializerMethodField()
    applyStatus = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    statusCode = serializers.SerializerMethodField()
    status_nm  = serializers.SerializerMethodField()
    sup_org_nm = serializers.SerializerMethodField()
    
    apl_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    apl_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    trn_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    trn_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = msch
        fields = ('ms_id','ms_name','status','statusCode','yr','yr_seq','sup_org','applyFlag','applyStatus','apl_fr_dt','apl_to_dt','cnt_trn','status','status_nm','applyFlagNm','sup_org_nm','trn_fr_dt','trn_to_dt')

    def get_applyFlag(self, obj):
        return obj.applyFlag    
    def get_applyFlagNm(self, obj):
        return obj.applyFlagNm    
    def get_applyStatus(self, obj):
        
        if obj.applyFlag == 'N':
            return '지원'
        else:
            # print(obj.applyFlag)
            # rows = com_cdd.objects.filter(std_grp_code='MP0053',std_detl_code=obj.applyFlag)
            # return str(rows[0].std_detl_code_nm)
            return '미지원'
        return obj.applyStatus    

    def get_statusCode(self,obj):
        return obj.statusCode 

    def get_status_nm(self,obj):
        return obj.status_nm   
    def get_status(self,obj):
        return obj.status
    def get_sup_org_nm(self,obj):
        return obj.sup_org_nm

class MS0101M_list(generics.ListAPIView):
    queryset = msch.objects.all()
    serializer_class = MS0101M_list_Serializer

    def list(self, request):
        l_yr = request.GET.get('yr', None)
        l_apl_term = request.GET.get('trn_term', None)
        l_user_id = request.GET.get('user_id', None)
        l_status = request.GET.get('status', '')


        query = " select apl_to_dt,  "
        query += "        IF(A.status = '10'  "
        query += "           AND Now() > A.apl_to_dt, 'xx', A.status) AS statusCode,  "
        query += "        IF(A.status = '10'  "
        query += "           AND Now() > A.apl_to_dt, '모집완료',  "
        query += "        (SELECT std_detl_code_nm  "
        query += "         FROM   service20_com_cdd  "
        query += "         WHERE  std_grp_code = 'MS0001'  "
        query += "                AND use_indc = 'y'  "
        query += "                AND std_detl_code = A.status))      AS status_nm,  "
        query += "        Ifnull(B.status, 'N')                       AS applyFlag,  "
    
        query += " CASE  "
        query += "      WHEN Ifnull(B.status, 'N') = 'N' THEN '미지원' "
        query += "      ELSE (SELECT std_detl_code_nm  "
        query += "              FROM   service20_com_cdd  "
        query += "              WHERE  std_grp_code = 'MS0024'  "
        query += "                 AND std_detl_code = B.status)  "
        query += " end                                         AS applyFlagNm,  "
        query += " c1.std_detl_code_nm   AS sup_org_nm, "
        query += "        A.*  "
        query += " FROM   service20_msch A  "
        query += "        LEFT JOIN service20_ms_apl B  "
        query += "               ON ( A.ms_id = B.ms_id  "
        # query += "                    AND A.yr = B.yr  "
        query += "                    AND B.apl_id = '"+str(l_user_id)+"' )  "
        query += "        LEFT JOIN service20_com_cdd c1 ON (c1.std_grp_code  = 'MP0004' AND c1.std_detl_code = A.sup_org) "
        query += " WHERE  A.yr = '"+str(l_yr)+"'  "
        query += "        AND A.apl_term = '"+str(l_apl_term)+"'  "
        # query += "        AND (SELECT Count(1)  "
        # query += "             FROM   service20_mentor  "
        # query += "             WHERE  apl_id = '"+str(ida)+"') > 0  "
        query += "        AND IF(A.status = '10'  "
        query += "               AND Now() > A.apl_to_dt, 'xx', A.status) LIKE  "
        query += "            Ifnull(Nullif('"+str(l_status)+"', ''), '%%')  "
        query += "            || '%%'  "
        query += " ORDER  BY A.apl_fr_dt DESC,  "
        query += "           A.apl_to_dt DESC  "
        queryset = msch.objects.raw(query)

        
        


        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 멘토스쿨 질문유형 가져오기
class MS0101M_quest_Serializer(serializers.ModelSerializer):

    std_detl_code_nm = serializers.SerializerMethodField()
    std_detl_code = serializers.SerializerMethodField()
    rmrk = serializers.SerializerMethodField()
    class Meta:
        model = ms_sub
        fields = ('id','ms_id','att_id','att_seq','att_cdh','att_cdd','att_val','use_yn','sort_seq','std_detl_code','std_detl_code_nm','rmrk')

        
    def get_std_detl_code(self,obj):
        return obj.std_detl_code
        
    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm

    def get_rmrk(self,obj):
        return obj.rmrk    

# 멘토스쿨 질문유형 가져오기
class MS0101M_quest(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = MS0101M_quest_Serializer
    def list(self, request):
        #ms_sub 테이블에서 질문내역 조회
        key1 = request.GET.get('ms_id', None)           
        
        query = "select B.std_detl_code,B.std_detl_code_nm,B.rmrk,A.* from service20_ms_sub A left outer join service20_com_cdd B on (A.att_id = B.std_grp_code and A.att_cdd = B.std_detl_code) where A.att_id='MS0014' and B.use_indc = 'Y' and A.ms_id = '"+key1+"'"
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
    
    client_ip = request.META['REMOTE_ADDR']

    #created,created_flag = vw_nanum_stdt.apl_id.get_or_create(user=request.user)
    ms_id = programId
    ms_apl_max = ms_apl.objects.all().aggregate(vlMax=Max('apl_no'))
    rows = vw_nanum_stdt.objects.filter(apl_id=ida)[0]
    #ms_apl_max = ms_apl.objects.all().last()
    #ms_apl_max = ms_apl_max + 1
    apl_no = ms_apl_max
    apl_id = ida
    v_gen = ""
    if str(rows.gen_cd) == "1":
        v_gen = "M"
    else:
        v_gen = "F"
    
    max_no = ms_apl_max['vlMax']    

    if max_no == None:
        apl_no = 0
    else:
        apl_no = ms_apl_max['vlMax']
        apl_no = apl_no + 1
        
    query = "select ifnull(max(apl_no),1) as apl_no from service20_ms_apl where apl_id = '"+apl_id+"' and ms_id = '"+ms_id+"'"  
    cursor = connection.cursor()
    cursor.execute(query)    
    results = namedtuplefetchall(cursor)    
    apl_no = results[0].apl_no

    query = " select t2.ms_id,t2.yr FROM service20_msch t2  WHERE 1=1 "
    query += " AND t2.ms_id          = '"+ms_id+"'"
    queryset = msch.objects.raw(query)[0]

    rowsChk = ms_apl.objects.filter(apl_id=apl_id,ms_id=ms_id).exists()

    if rowsChk == True:
        context = {'message': 'duplicate'}
    else:
        model_instance = ms_apl(
            ms_id=ms_id, 
            apl_no=apl_no, 
            mntr_id=ida,
            apl_id=apl_id,
            apl_nm=rows.apl_nm,
            unv_cd=rows.unv_cd,
            unv_nm=rows.unv_nm,
            cllg_cd=rows.cllg_cd,
            cllg_nm=rows.cllg_nm,
            dept_cd=rows.dept_cd,
            dept_nm=rows.dept_nm,
            brth_dt=rows.brth_dt,
            gen=v_gen,
            yr=queryset.yr,
            term_div=rows.term_div,
            sch_yr=rows.sch_yr,
            mob_no=rows.mob_no.replace('-', ''),
            tel_no=rows.tel_no.replace('-', ''),
            tel_no_g=rows.tel_no_g.replace('-', ''),
            h_addr=rows.h_addr,
            email_addr=rows.email_addr,
            # bank_acct=rows.bank_acct,
            # bank_cd=rows.bank_cd,
            # bank_nm=rows.bank_nm,
            score1=rows.score01,
            score2=rows.score02,
            score3=rows.score03,
            score4=rows.score04,
            score5=rows.score05,
            status='10', # 지원
            ins_id=apl_id,
            ins_ip=str(client_ip),
            ins_dt=datetime.datetime.today()
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

        
        # mp_mntr/ms_apl  -> mp_id만 조건 걸어서 count(*)
        # 해당 cnt값을 mpgm/msch -> cnt_apl

        update_text = " update service20_msch a "
        update_text += " SET a.cnt_apl = (select count(*) from service20_ms_apl where ms_id = '"+ms_id+"') "
        update_text += " WHERE 1=1 "
        update_text += " AND a.ms_id = '"+ms_id+"' "
        
        cursor = connection.cursor()
        query_result = cursor.execute(update_text)    
            
        context = {'message': 'Ok'}

    #return HttpResponse(json.dumss(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

@csrf_exempt
def MS0101M_detail(request):
    ida = request.POST.get('user_id', None)
    ms_ida = request.POST.get('ms_id', None)
    l_yr = request.POST.get('yr', None)
    
    
    #created,created_flag = vw_nanum_stdt.apl_id.get_or_create(user=request.user)
    created_flag = vw_nanum_stdt.objects.filter(apl_id=ida).exists()
    msch_flag = msch.objects.filter(ms_id=ms_ida,status='20').exists()
    # ms_apl_flag = ms_apl.objects.filter(apl_id=ida,ms_id=ms_ida).exists()
    ms_apl_flag = ms_apl.objects.filter(apl_id=ida,yr=l_yr,ms_id=ms_ida).exists()

    if not ms_apl_flag:
        applyYn = 'N'
    else:
        applyYn = 'Y'

    #rows = vw_nanum_stdt.objects.filter(apl_id=ida)
    #rows2 = vw_nanum_stdt.objects.get("apl_nm")
    if not created_flag:
        message = "Fail"
        context = {'message': message}
    else:
        if not msch_flag:
            message = "Fail"
            context = {'message': message}
        else:

            message = "Ok"
            rows = vw_nanum_stdt.objects.filter(apl_id=ida)[0]
            rows2 = ms_sub.objects.filter(ms_id=ms_ida)
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
                        'unv_cd' : rows.unv_cd,
                        'unv_nm' : rows.unv_nm,
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
                        'stds_div' : rows.stds_div,
                        'stds_nm' : rows.stds_nm,
                        'mob_no' : rows.mob_no,
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
                        'ms_id' : rows3.ms_id,
                        'ms_name' : rows3.ms_name,
                        }
    

    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

class MS0101M_adm_list_Serializer(serializers.ModelSerializer):
    
    ms_name = serializers.SerializerMethodField()
    pr_yr = serializers.SerializerMethodField()
    pr_sch_yr = serializers.SerializerMethodField()
    pr_term_div = serializers.SerializerMethodField()
    # statusNm = serializers.SerializerMethodField()
    statusCode = serializers.SerializerMethodField()
    status_nm = serializers.SerializerMethodField()
    # acpt_dt = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = ms_apl
        fields = ('ms_id','apl_no','mntr_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','fnl_rslt','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','ms_name','pr_yr','pr_sch_yr','pr_term_div','statusCode','status_nm')

    def get_ms_name(self,obj):
        return obj.ms_name

    def get_pr_yr(self,obj):
        return obj.pr_yr

    def get_pr_sch_yr(self,obj):
        return obj.pr_sch_yr

    def get_pr_term_div(self,obj):
        return obj.pr_term_div    

    def get_statusCode(self,obj):
        return obj.statusCode 

    def get_status_nm(self,obj):
        return obj.status_nm
    def get_status(self,obj):
        return obj.status

class MS0101M_adm_list(generics.ListAPIView):
    queryset = ms_apl.objects.all()
    serializer_class = MS0101M_adm_list_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        ms_ida = request.GET.get('ms_id', None)
        l_yr = request.GET.get('yr', None)
        
        # msch
        query = " select   "
        query += " if(C.status = '10'  "
        query += " and now() > C.apl_to_dt, 'xx', C.status) as statusCode,  "
        query += " if(C.status = '10'  "
        query += " and now() > C.apl_to_dt, '모집완료', (select std_detl_code_nm  "
        query += " from   service20_com_cdd  "
        query += " where  "
        query += " std_grp_code = 'MS0001'  "
        query += " and use_indc = 'y'  "
        query += " and std_detl_code = C.status)) as status_nm,  "

        query += " C.ms_name,B.pr_yr,B.pr_sch_yr,B.pr_term_div,A.* from service20_ms_apl A,service20_vw_nanum_stdt B,service20_msch C where A.apl_id=B.apl_id and A.ms_id = C.ms_id and A.yr='"+l_yr+"' and A.ms_id = '"+ms_ida+"' and A.apl_id='"+ida+"'"
        
        queryset = ms_apl.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램(관리자) - 어학
class MS0101M_adm_list_fe_Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = ms_apl_fe
        fields = ('frexm_cd','frexm_nm','score','grade')


class MS0101M_adm_list_fe(generics.ListAPIView):
    queryset = ms_apl.objects.all()
    serializer_class = MS0101M_adm_list_fe_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        ms_ida = request.GET.get('ms_id', None)
        l_yr = request.GET.get('yr', None)
        
        query = " select id,  "
        query += "        frexm_cd,  "
        query += "        frexm_nm,  "
        query += "        score,  "
        query += "        grade,  "
        query += "   fn_mp_mtr_fe_select_01('"+str(ms_ida)+"','"+str(ida)+"') as fn_score "
        query += " FROM   service20_ms_apl_fe  "
        query += " WHERE  ms_id = '"+str(ms_ida)+"'  "
        query += "        AND apl_id = '"+str(ida)+"' "

        queryset = ms_apl_fe.objects.raw(query)
        print(query)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램(관리자) - 봉사
class MS0101M_adm_list_sa_Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = ms_apl_sa
        fields = ('ms_id','apl_no','sa_no','apl_id','apl_nm','nation_inout_cd','nation_inout_nm','sch_inout_cd','sch_inout_nm','activity_nm','manage_org_nm','start_date','start_time','end_date','end_time','tot_time')


class MS0101M_adm_list_sa(generics.ListAPIView):
    queryset = ms_apl.objects.all()
    serializer_class = MS0101M_adm_list_sa_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        ms_ida = request.GET.get('ms_id', None)
        l_yr = request.GET.get('yr', None)
        
        query = " select a.* , "
        query += "   fn_mp_mtr_sa_select_01('"+str(ms_ida)+"','"+str(ida)+"') as fn_score "
        query += " FROM   service20_ms_apl_sa a  "
        query += " WHERE  ms_id = '"+str(ms_ida)+"'  "
        query += "        AND apl_id = '"+str(ida)+"' "

        queryset = ms_apl_sa.objects.raw(query)
        print(query)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 멘토스쿨(관리자) - 질문2
class MS0101M_adm_quest_Serializer2(serializers.ModelSerializer):

    
    std_detl_code = serializers.SerializerMethodField()
    std_detl_code_nm = serializers.SerializerMethodField()
    rmrk = serializers.SerializerMethodField()

    class Meta:
        model = ms_ans
        fields = ('id','ms_id','test_div','apl_no','ques_no','apl_id','apl_nm','sort_seq','ans_t1','ans_t2','ans_t3','score','std_detl_code','std_detl_code_nm','rmrk')

    def get_std_detl_code(self,obj):
        return obj.std_detl_code

    def get_std_detl_code_nm(self,obj):
        return obj.std_detl_code_nm

    def get_rmrk(self,obj):
        return obj.rmrk

# 멘토스쿨(관리자) - 질문
class MS0101M_adm_quest(generics.ListAPIView):
    queryset = com_cdd.objects.all()
    serializer_class = MS0101M_adm_quest_Serializer2
    def list(self, request):
        #ms_sub 테이블에서 질문내역 조회
        key1 = request.GET.get('ms_id', None) 
        l_user_id = request.GET.get('user_id', None)           
        l_exist = ms_sub.objects.filter(ms_id=key1).exists()
        
        query = "select B.std_detl_code,B.std_detl_code_nm,B.rmrk,A.* from service20_ms_ans A, service20_com_cdd B where A.ques_no = B.std_detl_code and B.use_indc = 'Y' and B.std_grp_code in (select att_cdh from service20_ms_sub where att_id='MS0014' and ms_id = '"+str(key1)+"') and A.ms_id = '"+str(key1)+"' and apl_id = '"+str(l_user_id)+"'"
        queryset = ms_ans.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토스쿨 수락
@csrf_exempt
def MS0101M_adm_acpt_save(request):
    ms_id = request.POST.get('ms_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    update_text = " update service20_ms_apl a "
    update_text += " SET a.acpt_dt = NOW() "
    update_text += " , a.acpt_div = 'Y' "
    update_text += " , a.acpt_cncl_rsn = null "
    update_text += " WHERE 1=1 "
    update_text += " AND a.ms_id = '"+ms_id+"' "
    update_text += " AND a.apl_no = '"+apl_no+"' "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)

        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

# 멘토스쿨 수락취소
@csrf_exempt
def MS0101M_adm_acpt_cancle(request):
    ms_id = request.POST.get('ms_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")
    acpt_cncl_rsn = request.POST.get('acpt_cncl_rsn', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    update_text = " update service20_ms_apl a "
    update_text += " SET a.acpt_dt = null "
    update_text += " , a.acpt_div = 'N' "
    update_text += " , a.acpt_cncl_rsn = '"+acpt_cncl_rsn+"' "
    update_text += " WHERE 1=1 "
    update_text += " AND a.ms_id = '"+ms_id+"' "
    update_text += " AND a.apl_no = '"+apl_no+"' "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)

        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True}) 

# 멘토스쿨 update
@csrf_exempt
def MS0101M_adm_update(request):
    ms_id = request.POST.get('ms_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")
    acpt_cncl_rsn = request.POST.get('acpt_cncl_rsn', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    maxRow = request.POST.get('maxRow', 0)

    update_text = " update service20_ms_apl a "
    update_text += " SET a.status = '10' "
    update_text += " WHERE 1=1 "
    update_text += " AND a.ms_id = '"+str(ms_id)+"' "
    update_text += " AND a.apl_id = '"+str(apl_id)+"' "
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)

    apl_max = int(maxRow)

    for i in range(0,apl_max):
        anst2 = request.POST.get('que'+str(i+1), None)
        ques_no = request.POST.get('ques_no'+str(i+1), None)
        ans_t2 = request.POST.get('ans_t2_'+str(i+1), None)

        update_text = " update service20_ms_ans a "
        update_text += " SET a.ans_t2 = '"+str(ans_t2)+"' "
        update_text += " WHERE 1=1 "
        update_text += " AND a.mp_id = '"+str(ms_id)+"' "
        update_text += " AND a.apl_no = '"+str(apl_no)+"' "
        update_text += " AND a.ques_no = '"+str(ques_no)+"' "
        
        cursor = connection.cursor()
        query_result = cursor.execute(update_text)

        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True}) 

# 멘토스쿨 cancle
@csrf_exempt
def MS0101M_adm_cancle(request):
    ms_id = request.POST.get('ms_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")
    acpt_cncl_rsn = request.POST.get('acpt_cncl_rsn', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    update_text = " update service20_msch a "
    update_text += " SET status = '19' "
    update_text += " , doc_cncl_dt = now() "
    update_text += " WHERE 1=1 "
    update_text += " AND a.ms_id = '"+ms_id+"' "
    update_text += " AND a.apl_no = '"+apl_no+"' "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)


    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})   

class MS0101M_report_list_Serializer(serializers.ModelSerializer):
    
    ms_name = serializers.SerializerMethodField()
    pr_yr = serializers.SerializerMethodField()
    pr_sch_yr = serializers.SerializerMethodField()
    pr_term_div = serializers.SerializerMethodField()
    statusNm = serializers.SerializerMethodField()
    statusCode = serializers.SerializerMethodField()
    pr_term_cnt = serializers.SerializerMethodField()
    trn_term_nm = serializers.SerializerMethodField()
    trn_term = serializers.SerializerMethodField()
    mpgm_yr = serializers.SerializerMethodField()


    # acpt_dt = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = ms_apl
        fields = ('ms_id','apl_no','mntr_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','fnl_rslt','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','ms_name','pr_yr','pr_sch_yr','pr_term_div','statusNm','statusCode','pr_term_cnt','trn_term_nm','trn_term','mpgm_yr')
    def get_ms_name(self,obj):
        return obj.ms_name

    def get_pr_yr(self,obj):
        return obj.pr_yr

    def get_pr_sch_yr(self,obj):
        return obj.pr_sch_yr

    def get_pr_term_div(self,obj):
        return obj.pr_term_div    

    def get_pr_term_cnt(self,obj):
        return obj.pr_term_cnt
    def get_trn_term_nm(self,obj):
        return obj.trn_term_nm
    def get_trn_term(self,obj):
        return obj.trn_term
    def get_mpgm_yr(self,obj):
        return obj.mpgm_yr

    def get_statusNm(self,obj):
        now = datetime.datetime.today()
        msch_query = msch.objects.all()
        msch_query = msch_query.filter(ms_id=obj.ms_id)[0]

        if msch_query.apl_fr_dt == None:
            return '개설중'
        elif now < msch_query.apl_fr_dt:
            return '개설중'
        elif msch_query.apl_fr_dt <= now < msch_query.apl_to_dt:
            return '모집중'
        elif now > msch_query.apl_to_dt:
            return '모집완료'
        else:
            return '개설중'

    def get_statusCode(self,obj):
        now = datetime.datetime.today()
        msch_query = msch.objects.all()
        msch_query = msch_query.filter(ms_id=obj.ms_id)[0]
        if msch_query.apl_fr_dt == None:
            # 개설중
            return '1'
        elif now < msch_query.apl_fr_dt:
            # 개설중
            return '1'
        elif msch_query.apl_fr_dt <= now < msch_query.apl_to_dt:
            # 모집중
            return '2'
        elif now > msch_query.apl_to_dt:
            # 모집완료
            return '3'  
        else:
            # 개설중
            return '1'    

class MS0101M_report_list(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MS0101M_report_list_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        ms_ida = request.GET.get('ms_id', None)
        l_yr = request.GET.get('yr', None)
        
        # ms_apl
        query = "select C.ms_name,B.pr_yr,B.pr_sch_yr,B.pr_term_div,A.* from service20_ms_apl A,service20_vw_nanum_stdt B,service20_msch C where A.apl_id=B.apl_id and A.ms_id = C.ms_id and A.yr='"+str(l_yr)+"' and A.ms_id = '"+str(ms_ida)+"' and A.apl_id='"+str(ida)+"'"
        
        query = "select c.yr AS mpgm_yr,  "
        query += "       c.trn_term,  "
        query += "       c.ms_name,  "
        query += "       b.pr_yr,  "
        query += "       b.pr_sch_yr,  "
        query += "       b.pr_term_div, "
        query += "       cast( ((b.pr_sch_yr-1)*2)+(substr(b.pr_term_div,1,1)*1) as UNSIGNED) pr_term_cnt, "
        query += "       d.std_detl_code_nm AS trn_term_nm,  "
        query += "       a.*  "
        query += "FROM   service20_ms_apl a,  " 
        query += "       service20_vw_nanum_stdt b, "
        query += "       service20_msch c,  "
        query += "       service20_com_cdd d "
        query += " WHERE a.ms_id = c.ms_id  "
        query += "   AND a.apl_id = b.apl_id "
        query += "   AND a.ms_id = '"+str(ms_ida)+"'  "
        query += "   AND a.apl_id = '"+str(ida)+"' "
        query += "   AND d.std_grp_code  = 'MS0022' "
        query += "   AND d.std_detl_code = c.trn_term "
        queryset = ms_apl.objects.raw(query)
        

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

class MP0101M_list_chk_1_Serializer(serializers.ModelSerializer):

    en_cnt = serializers.SerializerMethodField()
    mp_select01 = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    class Meta:
        model = vw_nanum_stdt
        fields = ('sch_yr','en_cnt','mp_select01','name','code')

    def get_mp_select01(self, obj):
        return obj.mp_select01
    def get_name(self, obj):
        return obj.name    
    def get_code(self, obj):
        return obj.code
    def get_en_cnt(self, obj):
        return obj.en_cnt        

class MP0101M_list_chk_1(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0101M_list_chk_1_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")
        mp_id = request.GET.get('mp_id', "")


        # 학년체크
        query = " select t1.id,t1.sch_yr, IFNULL(t4.en_cnt,0) as en_cnt, fn_mp_sub_desc_select_01('"+mp_id+"','MS0010') as mp_select01"
        query += "     , CASE WHEN IFNULL(t4.en_cnt,0) > 0 THEN '신청' ELSE CONCAT('신청불가:', fn_mp_sub_desc_select_01('"+mp_id+"','MS0010'), '만 신청가능') END  as name "
        query += "     , CASE WHEN IFNULL(t4.en_cnt,0) > 0 THEN 'Y' ELSE 'N' END  as code "
        query += "  FROM service20_vw_nanum_stdt t1     /* 부산대학교 학생 정보 */ "
        query += " LEFT JOIN (SELECT t2.apl_id, COUNT(*) en_cnt "
        query += "              FROM service20_vw_nanum_stdt t2     /* 부산대학교 학생 정보 */ "
        query += "             WHERE t2.sch_yr IN  "
        query += "                   (SELECT t3.att_cdd "
        query += "                      FROM service20_mp_sub t3 "
        query += "                     WHERE t3.mp_id   = '"+mp_id+"' "
        query += "                       AND t3.att_id  = 'MS0010' "
        query += "                       AND t3.att_cdh = 'MS0010' "
        query += "                   ) "
        query += "             GROUP BY t2.apl_id "
        query += "            ) t4 ON (t4.apl_id = t1.apl_id) "
        query += " WHERE t1.apl_id = '"+apl_id+"' "

        print(query)
        queryset = vw_nanum_stdt.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class MP0101M_list_chk_2_Serializer(serializers.ModelSerializer):

    
    name = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    class Meta:
        model = vw_nanum_stdt
        fields = ('name','code')

    def get_name(self, obj):
        return obj.name    
    def get_code(self, obj):
        return obj.code

class MP0101M_list_chk_2(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0101M_list_chk_2_Serializer

    def list(self, request):
        
        apl_id = request.GET.get('apl_id', "")
        mp_id = request.GET.get('mp_id', "")


        # -- 직전학기 학점 제한
        query = " select t2.id,CASE WHEN t2.score03 >= t3.att_val THEN '신청' ELSE CONCAT('신청불가 : 학점', t3.att_val, '미만') END as name "
        query += "      , CASE WHEN t2.score03 >= t3.att_val THEN 'Y' ELSE 'N' END as code "
        query += "   FROM service20_vw_nanum_stdt t2     /* 부산대학교 학생 정보 */ "
        query += "      , (  /* 학점 제한 */ "
        query += "         select cast(att_val as unsigned) att_val "
        query += "           FROM service20_mp_sub t3 "
        query += "          WHERE t3.mp_id   = '"+mp_id+"' "
        query += "            AND t3.att_id  = 'MP0071' "
        query += "            AND t3.att_cdh = 'MP0071' "
        query += "            AND t3.att_cdd = '10' "
        query += "       ) t3 "
        query += "   WHERE t2.apl_id = '"+apl_id+"' "

        print(query)
        queryset = vw_nanum_stdt.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class MP0101M_list_Serializer(serializers.ModelSerializer):

    applyFlag = serializers.SerializerMethodField()
    applyFlagNm = serializers.SerializerMethodField()
    applyStatus = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    statusCode = serializers.SerializerMethodField()
    status_nm  = serializers.SerializerMethodField()
    sup_org_nm = serializers.SerializerMethodField()
    code  = serializers.SerializerMethodField()
    code_nm = serializers.SerializerMethodField()
    score03 = serializers.SerializerMethodField()
    att_val = serializers.SerializerMethodField()

    apl_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    apl_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mnt_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mnt_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = mpgm
        fields = ('mp_id','mp_name','status','statusCode','yr','yr_seq','sup_org','applyFlag','applyStatus','apl_fr_dt','apl_to_dt','mnt_fr_dt','mnt_to_dt','cnt_trn','status','status_nm','applyFlagNm','sup_org_nm','code','code_nm','score03','att_val')

    def get_applyFlag(self, obj):
        return obj.applyFlag    
    def get_applyFlagNm(self, obj):
        return obj.applyFlagNm    
    def get_applyStatus(self, obj):
        
        if obj.applyFlag == 'N':
            return '지원'
        else:
            # print(obj.applyFlag)
            # rows = com_cdd.objects.filter(std_grp_code='MP0053',std_detl_code=obj.applyFlag)
            # return str(rows[0].std_detl_code_nm)
            return '미지원'
        return obj.applyStatus    

    def get_statusCode(self,obj):
        return obj.statusCode 

    def get_status_nm(self,obj):
        return obj.status_nm   
    def get_status(self,obj):
        return obj.status
    def get_sup_org_nm(self,obj):
        return obj.sup_org_nm
    def get_code(self,obj):
        return obj.code
    def get_code_nm(self,obj):
        return obj.code_nm
    def get_score03(self,obj):
        return obj.score03
    def get_att_val(self,obj):
        return obj.att_val

class MP0101M_list(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0101M_list_Serializer

    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_status = request.GET.get('status', "")
        ida = request.GET.get('user_id', "")

        query = "select ifnull((select 'Y' from service20_mp_mtr where yr = '"+str(l_yr)+"' and apl_id = '"+str(ida)+"' and mp_id = A.mp_id),'N') AS applyFlag,A.* from service20_mpgm A where A.yr='"+str(l_yr)+"' and A.apl_term='"+str(l_apl_term)+"'"
        
        # SELECT att_val
        #   FROM service20_mp_sub T3
        #  WHERE T3.mp_id   = 'P182014'
        #    AND T3.att_id  = 'MP0071'
        #    AND T3.att_cdh = 'MP0071'
        #    AND T3.att_cdd = '10'
        #    /*미만*/

        # 멘토만 조회가능.

        query = " select apl_to_dt,  "
        query += "        IF(A.status = '10'  "
        query += "           AND Now() > A.apl_to_dt, 'xx', A.status) AS statusCode,  "
        query += "        IF(A.status = '10'  "
        query += "           AND Now() > A.apl_to_dt, '모집완료',  "
        query += "        (SELECT std_detl_code_nm  "
        query += "         FROM   service20_com_cdd  "
        query += "         WHERE  std_grp_code = 'MP0001'  "
        query += "                AND use_indc = 'y'  "
        query += "                AND std_detl_code = A.status))      AS status_nm,  "
        query += "        Ifnull(B.status, 'N')                       AS applyFlag,  "
        

        query += " E.score03, D.att_val,"

        query += " CASE WHEN E.score03 >= D.att_val THEN '신청' ELSE CONCAT('신청불가 : 학점', D.att_val, '미만') END code_nm,CASE WHEN E.score03 >= D.att_val THEN 'Y' ELSE 'N' END code, "

        query += " CASE  "
        query += "      WHEN Ifnull(B.status, 'N') = 'N' THEN '미지원' "
        query += "      ELSE (SELECT std_detl_code_nm  "
        query += "              FROM   service20_com_cdd  "
        query += "              WHERE  std_grp_code = 'MP0053'  "
        query += "                 AND std_detl_code = B.status)  "
        query += " end                                         AS applyFlagNm,  "
        query += " c1.std_detl_code_nm   AS sup_org_nm, "
        query += "        A.*  "
        query += " FROM   service20_mpgm A  "
        query += "        LEFT JOIN service20_mp_mtr B  "
        query += "               ON ( A.mp_id = B.mp_id  "
        # query += "                    AND A.yr = B.yr  "
        query += "                    AND B.apl_id = '"+str(ida)+"' )  "
        query += "        LEFT JOIN service20_com_cdd c1 ON (c1.std_grp_code  = 'MP0004' AND c1.std_detl_code = A.sup_org) "
        

        query += "        LEFT JOIN        (  /* 학점 제한 */ "
        query += "               select cast(att_val as unsigned) att_val,mp_id "
        query += "                 FROM service20_mp_sub t3 "
        query += "                WHERE t3.att_id  = 'MP0071' "
        query += "                  AND t3.att_cdh = 'MP0071' "
        query += "                  AND t3.att_cdd = '10' "
        query += "               ) D ON (A.mp_id = D.mp_id) "

        # query += "       LEFT JOIN (SELECT t2.apl_id, COUNT(*) en_cnt "
        # query += "             FROM service20_vw_nanum_stdt t2     /* 부산대학교 학생 정보 */ "
        # query += "            WHERE t2.sch_yr IN  "
        # query += "                  (SELECT t3.att_cdd "
        # query += "                     FROM service20_mp_sub t3 "
        # query += "                    WHERE t3.mp_id   = 'P182014' "
        # query += "                      AND t3.att_id  = 'MS0010' "
        # query += "                      AND t3.att_cdh = 'MS0010' "
        # query += "                  ) "
        # query += "            GROUP BY t2.apl_id "
        # query += "           ) t4 ON (t4.apl_id = t1.apl_id) "

        query += " , service20_vw_nanum_stdt E "

        query += " WHERE  A.yr = '"+str(l_yr)+"'  "
        query += "        AND A.apl_term = '"+str(l_apl_term)+"'  "


        query += "        AND E.apl_id = '"+str(ida)+"'"
        # query += "        AND (SELECT Count(1)  "
        # query += "             FROM   service20_mentor  "
        # query += "             WHERE  apl_id = '"+str(ida)+"') > 0  "
        

        query += "        AND IF(A.status = '10'  "
        query += "               AND Now() > A.apl_to_dt, 'xx', A.status) LIKE  "
        query += "            Ifnull(Nullif('"+str(l_status)+"', ''), '%%')  "
        query += "            || '%%'  "
        query += " ORDER  BY A.apl_fr_dt DESC,  "
        query += "           A.apl_to_dt DESC  "


        print(query)
        queryset = mpgm.objects.raw(query)
        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, context={'request': request}, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class MP0101M_list_all_Serializer(serializers.ModelSerializer):

    applyFlag = serializers.SerializerMethodField()
    applyFlagNm = serializers.SerializerMethodField()
    applyStatus = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    statusCode = serializers.SerializerMethodField()
    status_nm  = serializers.SerializerMethodField()
    sup_org_nm = serializers.SerializerMethodField()

    apl_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    apl_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mnt_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mnt_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = mpgm
        fields = ('mp_id','mp_name','status','statusCode','yr','yr_seq','sup_org','applyFlag','applyStatus','apl_fr_dt','apl_to_dt','mnt_fr_dt','mnt_to_dt','cnt_trn','status','status_nm','applyFlagNm','sup_org_nm')

    def get_applyFlag(self, obj):
        return obj.applyFlag    
    def get_applyFlagNm(self, obj):
        return obj.applyFlagNm    
    def get_applyStatus(self, obj):
        
        if obj.applyFlag == 'N':
            return '지원'
        else:
            # print(obj.applyFlag)
            # rows = com_cdd.objects.filter(std_grp_code='MP0053',std_detl_code=obj.applyFlag)
            # return str(rows[0].std_detl_code_nm)
            return '미지원'
        return obj.applyStatus    

    def get_statusCode(self,obj):
        return obj.statusCode 

    def get_status_nm(self,obj):
        return obj.status_nm   
    def get_status(self,obj):
        return obj.status
    def get_sup_org_nm(self,obj):
        return obj.sup_org_nm


class MP0101M_list_all(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0101M_list_all_Serializer

    def list(self, request):
        ida = request.GET.get('user_id', "")

        
        # 멘토만 조회가능.
        query = " select apl_to_dt,  "
        query += "        IF(A.status = '10'  "
        query += "           AND Now() > A.apl_to_dt, 'xx', A.status) AS statusCode,  "
        query += "        IF(A.status = '10'  "
        query += "           AND Now() > A.apl_to_dt, '모집완료',  "
        query += "        (SELECT std_detl_code_nm  "
        query += "         FROM   service20_com_cdd  "
        query += "         WHERE  std_grp_code = 'MP0001'  "
        query += "                AND use_indc = 'y'  "
        query += "                AND std_detl_code = A.status))      AS status_nm,  "
        query += "        Ifnull(B.status, 'N')                       AS applyFlag,  "
    
        query += " CASE  "
        query += "      WHEN Ifnull(B.status, 'N') = 'N' THEN '미지원' "
        query += "      ELSE (SELECT std_detl_code_nm  "
        query += "              FROM   service20_com_cdd  "
        query += "              WHERE  std_grp_code = 'MP0053'  "
        query += "                 AND std_detl_code = B.status)  "
        query += " end                                         AS applyFlagNm,  "
        query += " c1.std_detl_code_nm   AS sup_org_nm, "
        query += "        A.*  "
        query += " FROM   service20_mpgm A  "
        query += "        LEFT JOIN service20_mp_mtr B  "
        query += "               ON ( A.mp_id = B.mp_id  "
        # query += "                    AND A.yr = B.yr  "
        query += "                    AND B.apl_id = '"+str(ida)+"' )  "
        query += "        LEFT JOIN service20_com_cdd c1 ON (c1.std_grp_code  = 'MP0004' AND c1.std_detl_code = A.sup_org) "
        query += " WHERE  B.apl_id = '"+str(ida)+"'  "        
        query += " ORDER  BY A.apl_fr_dt DESC,  "
        query += "           A.apl_to_dt DESC  "


        print(query)
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
        
        query = "select B.std_detl_code,B.std_detl_code_nm,B.rmrk,A.* from service20_mp_sub A left outer join service20_com_cdd B on (A.att_id = B.std_grp_code and A.att_cdd = B.std_detl_code) where A.att_id='MS0014' and B.use_indc = 'Y' and A.mp_id = '"+key1+"'"
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
    client_ip = request.META['REMOTE_ADDR']
    
    print("::ida::")
    print(ida)
    #created,created_flag = vw_nanum_stdt.apl_id.get_or_create(user=request.user)
    mp_id = programId
    mp_mtr_max = mp_mtr.objects.all().aggregate(vlMax=Max('apl_no'))
    rows = vw_nanum_stdt.objects.filter(apl_id=ida)[0]
    #mp_mtr_max = mp_mtr.objects.all().last()
    #mp_mtr_max = mp_mtr_max + 1

    print("::start::")

    apl_no = mp_mtr_max
    apl_id = ida
    v_gen = ""
    if str(rows.gen_cd) == "1":
        v_gen = "M"
    else:
        v_gen = "F"
    
    max_no = mp_mtr_max['vlMax']    
    print("::max_no::")
    print(max_no)
    if max_no == None:
        apl_no = 0
    else:
        apl_no = mp_mtr_max['vlMax']
        apl_no = apl_no + 1

    
    query = "select ifnull(max(apl_no),1) as apl_no from service20_mp_mtr where apl_id = '"+apl_id+"' and mp_id = '"+mp_id+"'"  
    cursor = connection.cursor()
    cursor.execute(query)    
    results = namedtuplefetchall(cursor)    
    apl_no = results[0].apl_no


    print("::apl_no::")
    print(apl_no)
    
    if rows.unv_cd == None:
        v_unv_cd = ''
    else:
        v_unv_cd = rows.unv_cd 

    if rows.unv_nm == None:
        v_unv_nm = ''
    else:
        v_unv_nm = rows.unv_nm


    query = " select t2.mp_id,t2.yr FROM service20_mpgm t2  WHERE 1=1 "
    query += " AND t2.mp_id          = '"+mp_id+"'"
    queryset = mpgm.objects.raw(query)[0]


    
    rowsChk = mp_mtr.objects.filter(apl_id=apl_id,mp_id=mp_id).exists()

    if rowsChk == True:
        context = {'message': 'duplicate'}
    else:
    
        model_instance = mp_mtr(
            mp_id=mp_id, 
            apl_no=apl_no, 
            mntr_id=ida,
            apl_id=apl_id,
            apl_nm=rows.apl_nm,
            unv_cd=v_unv_cd,
            unv_nm=v_unv_nm,
            cllg_cd=rows.cllg_cd,
            cllg_nm=rows.cllg_nm,
            dept_cd=rows.dept_cd,
            dept_nm=rows.dept_nm,
            brth_dt=rows.brth_dt,
            gen=v_gen,
            yr=queryset.yr,
            term_div=rows.term_div,
            sch_yr=rows.sch_yr,
            mob_no=rows.mob_no.replace('-', ''),
            tel_no=rows.tel_no.replace('-', ''),
            tel_no_g=rows.tel_no_g.replace('-', ''),
            h_addr=rows.h_addr,
            email_addr=rows.email_addr,
            bank_acct=rows.bank_acct,
            bank_cd=rows.bank_cd,
            bank_nm=rows.bank_nm,
            score1=rows.score01,
            score2=rows.score02,
            score3=rows.score03,
            score4=rows.score04,
            score5=rows.score05,
            inv_agr_div = 'Y',
            inv_agr_dt = datetime.datetime.today(),
            status='10', # 지원
            ins_id=apl_id,
            ins_ip=str(client_ip),
            ins_dt=datetime.datetime.today()
            )
        model_instance.save()
        
        apl_max = int(apl_max)

        for i in range(0,apl_max):
            anst2 = request.POST.get('que'+str(i+1), None)
            ques_no = request.POST.get('ques_no'+str(i+1), None)

            model_instance2 = mp_ans(
                mp_id=mp_id, 
                test_div='10', 
                apl_no=apl_no,
                ques_no=ques_no,
                apl_id=apl_id,
                apl_nm=rows.apl_nm,
                sort_seq =i+1,
                ans_t2=anst2,
                ins_id=apl_id,
                ins_ip=str(client_ip),
                ins_dt=datetime.datetime.today()
                )
            model_instance2.save()


        # mp_mntr/ms_apl  -> mp_id만 조건 걸어서 count(*)
        # 해당 cnt값을 mpgm/msch -> cnt_apl

        update_text = " update service20_mpgm a "
        update_text += " SET a.cnt_apl = (select count(*) from service20_mp_mtr where mp_id = '"+mp_id+"') "
        update_text += " WHERE 1=1 "
        update_text += " AND a.mp_id = '"+mp_id+"' "
        
        cursor = connection.cursor()
        query_result = cursor.execute(update_text)    


        # -- 생성_어학(mp_mtr_fe)_FROM_vw_nanum_foreign_exam

        update_text = " insert into service20_mp_mtr_fe     /* 프로그램 지원자(멘토) 어학 리스트 */ ";
        update_text += "      ( mp_id          /* 멘토링 프로그램id */ ";
        update_text += "      , apl_no         /* 지원 no */ ";
        update_text += "      , fe_no          /* 어학점수 no */ ";
        update_text += "      , apl_id         /* 학번 */ ";
        update_text += "      , apl_nm         /* 성명 */ ";
        update_text += "      , lang_kind_cd   /* 어학종류코드 */ ";
        update_text += "      , lang_kind_nm   /* 어학종류명 */ ";
        update_text += "      , lang_cd        /* 어학상위코드 */ ";
        update_text += "      , lang_nm        /* 어학상위코드명 */ ";
        update_text += "      , lang_detail_cd /* 어학하위코드 */ ";
        update_text += "      , lang_detail_nm /* 어학하위코드명 */ ";
        update_text += "      , frexm_cd       /* 외국어시험 코드 */ ";
        update_text += "      , frexm_nm       /* 외국어시험명 */ ";
        update_text += "      , score          /* 시험점수 */ ";
        update_text += "      , grade          /* 시험등급 */ ";
        update_text += "      , ins_id         /* 입력자id */ ";
        update_text += "      , ins_ip         /* 입력자ip */ ";
        update_text += "      , ins_dt         /* 입력일시 */ ";
        update_text += "      , ins_pgm        /* 입력프로그램id */ ";
        update_text += " ) ";
        update_text += " select '"+str(mp_id)+"' AS mp_id ";
        update_text += "      , '"+str(apl_no)+"' apl_no         /* 지원 no */ ";
        update_text += "      , @curRank := @curRank +1 AS fe_no  ";
        update_text += "      , t1.apl_id         /* 학번 */ ";
        update_text += "      , t1.apl_nm         /* 성명 */ ";
        update_text += "      , t1.lang_kind_cd   /* 어학종류코드 */ ";
        update_text += "      , t1.lang_kind_nm   /* 어학종류명 */ ";
        update_text += "      , t1.lang_cd        /* 어학상위코드 */ ";
        update_text += "      , t1.lang_nm        /* 어학상위코드명 */ ";
        update_text += "      , t1.lang_detail_cd /* 어학하위코드 */ ";
        update_text += "      , t1.lang_detail_nm /* 어학하위코드명 */ ";
        update_text += "      , '0' frexm_cd       /* 외국어시험 코드 */ ";
        update_text += "      , t1.frexm_nm       /* 외국어시험명 */ ";
        update_text += "      , t1.score          /* 시험점수 */ ";
        update_text += "      , t1.grade          /* 시험등급 */ ";
        update_text += "      , '"+apl_id+"' ins_id         /* 입력자id */ ";
        update_text += "      , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ ";
        update_text += "      , NOW() ins_dt         /* 입력일시 */ ";
        update_text += "      , 'c' ins_pgm        /* 입력프로그램id */ ";
        update_text += "   FROM service20_vw_nanum_foreign_exam t1     /* 유효한 외국어 성적 리스트 view(임시) */ ";
        update_text += "      , (SELECT @curRank := 0) r ";
        update_text += "  WHERE 1=1 ";
        update_text += "    AND t1.apl_id = '"+apl_id+"' ";
        print("::_FROM_vw_nanum_foreign_exam::")
        print(update_text) 
        cursor = connection.cursor()
        query_result = cursor.execute(update_text)    


        # -- 생성_봉사(mp_mtr_sa)_FROM_vw_nanum_foreign_exam

        update_text = "insert into service20_mp_mtr_sa     /* 프로그램 지원자(멘토) 봉사 리스트 */ ";
        update_text += "     ( mp_id           /* 멘토링 프로그램id */ ";
        update_text += "     , apl_no          /* 지원 no */ ";
        update_text += "     , sa_no           /* 어학점수 no */ ";
        update_text += "     , apl_id          /* 학번 */ ";
        update_text += "     , apl_nm          /* 성명 */ ";
        update_text += "     , nation_inout_cd /* 국내외구분코드 */ ";
        update_text += "     , nation_inout_nm /* 국내외구분명 */ ";
        update_text += "     , sch_inout_cd    /* 교내외구분코드 */ ";
        update_text += "     , sch_inout_nm    /* 교내외구분명 */ ";
        update_text += "     , activity_nm     /* 봉사명 */ ";
        update_text += "     , manage_org_nm   /* 주관기관명 */ ";
        update_text += "     , start_date      /* 시작일자 */ ";
        update_text += "     , start_time      /* 시작시간 */ ";
        update_text += "     , end_date        /* 종료일자 */ ";
        update_text += "     , end_time        /* 종료시간 */ ";
        update_text += "     , tot_time        /* 총시간 */ ";
        update_text += "     , ins_id          /* 입력자id */ ";
        update_text += "     , ins_ip          /* 입력자ip */ ";
        update_text += "     , ins_dt          /* 입력일시 */ ";
        update_text += "     , ins_pgm         /* 입력프로그램id */ ";
        update_text += ") ";
        update_text += "select '"+str(mp_id)+"' AS mp_id ";
        update_text += "     , '"+str(apl_no)+"' apl_no         /* 지원 no */ ";
        update_text += "     , @curRank := @curRank +1 AS sa_no ";
        update_text += "     , t1.apl_id          /* 학번 */ ";
        update_text += "     , t1.apl_nm          /* 성명 */ ";
        update_text += "     , t1.nation_inout_cd /* 국내외구분코드 */ ";
        update_text += "     , t1.nation_inout_nm /* 국내외구분명 */ ";
        update_text += "     , t1.sch_inout_cd    /* 교내외구분코드 */ ";
        update_text += "     , t1.sch_inout_nm    /* 교내외구분명 */ ";
        update_text += "     , t1.activity_nm     /* 봉사명 */ ";
        update_text += "     , t1.manage_org_nm   /* 주관기관명 */ ";
        update_text += "     , t1.start_date      /* 시작일자 */ ";
        update_text += "     , t1.start_time      /* 시작시간 */ ";
        update_text += "     , t1.end_date        /* 종료일자 */ ";
        update_text += "     , t1.end_time        /* 종료시간 */ ";
        update_text += "     , t1.tot_time        /* 총시간 */ ";
        update_text += "     , '"+apl_id+"' ins_id         /* 입력자id */ ";
        update_text += "     , '"+str(client_ip)+"' ins_ip         /* 입력자ip */ ";
        update_text += "     , NOW() ins_dt         /* 입력일시 */ ";
        update_text += "     , 'c' ins_pgm        /* 입력프로그램id */ ";
        update_text += "  FROM service20_vw_nanum_service_activ t1     /* 학생 봉사 시간 view(임시) */ ";
        update_text += "     , (SELECT @curRank := 0) r ";
        update_text += " WHERE 1=1 ";
        update_text += "   AND t1.apl_id = '"+apl_id+"' ";
        print("::_FROM_vw_nanum_foreign_exam::")
        print(update_text) 
        cursor = connection.cursor()
        query_result = cursor.execute(update_text)    


        context = {'message': 'Ok'}


    #return HttpResponse(json.dumps(context), content_type="application/json")
    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

@csrf_exempt
def MP0101M_detail(request):    

    ida = request.POST.get('user_id', None)
    ms_ida = request.POST.get('ms_id', None)
    l_yr = request.POST.get('yr', None)

    created_flag = vw_nanum_stdt.objects.filter(apl_id=ida).exists()
    mpgm_flag = mpgm.objects.filter(mp_id=ms_ida,status='20').exists()
    ms_apl_flag = mp_mtr.objects.filter(apl_id=ida,mp_id=ms_ida).exists()
    print(mpgm_flag)
    if not ms_apl_flag:
        applyYn = 'N'
    else:
        applyYn = 'Y'

    print('========')
    if not created_flag:
        print('0')
        message = "Fail"
        context = {'message': message}
    else:
        if mpgm_flag == False:
            print('1')
            message = "Fail"
            context = {'message': message}
        else:
            print('2')
            message = "Ok"
            rows = vw_nanum_stdt.objects.filter(apl_id=ida)[0]
            rows2 = mp_sub.objects.filter(mp_id=ms_ida)
            rows3 = mpgm.objects.filter(mp_id=ms_ida)[0]
            


            for val in rows2:
                key1 = val.att_id
                #key2 = val.att_cdd


            context = {'message': message,
                        'applyYn' : applyYn,
                        'apl_nm' : rows.apl_nm,
                        'unv_cd' : rows.unv_cd,
                        'unv_nm' : rows.unv_nm,
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
                        'stds_div' : rows.stds_div,
                        'stds_nm' : rows.stds_nm,
                        'mob_no' : rows.mob_no,
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
                        'ms_id' : rows3.mp_id,
                        'ms_name' : rows3.mp_name,
                        }
        

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

class MP0101M_adm_list_Serializer(serializers.ModelSerializer):
    
    mp_name = serializers.SerializerMethodField()
    pr_yr = serializers.SerializerMethodField()
    pr_sch_yr = serializers.SerializerMethodField()
    pr_term_div = serializers.SerializerMethodField()
    statusCode = serializers.SerializerMethodField()
    status_nm = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    acpt_dt = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = mp_mtr
        fields = ('mp_id','apl_no','mntr_id','indv_div','team_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','bank_acct','bank_cd','bank_nm','bank_dpsr','cnt_mp_a','cnt_mp_p','cnt_mp_c','cnt_mp_g','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','fnl_rslt','acpt_dt','acpt_div','acpt_cncl_rsn','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','mp_name','pr_yr','pr_sch_yr','pr_term_div','statusCode','status_nm')

    def get_mp_name(self,obj):
        return obj.mp_name

    def get_pr_yr(self,obj):
        return obj.pr_yr

    def get_pr_sch_yr(self,obj):
        return obj.pr_sch_yr

    def get_pr_term_div(self,obj):
        return obj.pr_term_div  

    def get_statusCode(self,obj):
        return obj.statusCode 

    def get_status_nm(self,obj):
        return obj.status_nm
    def get_status(self,obj):
        return obj.status

class MP0101M_adm_list(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MP0101M_adm_list_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        mp_ida = request.GET.get('mp_id', None)
        l_yr = request.GET.get('yr', None)
        
        # mpgm

        query = " select   "
        query += " if(C.status = '10'  "
        query += " and now() > C.apl_to_dt, 'xx', C.status) as statusCode,  "
        query += " if(A.status = '10'  "
        query += " and now() > C.apl_to_dt, '모집완료', (select std_detl_code_nm  "
        query += " from   service20_com_cdd  "
        query += " where  "
        query += " std_grp_code = 'MP0001'  "
        query += " and use_indc = 'y'  "
        query += " and std_detl_code = C.status)) as status_nm,  "

        query += " C.mp_name,B.pr_yr,B.pr_sch_yr,B.pr_term_div,A.* from service20_mp_mtr A,service20_vw_nanum_stdt B,service20_mpgm C where A.apl_id=B.apl_id and A.mp_id = C.mp_id and A.mp_id = '"+mp_ida+"' and A.apl_id='"+ida+"'"
        queryset = mp_mtr.objects.raw(query)
        print(query)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램(관리자) - 어학
class MP0101M_adm_list_fe_Serializer(serializers.ModelSerializer):
    
    fn_score = serializers.SerializerMethodField()

    class Meta:
        model = mp_mtr_fe
        fields = ('frexm_cd','frexm_nm','score','grade','fn_score')

    def get_fn_score(self,obj):
        return obj.fn_score

class MP0101M_adm_list_fe(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MP0101M_adm_list_fe_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        mp_ida = request.GET.get('mp_id', None)
        l_yr = request.GET.get('yr', None)
        
        query = " select id,  "
        query += "        frexm_cd,  "
        query += "        frexm_nm,  "
        query += "        score,  "        
        query += "        grade,  "
        query += "   fn_mp_mtr_fe_select_01('"+str(mp_ida)+"','"+str(ida)+"') as fn_score "
        query += " FROM   service20_mp_mtr_fe  "
        query += " WHERE  mp_id = '"+str(mp_ida)+"'  "
        query += "        AND apl_id = '"+str(ida)+"' "

        queryset = mp_mtr_fe.objects.raw(query)
        print(query)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램(관리자) - 봉사
class MP0101M_adm_list_sa_Serializer(serializers.ModelSerializer):
    
    fn_score = serializers.SerializerMethodField()

    class Meta:
        model = mp_mtr_sa
        fields = ('mp_id','apl_no','sa_no','apl_id','apl_nm','nation_inout_cd','nation_inout_nm','sch_inout_cd','sch_inout_nm','activity_nm','manage_org_nm','start_date','start_time','end_date','end_time','tot_time','fn_score')

    def get_fn_score(self,obj):
        return obj.fn_score

class MP0101M_adm_list_sa(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MP0101M_adm_list_sa_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        mp_ida = request.GET.get('mp_id', None)
        l_yr = request.GET.get('yr', None)
        
        query = " select a.* , "
        query += "   fn_mp_mtr_sa_select_01('"+str(mp_ida)+"','"+str(ida)+"') as fn_score "
        query += " FROM   service20_mp_mtr_sa a  "
        query += " WHERE  mp_id = '"+str(mp_ida)+"'  "
        query += "        AND apl_id = '"+str(ida)+"' "

        queryset = mp_mtr_sa.objects.raw(query)
        print(query)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램(관리자) - 질문2
class MP0101M_adm_quest_Serializer2(serializers.ModelSerializer):

    std_detl_code = serializers.SerializerMethodField()
    std_detl_code_nm = serializers.SerializerMethodField()
    rmrk = serializers.SerializerMethodField()

    class Meta:
        model = mp_ans
        fields = ('id','mp_id','test_div','apl_no','ques_no','apl_id','apl_nm','sort_seq','ans_t1','ans_t2','ans_t3','score','std_detl_code','std_detl_code_nm','rmrk')

    def get_std_detl_code(self,obj):
        return obj.std_detl_code

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
        
        query = "select B.std_detl_code,B.std_detl_code_nm,B.rmrk,A.* from service20_mp_ans A, service20_com_cdd B where A.ques_no = B.std_detl_code and B.use_indc = 'Y' and B.std_grp_code in (select att_cdh from service20_mp_sub where att_id='MS0014' and mp_id = '"+str(key1)+"') and A.mp_id = '"+str(key1)+"' and apl_id = '"+str(l_user_id)+"'"
        queryset = mp_ans.objects.raw(query)

        

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 멘토링 프로그램 수락
@csrf_exempt
def MP0101M_adm_acpt_save(request):
    mp_id = request.POST.get('mp_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    update_text = " update service20_mp_mtr a "
    update_text += " SET a.acpt_dt = NOW() "
    update_text += " , a.acpt_div = 'Y' "
    update_text += " , a.acpt_cncl_rsn = null "
    update_text += " WHERE 1=1 "
    update_text += " AND a.mp_id = '"+mp_id+"' "
    update_text += " AND a.apl_no = '"+apl_no+"' "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)

        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

# 멘토링 프로그램 수락취소
@csrf_exempt
def MP0101M_adm_acpt_cancle(request):
    mp_id = request.POST.get('mp_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")
    acpt_cncl_rsn = request.POST.get('acpt_cncl_rsn', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    update_text = " update service20_mp_mtr a "
    update_text += " SET a.acpt_dt = null "
    update_text += " , a.acpt_div = 'N' "
    update_text += " , a.acpt_cncl_rsn = '"+acpt_cncl_rsn+"' "
    update_text += " WHERE 1=1 "
    update_text += " AND a.mp_id = '"+mp_id+"' "
    update_text += " AND a.apl_no = '"+apl_no+"' "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)

        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True}) 

# 멘토링 프로그램 update
@csrf_exempt
def MP0101M_adm_update(request):
    mp_id = request.POST.get('mp_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")
    acpt_cncl_rsn = request.POST.get('acpt_cncl_rsn', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    maxRow = request.POST.get('maxRow', 0)


    apl_max = int(maxRow)
    

    update_text = " update service20_mp_mtr a "
    update_text += " SET a.status = '10' "
    update_text += " WHERE 1=1 "
    update_text += " AND a.mp_id = '"+str(mp_id)+"' "
    update_text += " AND a.apl_id = '"+str(apl_id)+"' "
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)

    for i in range(0,apl_max):
        anst2 = request.POST.get('que'+str(i+1), None)
        ques_no = request.POST.get('ques_no'+str(i+1), None)
        ans_t2 = request.POST.get('ans_t2_'+str(i+1), None)

        update_text = " update service20_mp_ans a "
        update_text += " SET a.ans_t2 = '"+str(ans_t2)+"' "
        update_text += " WHERE 1=1 "
        update_text += " AND a.mp_id = '"+str(mp_id)+"' "
        update_text += " AND a.apl_no = '"+str(apl_no)+"' "
        update_text += " AND a.ques_no = '"+str(ques_no)+"' "
        
        cursor = connection.cursor()
        query_result = cursor.execute(update_text)

        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True}) 

# 멘토링 프로그램 cancle
@csrf_exempt
def MP0101M_adm_cancle(request):
    mp_id = request.POST.get('mp_id', "")
    apl_id = request.POST.get('apl_id', "")
    apl_no = request.POST.get('apl_no', "")
    acpt_cncl_rsn = request.POST.get('acpt_cncl_rsn', "")

    ins_id = request.POST.get('ins_id', "")
    ins_ip = request.POST.get('ins_ip', "")
    ins_dt = request.POST.get('ins_dt', "")
    ins_pgm = request.POST.get('ins_pgm', "")
    upd_id = request.POST.get('upd_id', "")
    upd_ip = request.POST.get('upd_ip', "")
    upd_dt = request.POST.get('upd_dt', "")
    upd_pgm = request.POST.get('upd_pgm', "")

    update_text = " update service20_mp_mtr a "
    update_text += " SET status = '19' "
    update_text += " , doc_cncl_dt = now() "
    update_text += " WHERE 1=1 "
    update_text += " AND a.mp_id = '"+mp_id+"' "
    update_text += " AND a.apl_no = '"+apl_no+"' "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)


    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})            

class MP0101M_report_list_Serializer(serializers.ModelSerializer):
    
    mp_name = serializers.SerializerMethodField()
    statusNm = serializers.SerializerMethodField()
    statusCode = serializers.SerializerMethodField()
    mpgm_yr = serializers.SerializerMethodField()
    mnt_term = serializers.SerializerMethodField()
    mnt_term_nm = serializers.SerializerMethodField()
    pr_yr = serializers.SerializerMethodField()
    pr_sch_yr = serializers.SerializerMethodField()
    pr_term_div = serializers.SerializerMethodField()
    pr_term_cnt = serializers.SerializerMethodField()

    acpt_dt = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = mp_mtr
        fields = ('mp_id','apl_no','mntr_id','indv_div','team_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','bank_acct','bank_cd','bank_nm','bank_dpsr','cnt_mp_a','cnt_mp_p','cnt_mp_c','cnt_mp_g','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','fnl_rslt','acpt_dt','acpt_div','acpt_cncl_rsn','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','mp_name','statusNm','statusCode','id_pic','mpgm_yr','mnt_term','mnt_term_nm','pr_yr','pr_sch_yr','pr_term_div','pr_term_cnt')

    def get_mp_name(self,obj):
        return obj.mp_name

    def get_pr_yr(self,obj):
        return obj.pr_yr

    def get_pr_sch_yr(self,obj):
        return obj.pr_sch_yr

    def get_pr_term_div(self,obj):
        return obj.pr_term_div  

    def get_pr_term_cnt(self,obj):
        return obj.pr_term_cnt      

    def get_statusNm(self,obj):
        now = datetime.datetime.today()
        mpgm_query = mpgm.objects.all()
        mpgm_query = mpgm_query.filter(mp_id=obj.mp_id)[0]

        if mpgm_query.apl_fr_dt == None:
            return '개설중'
        elif now < mpgm_query.apl_fr_dt:
            return '개설중'
        elif mpgm_query.apl_fr_dt <= now < mpgm_query.apl_to_dt:
            return '모집중'
        elif now > mpgm_query.apl_to_dt:
            return '모집완료'
        else:
            return '개설중'

    def get_statusCode(self,obj):
        now = datetime.datetime.today()
        mpgm_query = mpgm.objects.all()
        mpgm_query = mpgm_query.filter(mp_id=obj.mp_id)[0]
        if mpgm_query.apl_fr_dt == None:
            # 개설중
            return '1'
        elif now < mpgm_query.apl_fr_dt:
            # 개설중
            return '1'
        elif mpgm_query.apl_fr_dt <= now < mpgm_query.apl_to_dt:
            # 모집중
            return '2'
        elif now > mpgm_query.apl_to_dt:
            # 모집완료
            return '3'  
        else:
            # 개설중
            return '1'      
    def get_mpgm_yr(self,obj):
        return obj.mpgm_yr
    def get_mnt_term(self,obj):
        return obj.mnt_term
    def get_mnt_term_nm(self,obj):
        return obj.mnt_term_nm

class MP0101M_report_list(generics.ListAPIView):
    queryset = mp_mtr.objects.all()
    serializer_class = MP0101M_report_list_Serializer
    
    def list(self, request):
        ida = request.GET.get('user_id', None)
        mp_ida = request.GET.get('mp_id', None)
        l_yr = request.GET.get('yr', None)
        
        # mpgm
        # query = "select C.yr as mpgm_yr,C.mnt_term,C.mp_name,B.pr_yr,B.pr_sch_yr,B.pr_term_div,A.* from service20_mp_mtr A,service20_vw_nanum_stdt B,service20_mpgm C where A.apl_id=B.apl_id and A.mp_id = C.mp_id and A.mp_id = '"+str(mp_ida)+"' and A.apl_id='"+str(ida)+"'"

        query = "select c.yr AS mpgm_yr,  "
        query += "       c.mnt_term,  "
        query += "       c.mp_name,  "
        query += "       b.pr_yr,  "
        query += "       b.pr_sch_yr,  "
        query += "       b.pr_term_div, "
        query += "       cast( ((b.pr_sch_yr-1)*2)+(substr(b.pr_term_div,1,1)*1) as UNSIGNED) pr_term_cnt, "
        query += "       d.std_detl_code_nm AS mnt_term_nm,  "
        query += "       a.*  "
        query += "FROM   service20_mp_mtr a,  " 
        query += "       service20_vw_nanum_stdt b, "
        query += "       service20_mpgm c,  "
        query += "       service20_com_cdd d "
        query += " WHERE a.mp_id = c.mp_id  "
        query += "   AND a.apl_id = b.apl_id "
        query += "   AND a.mp_id = '"+str(mp_ida)+"'  "
        query += "   AND a.apl_id = '"+str(ida)+"' "
        query += "   AND d.std_grp_code  = 'MS0022' "
        query += "   AND d.std_detl_code = c.mnt_term "


        queryset = mp_mtr.objects.raw(query)
        
        

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
        
        query = "select * from service20_mp_spc where yr='"+l_yr+"' and apl_term='"+l_apl_term+"'"
        queryset = mp_spc.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 학습외신청(멘토) Detail ###################################################
class MP0102M_detail_Serializer(serializers.ModelSerializer):

    testField = serializers.SerializerMethodField()
    class Meta:
        model = mp_spc
        fields = ('id','mp_id','spc_no','spc_div','status','spc_name','spc_intro','yr','yr_seq','apl_ntc_fr_dt','apl_ntc_to_dt','apl_term','apl_fr_dt','apl_to_dt','mnt_term','mnt_fr_dt','mnt_to_dt','cnf_dt','appr_tm','tot_apl','cnt_apl','cnt_pln','cnt_att','use_div','pic_div','rep_div','ord_div','grd_appr_div','tch_appr_div')

    def get_testField(self, obj):
        return 'test'     


class MP0102M_detail(generics.ListAPIView):
    queryset = mp_spc.objects.all()
    serializer_class = MP0102M_detail_Serializer

    # mp_spc

    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_apl_term = request.GET.get('apl_term', "")
        l_status = request.GET.get('status', "")
        ida = request.GET.get('user_id', "")
        
        queryset = self.get_queryset()
        
        query = "select * from service20_mp_spc where yr='"+l_yr+"' and apl_term='"+l_apl_term+"'"
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
class MP0103M_v1_Serializer(serializers.ModelSerializer):

    mnt_fr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mnt_to_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    
    class Meta:
        model = mpgm
        fields = ('mp_id','mnt_fr_dt','mnt_to_dt')
      


class MP0103M_v1(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0103M_v1_Serializer

    def list(self, request):
        mp_id = request.GET.get('mp_id', "")

        queryset = self.get_queryset()

        query = " select t1.mp_id,t1.mnt_fr_dt"
        query += "      , t1.mnt_to_dt"
        query += "   from service20_mpgm t1"
        query += "  where t1.mp_id  = '" + mp_id +"'"

        

        queryset = mpgm.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


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
    apl_no = serializers.SerializerMethodField()
    
    mgr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    pln_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    appr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    pln_sedt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = mpgm
        fields = ('mp_id','mp_name','apl_term','yr_seq','mnte_nm','sch_nm','sch_yr','pln_dt','appr_nm','appr_dt','mgr_id','mgr_dt','apl_id','apl_nm','tchr_nm','pln_dt','mtr_sub','pln_sedt','apl_no')
    
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
    def get_apl_no(self,obj):
        return obj.apl_no    
    


class MP0103M_list(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0103M_list_Serializer

    # mp_mtr - 프로그램 지원자(멘토) => mp_id(멘토링ID), apl_id
    # mp_mte - 프로그램 지원자(멘티) => mp_id(멘토링ID)


    def list(self, request):
        l_user_id = request.GET.get('user_id', "")

        queryset = self.get_queryset()

        query = " select b.mp_id      AS mp_id "
        query += " , b.mp_name    AS mp_name "
        query += " , b.apl_term   AS apl_term "
        query += " , b.yr_seq     AS yr_seq "
        query += " , c.mnte_nm    AS mnte_nm "
        query += " , c.sch_nm     AS sch_nm "
        query += " , c.sch_yr     AS sch_yr "
        query += " , a.pln_dt     AS pln_dt "
        query += " , a.appr_nm    AS appr_nm "
        query += " , a.appr_dt    AS appr_dt "
        query += " , a.mgr_id     AS mgr_id "
        query += " , a.mgr_dt     AS mgr_dt "
        query += " , d.apl_id     AS apl_id "
        query += " , d.apl_nm     AS apl_nm "
        query += " , c.tchr_nm    AS tchr_nm "
        query += " , a.mtr_sub     AS mtr_sub "
        query += " , d.apl_no     AS apl_no "
        query += " , (SELECT concat(pln_sdt, CONCAT('~', pln_edt)) FROM service20_mp_plnd WHERE mp_id = a.mp_id AND apl_no = a.apl_no LIMIT 1) AS pln_sedt "
        query += " from service20_mp_plnh a "
        query += " , service20_mpgm b "
        query += " , service20_mp_mte c "
        query += " , (SELECT mp_id "
        query += " , apl_no "
        query += " , apl_id "
        query += " , apl_nm "
        query += " FROM service20_mp_mtr "
        query += " WHERE mntr_id = '"+l_user_id+"' or apl_id = '"+l_user_id+"') d "
        query += " WHERE a.mp_id = b.mp_id "
        query += " AND a.mp_id = c.mp_id "
        query += " AND a.mp_id = d.mp_id "
        query += " AND a.apl_no = d.apl_no "
        query += " AND d.apl_no = c.apl_no "

        

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
        

        query = " select b.*"
        query += " from service20_mp_plnh a"
        query += " , service20_mp_plnd b"
        query += " , (SELECT mp_id"
        query += " , apl_no"
        query += " FROM service20_mp_mtr"
        query += " WHERE mp_id = '"+l_mp_id+"'"
        query += " AND ( apl_id = '"+l_user_id+"') ) c"
        query += " WHERE a.mp_id = b.mp_id"
        query += "    AND a.mp_id = c.mp_id"
        query += "    AND a.apl_no = b.apl_no"
        query += "    AND a.apl_no = c.apl_no"

        queryset = mp_plnd.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 프로그램 수행계획서 작성 폼 데이터 ###################################################
class MP0103M_Detail_v2_Serializer(serializers.ModelSerializer):

    prn_fg = serializers.SerializerMethodField()
    tchr_nm = serializers.SerializerMethodField()
    sch_nm = serializers.SerializerMethodField()
    mtr_sub = serializers.SerializerMethodField()
    pln_time  = serializers.SerializerMethodField()
    class Meta:
        model = mp_mtr
        fields = ('apl_nm','apl_id','prn_fg','tchr_nm','sch_nm','mtr_sub','pln_time')
      
    def get_prn_fg(self, obj):
        return obj.prn_fg
    def get_tchr_nm(self, obj):
        return obj.tchr_nm
    def get_sch_nm(self, obj):
        return obj.sch_nm
    def get_mtr_sub(self, obj):
        return obj.mtr_sub
    def get_pln_time(self, obj):
        return obj.pln_time

class MP0103M_Detail_v2(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0103M_Detail_v2_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        apl_id = request.GET.get('apl_id', "")
        apl_no = request.GET.get('apl_no', "")
        

        queryset = self.get_queryset()
        

        # /* 프로그램 수행계획서 작성 폼 데이터 */
        select_text = "select d.id,case when a.pln_dt is not NULL then 'true' ELSE 'false' END AS prn_fg"
        select_text += ", d.apl_id AS apl_id, d.apl_nm AS apl_nm, c.tchr_nm AS tchr_nm, c.sch_nm AS sch_nm, a.mtr_sub AS mtr_sub, '60' AS pln_time"
        select_text += " from service20_mp_plnh a, service20_mpgm b, service20_mp_mte c"
        select_text += ", (SELECT id,mp_id, apl_no, apl_id, apl_nm"
        select_text += " FROM service20_mp_mtr"
        select_text += " WHERE apl_id = '"+apl_id+"' AND apl_no = '"+apl_no+"') d"
        select_text += " WHERE a.mp_id = b.mp_id"
        select_text += " AND a.mp_id = c.mp_id"
        select_text += " AND a.mp_id = d.mp_id"
        select_text += " AND a.apl_no = d.apl_no"
        select_text += " AND d.apl_no = c.apl_no"
        select_text += " AND a.mp_id = '"+l_mp_id+"'"

        

        queryset = mp_mtr.objects.raw(select_text)

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

        query = " select t2.id,t2.att_val AS att_val "
        query += " FROM service20_mp_mtr t1 "
        query += " LEFT JOIN service20_mp_sub t2 ON (t2.mp_id = t1.mp_id "
        query += " AND t2.att_id= 'MP0013' "
        query += " AND t2.att_cdh = 'MP0013' "
        query += " AND t2.att_cdd = '20') "
        query += " WHERE t1.mp_id = '"+l_mp_id+"' "
        query += " AND t1.apl_id='"+l_apl_id+"' "


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

    mnt_fr_dt = request.POST.get('mnt_fr_dt', "")
    mnt_to_dt = request.POST.get('mnt_to_dt', "")

    maxRow = request.POST.get('maxRow', 0)              # 1번 insert
    
    mnt_dt_cnt = request.POST.get('mnt_dt_cnt', 0)      # 2번 insert
    rep_ym = request.POST.get('rep_ym', "")
    
    client_ip = request.META['REMOTE_ADDR']

    update_text = " update service20_mp_plnh a "
    update_text += " , service20_mpgm b "
    update_text += " , service20_mp_mte c "
    update_text += " , (SELECT mp_id "
    update_text += " , apl_no "
    update_text += " , apl_id "
    update_text += " , apl_nm "
    update_text += " FROM service20_mp_mtr "
    update_text += " WHERE apl_id = '"+apl_id+"' "
    update_text += " AND apl_no = '"+apl_no+"') d "
    update_text += " SET a.pln_dt = NOW() "
    update_text += " WHERE a.mp_id = b.mp_id "
    update_text += " AND a.mp_id = c.mp_id "
    update_text += " AND a.mp_id = d.mp_id "
    update_text += " AND a.apl_no = d.apl_no "
    update_text += " AND d.apl_no = c.apl_no "
    
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)

    
    row_max = int(maxRow)
    for i in range(0,row_max):
    
        # pln_no_max = mp_plnd.objects.all().aggregate(vlMax=Max('pln_no'))
        
        # apl_no = 0
        
        # max_no = mp_plnd_max['vlMax']    

        # if max_no == None:
        #     apl_no = 0
        # else:
        #     apl_no = mp_plnd_max['vlMax']
        #     apl_no = apl_no + 1

        mtr_desc = request.POST.get('mtr_desc'+str(i), "")
        pln_no = request.POST.get('pln_no'+str(i+1), "")

        insert_text = " insert into service20_mp_plnd ( "
        insert_text += " mp_id "
        insert_text += " , apl_no "
        insert_text += " , pln_no "
        insert_text += " , pln_sdt "
        insert_text += " , pln_edt "
        insert_text += " , mtr_desc "
        insert_text += " , ins_id "
        insert_text += " , ins_ip "
        insert_text += " , ins_dt "
        insert_text += " , ins_pgm "
        insert_text += " , upd_id "
        insert_text += " , upd_ip "
        insert_text += " , upd_dt "
        insert_text += " , upd_pgm "
        insert_text += " ) "
        insert_text += "  ( select "
        insert_text += " '"+str(mp_id)+"' "
        insert_text += " , '"+str(apl_no)+"' "
        insert_text += " , '"+str(pln_no)+"' "
        insert_text += " , adddate(t2.mnt_fr_dt, 7*('"+str(pln_no)+"'*1-1) + 0) pln_sdt "
        insert_text += " , adddate(t2.mnt_fr_dt, 7*('"+str(pln_no)+"'*1-1) + 6) pln_edt "
        insert_text += " , '"+str(mtr_desc)+"' "
        insert_text += " , '"+str(apl_id)+"' "
        insert_text += " , '"+str(client_ip)+"' "
        insert_text += " , now() "
        insert_text += " , '"+str(ins_pgm)+"' "
        insert_text += " , '"+str(apl_id)+"' "
        insert_text += " , '"+str(client_ip)+"' "
        insert_text += " , now() "
        insert_text += " , '"+str(upd_pgm)+"' "
        insert_text += " from service20_mp_mtr t1 "
        insert_text += " left join service20_mpgm t2 on (t2.mp_id = t1.mp_id) "
        insert_text += " where t1.mp_id = '"+str(mp_id)+"' "
        insert_text += " and apl_id = '"+str(apl_id)+"' "
        insert_text += " )"
        print("ins_1")
        print(insert_text)
        cursor = connection.cursor()
        query_result = cursor.execute(insert_text)    
    
    row_mnt_dt_cnt = int(mnt_dt_cnt)
    for i in range(1,row_mnt_dt_cnt):
        
        # /* 계획서 최초 작성 시 보고서 insert */
        # /* 화면으로부터 넘겨받은 mnt_dt_cnt로 for(i = 1 i < mnt_dt_cnt i++) */
        # /* MP0103M/insert 시 같이 수행되게 해주세요 */
        query = "insert into service20_mp_rep ("
        query += "  mp_id"
        query += ", apl_no"
        query += ", rep_no"
        query += ", rep_div"
        query += ", rep_ym"
        query += ", mnte_id"
        query += ", mnte_nm"
        query += ", tchr_id"
        query += ", tchr_nm"
        query += ", sch_nm"
        query += ", mtr_sub"
        query += ", att_desc"
        query += ", rep_ttl"
        query += ", mtr_obj"
        query += ", rep_dt"
        query += ", req_dt"
        query += ", mtr_desc"
        query += ", coatching"
        query += ", spcl_note"
        query += ", mtr_revw"
        query += ", appr_id"
        query += ", appr_nm"
        query += ", appr_dt"
        query += ", mgr_id"
        query += ", mgr_dt"
        query += ", status"
        query += ", ins_id"
        query += ", ins_ip"
        query += ", ins_dt"
        query += ", ins_pgm"
        query += ", upd_id"
        query += ", upd_ip"
        query += ", upd_dt"
        query += ", upd_pgm"
        query += ")"
        query += "select t1.mp_id  as mp_id"
        query += "     , t1.apl_no as apl_no"
        query += "     , '" + str(i) + "'        as rep_no /* {!i} */"
        query += "     , 'M'       as rep_div /*m - 교육 */"
        query += "     , '" + str(rep_ym) + "'  as rep_ym /* {!rep_ym} */"
        query += "     , null      as mnte_id"
        query += "     , null      as mnte_nm"
        query += "     , null      as tchr_id"
        query += "     , null      as tchr_nm"
        query += "     , null      as sch_nm"
        query += "     , null      as mtr_sub"
        query += "     , null      as att_desc"
        query += "     , concat(date_format(date( STR_TO_DATE('"+str(mnt_fr_dt)+"','%%Y-%%m-%%d %%H:%%i:%%S') + interval "+str(i)+"-1 month), '%%y'), '년 ', date_format(date( STR_TO_DATE('"+str(mnt_fr_dt)+"','%%Y-%%m-%%d %%H:%%i:%%S') + interval "+str(i)+"-1 month), '%%m'), '월 보고서') as rep_ttl"
        query += "     , null      as mtr_obj"
        query += "     , null      as rep_dt"
        query += "     , null      as req_dt"
        query += "     , null      as mtr_desc"
        query += "     , null      as coatching"
        query += "     , null      as spcl_note"
        query += "     , null      as mtr_revw"
        query += "     , null      as appr_id"
        query += "     , null      as appr_nm"
        query += "     , null      as appr_dt"
        query += "     , null      as mgr_id"
        query += "     , null      as mgr_dt"
        query += "     , '00'      as status"
        query += "     , '" + str(apl_id) + "' as ins_id   /* {!login_id} */"
        query += "     , '" + str(client_ip) + "' as ins_ip   /* {!ins_ip} */"
        query += "     , now()     as ins_dt"
        query += "     , '" + str(ins_pgm) + "'   as ins_pgm  /* {!ins_pgm} */"
        query += "     , '" + str(apl_id) + "' as upd_id"
        query += "     , '" + str(client_ip) + "' as upd_ip"
        query += "     , now() as upd_dt"
        query += "     , '" + str(upd_pgm) + "' as upd_pgm"
        query += "  from service20_mp_mtr t1"
        query += " where t1.mp_id  = '" + str(mp_id) + "'"
        query += "   and t1.apl_id = '" + str(apl_id) + "' /* {!apl_id} */"
        print("query_"+str(i))
        print(query)
        cursor = connection.cursor()
        query_result = cursor.execute(insert_text) 

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
    client_ip = request.META['REMOTE_ADDR']

    row_max = int(maxRow)


    ####################################
    # 1번쿼리
    ####################################
    update_text = " update service20_mp_plnh "
    update_text += " SET mtr_sub = '"+str(mtr_sub)+"' "
    # update_text += " , pln_sdt = ifnull(trim(NULLIF('"+str(mtr_pln_sdt)+"','')),DATE_FORMAT(now(),'%Y-%m-%d')) "
    # update_text += " , pln_edt = ifnull(trim(NULLIF('"+str(mtr_pln_edt)+"','')),DATE_FORMAT(now(),'%Y-%m-%d')) "
    update_text += " , upd_id = '"+str(apl_id)+"' "
    update_text += " , upd_ip = '"+str(client_ip)+"' "
    update_text += " , upd_dt = now() "
    update_text += " , upd_pgm = '"+str(upd_pgm)+"' "
    update_text += " WHERE mp_id = '"+str(mp_id)+"' "
    # update_text += " AND apl_no = '"+str(apl_no)+"' "
    update_text += " AND apl_no = '"+str(apl_no)+"' "


    print(update_text)
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)    
    
    ####################################
    # 1번쿼리
    ####################################


    for i in range(0,row_max):

        mtr_desc = request.POST.get('mtr_desc'+str(i), "")
        pln_no = request.POST.get('pln_no'+str(i+1), "")

        ####################################
        # 2번쿼리
        ####################################
        update_text = " update service20_mp_plnd "
        update_text += " SET mtr_desc = '"+str(mtr_desc)+"' "
        # update_text += " , pln_sdt = ifnull(trim(NULLIF('"+str(mtr_pln_sdt)+"','')),DATE_FORMAT(now(),'%Y-%m-%d')) "
        # update_text += " , pln_edt = ifnull(trim(NULLIF('"+str(mtr_pln_edt)+"','')),DATE_FORMAT(now(),'%Y-%m-%d')) "
        update_text += " , upd_id = '"+str(apl_id)+"' "
        update_text += " , upd_ip = '"+str(client_ip)+"' "
        update_text += " , upd_dt = now() "
        update_text += " , upd_pgm = '"+str(upd_pgm)+"' "
        update_text += " WHERE mp_id = '"+str(mp_id)+"' "
        # update_text += " AND apl_no = '"+str(apl_no)+"' "
        update_text += " AND apl_no = '"+str(apl_no)+"' "
        update_text += " AND pln_no = '"+str(pln_no)+"' "

        print(update_text)
        cursor = connection.cursor()
        query_result = cursor.execute(update_text)    
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
# MP0103M - START
#####################################################################################

# 출석관리 리스트 ###################################################
class MP0104M_list_Serializer(serializers.ModelSerializer):

    apl_no = serializers.SerializerMethodField()
    sum_elap_tm = serializers.SerializerMethodField()
    sum_appr_tm = serializers.SerializerMethodField()
    sum_exp_amt = serializers.SerializerMethodField()
    cum_appr_tm = serializers.SerializerMethodField()
    
    
    # mgr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    # pln_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    # appr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    # pln_sedt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = mp_mtr
        fields = ('mp_id','apl_no','mntr_id','indv_div','team_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','bank_acct','bank_cd','bank_nm','bank_dpsr','cnt_mp_a','cnt_mp_p','cnt_mp_c','cnt_mp_g','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','sum_elap_tm','sum_appr_tm','sum_exp_amt','cum_appr_tm')
    
    def get_apl_no(self,obj):
        return obj.apl_no
    def get_sum_elap_tm(self,obj):
        return obj.sum_elap_tm
    def get_sum_appr_tm(self,obj):
        return obj.sum_appr_tm
    def get_sum_exp_amt(self,obj):
        return obj.sum_exp_amt
    def get_cum_appr_tm(self,obj):
        return obj.cum_appr_tm
    


class MP0104M_list(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0104M_list_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_id = request.GET.get('apl_id', "")

        queryset = self.get_queryset()

        query = " select t3.id,t3.mp_id     /* 멘토링 프로그램id*/ "
        query += " , t1.apl_no    /* 멘토 지원 no*/ "
        query += " , t3.mntr_id         /* 멘토id*/ "
        query += " , t3.apl_nm          /* 지원자(멘토,학생) 명*/ "
        query += " , t3.unv_nm          /* 지원자 대학교 명*/ "
        query += " , t3.cllg_nm         /* 지원자 대학 명*/ "
        query += " , t3.dept_nm         /* 지원자 학부/학과 명*/ "
        query += " , t3.sch_yr          /* 학년 */"
        query += " , sec_to_time(sum(time_to_sec(t1.elap_tm))) sum_elap_tm  /* 경과시간*/ "
        query += " , sum(t1.appr_tm)   sum_appr_tm /* 인정시간*/ "
        query += " , sum(t1.exp_amt)   sum_exp_amt /* 지급 활동비 */"
        query += " , sum(t1.appr_tm)   cum_appr_tm /* 누적시간*/ "
        query += " , t3.bank_nm         /* 은행 명*/ "
        query += " , t3.bank_acct       /* 은행 계좌 번호*/ "
        query += " , t3.apl_id "
        query += " from service20_mp_att t1     /* 프로그램 출석부(멘토)*/ "
        query += " left join service20_mp_mtr t3 on (t3.mp_id    = t1.mp_id "
        query += " and t3.apl_no   = t1.apl_no) "
        query += " where 1=1 "
        # query += " and t1.mp_id    = '"+l_mp_id+"'    /* 멘토링 프로그램id */ "
        query += " and t3.apl_id   = '"+l_apl_id+"'   "
        query += " group by t1.mp_id     /* 멘토링 프로그램id */ "
        query += " , t1.apl_no    /* 멘토 지원 no */ "
        query += " , t3.mntr_id         /* 멘토id  */ "
        query += " , t3.apl_nm          /* 지원자(멘토,학생) 명 */ "
        query += " , t3.unv_nm          /* 지원자 대학교 명 */ "
        query += " , t3.cllg_nm         /* 지원자 대학 명 */ "
        query += " , t3.dept_nm         /* 지원자 학부/학과 명 */ "
        query += " , t3.sch_yr          /* 학년 */ "
        query += " , t3.bank_nm         /* 은행 명 */ "
        query += " , t3.bank_acct "



        queryset = mp_mtr.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

# 출석관리 리스트 상세 ###################################################
class MP0104M_Detail_Serializer(serializers.ModelSerializer):

    mp_div_nm = serializers.SerializerMethodField()
    mnte_id = serializers.SerializerMethodField()
    mnte_nm = serializers.SerializerMethodField()
    mgr_nm = serializers.SerializerMethodField()
    expl_yn = serializers.SerializerMethodField()
    apl_id = serializers.SerializerMethodField()
    att_etm = serializers.SerializerMethodField()
    att_stm = serializers.SerializerMethodField()
    
    # mgr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    
    class Meta:
        model = mp_att
        fields = ('mp_id','apl_no','att_no','mp_div','spc_no','att_div','att_sts','att_sdt','att_saddr','att_sdist','att_edt','att_eaddr','att_edist','elap_tm','appr_tm','mtr_desc','mtr_pic','appr_id','appr_nm','appr_dt','mgr_id','mgr_dt','expl_yn','rep_no','exp_div','exp_no','exp_dt','exp_amt','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','mp_div_nm','mnte_id','mnte_nm','mgr_nm','expl_yn','apl_id','att_etm','att_stm')
    
    def get_mp_div_nm(self,obj):
        return obj.mp_div_nm
    def get_mnte_id(self,obj):
        return obj.mnte_id
    def get_mnte_nm(self,obj):
        return obj.mnte_nm
    def get_mgr_nm(self,obj):
        return obj.mgr_nm
    def get_expl_yn(self,obj):
        return obj.expl_yn
    def get_apl_id(self,obj):
        return obj.apl_id
    def get_att_etm(self,obj):
        return obj.att_etm
    def get_att_stm(self,obj):
        return obj.att_stm  


class MP0104M_Detail(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = MP0104M_Detail_Serializer

    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_id = request.GET.get('apl_id', "")

        queryset = self.get_queryset()

        query = " select t1.id,t1.mp_id     /* 멘토링 프로그램id */  "
        query += " , t1.apl_no    /* 멘토 지원 no */  "
        query += " , t1.att_no    /* 출석순서(seq) */  "
        query += " , t1.mp_div    /* 교육구분(mp0059) */  "
        query += " , c1.std_detl_code_nm   as mp_div_nm "
        query += " , t2.mnte_id     /* 멘티id */  "
        query += " , t2.mnte_nm     /* 멘티명 */  "
        query += " , substring(t1.att_sdt, 1, 10) as att_sdt   /* 출석일시(교육시작일시) */  "
        query += " , substring(t1.att_sdt, 12, 5) as att_stm   /* 출석일시(교육시작일시) */  "
        query += " , substring(t1.att_edt, 12, 5) as att_etm   /* 출석일시(교육시작일시) */  "
        query += " , substring(t1.elap_tm, 1, 5)  as elap_tm   /* 경과시간 */  "
        query += " , t1.appr_tm   /* 인정시간 */  "
        query += " , t1.mtr_desc  /* 멘토링 내용(보고서) */  "
        query += " , t1.appr_id   /* 승인자id */  "
        query += " , t1.appr_nm   /* 승인자명 */  "
        query += " , substring(t1.appr_dt, 1, 16)  as appr_dt  /* 보호자 승인일시 */  "
        query += " , t1.mgr_id    /* 관리자id */  "
        query += " , t4.mgr_nm    /* 관리자명 */  "
        query += " , substring(t1.mgr_dt, 1, 16)  as mgr_dt   /* 관리자 승인일시 */  "
        query += " , ' ' expl_yn   /* 소명상태 */  "
        query += " , t1.exp_amt   /* 지급 활동비 */  "
        query += " , t3.apl_id /* 학번 */ "
        query += " from service20_mp_att t1     /* 프로그램 출석부(멘토) */ "
        query += " left join service20_mp_mte t2  on (t2.mp_id  = t1.mp_id and t2.apl_no = t1.apl_no)  "
        query += " left join service20_mp_mtr t3 on (t3.mp_id    = t1.mp_id and t3.apl_no   = t1.apl_no) "
        query += " left join service20_mpgm   t4 on (t4.mp_id    = t1.mp_id) "
        query += " left join service20_com_cdd c1 on (c1.std_grp_code  = 'mp0059' and c1.std_detl_code = t1.mp_div) "
        query += " where 1=1 "
        query += " and t1.mp_id    = '"+l_mp_id+"'   /* 멘토링 프로그램id */ "
        query += " and t3.apl_id   = '"+l_apl_id+"' "
        query += " order by t1.att_no DESC    /* 출석순서(seq) */ "



        queryset = mp_att.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


#####################################################################################
# MP0104M - END
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

        query = " select A.id "
        query += " , A.mp_id "
        query += " , A.apl_no "
        query += " , B.mp_name "
        query += " FROM service20_mp_mtr A "
        query += " , service20_mpgm B "
        query += " WHERE apl_id = '"+l_apl_id+"' "
        query += " AND mntr_id IS NOT null "
        query += " AND A.mp_id = B.mp_id "

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
        fields = ('mp_id','apl_no','rep_no','rep_div','rep_ttl','mtr_obj','rep_dt','req_dt','mtr_desc','coatching','spcl_note','mtr_revw','appr_id','appr_nm','appr_dt','mgr_id','mgr_dt','status','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','unv_nm','cllg_nm','dept_nm','apl_id','apl_nm','rep_div_nm','status_nm','req_dt_sub','appr_dt_sub','mgr_dt_sub','rep_ym')
    
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

        query = " select t1.id "
        query += " , t1.mp_id     /* 멘토링 프로그램id */ "
        query += " , t2.unv_nm          /* 지원자 대학교 명 */ "
        query += " , t2.cllg_nm         /* 지원자 대학 명 */ "
        query += " , t2.dept_nm         /* 지원자 학부/학과 명 */ "
        query += " , t2.apl_id          /* 지원자(멘토,학생) 학번 */ "
        query += " , t2.apl_nm          /* 지원자(멘토,학생) 명 */ "
        query += " , t1.rep_div         /* 보고서 구분(mp0062) */ "
        query += " , c2.std_detl_code_nm   as rep_div_nm "
        query += " , t1.status          /* 상태(mp0070) */ "
        query += " , c1.std_detl_code_nm   as status_nm "
        query += " , substring(t1.req_dt,  1, 10) req_dt_sub    /* 승인요청일 */ "
        query += " , substring(t1.appr_dt, 1, 10) appr_dt_sub   /* 보호자 승인일시 */ "
        query += " , substring(t1.mgr_dt,  1, 10) mgr_dt_sub   /* 관리자 승인일시 */ "
        query += " , t1.rep_ttl   /* 보고서 제목 : 내용 */ "
        query += " , t1.apl_no    /* 멘토 지원 no */ "
        query += " , t1.rep_no    /* 보고서 no */ "
        query += " , t1.rep_div   /* 보고서 구분(mp0062) */ "
        query += " , t1.rep_ttl   /* 보고서 제목 */ "
        query += " , t1.mtr_obj   /* 학습목표 */ "
        query += " , t1.rep_dt    /* 보고서작성일 */ "
        query += " , t1.req_dt    /* 승인요청일 */ "
        query += " , t1.mtr_desc  /* 학습내용 */ "
        query += " , t1.coatching /* 학습외 지도(상담) */ "
        query += " , t1.spcl_note /* 특이사항 */ "
        query += " , t1.mtr_revw  /* 소감문 */ "
        query += " , t1.appr_id   /* 승인자id */ "
        query += " , t1.appr_nm   /* 승인자명 */ "
        query += " , t1.appr_dt   /* 보호자 승인일시 */ "
        query += " , t1.mgr_id    /* 관리자id */ "
        query += " , t1.mgr_dt    /* 관리자 승인일시 */ "
        query += " , t1.rep_ym     "
        query += " from service20_mp_rep t1     /* 프로그램 보고서 */ "
        query += " left join service20_mp_mtr t2 on (t2.mp_id   = t1.mp_id "
        query += " and t2.apl_no = t1.apl_no)       /* 지원 멘토 */ "
        query += " left join service20_com_cdd c1 on (c1.std_grp_code  = 'MP0070'  /* 상태(mp0070) */ "
        query += " and c1.std_detl_code = t1.status) "
        query += " left join service20_com_cdd c2 on (c2.std_grp_code  = 'MP0062'  /* 보고서 구분(mp0062) */ "
        query += " and c2.std_detl_code = t1.rep_div) "
        query += " where 1=1 "
        query += " and date_format(now(),'%%Y%%m') > t1.rep_ym "
        query += " and t1.mp_id     = '"+l_mp_id+"'     /* 멘토링 프로그램id */ "
        # query += " and t1.rep_div   = 'M' "
        # query += " and t1.status    =  '20' /* 제출, 40 완료 */ "
        query += " and t2.apl_id    =  '"+l_apl_id+"' "

        
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
    tchr_id = serializers.SerializerMethodField()
    mnte_id = serializers.SerializerMethodField()

    req_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    appr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mgr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = mp_rep
        fields = ('mp_id','apl_no','rep_no','rep_div','rep_ttl','mtr_obj','rep_dt','req_dt','mtr_desc','coatching','spcl_note','mtr_revw','appr_id','appr_nm','appr_dt','mgr_id','mgr_dt','status','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','rep_div_nm','apl_m','teacher','mte_nm','sch_yr','obj_sub','aaa','status_nm','unv_nm','cllg_nm','dept_nm','mgr_nm','tchr_id','mnte_id')
    
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
    def get_tchr_id(self,obj):    
        return obj.tchr_id
    def get_mnte_id(self,obj):    
        return obj.mnte_id    

class MP0105M_detail(generics.ListAPIView):
    queryset = mp_rep.objects.all()
    serializer_class = MP0105M_detail_Serializer


    def list(self, request):
        
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_id = request.GET.get('apl_id', "")
        l_rep_ym = request.GET.get('rep_ym', "")

        queryset = self.get_queryset()

        # /*보고서 상세*/
        query = " select t1.id,t1.mp_id                                         /* 멘토링 프로그램id   */ "
        query += " , t1.rep_div                                       /* 보고서 구분(mp0062) */ "
        query += " , t1.rep_ttl                                       /* 보고서 제목 : 내용  */ "
        query += " , c2.std_detl_code_nm               as rep_div_nm    "
        query += " , concat(t2.apl_id, '/', t2.apl_nm) as apl_m       /* 지원자(멘토,학생) 명*/ "
        
        query += " , t1.tchr_id                                       /* 담당멘티id*/ "
        query += " , t1.tchr_nm                        as teacher     /* 담당멘티명*/ "
        query += " , t1.mnte_id                                       /* 담당멘티id*/ "
        query += " , t1.mnte_nm                        as mte_nm        /* 담당멘티명*/ "
        query += " , t1.sch_nm                         as sch_yr        /* 학교명*/ "
        query += " , t1.mtr_sub                        as obj_sub     /* 지도과목*/ " 
        query += " , t1.att_desc                       as aaa          /* 출석현황*/ "

        query += " , substring(t1.rep_dt,  1, 10)      as rep_dt      /* 보고서작성일         */ "
        query += " , substring(t1.req_dt,  1, 10)      as req_dt      /* 승인요청일         */ "
        query += " , t1.appr_nm                                       /* 승인자명            */ "
        query += " , substring(t1.appr_dt,  1, 10)     as appr_dt     /* 보호자 승인일시      */ "
        query += " , t1.mgr_id                         as mgr_id      /* 관리자id            */ "
        query += " , (select mgr_nm from service20_mpgm where mp_id = t1.mp_id) as mgr_nm "
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
        query += " and t1.rep_ym    = '"+l_rep_ym+"' "

        queryset = mp_rep.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)                

class MP0105M_detail_2_Serializer(serializers.ModelSerializer):

    # testField = serializers.SerializerMethodField()
    mp_id = serializers.SerializerMethodField()
    rep_div_nm = serializers.SerializerMethodField()
    apl_m = serializers.SerializerMethodField()
    tchr_id = serializers.SerializerMethodField()
    tchr_nm = serializers.SerializerMethodField()
    mnte_id = serializers.SerializerMethodField()
    mnte_nm = serializers.SerializerMethodField()
    sch_yr = serializers.SerializerMethodField()
    mtr_sub = serializers.SerializerMethodField()
    att_desc = serializers.SerializerMethodField()
    rep_dt = serializers.SerializerMethodField()
    req_dt = serializers.SerializerMethodField()
    appr_id = serializers.SerializerMethodField()
    appr_nm = serializers.SerializerMethodField()
    appr_dt = serializers.SerializerMethodField()
    mgr_id = serializers.SerializerMethodField()
    mgr_nm = serializers.SerializerMethodField()
    mgr_dt = serializers.SerializerMethodField()
    status_nm = serializers.SerializerMethodField()
    mtr_desc = serializers.SerializerMethodField()
    coatching = serializers.SerializerMethodField()
    spcl_note = serializers.SerializerMethodField()
    mtr_revw = serializers.SerializerMethodField()
    apl_no = serializers.SerializerMethodField()
    apl_id = serializers.SerializerMethodField()
    teacher = serializers.SerializerMethodField()
    mte_nm = serializers.SerializerMethodField()
    obj_sub = serializers.SerializerMethodField()
    aaa = serializers.SerializerMethodField()
    grd_id = serializers.SerializerMethodField()
    grd_nm = serializers.SerializerMethodField()

    req_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    appr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    mgr_dt = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    class Meta:
        model = mp_rep
        fields = ('mp_id','apl_no','rep_no','rep_div','rep_ttl','mtr_obj','rep_dt','req_dt','mtr_desc','coatching','spcl_note','mtr_revw','appr_id','appr_nm','appr_dt','mgr_id','mgr_dt','status','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','rep_ym','sch_yr','rep_div_nm','apl_m','tchr_id','tchr_nm','mnte_id','mnte_nm','mtr_sub','att_desc','status_nm','apl_id','teacher','mte_nm','obj_sub','aaa','mgr_nm','grd_id','grd_nm')
    
    def get_mp_id(self,obj):
        return obj.mp_id
    def get_rep_div_nm(self,obj):
        return obj.rep_div_nm
    def get_apl_m(self,obj):
        return obj.apl_m
    def get_tchr_id(self,obj):
        return obj.tchr_id
    def get_tchr_nm(self,obj):
        return obj.tchr_nm
    def get_mnte_id(self,obj):
        return obj.mnte_id
    def get_mnte_nm(self,obj):
        return obj.mnte_nm
    def get_sch_yr(self,obj):
        return obj.sch_yr
    def get_mtr_sub(self,obj):
        return obj.mtr_sub
    def get_att_desc(self,obj):
        return obj.att_desc
    def get_rep_dt(self,obj):
        return obj.rep_dt
    def get_req_dt(self,obj):
        return obj.req_dt
    def get_appr_id(self,obj):
        return obj.appr_id
    def get_appr_nm(self,obj):
        return obj.appr_nm
    def get_appr_dt(self,obj):
        return obj.appr_dt
    def get_mgr_id(self,obj):
        return obj.mgr_id
    def get_mgr_nm(self,obj):
        return obj.mgr_nm
    def get_mgr_dt(self,obj):
        return obj.mgr_dt
    def get_status_nm(self,obj):
        return obj.status_nm
    def get_mtr_desc(self,obj):
        return obj.mtr_desc
    def get_coatching(self,obj):
        return obj.coatching
    def get_spcl_note(self,obj):
        return obj.spcl_note
    def get_mtr_revw(self,obj):
        return obj.mtr_revw
    def get_apl_no(self,obj):
        return obj.apl_no
    def get_apl_id(self,obj):
        return obj.apl_id   
    def get_teacher(self,obj):
        return obj.teacher
    def get_mte_nm(self,obj):
        return obj.mte_nm
    def get_obj_sub(self,obj):
        return obj.obj_sub
    def get_aaa(self,obj):    
        return obj.aaa 
    def get_grd_id(self,obj):
        return obj.grd_id       
    def get_grd_nm(self,obj):
        return obj.grd_nm

class MP0105M_detail_2(generics.ListAPIView):
    queryset = mp_rep.objects.all()
    serializer_class = MP0105M_detail_2_Serializer


    def list(self, request):
        mp_id = request.GET.get('mp_id', "")
        apl_id = request.GET.get('apl_id', "")
        rep_ym = request.GET.get('rep_ym', "")

        queryset = self.get_queryset()

        # /*보고서 상세*/
        query = "select t2.id,t1.mp_id       /* 멘토링 프로그램id   */ "
        query += "     , t2.rep_div     /* 보고서 구분(mp0062) */"
        query += "     , t2.rep_ttl     /* 보고서 제목 : 내용  */"
        query += "     , (select std_detl_code_nm "
        query += "          from service20_com_cdd "
        query += "         where std_grp_code  = 'mp0062' "
        query += "           and std_detl_code = t2.rep_div)   as rep_div_nm     "
        query += "     , concat(t1.apl_id, '/', t1.apl_nm)     as apl_m       /* 지원자(멘토,학생) 명*/ "
        query += "     , t3.tchr_id     /* 지도교사 id */"
        query += "     , t3.tchr_nm  as teacher   /* 지도교사 명 */     "
        query += "     , t3.mnte_id     /* 멘티id */ "
        query += "     , t3.mnte_nm  as mte_nm"
        query += "     , t3.sch_yr      /* 학교명/학년 */ "
        query += "     , t3.mtr_sub  as obj_sub   /* 지도과목 */ "
        query += "     , (select concat(count(*), '회 ', ifnull(sum(s1.appr_tm), 0), '시간') "
        query += "         from service20_mp_att s1 "
        query += "        where s1.mp_id = t1.mp_id "
        query += "          and s1.apl_no = t1.apl_no "
        query += "          and "
        query += "              ("
        query += "                  s1.att_sdt >= concat(t2.rep_ym, '01') "
        query += "              and s1.att_sdt  < concat(date_format(date(concat(t2.rep_ym, '01') + interval 1 month), '%%y%%m'), '01')"
        query += "              ) "
        query += "       ) as aaa   /*출석현황*/  "
        query += "     , null as rep_dt "
        query += "     , null as req_dt              "
        query += "     , t3.tchr_id as appr_id "
        query += "     , t3.tchr_nm as appr_nm "
        query += "     , null       as appr_dt "
        query += "     , t4.mgr_id  as mgr_id "
        query += "     , t4.mgr_nm  as mgr_nm "
        query += "     , null       as mgr_dt"
        query += "     , t2.status "
        query += "     , c1.std_detl_code_nm as status_nm     "
        query += "     , t2.mtr_obj "
        query += "     , fn_mp_att_select_01(t1.mp_id, t1.apl_id, t2.rep_ym ) as mtr_desc ";
        query += "     , '' as coatching "
        query += "     , '' as spcl_note "
        query += "     , '' as mtr_revw    "
        query += "     "
        query += "     , t1.apl_no "
        query += "     , t1.apl_id "
        query += "     , t2.rep_no "
        query += "     , t2.rep_ym "
        query += "     , t3.grd_id    /*주보호자id*/";
        query += "     , t3.grd_nm    /*보호자명*/";
        query += "  from service20_mp_mtr t1 "
        query += "   left join service20_mp_rep t2 "
        query += "       on ("
        query += "           t2.mp_id = t1.mp_id "
        query += "       and t2.apl_no = t1.apl_no"
        query += "       ) "
        query += "   left join service20_mpgm t4 "
        query += "       on ("
        query += "           t4.mp_id = t1.mp_id"
        query += "       ) "
        query += "   left join "
        query += "       (select distinct s2.tchr_id  "
        query += "            , s2.tchr_nm  "
        query += "            , s2.mnte_id  "
        query += "            , s2.mnte_nm "
        query += "            , concat(s2.sch_nm, '/', s2.sch_yr, '학년') as sch_yr /* 학교명/학년 */ "
        query += "            , s3.mtr_sub /* 지도과목 */"
        query += "            , truncate(rand()*7 + 1, 0) as att_desc  "
        query += "            , s3.mtr_obj "
        query += "            , s1.mp_id "
        query += "            , s1.apl_no "
        query += "            , s1.apl_id "
        query += "            , s2.grd_id "
        query += "            , s2.grd_nm "
        query += "         from service20_mp_mtr s1 "
        query += "          left join service20_mp_mte s2 "
        query += "              on ("
        query += "                  s2.mp_id = s1.mp_id "
        query += "              and s2.apl_no = s1.apl_no"
        query += "              ) "
        query += "          left join service20_mp_plnh s3 "
        query += "              on ("
        query += "                  s3.mp_id = s1.mp_id "
        query += "              and s3.apl_no = s1.apl_no"
        query += "              ) "
        query += "       ) t3 "
        query += "       on ("
        query += "           t3.mp_id = t1.mp_id "
        query += "       and t3.apl_no = t1.apl_no"
        query += "       ) "
        query += "   left join service20_com_cdd c1 "
        query += "       on ("
        query += "           c1.std_grp_code = 'mp0070'  "
        query += "       and c1.std_detl_code = t2.status"
        query += "       ) "
        query += " where t1.mp_id = '"+str(mp_id)+"' "
        query += "   and t1.apl_id = '"+str(apl_id)+"' "
        query += "   and t2.status = '00' "
        query += "   and t2.rep_ym = '"+str(rep_ym)+"'"


        queryset = mp_rep.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)        

# 보고서 현황 save
@csrf_exempt
def MP0105M_update(request,pk):


    mp_id     = request.POST.get('mp_id', "")
    apl_no    = request.POST.get('apl_no', 0)
    rep_no    = request.POST.get('rep_no', 0)
    rep_div   = request.POST.get('rep_div', "")
    mnte_id   = request.POST.get('mnte_id', "")
    mnte_nm   = request.POST.get('mnte_nm', "")
    tchr_id   = request.POST.get('tchr_id', "")
    tchr_nm   = request.POST.get('tchr_nm', "")
    sch_nm    = request.POST.get('sch_nm', "")
    mtr_sub   = request.POST.get('mtr_sub', "")
    att_desc  = request.POST.get('att_desc', "")
    rep_ttl   = request.POST.get('rep_ttl', "")
    mtr_obj   = request.POST.get('mtr_obj', "")
    rep_dt    = request.POST.get('rep_dt', "")
    req_dt    = request.POST.get('req_dt', "")
    mtr_desc  = request.POST.get('mtr_desc', "")
    coatching = request.POST.get('coatching', "")
    spcl_note = request.POST.get('spcl_note', "")
    mtr_revw  = request.POST.get('mtr_revw', "")
    appr_id   = request.POST.get('appr_id', "")
    appr_nm   = request.POST.get('appr_nm', "")
    appr_dt   = request.POST.get('appr_dt', "")
    mgr_id    = request.POST.get('mgr_id', "")
    mgr_dt    = request.POST.get('mgr_dt', "")
    status    = request.POST.get('status', "")
    ins_id    = request.POST.get('ins_id', "")
    ins_ip    = request.POST.get('ins_ip', "")
    ins_dt    = request.POST.get('ins_dt', "")
    ins_pgm   = request.POST.get('ins_pgm', "")
    upd_id    = request.POST.get('upd_id', "")
    upd_ip    = request.POST.get('upd_ip', "")
    upd_dt    = request.POST.get('upd_dt', "")
    upd_pgm   = request.POST.get('upd_pgm', "")

    teacher   = request.POST.get('teacher', "")
    sch_yr    = request.POST.get('sch_yr', "")
    obj_sub   = request.POST.get('obj_sub', "")
    aaa       = request.POST.get('aaa', "")
    mte_nm   = request.POST.get('mte_nm', "")
    status   = request.POST.get('status', "")
    appr_id  = request.POST.get('appr_id', "")
    appr_nm  = request.POST.get('appr_nm', "")
    mgr_id   = request.POST.get('mgr_id', "")
    grd_id   = request.POST.get('grd_id', "")
    grd_nm   = request.POST.get('grd_nm', "")
    client_ip = request.META['REMOTE_ADDR']

    update_text = ""
    if pk == 1:
        # /*보고서현황작성_승인요청*/
        update_text = " update service20_mp_rep "
        update_text += " set mtr_obj    = '"+str(mtr_obj)  +"'    /*학습목표*/         "    
        update_text += " , mtr_desc    = '"+str(mtr_desc) +"'    /*학습내용*/         "    
        update_text += " , coatching   = '"+str(coatching)+"'    /*학습외 지도(상담)*/"    
        update_text += " , spcl_note   = '"+str(spcl_note)+"'    /*특이사항*/         "    
        update_text += " , mtr_revw    = '"+str(mtr_revw) +"'    /*소감문*/           "    

        update_text += " , mnte_id     = '" +mnte_id+"'      /*담당멘티id*/ "
        update_text += " , mnte_nm     = '" +mte_nm+"'      /*담당멘티명*/ "
        update_text += " , tchr_id     = '" +tchr_id+"'      /*담당교사id*/ "
        update_text += " , tchr_nm     = '" +teacher+"'      /*담당교사명*/ "
        update_text += " , sch_nm      = '" +sch_yr+"'       /*학교명*/ "
        update_text += " , mtr_sub     = '" +obj_sub+"'      /*지도과목*/ "
        update_text += " , att_desc    = '" +aaa+"'          /*출석현황*/   "
        update_text += " , status    = '10'          /*status - 제출*/   "
        update_text += " , appr_id     = '" +str(appr_id)+"'       "
        update_text += " , appr_nm     = '" +str(appr_nm)+"'       "
        update_text += " , mgr_id      = '" +str(mgr_id)+"'        "

        update_text += " , grd_id      = '" +str(grd_id)+"'      /*주보호자id*/";
        update_text += " , grd_nm      = '" +str(grd_nm)+"'      /*보호자명*/";

        update_text += " , rep_dt      = now()    /*보고서작성일*/     "    
        update_text += " , upd_id      = '"+str(upd_id)   +"'    /*수정자id*/         "    
        update_text += " , upd_ip      = '"+str(client_ip)   +"'    /*수정자ip*/         "    
        update_text += " , upd_dt      = now()    /*수정일시*/         "    
        update_text += " , upd_pgm     = '"+str(upd_pgm)  +"'    /*수정프로그램id*/   "    
        update_text += " where 1=1 "
        update_text += " and mp_id  = '" +mp_id+"' "
        update_text += " and apl_no = '"+str(apl_no)+"' "
        update_text += " and rep_no = '"+str(rep_no)+"' "

        
    elif pk == 2:
        # /*보고서현황작성_승인요청*/
        update_text = " update service20_mp_rep "
        update_text += " set mtr_obj    = '"+str(mtr_obj)  +"'    /*학습목표*/         "    
        update_text += " , mtr_desc    = '"+str(mtr_desc) +"'    /*학습내용*/         "    
        update_text += " , coatching   = '"+str(coatching)+"'    /*학습외 지도(상담)*/"    
        update_text += " , spcl_note   = '"+str(spcl_note)+"'    /*특이사항*/         "    
        update_text += " , mtr_revw    = '"+str(mtr_revw) +"'    /*소감문*/           "    
        update_text += " , rep_dt      = case when rep_dt is null then rep_dt else now() end    /*보고서작성일*/     "    

        update_text += " , mnte_id     = '" +mnte_id+"'      /*담당멘티id*/ "
        update_text += " , mnte_nm     = '" +mte_nm+"'      /*담당멘티명*/ "
        update_text += " , tchr_id     = '" +tchr_id+"'      /*담당교사id*/ "
        update_text += " , tchr_nm     = '" +teacher+"'      /*담당교사명*/ "
        update_text += " , sch_nm      = '" +sch_yr+"'       /*학교명*/ "
        update_text += " , mtr_sub     = '" +obj_sub+"'      /*지도과목*/ "
        update_text += " , att_desc    = '" +aaa+"'          /*출석현황*/   "
        update_text += " , status    = '20'          /*status - 제출*/   "
        update_text += " , appr_id     = '" +str(appr_id)+"'       "
        update_text += " , appr_nm     = '" +str(appr_nm)+"'       "
        update_text += " , mgr_id      = '" +str(mgr_id)+"'        "

        update_text += " , grd_id      = '" +str(grd_id)+"'      /*주보호자id*/";
        update_text += " , grd_nm      = '" +str(grd_nm)+"'      /*보호자명*/";

        update_text += " , req_dt      = now()    /*승인요청일*/       "
        update_text += " , upd_id      = '"+str(upd_id)   +"'    /*수정자id*/         "    
        update_text += " , upd_ip      = '"+str(client_ip)   +"'    /*수정자ip*/         "    
        update_text += " , upd_dt      = now()    /*수정일시*/         "    
        update_text += " , upd_pgm     = '"+str(upd_pgm)  +"'    /*수정프로그램id*/   "    
        update_text += " where 1=1 "
        update_text += " and mp_id  = '" +mp_id+"' "
        update_text += " and apl_no = '"+str(apl_no)+"' "
        update_text += " and rep_no = '"+str(rep_no)+"' "
    
    print(update_text)
    cursor = connection.cursor()
    query_result = cursor.execute(update_text)
 
        
    context = {'message': 'Ok'}

    return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

#####################################################################################
# MP0105M - END
#####################################################################################


#####################################################################################
# MP0106M - START
#####################################################################################

# 보고서 현황 리스트 ###################################################
class MP0106M_list_Serializer(serializers.ModelSerializer):

    bank_acct_mask = serializers.SerializerMethodField()

    class Meta:
        model = mp_exp
        fields = ('mp_id','apl_no','exp_no','exp_mon','exp_div','exp_ttl','exp_dt','bank_dt','elap_tm','unit_price','appr_tm','sum_exp','bank_acct','bank_cd','bank_nm','bank_dpsr','mp_sname','mgr_id','mgr_dt','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','bank_acct_mask')

    def get_bank_acct_mask(self,obj):
        return obj.bank_acct_mask

class MP0106M_list(generics.ListAPIView):
    queryset = mp_rep.objects.all()
    serializer_class = MP0106M_list_Serializer


    def list(self, request):
        l_mp_id = request.GET.get('mp_id', "")
        l_apl_id = request.GET.get('apl_id', "")


        queryset = self.get_queryset()

        query = " select t1.id,t1.mp_id                              /*멘토링 프로그램id     */ "
        query += " , t1.apl_no                             /*멘토 지원 no        */ "
        query += " , t1.exp_no                             /*활동비 no        */ "
        query += " , substring(t1.exp_mon,5,2) as exp_mon  /*활동비 월        */ "
        query += " , t1.exp_div                            /*활동비 구분        */ "
        query += " , t1.exp_ttl                            /*활동비 제목        */ "
        query += " , t1.appr_tm                            /*인정시간 합계        */ "
        query += " , t1.sum_exp                            /*활동비=appr_tm * unit_price*/ "
        query += " , t1.bank_acct                          /*은행 계좌 번호        */ "
        query += " , t1.bank_cd                            /*은행 코드        */ "
        query += " , t1.bank_nm                            /*은행 명           */ "
        query += " , t1.bank_dpsr                          /*예금주           */ "
        query += ", concat(left(t1.bank_acct,2),repeat('*',length(t1.bank_acct)-4),right(t1.bank_acct,2))  as bank_acct_mask ";
        query += " from service20_mp_exp t1                   /*프로그램 출석부(멘토)     */ "
        query += " left join service20_mp_mtr t3 on (t3.mp_id    = t1.mp_id "
        query += " and t3.apl_no   = t1.apl_no) "
        query += " where 1=1 "
        query += " and t1.mp_id    = '"+l_mp_id+"'     "
        query += " and t3.apl_id   = '"+l_apl_id+"' "
        query += " order by t1.exp_mon "

        queryset = mp_exp.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


#####################################################################################
# MP0106M - END
#####################################################################################



#####################################################################################
# TE0201 - START
#####################################################################################

# 멘티의 프로그램 신청현황 리스트 ###################################################
class TE0201_list_Serializer(serializers.ModelSerializer):

    # testField = serializers.SerializerMethodField()
    mp_name = serializers.SerializerMethodField()
    

    class Meta:
        model = mp_mtr
        fields = ('mp_id','apl_no','mntr_id','indv_div','team_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','bank_acct','bank_cd','bank_nm','bank_dpsr','cnt_mp_a','cnt_mp_p','cnt_mp_c','cnt_mp_g','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','mp_name','pr_yr','pr_sch_yr','pr_term_div','mp_name')

    def get_mp_name(self,obj):
        return obj.mp_name

class TE0201_list(generics.ListAPIView):
    queryset = mp_rep.objects.all()
    serializer_class = TE0201_list_Serializer


    def list(self, request):
        l_yr = request.GET.get('yr', "")
        l_mp_id = request.GET.get('mp_id', "")
        l_mnt_term = request.GET.get('mnt_term', "")
        l_mnte_id = request.GET.get('mnte_id', "")


        queryset = self.get_queryset()


        # /* 멘티의 프로그램 신청현황 조회 TE0201/list */
        select_text = " select a.yr, a.mnt_term, a.mp_name, b.mp_hm, b.mp_plc, b.status"
        select_text += " FROM service20_mpgm a LEFT JOIN service20_mp_mte b ON (a.mp_id = b.mp_id)"
        select_text += " WHERE a.yr like '"+l_yr+"'"
        select_text += " AND a.mnt_term like '"+l_mnt_term+"'"
        select_text += " AND a.mp_id like '"+l_mp_id+"'"
        select_text += " AND b.mnte_id like '"+l_mnte_id+"'"

        queryset = mp_mtr.objects.raw(select_text)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# 멘티의 프로그램 신청현황 리스트 ###################################################
class TE0201_detail_Serializer(serializers.ModelSerializer):

    # testField = serializers.SerializerMethodField()
    mp_name = serializers.SerializerMethodField()
    

    class Meta:
        model = mp_mtr
        fields = ('mp_id','apl_no','mntr_id','indv_div','team_id','apl_id','apl_nm','apl_nm_e','unv_cd','unv_nm','cllg_cd','cllg_nm','dept_cd','dept_nm','brth_dt','gen','yr','term_div','sch_yr','mob_no','tel_no','tel_no_g','h_addr','post_no','email_addr','bank_acct','bank_cd','bank_nm','bank_dpsr','cnt_mp_a','cnt_mp_p','cnt_mp_c','cnt_mp_g','apl_dt','status','doc_cncl_dt','doc_cncl_rsn','tot_doc','score1','score2','score3','score4','score5','score6','cscore1','cscore2','cscore3','cscore4','cscore5','cscore6','doc_rank','doc_rslt','intv_team','intv_dt','intv_part_pl','intv_np_rsn_pl','intv_part_pl_dt','intv_part_ac','intv_np_rsn_ac','intv_part_ac_dt','intv_tot','intv_rslt','ms_trn_yn','fnl_rslt','mntr_dt','sms_send_no','ins_id','ins_ip','ins_dt','ins_pgm','upd_id','upd_ip','upd_dt','upd_pgm','mp_name','pr_yr','pr_sch_yr','pr_term_div','mp_name')

    def get_mp_name(self,obj):
        return obj.mp_name

class TE0201_detail(generics.ListAPIView):
    queryset = mp_rep.objects.all()
    serializer_class = TE0201_detail_Serializer


    def list(self, request):

        l_mnte_id = request.GET.get('mnte_id', "")


        queryset = self.get_queryset()


        # /* 멘티의 프로그램 신청현황 멘티 상세 조회 TE0201/detail */
        select_text = "select mnte_nm, sch_nm, h_addr, brth_dt, sch_yr, mob_no, grd_nm"
        select_text += ", case when grd_rel = '11' then '부'"
        select_text += " when grd_rel = '12' then '모'"
        select_text += " when grd_rel = '21' then '조부'"
        select_text += " when grd_rel = '22' then '조모'"
        select_text += " when grd_rel = '31' then '삼촌'"
        select_text += " when grd_rel = '32' then '고모'"
        select_text += " ELSE '' END AS grd_rel"
        select_text += ", grd_tel, prnt_nat_nm, tchr_nm, tchr_tel"
        select_text += " FROM service20_mp_mte"
        select_text += " WHERE mnte_id = '"+l_mnte_id+"'"

        queryset = mp_mtr.objects.raw(select_text)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)
#####################################################################################
# TE0201 - END
#####################################################################################


@csrf_exempt
def post_user_info(request):
    ida = request.POST.get('user_id', None)
    ms_ida = request.POST.get('ms_id', None)
    
    created_flag = vw_nanum_stdt.objects.filter(apl_id=ida).exists()
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
        rows = vw_nanum_stdt.objects.filter(apl_id=ida)[0]
        rows2 = mp_sub.objects.filter(mp_id=ms_ida)
        rows3 = msch.objects.filter(ms_id=ms_ida)[0]


        for val in rows2:
            key1 = val.att_id

        context = {'message': message,
                        'applyYn' : applyYn,
                        'apl_nm' : rows.apl_nm,
                        'unv_cd' : rows.unv_cd,
                        'unv_nm' : rows.unv_nm,
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
                        'stds_div' : rows.stds_div,
                        'stds_nm' : rows.stds_nm,
                        'mob_no' : rows.mob_no,
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

    apl_fr_dt = serializers.DateTimeField(format='%Y-%m-%d')
    apl_to_dt = serializers.DateTimeField(format='%Y-%m-%d')
    class Meta:
        model = mpgm
        fields = ('mp_id','mp_name','status','img_src','testField','apl_fr_dt','apl_to_dt','mp_intro')

    def get_testField(self, obj):
        return 'test'     


class mpmgListView(generics.ListAPIView):
    queryset = mpgm.objects.all()
    serializer_class = mpmgListSerializer

    def list(self, request):
        queryset = self.get_queryset()

        query = "select * from service20_mpgm order by apl_fr_dt desc, apl_to_dt desc"


        queryset = mpgm.objects.raw(query)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class main_list_mento_count_Serializer(serializers.ModelSerializer):

    cnt = serializers.SerializerMethodField()
    class Meta:
        model = mentor
        fields = ('mntr_id','cnt')

    def get_cnt(self, obj):
        return obj.cnt     


class main_list_mento_count(generics.ListAPIView):
    queryset = mentor.objects.all()
    serializer_class = main_list_mento_count_Serializer

    def list(self, request):
        queryset = self.get_queryset()

        v_count = mentor.objects.count()
        

        context = {'count': v_count,
                    }
    
        return JsonResponse(context,json_dumps_params={'ensure_ascii': True})

        # query = "select count(*) as cnt from service20_mentor"
        # queryset = mentor.objects.raw(query)

        # serializer_class = self.get_serializer_class()
        # serializer = serializer_class(queryset, many=True)

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        # return Response(serializer.data)        

#파일업로드 테스트
@csrf_exempt
def com_upload(request):

    req = request
    DIR = os.getcwd()
    UPLOAD_DIR = str(DIR) + '/media/mp_mtr/'
    UPLOAD_DIR = '/NANUM/www/img/mp_mtr/'
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
        fullFile = "/img/mp_mtr/"+ str(n_filename)
        insert_sql = "update service20_mp_mtr set  id_pic = '" + str(fullFile) + "' where mp_id = '"+ str(l_mp_id) + "' and apl_id = '" +  str(l_user_id) +"' "
        print(insert_sql)
        cursor.execute(insert_sql)

        return HttpResponse('File Uploaded')

    return HttpResponse('Failed to Upload File')


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
