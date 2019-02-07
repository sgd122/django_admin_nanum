import uuid

import datetime
from django.contrib.auth.models import AbstractUser

from django.db import models

from ckeditor.fields import RichTextField

# Create your models here.

class com_cdh(models.Model):
	std_grp_code = models.CharField(max_length=6, null=False, verbose_name='그룹코드' )
	lang_key = models.CharField(max_length=2, null=False, verbose_name='언어' )
	std_grp_code_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='그룹코드명' )
	rmrk = models.CharField(max_length=255, null=True, blank=True, verbose_name='비고' )
	use_indc = models.CharField(max_length=1, default= 'Y', verbose_name='사용여부' )
	cls_date = models.CharField(max_length=8, default= '99991231', verbose_name='사용 종료일' )
	sys_id = models.CharField(max_length=12, null=True, blank=True, verbose_name='시스템ID' )
	grp_type = models.CharField(max_length=2, null=True, blank=True, verbose_name='그룹유형 - 시스템,사용자 → 수정가능' )
	ins_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='입력자ID' )
	ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
	ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
	ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
	upd_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='수정자ID' )
	upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
	upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
	upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

	class Meta:
		verbose_name = 'Common Code Master Head'
		verbose_name_plural =  verbose_name
		unique_together=("std_grp_code", "lang_key")	



class com_cdd(models.Model):
	std_grp_code = models.CharField(max_length=6, null=False, verbose_name='그룹코드' )
	#std_grp_code = models.ForeignKey(to='com_cdh',to_field='std_grp_code', on_delete=models.SET_NULL,null=True,blank=True,verbose_name='그룹코드')
	std_detl_code = models.CharField(max_length=10, null=False, verbose_name='공통코드' )
	lang_key = models.CharField(max_length=2, null=False, verbose_name='언어' )
	std_detl_code_nm = models.CharField(max_length=60, null=False, verbose_name='공통코드명' )
	rmrk = models.CharField(max_length=255, null=True, blank=True, verbose_name='비고' )
	rmrk_2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='비고2' )
	up_std_detl_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='상위공통코드' )
	use_indc = models.CharField(max_length=1, default= 'N', verbose_name='사용여부' )
	cls_date = models.CharField(max_length=8, default= '00000000', verbose_name='종료일' )
	sort_seq_no = models.CharField(max_length=10, default= '0000000000', verbose_name='순서' )
	co_code = models.CharField(max_length=4, null=True, blank=True, verbose_name='예비 코드' )
	plnt = models.CharField(max_length=4, null=True, blank=True, verbose_name='공장' )
	sys_id = models.CharField(max_length=12, null=True, blank=True, verbose_name='시스템ID' )
	text1 = models.CharField(max_length=255, null=True, blank=True, verbose_name='예비 텍스트1' )
	text2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='예비 텍스트2' )
	text3 = models.CharField(max_length=255, null=True, blank=True, verbose_name='예비 텍스트3' )
	text4 = models.CharField(max_length=255, null=True, blank=True, verbose_name='예비 텍스트4' )
	text5 = models.CharField(max_length=255, null=True, blank=True, verbose_name='예비 텍스트5' )
	ins_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='입력자ID' )
	ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
	ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
	ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
	upd_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='수정자ID' )
	upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
	upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
	upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

	class Meta:
		verbose_name = 'Common Code Master Detail'
		verbose_name_plural =  verbose_name
		unique_together=("std_grp_code", "std_detl_code", "lang_key")
		index_together = ["std_detl_code_nm", "std_detl_code"]

class vm_nanum_stdt(models.Model):
	apl_id = models.CharField(max_length=10, null=False, verbose_name='학번')
	apl_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='성명' )
	apl_nm_e = models.CharField(max_length=150, null=True, blank=True, verbose_name='성명_영문' )
	univ_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='대학교코드' )
	univ_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='대학교명' )
	grad_div_cd = models.CharField(max_length=10, null=True, blank=True, verbose_name='대학원구분코드' )
	grad_div_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='대학원구분명' )
	cllg_cd = models.CharField(max_length=255, null=True, blank=True, verbose_name='대학코드' )
	cllg_nm = models.CharField(max_length=255, null=True, blank=True, verbose_name='대학명' )
	dept_cd = models.CharField(max_length=255, null=True, blank=True, verbose_name='학과코드' )
	dept_nm = models.CharField(max_length=255, null=True, blank=True, verbose_name='학과명' )
	mjr_cd = models.CharField(max_length=255, null=True, blank=True, verbose_name='전공코드' )
	mjr_nm = models.CharField(max_length=255, null=True, blank=True, verbose_name='전공명' )
	brth_dt = models.CharField(max_length=255, null=True, blank=True, verbose_name='생년월일' )
	gen_cd = models.CharField(max_length=255, null=True, blank=True, verbose_name='성별코드' )
	gen_nm = models.CharField(max_length=255, null=True, blank=True, verbose_name='성별명' )
	yr = models.CharField(max_length=255, null=True, blank=True, verbose_name='학년도' )
	sch_yr = models.CharField(max_length=255, null=True, blank=True, verbose_name='학년' )
	term_div = models.CharField(max_length=255, null=True, blank=True, verbose_name='학기코드' )
	term_nm = models.CharField(max_length=255, null=True, blank=True, verbose_name='학기명' )
	stdt_div = models.CharField(max_length=255, null=True, blank=True, verbose_name='학적상태코드' )
	stdt_nm = models.CharField(max_length=255, null=True, blank=True, verbose_name='학적상태명' )
	mob_nm = models.CharField(max_length=255, null=True, blank=True, verbose_name='휴대전화번호' )
	tel_no = models.CharField(max_length=255, null=True, blank=True, verbose_name='집전화' )
	tel_no_g = models.CharField(max_length=255, null=True, blank=True, verbose_name='보호자연락처' )
	h_addr = models.CharField(max_length=255, null=True, blank=True, verbose_name='집주소' )
	post_no = models.CharField(max_length=255, null=True, blank=True, verbose_name='우편번호' )
	email_addr = models.CharField(max_length=255, null=True, blank=True, verbose_name='이메일주소' )
	bank_acct = models.CharField(max_length=255, null=True, blank=True, verbose_name='은행계좌번호' )
	bank_cd = models.CharField(max_length=255, null=True, blank=True, verbose_name='은행코드' )
	bank_nm = models.CharField(max_length=255, null=True, blank=True, verbose_name='은행명' )
	bank_dpsr = models.CharField(max_length=255, null=True, blank=True, verbose_name='예금주' )
	pr_yr = models.CharField(max_length=255, null=True, blank=True, verbose_name='직전 학년도' )
	pr_sch_yr = models.CharField(max_length=255, null=True, blank=True, verbose_name='직전 학년' )
	pr_term_div = models.CharField(max_length=255, null=True, blank=True, verbose_name='직전학기코드' )
	score01 = models.CharField(max_length=255, null=True, blank=True, verbose_name='직전학기 석차' )
	score02 = models.CharField(max_length=255, null=True, blank=True, verbose_name='직전학기 총원' )
	score03 = models.CharField(max_length=255, null=True, blank=True, verbose_name='봉사점수합계' )
	score04 = models.CharField(max_length=255, null=True, blank=True, verbose_name='외국어점수(추후협의)' )
	score04_tp = models.CharField(max_length=255, null=True, blank=True, verbose_name='외국어구분(추후협의)' )
	score05 = models.CharField(max_length=255, null=True, blank=True, verbose_name='자격증 개수' )
	if_dt = models.DateTimeField(null=True, blank=True, verbose_name='조회일시' )




class article(models.Model):
	html = RichTextField()