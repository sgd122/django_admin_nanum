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


class article(models.Model):
	html = RichTextField()