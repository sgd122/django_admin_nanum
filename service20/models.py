import uuid

import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from member.models import Member


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

	def __str__(self):
		return self.std_grp_code_nm		


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

	def __str__(self):
		return self.std_detl_code_nm		


class msch(models.Model):
	ms_id = models.CharField(max_length=10, primary_key=True, verbose_name='멘토스쿨ID' )
	#ms_id = models.ForeignKey(Member, verbose_name='멘토스쿨ID',on_delete=models.SET_NULL,null=True,blank=True)
	status = models.CharField(max_length=2, null=True, blank=True, verbose_name='상태' )
	ms_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='멘토스쿨 명' )
	img_src = models.CharField(max_length=100, null=True, blank=True, verbose_name='이미지경로' )	
	ms_sname = models.CharField(max_length=20, null=True, blank=True, verbose_name='멘토스쿨 단명' )
	ms_intro = models.CharField(max_length=1000, null=True, blank=True, verbose_name='멘토스쿨 소개' )
	mng_area = models.CharField(max_length=2, null=True, blank=True, verbose_name='멘토스쿨 관리 영역' )
	mgr_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='멘토스쿨 관리자 ID' )
	mgr_nm = models.CharField(max_length=20, null=True, blank=True, verbose_name='멘토스쿨 관리자 명' )
	mng_org = models.CharField(max_length=10, null=True, blank=True, verbose_name='관리기관' )
	sup_org = models.CharField(max_length=10, null=True, blank=True, verbose_name='주관기관' )
	yr = models.CharField(max_length=4, null=True, blank=True, verbose_name='연도' )
	yr_seq = models.PositiveIntegerField(null=True, blank=True, verbose_name='차수' )
	apl_ntc_fr_dt = models.DateTimeField(null=True, blank=True, verbose_name='공지시작일' )
	apl_ntc_to_dt = models.DateTimeField(null=True, blank=True, verbose_name='공지종료일' )	

	#apl_term = models.CharField(max_length=2, null=True, blank=True, verbose_name='모집시기(MS0022)' )


	apl_term = models.ForeignKey(
		to='com_cdd',
		on_delete=models.CASCADE,
		null=True, 
		blank=True, 
		verbose_name='모집시기(MS0022)' ,
		limit_choices_to={'std_grp_code' : 'MS0022'}
		#limit_choices_to=Q('std_grp_code'='MS0022')
	)



	apl_fr_dt = models.DateTimeField(null=True, blank=True, verbose_name='모집기간-시작' )
	apl_to_dt = models.DateTimeField(null=True, blank=True, verbose_name='모집기간-종료' )
	trn_term = models.CharField(max_length=2, null=True, blank=True, verbose_name='교육시기(MS0022)' )
	trn_fr_dt = models.DateTimeField(null=True, blank=True, verbose_name='교육기간-시작' )
	trn_to_dt = models.DateTimeField(null=True, blank=True, verbose_name='교육기간-종료' )


	tot_apl = models.PositiveIntegerField(default=0, verbose_name='모집인원(정원)-합격' )
	cnt_apl = models.PositiveIntegerField(default=0, verbose_name='지원인원' )
	cnt_doc_suc = models.PositiveIntegerField(default=0, verbose_name='서류전형 합격인원' )
	cnt_doc_res = models.PositiveIntegerField(default=0, verbose_name='서류전형 예비인원(실제 없음)' )


	cnt_intv_pl = models.PositiveIntegerField(default=0, verbose_name='면접전형 참여 계획 인원' )
	cnt_intv_ac = models.PositiveIntegerField(default=0, verbose_name='면접전형 참여 인원' )
	intv_dt = models.CharField(max_length=8, null=True, blank=True, verbose_name='면접일' )
	cnt_intv_suc = models.PositiveIntegerField(default=0, verbose_name='면접전형 합격인원' )
	cnt_iintv_res = models.PositiveIntegerField(default=0, verbose_name='면접전형 예비합격인원' )


	cnt_trn = models.PositiveIntegerField(default=0, verbose_name='교육인원' )
	cnt_mtr = models.PositiveIntegerField(default=0, verbose_name='최종합격 멘토인원' )

	doc_dt = models.DateTimeField(null=True, blank=True, verbose_name='서류전형일' )
	doc_mgr = models.CharField(max_length=10, null=True, blank=True, verbose_name='서류전형 수행자' )

	intv_dt = models.DateTimeField(null=True, blank=True, verbose_name='면접전형-입력-일' )
	intv_mgr = models.CharField(max_length=10, null=True, blank=True, verbose_name='면접전형-입력-자' )

	fin_dt = models.DateTimeField(null=True, blank=True, verbose_name='최종합격-입력-일' )
	fin_mgr = models.CharField(max_length=10, null=True, blank=True, verbose_name='최종합격-입력-자' )
	ins_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='입력자ID' )
	ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
	ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
	ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
	upd_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='수정자ID' )
	upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
	upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
	upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

	def __str__(self):
		return self.ms_name

class Meta:
	verbose_name = '개설멘토스쿨'
	verbose_name_plural =  verbose_name


class ms_sub(models.Model):
	#ms_id = models.CharField(max_length=10, null=False, verbose_name='멘토스쿨ID' )

	ms_id = models.ForeignKey(
		to='msch',
		on_delete=models.CASCADE,
		null=True, 
		blank=True, 
		verbose_name='멘토스쿨ID' ,
		#limit_choices_to={'std_grp_code' : 'MS0022'}
	)

	#att_id = models.CharField(max_length=10, null=False, verbose_name='속성ID' )

	att_id = models.ForeignKey(
		to='com_cdh',
		on_delete=models.CASCADE,
		null=True, 
		blank=True, 
		verbose_name='속성ID' ,
		#limit_choices_to=f_std_grp_code,
		#limit_choices_to = Q(std_grp_code='MS0010') | Q(std_grp_code='MS0011')
		#choices=(('MS0010', '지원학년'), ('MS0011', '지원학기'), ('MS0012', '지원성별')),
		#limit_choices_to={'std_grp_code' : 'MS0010'}
		#limit_choices_to={'std_grp_code' : 'MS0022'}
	)

	#att_seq = models.PositiveIntegerField(max_length=1, null=True, blank=True,verbose_name='속성 SEQ → PK 자동생성 시 필요없음' )

	att_cdh = models.CharField(max_length=6, null=True, blank=True, verbose_name='속성 CODE HEADER' )

	att_cdd = models.ForeignKey(
		to='com_cdd',
		on_delete=models.CASCADE,
		null=True, 
		blank=True, 
		verbose_name='속성 CODE' ,
		#limit_choices_to=f_std_grp_code,
		#limit_choices_to = Q(std_grp_code='MS0010') | Q(std_grp_code='MS0011')
		#choices=(('MS0010', '지원학년'), ('MS0011', '지원학기'), ('MS0012', '지원성별')),
		#limit_choices_to={'std_grp_code' : 'MS0010'}
		#limit_choices_to={'std_grp_code' : 'MS0022'}
	)
	#att_cdd = models.CharField(max_length=10, null=True, blank=True, verbose_name='속성 CODE' )


	att_val = models.CharField(max_length=60, null=True, blank=True, verbose_name='속성 값' )


	att_unit = models.CharField(max_length=10, null=True, blank=True, verbose_name='속성 단위' )
	use_yn = models.CharField(max_length=1, null=True, blank=True, verbose_name='사용여부' )
	sort_seq = models.PositiveIntegerField(default=1, verbose_name='정렬' )
	ins_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='입력자ID' )
	ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
	ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
	ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
	upd_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='수정자ID' )
	upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
	upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
	upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

	class Meta: 
		verbose_name = '개설멘토스쿨 속성(질문지, 채점항목,채점자)'
		verbose_name_plural =  verbose_name
		unique_together=("ms_id", "att_id","att_cdd")





class ms_apl(models.Model):
	#ms_id = models.CharField(max_length=10, null=False, verbose_name='멘토스쿨ID' )
	ms_id = models.ForeignKey(msch, verbose_name='멘토스쿨ID',on_delete=models.SET_NULL,null=True,blank=True)
	apl_no = models.IntegerField(null=False, verbose_name='지원 NO' )
	apl_id = models.CharField(max_length=10, null=False, verbose_name='지원자ID(학번)' )
	#apl_id = models.ForeignKey(Member, verbose_name='지원자ID(학번)',on_delete=models.SET_NULL,null=True,blank=True)
	apl_nm = models.CharField(max_length=20, null=False, verbose_name='지원자 명' )
	apl_nm_e = models.CharField(max_length=20, null=True, blank=False, verbose_name='멘토 영문명' )
	unv_cd = models.CharField(max_length=10, null=False, verbose_name='지원자 대학교 코드' )
	unv_nm = models.CharField(max_length=10, null=False, verbose_name='지원자 대학교 명' )
	cllg_cd = models.CharField(max_length=10, null=False, verbose_name='지원자 대학 코드' )
	cllg_nm = models.CharField(max_length=10, null=False, verbose_name='지원자 대학 명' )
	dept_cd = models.CharField(max_length=10, null=False, verbose_name='지원자 학부/학과 코드' )
	dept_nm = models.CharField(max_length=10, null=False, verbose_name='지원자 학부/학과 명' )
	brth_dt = models.CharField(max_length=8, null=False, verbose_name='생년월일' )
	gen = models.CharField(max_length=1, choices=(('M', '남자'), ('W', '여자')), null=False, verbose_name='성별' )
	yr = models.CharField(max_length=4, null=False, verbose_name='학년도' )
	term_div = models.CharField(max_length=2, null=False, verbose_name='학기' )
	sch_yr = models.CharField(max_length=1, null=False, verbose_name='학년' )
	mob_no = models.CharField(max_length=22, null=False, verbose_name='휴대전화' )
	tel_no = models.CharField(max_length=22, null=True, blank=True, verbose_name='집전화' )
	tel_no_g = models.CharField(max_length=22, null=True, blank=True, verbose_name='보호자 연락처' )
	h_addr = models.CharField(max_length=200, null=False, verbose_name='집주소' )
	post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
	email_addr = models.CharField(max_length=50, null=True, blank=True, verbose_name='이메일 주소' )
	apl_dt = models.DateTimeField(null=True, blank=True, verbose_name='접수일(지원서 저장)' )
	status = models.CharField(max_length=1, null=True, blank=True, verbose_name='상태(지원,취소,…)' )
	doc_cncl_dt = models.DateTimeField(null=True, blank=True, verbose_name='지원취소일' )
	doc_cncl_rsn = models.CharField(max_length=2, null=True, blank=True, verbose_name='서류전형취소사유' )
	tot_doc = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='서류전형  총 점수' )
	score1 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='원점수1(성적,봉사,외국어,지원서)' )
	score2 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='원점수2' )
	score3 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='원점수3' )
	score4 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='원점수4' )
	score5 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='원점수5' )
	score6 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='원점수6' )
	cscore1 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수1' )
	cscore2 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수2' )
	cscore3 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수3' )
	cscore4 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수4' )
	cscore5 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수5' )
	cscore6 = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='변환점수6' )
	doc_rank = models.PositiveIntegerField(null=True, blank=True, verbose_name='서류심사등수' )
	doc_rslt = models.CharField(max_length=1, null=True, blank=True, verbose_name='서류심사결과' )
	intv_team = models.PositiveIntegerField(null=True, blank=True, verbose_name='면접팀' )
	intv_dt = models.DateTimeField(null=True, blank=True, verbose_name='면접일' )
	intv_part_pl = models.CharField(max_length=1, null=True, blank=True, verbose_name='면접참여계획' )
	intv_np_rsn_pl = models.CharField(max_length=2, null=True, blank=True, verbose_name='면접불참사유' )
	intv_part_pl_dt = models.DateTimeField(null=True, blank=True, verbose_name='면접참여계획 입력일' )
	intv_part_ac = models.CharField(max_length=1, null=True, blank=True, verbose_name='면접참여여부' )
	intv_np_rsn_ac = models.CharField(max_length=2, null=True, blank=True, verbose_name='면접불참사유' )
	intv_part_ac_dt = models.DateTimeField(null=True, blank=True, verbose_name='면접참여 입력일' )
	intv_tot = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, verbose_name='면접점수' )
	intv_rslt = models.CharField(max_length=1, null=True, blank=True, verbose_name='면접심사결과' )
	ms_trn_yn = models.CharField(max_length=1, null=True, blank=True, verbose_name='멘토스쿨 이수여부' )
	fnl_rslt = models.CharField(max_length=1, null=True, blank=True, verbose_name='최종합격 여부' )
	mntr_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='멘토ID' )
	mntr_dt = models.DateField(null=True, blank=True, verbose_name='멘토 자격 부여일' )
	sms_send_no = models.CharField(max_length=20, null=True, blank=True, verbose_name='문자발송번호' )
	ins_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='입력자ID' )
	ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
	ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
	ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
	upd_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='수정자ID' )
	upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
	upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
	upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

	def __str__(self):
		return self.apl_nm

	class Meta:
		verbose_name = '멘토스쿨 지원자'
		verbose_name_plural =  verbose_name
		unique_together=("ms_id", "apl_no")
		index_together = ["apl_id"]
		index_together = ["apl_nm"]


class ms_ans(models.Model):
	ms_id = models.CharField(max_length=10, null=False, verbose_name='멘토스쿨ID' )
	test_div = models.CharField(max_length=10, null=False, verbose_name='전형구분(서류/면접)' )
	apl_no = models.CharField(max_length=10, null=False, verbose_name='지원 NO' )
	ques_no = models.PositiveIntegerField(null=False, verbose_name='질문 번호' )
	apl_id = models.CharField(max_length=10, null=False, verbose_name='지원자ID(학번)' )
	apl_nm = models.CharField(max_length=20, null=False, verbose_name='지원자 명' )
	sort_seq = models.PositiveIntegerField(null=False, verbose_name='정렬' )
	ans_t1 = models.PositiveIntegerField(null=True, blank=True, verbose_name='선다형 답' )
	ans_t2 = models.CharField(max_length=1000, null=True, blank=True, verbose_name='수필형 답' )
	ans_t3 = models.CharField(max_length=2, null=True, blank=True, verbose_name='선택 답' )
	score = models.PositiveIntegerField(null=True, blank=True, verbose_name='점수' )
	ins_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='입력자ID' )
	ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
	ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
	ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
	upd_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='수정자ID' )
	upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
	upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
	upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
	class Meta:
		verbose_name = '지원서 답변'
		verbose_name_plural =  verbose_name
		unique_together=("ms_id", "test_div", "apl_no", "ques_no")

class ms_mrk(models.Model):
	ms_id = models.CharField(max_length=10, null=False, verbose_name='멘토스쿨ID' )
	test_div = models.CharField(max_length=10, null=False, verbose_name='전형구분(서류/면접)' )
	apl_no = models.CharField(max_length=10, null=False, verbose_name='지원 NO' )
	mrk_seq = models.PositiveIntegerField(null=False, verbose_name='채점 항목 SEQ(NO)' )
	mrk_no = models.PositiveIntegerField(null=False, verbose_name='채점자 NO' )
	mrk_id = models.CharField(max_length=10, null=False, verbose_name='채점자 ID' )
	mak_nm = models.CharField(max_length=20, null=False, verbose_name='채점자 명' )
	score = models.PositiveIntegerField(null=True, blank=True, verbose_name='점수' )
	ins_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='입력자ID' )
	ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
	ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
	ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
	upd_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='수정자ID' )
	upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
	upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
	upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
	class Meta:
		verbose_name = '지원서 채점'
		verbose_name_plural =  verbose_name
		unique_together=("ms_id", "test_div", "apl_no", "mrk_seq", "mrk_no")



class mentor(models.Model):
	mntr_id = models.CharField(max_length=10, primary_key=True, verbose_name='멘토ID' )
	mntr_nm = models.CharField(max_length=20, null=False, verbose_name='멘토 명' )
	mntr_nm_e = models.CharField(max_length=20, null=False, verbose_name='멘토 영문명' )
	ms_id = models.CharField(max_length=10, null=False, verbose_name='멘토스쿨ID' )
	apl_no = models.PositiveIntegerField(null=False, verbose_name='지원 NO' )
	apl_id = models.CharField(max_length=10, null=False, verbose_name='지원자ID(학번)' )
	mntr_dt = models.DateField(null=False, verbose_name='멘토 자격 부여일' )
	unv_cd = models.CharField(max_length=10, null=False, verbose_name='멘토 대학교 코드' )
	unv_nm = models.CharField(max_length=30, null=False, verbose_name='멘토 대학교 명' )
	cllg_cd = models.CharField(max_length=10, null=False, verbose_name='멘토 대학 코드' )
	cllg_nm = models.CharField(max_length=30, null=False, verbose_name='멘토 대학 명' )
	dept_cd = models.CharField(max_length=10, null=False, verbose_name='멘토 학부/학과 코드' )
	dept_nm = models.CharField(max_length=30, null=False, verbose_name='멘토 학부/학과 명' )
	brth_dt = models.CharField(max_length=8, null=False, verbose_name='생년월일' )
	gen = models.CharField(max_length=1, null=False, verbose_name='성별' )
	yr = models.CharField(max_length=4, null=False, verbose_name='학년도' )
	term_div = models.CharField(max_length=2, null=False, verbose_name='학기' )
	sch_yr = models.CharField(max_length=1, null=False, verbose_name='학년' )
	exp_dt = models.DateField(null=True, blank=True, verbose_name='멘토 자격 박탈일' )
	exp_rsn = models.CharField(max_length=10, null=True, blank=True, verbose_name='자격박탈 사유' )
	mob_no = models.CharField(max_length=12, null=True, blank=True, verbose_name='휴대전화' )
	tel_no = models.CharField(max_length=12, null=True, blank=True, verbose_name='집전화' )
	tel_no_g = models.CharField(max_length=12, null=True, blank=True, verbose_name='보호자 연락처' )
	h_addr = models.CharField(max_length=200, null=True, blank=True, verbose_name='집주소' )
	post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
	email_addr = models.CharField(max_length=50, null=True, blank=True, verbose_name='이메일 주소' )
	bank_acct = models.CharField(max_length=20, null=True, blank=True, verbose_name='은행 계좌 번호' )
	bank_nm = models.CharField(max_length=50, null=True, blank=True, verbose_name='은행 명' )
	bank_dpsr = models.CharField(max_length=20, null=True, blank=True, verbose_name='예금주' )
	cnt_mp_a = models.PositiveIntegerField(default=0, verbose_name='멘토링 지원 경력' )
	cnt_mp_p = models.PositiveIntegerField(default=0, verbose_name='멘토링 수행 경력' )
	cnt_mp_c = models.PositiveIntegerField(default=0, verbose_name='멘토링 완료 경력' )
	cnt_mp_g = models.PositiveIntegerField(default=0, verbose_name='멘토링 중도포기 경력' )
	ins_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='입력자ID' )
	ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
	ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
	ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
	upd_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='수정자ID' )
	upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
	upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
	upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
	
	class Meta:
		verbose_name = '멘토'
		verbose_name_plural = verbose_name


class mentee(models.Model):
	mnte_id = models.CharField(max_length=10, primary_key=True, verbose_name='멘티ID' )
	mnte_nm = models.CharField(max_length=20, null=False, verbose_name='멘티 명' )
	mnte_nm_e = models.CharField(max_length=20, null=False, verbose_name='멘티 영문명' )
	brth_dt = models.CharField(max_length=8, null=False, verbose_name='생년월일(+ 멘티명 → 동일인 찾기)' )
	sch_grd = models.CharField(max_length=1, null=False, verbose_name='학교구분' )
	sch_cd = models.CharField(max_length=10, null=False, verbose_name='학교' )
	sch_nm = models.CharField(max_length=30, null=False, verbose_name='학교명' )
	gen = models.CharField(max_length=1, null=False, verbose_name='성별' )
	yr = models.CharField(max_length=4, null=False, verbose_name='학년도' )
	term_div = models.CharField(max_length=2, null=False, verbose_name='학기' )
	sch_yr = models.CharField(max_length=1, null=False, verbose_name='학년' )
	mob_no = models.CharField(max_length=12, null=True, blank=True, verbose_name='휴대전화' )
	tel_no = models.CharField(max_length=12, null=True, blank=True, verbose_name='집전화' )
	tel_no_g = models.CharField(max_length=12, null=True, blank=True, verbose_name='보호자 연락처' )
	prnt_nat_cd = models.CharField(max_length=10, null=False, verbose_name='부모출신국가코드' )
	prnt_nat_nm = models.CharField(max_length=20, null=False, verbose_name='부모출신국가명' )
	grd_id = models.CharField(max_length=10, null=False, verbose_name='주 보호자 ID' )
	tchr_id = models.CharField(max_length=10, null=False, verbose_name='지도교사 ID' )
	area_city = models.CharField(max_length=10, null=False, verbose_name='시/도' )
	area_gu = models.CharField(max_length=10, null=False, verbose_name='지역구(시/군)' )
	h_addr = models.CharField(max_length=200, null=False, verbose_name='집주소' )
	h_post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
	s_addr = models.CharField(max_length=200, null=False, verbose_name='학교주소' )
	s_post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
	email_addr = models.CharField(max_length=50, null=False, verbose_name='이메일 주소' )
	mp_id = models.CharField(max_length=10, null=False, verbose_name='첫 지원 멘토링 프로그램ID' )
	mp_nm = models.CharField(max_length=100, null=True, blank=True, verbose_name='첫 지원 멘토링 프로그램 명' )
	apl_no = models.PositiveIntegerField(null=False, verbose_name='첫 지원 멘토링 지원 NO' )
	mp_dt = models.CharField(max_length=8, null=False, verbose_name='첫 멘토링 시작일' )
	cnt_mp_a = models.PositiveIntegerField(default=0, verbose_name='멘토링 지원 경력' )
	cnt_mp_p = models.PositiveIntegerField(default=0, verbose_name='멘토링 수행 경력' )
	cnt_mp_c = models.PositiveIntegerField(default=0, verbose_name='멘토링 완료 경력' )
	cnt_mp_g = models.PositiveIntegerField(default=0, verbose_name='멘토링 중도포기 경력' )
	ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
	ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
	ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
	upd_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='수정자ID' )
	upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
	upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
	upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

class Meta:
	verbose_name = '멘티'
	verbose_name_plural =  verbose_name


class guardian(models.Model):
	grdn_id = models.CharField(max_length=10, primary_key=True, verbose_name='보호자ID' )
	grdn_nm = models.CharField(max_length=20, null=False, verbose_name='보호자명' )
	grdn_nm_e = models.CharField(max_length=20, null=False, verbose_name='보호자 영문명' )
	rel_tp = models.CharField(max_length=2, null=True, blank=True, verbose_name='관계' )
	brth_dt = models.CharField(max_length=8, null=False, verbose_name='생년월일(+ 멘티명 → 동일인 찾기)' )
	mob_no = models.CharField(max_length=12, null=True, blank=True, verbose_name='휴대전화' )
	tel_no = models.CharField(max_length=12, null=True, blank=True, verbose_name='집전화' )
	moth_nat_cd = models.CharField(max_length=10, null=False, verbose_name='출신국가코드' )
	moth_nat_nm = models.CharField(max_length=20, null=False, verbose_name='출신국가명' )
	tch_id = models.CharField(max_length=10, null=False, verbose_name='지도교사 ID' )
	h_addr = models.CharField(max_length=200, null=False, verbose_name='집주소' )
	h_post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
	email_addr = models.CharField(max_length=50, null=False, verbose_name='이메일 주소' )
	ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
	ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
	ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
	upd_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='수정자ID' )
	upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
	upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
	upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )


class teacher(models.Model):
	tchr_id = models.CharField(max_length=10, primary_key=True, verbose_name='교사 ID(학교별 부여)' )
	tchr_nm = models.CharField(max_length=20, null=False, verbose_name='교사명' )
	tchr_nm_e = models.CharField(max_length=20, null=False, verbose_name='교사 영문명' )
	sch_grd = models.CharField(max_length=1, null=False, verbose_name='학교구분' )
	sch_cd = models.CharField(max_length=10, null=False, verbose_name='학교' )
	sch_nm = models.CharField(max_length=30, null=False, verbose_name='학교명' )
	mob_no = models.CharField(max_length=12, null=True, blank=True, verbose_name='휴대전화' )
	tel_no = models.CharField(max_length=12, null=True, blank=True, verbose_name='사무실전화' )
	area_city = models.CharField(max_length=10, null=False, verbose_name='시/도' )
	area_gu = models.CharField(max_length=10, null=False, verbose_name='지역구(시/군)' )
	h_addr = models.CharField(max_length=200, null=False, verbose_name='집주소' )
	h_post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
	s_addr = models.CharField(max_length=200, null=False, verbose_name='학교주소' )
	s_post_no = models.CharField(max_length=6, null=True, blank=True, verbose_name='우편번호' )
	email_addr = models.CharField(max_length=50, null=False, verbose_name='이메일 주소' )
	ins_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='입력자ID' )
	ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
	ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
	ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
	upd_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='수정자ID' )
	upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
	upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
	upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

class Meta:
	verbose_name = '교사(학교)'
	verbose_name_plural =  verbose_name


class Meta:
	verbose_name = '학부모(보호자 Gardian)'
	verbose_name_plural =  verbose_name


class mpgm(models.Model):
	mp_id = models.CharField(max_length=10, primary_key=True, verbose_name='멘토링 프로그램ID' )
	status = models.CharField(max_length=2, null=True, blank=True, verbose_name='상태' )
	mp_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='멘토링 프로그램 명' )
	mp_sname = models.CharField(max_length=20, null=True, blank=True, verbose_name='멘토링 프로그램 단명' )
	img_src = models.CharField(max_length=100, null=True, blank=True, verbose_name='이미지경로' )
	base_div = models.PositiveIntegerField(null=True, blank=True, verbose_name='기준 프로그램 여부' )
	mp_intro = models.CharField(max_length=1000, null=True, blank=True, verbose_name='프로그램 소개, CMS ID' )
	mng_area = models.CharField(max_length=2, null=True, blank=True, verbose_name='프로그램 관리자 영역' )
	mgr_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='프로그램 관리자 ID' )
	mgr_nm = models.CharField(max_length=20, null=True, blank=True, verbose_name='프로그램 관리자 명' )
	mng_org = models.CharField(max_length=10, null=True, blank=True, verbose_name='관리기관' )
	sup_org = models.CharField(max_length=10, null=True, blank=True, verbose_name='주관기관' )
	yr = models.CharField(max_length=4, null=True, blank=True, verbose_name='연도' )
	yr_seq = models.PositiveIntegerField(null=True, blank=True, verbose_name='차수' )
	apl_ntc_fr_dt = models.DateTimeField(null=True, blank=True, verbose_name='공지시작일' )
	apl_ntc_to_dt = models.DateTimeField(null=True, blank=True, verbose_name='공지종료일' )
	apl_term = models.CharField(max_length=2, null=True, blank=True, verbose_name='모집시기' )
	apl_fr_dt = models.DateTimeField(null=True, blank=True, verbose_name='모집기간-시작' )
	apl_to_dt = models.DateTimeField(null=True, blank=True, verbose_name='모집기간-종료' )
	mnt_term = models.CharField(max_length=2, null=True, blank=True, verbose_name='활동시기' )
	mnt_fr_dt = models.DateTimeField(null=True, blank=True, verbose_name='활동기간-시작' )
	mnt_to_dt = models.DateTimeField(null=True, blank=True, verbose_name='활동기간-시작' )
	tot_apl = models.PositiveIntegerField(default=0, verbose_name='모집인원(정원)-합격' )
	cnt_apl = models.PositiveIntegerField(default=0, verbose_name='지원인원' )
	cnt_doc_suc = models.PositiveIntegerField(default=0, verbose_name='서류전형 합격인원' )
	cnt_doc_res = models.PositiveIntegerField(default=0, verbose_name='서류전형 예비인원(실제 없음)' )
	cnt_intv_pl = models.PositiveIntegerField(default=0, verbose_name='면접전형 참여 계획 인원' )
	cnt_intv_ac = models.PositiveIntegerField(default=0, verbose_name='면접전형 참여 인원' )
	intv_dt = models.CharField(max_length=8, null=True, blank=True, verbose_name='면접일' )
	cnt_intv_suc = models.PositiveIntegerField(default=0, verbose_name='면접전형 합격인원' )
	cnt_iintv_res = models.PositiveIntegerField(default=0, verbose_name='면접전형 예비합격인원' )
	cnt_trn = models.PositiveIntegerField(default=0, verbose_name='교육인원' )
	cnt_mtr = models.PositiveIntegerField(default=0, verbose_name='최종합격 멘토인원' )
	doc_dt = models.DateTimeField(null=True, blank=True, verbose_name='서류전형일' )
	doc_mgr = models.CharField(max_length=10, null=True, blank=True, verbose_name='서류전형 수행자' )
	intv_dt = models.DateTimeField(null=True, blank=True, verbose_name='면접전형-입력-일' )
	intv_mgr = models.CharField(max_length=10, null=True, blank=True, verbose_name='면접전형-입력-자' )
	fin_dt = models.DateTimeField(null=True, blank=True, verbose_name='최종합격-입력-일' )
	fin_mgr = models.CharField(max_length=10, null=True, blank=True, verbose_name='최종합격-입력-자' )
	use_div = models.CharField(max_length=1, null=True, blank=True, verbose_name='사용 여부' )
	ins_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='입력자ID' )
	ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
	ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
	ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
	upd_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='수정자ID' )
	upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
	upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
	upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

class Meta:
	verbose_name = '멘토링프로그램'
	verbose_name_plural =  verbose_name


class mp_sub(models.Model):
	ms_id = models.CharField(max_length=10, null=False, verbose_name='멘토스쿨ID' )
	att_id = models.CharField(max_length=10, null=False, verbose_name='속성ID' )
	att_seq = models.PositiveIntegerField(null=False, verbose_name='속성 SEQ' )
	att_cdh = models.CharField(max_length=6, null=True, blank=True, verbose_name='속성 CODE HEADER' )
	att_cdd = models.CharField(max_length=10, null=True, blank=True, verbose_name='속성 CODE' )
	att_val = models.CharField(max_length=60, null=True, blank=True, verbose_name='속성 값' )
	use_yn = models.CharField(max_length=1, null=True, blank=True, verbose_name='사용여부' )
	sort_seq = models.PositiveIntegerField(default=1, verbose_name='정렬' )

	ins_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='입력자ID' )
	ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
	ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
	ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
	upd_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='수정자ID' )
	upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
	upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
	upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

class Meta:
	verbose_name = '멘토링프로그램 속성'
	verbose_name_plural =  verbose_name
	unique_together=("ms_id", "att_id", "att_seq")


class cm_cnv_scr(models.Model):
	eval_item = models.CharField(max_length=2, null=False, verbose_name='항목' )
	eval_seq = models.PositiveIntegerField(null=False, verbose_name='순서' )
	min_scr = models.PositiveIntegerField(null=False, verbose_name='최소 점수' )
	max_scr = models.PositiveIntegerField(null=False, verbose_name='최대 점수' )
	eval_unit = models.CharField(max_length=10, null=False, verbose_name='단위' )
	fin_scr = models.PositiveIntegerField(null=False, verbose_name='점수' )
	ins_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='입력자ID' )
	ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
	ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
	ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
	upd_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='수정자ID' )
	upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
	upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
	upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )
	
	class Meta:
		verbose_name = '점수변환표'
		verbose_name_plural =  verbose_name
		unique_together=("eval_item", "eval_seq")

# Create your models here.




class mp_sub(models.Model):
	ms_id = models.CharField(max_length=10, null=False, verbose_name='멘토스쿨ID' )
	att_id = models.CharField(max_length=10, null=False, verbose_name='속성ID' )
	att_seq = models.PositiveIntegerField(null=False, verbose_name='속성 SEQ' )
	att_cdh = models.CharField(max_length=6, null=True, blank=True, verbose_name='속성 CODE HEADER' )
	att_cdd = models.CharField(max_length=10, null=True, blank=True, verbose_name='속성 CODE' )
	att_val = models.CharField(max_length=60, null=True, blank=True, verbose_name='속성 값' )
	att_unit = models.CharField(max_length=10, null=True, blank=True, verbose_name='속성 단위' )
	use_yn = models.CharField(max_length=1, null=True, blank=True, verbose_name='사용여부' )
	sort_seq = models.PositiveIntegerField(default=1, verbose_name='정렬' )
	ins_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='입력자ID' )
	ins_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력자IP' )
	ins_dt = models.DateTimeField(null=True, blank=True, verbose_name='입력일시' )
	ins_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='입력프로그램ID' )
	upd_id = models.CharField(max_length=10, null=True, blank=True, verbose_name='수정자ID' )
	upd_ip = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정자IP' )
	upd_dt = models.DateTimeField(null=True, blank=True, verbose_name='수정일시' )
	upd_pgm = models.CharField(max_length=20, null=True, blank=True, verbose_name='수정프로그램ID' )

class Meta: 
	verbose_name = '멘토링프로그램 속성'
	verbose_name_plural =  verbose_name
	unique_together=("ms_id", "att_id", "att_seq")

