from django.urls import path
from service20.views import *
from service20.views2 import *
from . import views
from . import views2

app_name = 'service20'

urlpatterns = [
    
     #path('', views.stdApplyIns, name='stdApplyIns'),
    path('stdApplyStdView/', stdApplyStdView, name='detail'),
    path('Service20_01/', Service20_01_View, name='detail'),


    path('mpmgListView/', mpmgListView.as_view(), name='mpmgListView'),
    path('mpmgListPersionView/', mpmgListPersionView.as_view(), name='mpmgListPersionView'),

    ########################################################################################
    # 멘토스쿨
    #
    ########################################################################################
    #멘토스쿨 리스트
    path('', Service20ListView.as_view(), name='Service20ListView'),
    # 성적,봉사,어학 가져오기
    path('authUserPersionInfo/', post_user_info_persion, name='post_user_info_persion'),
    # 멘토스쿨 기본정보
    path('authUserInfo/', post_user_info, name='post_user_info'),
    # 멘토스쿨 질문유형
    path('authUserInfoQuest/', post_user_info_Quest.as_view(), name='post_user_info_Quest'),
    # 멘토스쿨 신청
    path('msApply/', post_msApply, name='post_msApply'),

    # 멘토스쿨(관리자) - 질문
    path('authUserInfoViewQuest/', post_user_info_view_Quest.as_view(), name='post_user_info_view_Quest'),
    ########################################################################################
    # 멘토스쿨
    #
    ########################################################################################

    ########################################################################################
    # 멘토링 프로그램
    #
    ########################################################################################
    #멘토링 질문리스트
    path('post_mt_quest/', post_mt_quest, name='post_mt_Quest'),
    # 멘토링 프로그램 질문유형 가져오기
    path('authUserInfoPersionQuest/', post_user_info_persion_Quest.as_view(), name='post_user_info_persion_Quest'), 
    # 멘토링 프로그램 신청
    path('msProgramApply/', post_msProgramApply, name='post_msProgramApply'),    
    ########################################################################################
    # 멘토링 프로그램
    #
    ########################################################################################
    
    
    #멘토스쿨 콤보박스
    path('comboMpmgListView/', comboMpmgListView.as_view(), name='comboMpmgListView'),
    #멘토스쿨 콤보박스 Detail
    path('comboMpmgListViewDetail/', comboMpmgListViewDetail.as_view(), name='comboMpmgListViewDetail'),
    #멘토스쿨 환산표
    path('msFn1/', msFn1, name='msFn1'),

    

    # 프로그램 수행계획서 리스트
    path('mpPlnh_mpgmListView/', mpPlnh_mpgmListView.as_view(), name='mpPlnh_mpgmListView'),
    # 학습외신청(멘토) 리스트
    path('mpSpc_ListView/', mpSpc_ListView.as_view(), name='mpSpc_ListView'),   
]