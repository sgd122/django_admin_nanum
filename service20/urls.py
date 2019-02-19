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
    # 멘토스쿨
    #
    ########################################################################################
    #멘토스쿨 리스트
    # path('', MS0101M_list.as_view(), name='MS0101M_list'),
    path('MS0101M/list/', MS0101M_list.as_view(), name='MS0101M_list'),
    # 멘토스쿨 기본정보
    path('MS0101M/detail/', MS0101M_detail, name='MS0101M_detail'),
    # 멘토스쿨 질문유형
    path('MS0101M/quest/', MS0101M_quest.as_view(), name='MS0101M_quest'),
    # 멘토스쿨 신청
    path('MS0101M/save/', MS0101M_save, name='MS0101M_save'),
    # 멘토스쿨(관리자) - 기본정보
    path('MS0101M/admin/list/', MS0101M_adm_list.as_view(), name='MS0101M_adm_list'),
    # 멘토스쿨(관리자) - 질문
    path('MS0101M/admin/quest/', MS0101M_adm_quest.as_view(), name='MS0101M_adm_quest'),
    ########################################################################################
    # 멘토스쿨
    #
    ########################################################################################

    ########################################################################################
    # 멘토링 프로그램
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
    # 멘토링 프로그램(관리자) - 기보정보
    path('MP0101M/admin/list/', MP0101M_adm_list.as_view(), name='MP0101M_adm_list'),
    # 멘토링 프로그램(관리자) - 질문
    path('MP0101M/admin/quest/', MP0101M_adm_quest.as_view(), name='MP0101M_adm_quest'),
    ########################################################################################
    # 멘토링 프로그램(MP0101M - END )
    #
    ########################################################################################
    
    ########################################################################################
    # 프로그램 수행계획서
    #
    ########################################################################################
    # 프로그램 수행계획서 리스트
    path('MP0103M/list/', MP0103M_list.as_view(), name='MP0103M_list'),
    # 프로그램 수행계획서 상세
    path('MP0103M/detail/', MP0103M_Detail.as_view(), name='MP0103M_Detail'),
    # 프로그램 수행계획서 Insert
    path('MP0103M/insert/', MP0103M_Insert, name='MP0103M_Insert'),
    # 프로그램 수행계획서 Update
    path('MP0103M/update/', MP0103M_Update.as_view(), name='MP0103M_Update'),
    ########################################################################################
    # 프로그램 수행계획서
    #
    ########################################################################################

    ########################################################################################
    # 학습외신청(멘토) 리스트
    #
    ########################################################################################
    # 학습외신청(멘토) 리스트
    path('MP0102M/list/', MP0102M_list.as_view(), name='MP0102M_list'),   
    ########################################################################################
    # 학습외신청(멘토) 리스트
    #
    ########################################################################################
    
    

    





    
    
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
    #멘토스쿨 팝업1
    path('msPop1/', msPop1, name='msPop1'),    
    #멘토스쿨 핍압1_조회1
    path('msPop1_Det1/', msPop1_Det1.as_view(), name='msPop1_Det1'), 
    #멘토스쿨 핍압1_조회2
    path('msPop1_Det2/', mpPop1_Det2, name='msPop1_Det2'), 

    #멘토스쿨 핍압1_조회3_채점자 교수 조회
    path('msPop1_Det3/', msPop1_Det3.as_view(), name='msPop1_Det3'), 



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

    #멘토링 팝업1
    path('mpPop1/', mpPop1, name='mpPop1'),    
    #멘토랑핍압1_조회1
    path('mpPop1_Det1/', mpPop1_Det1.as_view(), name='mpPop1_Det1'), 
    #멘토랑핍압1_조회2   
    path('mpPop1_Det2/', mpPop1_Det2, name='mpPop1_Det2'), 
    ########################################################################################
    # view2 부분 (종료)
    #
    ########################################################################################
]