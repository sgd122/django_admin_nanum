from django.urls import path
from service20.views import *
from service20.views2 import *
from . import views
from . import views2

app_name = 'service20'

urlpatterns = [
    
     #path('', views.stdApplyIns, name='stdApplyIns'),

     #멘토링 질문리스트 (미사용)
    # path('post_mt_quest/', post_mt_quest, name='post_mt_Quest'),   

    path('stdApplyStdView/', stdApplyStdView, name='detail'),
    path('Service20_01/', Service20_01_View, name='detail'),
    path('mpmgListView/', mpmgListView.as_view(), name='mpmgListView'),

    ########################################################################################
    # 공통(com)
    #
    ########################################################################################    
    #리턴URLTest
    path('login/login/', login_login, name='login_login'), 
    #리턴URLTest
    path('login/returnsso/', login_returnsso, name='login_returnsso'), 
    #리턴URLTest
    path('login/session/', login_session, name='login_session'), 
    # 년도 콤보박스
    path('com/combo/yr/', com_combo_yr.as_view(), name='com_combo_yr'),
    # 학기 콤보박스
    path('com/combo/termdiv/', com_combo_termdiv.as_view(), name='com_combo_termdiv'),
    # 모집상태 콤보박스
    path('com/combo/status/', com_combo_status.as_view(), name='com_combo_status'),
    # 취소사유 콤보박스
    path('com/combo/cnclRsn/', com_combo_cnclRsn.as_view(), name='com_combo_cnclRsn'),
    # 멘토의 학번으로 해당되는 멘티찾기
    path('com/list/my_mentee/', com_list_my_mentee.as_view(), name='com_list_my_mentee'),
    # 프로그램 찾기
    path('com/combo/program/', com_combo_program.as_view(), name='com_combo_program'),
    ########################################################################################
    # 공통(com)
    #
    ########################################################################################    

    ########################################################################################
    # MainPage
    #
    ########################################################################################
    # 현재 모집중인 멘토링 프로그램
    path('main/list/1/', mpmgListView.as_view(), name='mpmgListView'),
    # 현재 등록된 멘토건수
    path('main/list/mento_count/', main_list_mento_count.as_view(), name='main_list_mento_count'),
    ########################################################################################
    # MainPage
    #
    ########################################################################################
    

    ########################################################################################
    # 멘토스쿨
    #
    ########################################################################################
    # 멘토스쿨 리스트 조회
    path('MS0101M/list/', MS0101M_list.as_view(), name='MS0101M_list'),
    # 멘토스쿨 질문유형 가져오기
    path('MS0101M/quest/', MS0101M_quest.as_view(), name='MS0101M_quest'), 
    # 멘토스쿨 신청
    path('MS0101M/save/', MS0101M_save, name='MS0101M_save'), 
    # 성적,봉사,어학 가져오기
    path('MS0101M/detail/', MS0101M_detail, name='MS0101M_detail'),
    # 멘토링 프로그램 - 어학점수
    path('MS0101M/detail/fe/', MS0101M_detail_fe.as_view(), name='MS0101M_detail_fe'),
    # 멘토링 프로그램 - 봉사점수
    path('MS0101M/detail/sa/', MS0101M_detail_sa.as_view(), name='MS0101M_detail_sa'),
    # 멘토스쿨(관리자) - 기본정보
    path('MS0101M/admin/list/', MS0101M_adm_list.as_view(), name='MS0101M_adm_list'),
    # 멘토링 프로그램(관리자) - 어학점수
    path('MS0101M/admin/list/fe/', MS0101M_adm_list_fe.as_view(), name='MS0101M_adm_list_fe'),
    # 멘토링 프로그램(관리자) - 봉사점수
    path('MS0101M/admin/list/sa/', MS0101M_adm_list_sa.as_view(), name='MS0101M_adm_list_sa'),
    # 멘토스쿨(관리자) - 질문
    path('MS0101M/admin/quest/', MS0101M_adm_quest.as_view(), name='MS0101M_adm_quest'),
    # 멘토스쿨(관리자) 수락
    path('MS0101M/admin/acpt_save/', MS0101M_adm_acpt_save, name='MS0101M_adm_acpt_save'), 
    # 멘토스쿨(관리자) 수락취소
    path('MS0101M/admin/acpt_cancle/', MS0101M_adm_acpt_cancle, name='MS0101M_adm_acpt_cancle'), 
    # 멘토스쿨(관리자) update
    path('MS0101M/admin/update/', MS0101M_adm_update, name='MS0101M_adm_update'), 
    # 멘토스쿨(관리자) cancle
    path('MS0101M/admin/cancle/', MS0101M_adm_cancle, name='MS0101M_adm_cancle'), 
    # 멘토링 프로그램(레포트) - 기본정보
    path('MS0101M/report/list/', MS0101M_report_list.as_view(), name='MS0101M_report_list'),
    ########################################################################################
    # 멘토스쿨
    #
    ########################################################################################

    ########################################################################################
    # 멘토링 프로그램(MP0101M - START )
    #
    ########################################################################################
    # 멘토링 프로그램 리스트 조회
    path('MP0101M/list/', MP0101M_list.as_view(), name='MP0101M_list'),
    # 멘토링 프로그램 질문유형 가져오기
    path('MP0101M/quest/', MP0101M_quest.as_view(), name='MP0101M_quest'), 
    # 멘토링 프로그램 신청
    path('MP0101M/save/', MP0101M_save, name='MP0101M_save'), 
    # 성적,봉사,어학 가져오기
    path('MP0101M/detail/', MP0101M_detail, name='MP0101M_detail'),
    # 멘토링 프로그램(관리자) - 기본정보
    path('MP0101M/admin/list/', MP0101M_adm_list.as_view(), name='MP0101M_adm_list'),
    # 멘토링 프로그램(관리자) - 어학점수
    path('MP0101M/admin/list/fe/', MP0101M_adm_list_fe.as_view(), name='MP0101M_adm_list_fe'),
    # 멘토링 프로그램(관리자) - 봉사점수
    path('MP0101M/admin/list/sa/', MP0101M_adm_list_sa.as_view(), name='MP0101M_adm_list_sa'),
    # 멘토링 프로그램(관리자) - 질문
    path('MP0101M/admin/quest/', MP0101M_adm_quest.as_view(), name='MP0101M_adm_quest'),
    # 멘토링 프로그램(관리자) 수락
    path('MP0101M/admin/acpt_save/', MP0101M_adm_acpt_save, name='MP0101M_adm_acpt_save'), 
    # 멘토링 프로그램(관리자) 수락취소
    path('MP0101M/admin/acpt_cancle/', MP0101M_adm_acpt_cancle, name='MP0101M_adm_acpt_cancle'), 
    # 멘토링 프로그램(관리자) update
    path('MP0101M/admin/update/', MP0101M_adm_update, name='MP0101M_adm_update'), 
    # 멘토링 프로그램(관리자) cancle
    path('MP0101M/admin/cancle/', MP0101M_adm_cancle, name='MP0101M_adm_cancle'), 
    # 멘토링 프로그램(레포트) - 기본정보
    path('MP0101M/report/list/', MP0101M_report_list.as_view(), name='MP0101M_report_list'),
    ########################################################################################
    # 멘토링 프로그램(MP0101M - END )
    #
    ########################################################################################
    
    ########################################################################################
    # 학습외신청(멘토) 리스트(MP0102M - START )
    #
    ########################################################################################
    # 학습외신청(멘토) 리스트
    path('MP0102M/mento/list/', MP0102M_list.as_view(), name='MP0102M_list'),   
    path('MP0102M/mento/list_detail/', MP0102M_list.as_view(), name='MP0102M_list'),   
    ########################################################################################
    # 학습외신청(멘토) 리스트(MP0102M - END )
    #
    ########################################################################################

    ########################################################################################
    # 프로그램 수행계획서(MP0103M - START )
    #
    ########################################################################################
    # 프로그램 수행계획서 콤보
    path('MP0103M/v1/', MP0103M_v1.as_view(), name='MP0103M_v1'),
    # 프로그램 수행계획서 리스트
    path('MP0103M/list/', MP0103M_list.as_view(), name='MP0103M_list'),
    # 프로그램 수행계획서 상세
    path('MP0103M/detail/', MP0103M_Detail.as_view(), name='MP0103M_Detail'),
    # 프로그램 수행계획서 작성 폼 데이터
    path('MP0103M/detail/v2/', MP0103M_Detail_v2.as_view(), name='MP0103M_Detail_v2'),
    # 프로그램 수행계획서 -> 최초 작성 시 주차 수를 셋팅
    path('MP0103M/list/v1/', MP0103M_list_v1.as_view(), name='MP0103M_list_v1'),
    # 프로그램 수행계획서 Insert
    path('MP0103M/insert/', MP0103M_Insert, name='MP0103M_Insert'),
    # 프로그램 수행계획서 Update
    path('MP0103M/update/', MP0103M_Update, name='MP0103M_Update'),
    ########################################################################################
    # 프로그램 수행계획서(MP0103M - END )
    #
    ########################################################################################

    ########################################################################################
    # 출석관리 리스트(MP0104M - START )
    #
    ########################################################################################
    # 출석관리 리스트
    path('MP0104M/list/', MP0104M_list.as_view(), name='MP0104M_list'),
    # 출석관리 상세
    path('MP0104M/detail/', MP0104M_Detail.as_view(), name='MP0104M_Detail'),
    ########################################################################################
    # 출석관리 리스트(MP0104M - END )
    #
    ########################################################################################
    
    ########################################################################################
    # 보고서 현황(MP0105M - START )
    #
    ########################################################################################
    # 보고서 현황 리스트
    path('MP0105M/list/', MP0105M_list.as_view(), name='MP0105M_list'),   
    # 보고서 현황 상세
    path('MP0105M/detail/', MP0105M_detail.as_view(), name='MP0105M_detail'),   
    # 보고서 현황 상세
    path('MP0105M/detail/2/', MP0105M_detail_2.as_view(), name='MP0105M_detail_2'),   
    # 보고서 현황 콤보1
    path('MP0105M/combo/1/', MP0105M_combo_1.as_view(), name='MP0105M_combo_1'),   
    # 보고서 현황 save
    path('MP0105M/update/<int:pk>/', MP0105M_update, name='MP0105M_update'),
    ########################################################################################
    # 보고서 현황(MP0105M - END )
    #
    ########################################################################################

    ########################################################################################
    # 월별 활동비 (MP0106M - START )
    #
    ########################################################################################
    # 월별 활동비 리스트
    path('MP0106M/list/', MP0106M_list.as_view(), name='MP0106M_list'),   
    ########################################################################################
    # 월별 활동비 (MP0106M - END )
    #
    ########################################################################################


################################################################################################################################################################################
# 멘티
# 
################################################################################################################################################################################    


    ########################################################################################
    # 멘티의 프로그램 신청현황(TE0201 - START )
    #
    ########################################################################################
    # # 멘티의 프로그램 신청현황 리스트
    path('TE0201/list/', TE0201_list.as_view(), name='TE0201_list'),   
    # # 멘티의 프로그램 신청현황 상세
    path('TE0201/detail/', TE0201_detail.as_view(), name='TE0201_detail'),   
    ########################################################################################
    # 멘티의 프로그램 신청현황(TE0201 - END )
    #
    ########################################################################################


################################################################################################################################################################################
# 멘티
# 
################################################################################################################################################################################    

    
    
   ########################################################################################
    # view2 부분 (시작)
    #
    ########################################################################################
    #멘토스쿨 콤보박스
    path('msComboListView/', msComboListView.as_view(), name='msComboListView'),
    #멘토스쿨 콤보박스 Detail
    path('msComboListViewDetail/', msComboListViewDetail.as_view(), name='comboMpmgListViewDetail'),
       #환산
    path('msFn1/', msFn1, name='msFn1'),
    #사정
    path('msFn2/', msFn2, name='msFn2'),
    #엑셀
    path('msFn3/', msFn3, name='msFn3'),    
    #면접
    path('msFn4/', msFn4, name='msFn4'),
    #합격자업로드
    path('msFn6/', msFn6, name='msFn6'),
    #합격자업로드_전송
    path('msFn6_Submit/', msFn6_Submit, name='msFn6_Submit'),
    #합격자업로드_전송
    path('msFn6_Submit2/', msFn6_Submit2, name='msFn6_Submit2'),

    #합격자업로드
    path('msFn7/', msFn7, name='msFn7'),
    #최종합격자업로드_전송
    path('msFn7_Submit/', msFn7_Submit, name='msFn7_Submit'),
    #최종합격자업로드_전송
    path('msFn7_Submit2/', msFn7_Submit2, name='msFn7_Submit2'),

    #멘토스쿨 팝업1
    path('msPop1/', msPop1, name='msPop1'),    
    #멘토스쿨 핍압1_조회1
    path('msPop1_Det1/', msPop1_Det1.as_view(), name='msPop1_Det1'), 
    #멘토스쿨 핍압1_조회2
    path('msPop1_Det2/', mpPop1_Det2, name='msPop1_Det2'), 

    #멘토스쿨 핍압1_조회3_채점자 교수 조회
    path('msPop1_Det3/', msPop1_Det3.as_view(), name='msPop1_Det3'), 
    #멘토스쿨 핍압1_조회4_채점문항 
    path('msPop1_Det4/', msPop1_Det4.as_view(), name='msPop1_Det4'), 
    #멘토스쿨 핍압1_조회5_답변
    path('msPop1_Det5/', msPop1_Det5.as_view(), name='msPop1_Det5'), 
    #멘토스쿨 핍압1_조회5_답변_저장
    path('msPop1_Det5_Save/', msPop1_Det5_Save, name='msPop1_Det5_Save'), 

    #멘토스쿨 환산표
    #path('msFn1/', msFn1, name='msFn1'),

    #멘토링 콤보박스
    path('mpComboListView/', mpComboListView.as_view(), name='mpComboListView'),
    #멘토링 콤보박스 Detail
    path('mpComboListViewDetail/', mpComboListViewDetail.as_view(), name='mpComboListViewDetail'),
    #환산
    path('mpFn1/', mpFn1, name='mpFn1'),
    #사정
    path('mpFn2/', mpFn2, name='mpFn2'),
    #엑셀
    path('mpFn3/', mpFn3, name='mpFn3'),    
    #면접
    path('mpFn4/', mpFn4, name='mpFn4'),
    #합격자업로드
    path('mpFn6/', mpFn6, name='mpFn6'), 
    #합격자업로드_전송
    path('mpFn6_Submit/', mpFn6_Submit, name='mpFn6_Submit'),
    #합격자업로드_전송
    path('mpFn6_Submit2/', mpFn6_Submit2, name='mpFn6_Submit2'),

    #합격자업로드
    path('mpFn7/', mpFn7, name='mpFn7'),
    #최종합격자업로드_전송
    #path('msFn7_Submit/', msFn7_Submit, name='msFn7_Submit'),
    #최종합격자업로드_전송
    #path('msFn7_Submit2/', msFn7_Submit2, name='msFn7_Submit2'),

    #멘토링 팝업1
    path('mpPop1/', mpPop1, name='mpPop1'),    
    #멘토랑핍압1_조회1
    path('mpPop1_Det1/', mpPop1_Det1.as_view(), name='mpPop1_Det1'), 
    #멘토랑핍압1_조회2   
    path('mpPop1_Det2/', mpPop1_Det2, name='mpPop1_Det2'), 
    #멘토랑 핍압1_조회3_채점자 교수 조회
    path('mpPop1_Det3/', mpPop1_Det3.as_view(), name='mpPop1_Det3'), 
    #멘토랑 핍압1_조회4_채점문항 
    path('mpPop1_Det4/', mpPop1_Det4.as_view(), name='mpPop1_Det4'), 
    #멘토랑 핍압1_조회5_답변
    path('mpPop1_Det5/', mpPop1_Det5.as_view(), name='mpPop1_Det5'), 
    #멘토랑 핍압1_조회5_답변_저장 
    path('mpPop1_Det5_Save/', mpPop1_Det5_Save, name='mpPop1_Det5_Save'), 
 

    #SMS 팝업
    path('sms/', sms, name='sms'), 
    path('sms_result/', sms_result, name='sms_result'), 


    #리턴URLTest
    path('returnsso/', returnsso, name='returnsso'), 



    #개인정보리턴
    path('agree_cont1/', agree_cont1.as_view(), name='agree_cont1'), 
    ########################################################################################
    # view2 부분 (종료)
    #
    ########################################################################################
]