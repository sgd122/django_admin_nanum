# 버전
  python3.6.7

# model추가시
	
	makemigrateions
	python manage.py migrate

# 요청사항
	
	ms_apl 테이블
	msch   테이블
		
		결과적으로 보여줄 테이블 : msch

		단계
			1. ms_apl에서 현재 request에서 받은 user_id(사용자ID),yr(년도),trn_term(학기) 토대로 ms_id_id를 가져온다.
			2. msch에서 조회한 쿼리의 row마다 ms_apl.ms_id_id <-> msch.ms_id 가 일치하면 "지원" 불일치하면 "미지원" 으로 값이 나온다.



	ms_sub 	테이블
	com_cdd 테이블
	ms_ans 	테이블

	1. ms_sub 테이블에서 질문내역 조회 -> 조회한 질문내역 기준으로 공통코드 조회
	2. ms_ans 테이블에서 ms_id,apl_id로 조회한 답변내역 
	3. 1번과 2번의 쿼리결과 합치기.



	mpgm 	테이블
	mentee 	테이블

	한개의 프로그램(mpgm)에 대한 멘티(mentee)를 조인해서 프로그램 및 맨티를 조회한다.
	한 row에 1개의 프로그램이고, 1개의 프로그램에 대한 맨티는 여러명.
	





