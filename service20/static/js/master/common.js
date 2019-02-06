/*==========================================================================
		Default Init
 ==========================================================================*/

/*==========================================================
String 객체의 문자열 모두 변환하기 (기본 replace 함수는 1회 1단어 변환)
=============================================================*/
String.prototype.replaceAll = function( searchStr, replaceStr ){
	var temp = this;
	while( temp.indexOf( searchStr ) != -1 ){temp = temp.replace( searchStr, replaceStr );}
	return temp;
}


/*=======================================================================
숫자 천단위 콤마 찍기
=======================================================================*/
function fnCommify(n) {
  var reg = /(^[+-]?\d+)(\d{3})/;   // 정규식
  n += '';                          // 숫자를 문자열로 변환
  while (reg.test(n))
    n = n.replace(reg, '$1' + ',' + '$2');
  return n;
}


/*=============================================================
리스트에서 페이지 이동 (library.inc 파일과 연동)
=============================================================*/
npage=0;
function fnGoPage(page){if(page!=npage)document.location=document.location.pathname + "?pgData=" + pgData +"&page=" + page;}

	
<!--
/*===============================================================================
입력한 숫자를 한글로 변환해 줍니다.
사용예제 : this.form.han.value=Number(this.value).read()
===============================================================================*/
Number.prototype.read = function() {
	if (this == 0 || isNaN(this)) return '영';
	var phonemic = ['','일','이','삼','사','오','육','칠','팔','구'];
	var unit = ['','','십','백','천','만','십만','백만','천만','억','십억','백억','천억','조','십조','백조'];
	var ret = '';
	var part = new Array();
	for (var x=0; x<String(this).length; x++) part[x] = String(this).substring(x,x+1);
		
	startPoint=0;	
	limitPoint=0
	
	//-- 마이너스 처리
	if(part[0]=="-"){
		ret="-";
		startPoint=1;
		limitPoint=1;
	}
	
	for (var i=startPoint, cnt = String(this).length-limitPoint; cnt > 0; --cnt,++i) {
		p = phonemic[part[i]];
		p+= (p) ? (cnt>4 && phonemic[part[i+1]]) ? unit[cnt].substring(0,1) : unit[cnt] : '';
		ret+= p;
	}
	return ret;
}
//-->

	/*===============================================================
		숫자 체크
	===============================================================*/	
	function fnValueNumCheck(obj){
		if(isNaN(obj.val())){
			alert("숫자로만 입력해주세요");
			obj.val('');
			obj.focus();
		}
	}
	
	/*===============================================================
		입력키 특수문자 체크 (영문과 숫자만 입력 가능)
	===============================================================*/
	function fnCharCheck(strValue){
			var intErr=true;		 
			 var retCode = 0;
			 var re = /[~!@\#$%<>^&*\()\-=+_\']/gi; //특수문자 정규식 변수 선언
			 
			 for (i = 0; i < strValue.length; i++) {
			  var retCode = strValue.charCodeAt(i);
			  var retChar = strValue.substr(i,1).toUpperCase();
			  retCode = parseInt(retCode);
			  
			  //입력받은 값중에 한글이 있으면 에러
			  if ( (retChar < "0" || retChar > "9") && (retChar < "A" || retChar > "Z") && ((retCode > 255) || (retCode < 0)) ) {
			   intErr = false;
			   break;
			  //입력받은 값중에 특수문자가 있으면 에러
			  } else if(re.test(strValue)) {
			   intErr = false;
			   break;
			  }
			 }
			 return intErr;
	}
	
	/*===============================================================
		입력키 특수문자 체크 (영문과 숫자 + 특수문자만 입력 가능 - 한글입력불가)
	===============================================================*/
	function fnCharCheck2(strValue){
			var intErr=true;		 
			 var retCode = 0;
			 var re = /[~!@\#$%<>^&*\()\-=+_\']/gi; //특수문자 정규식 변수 선언
			 
			 for (i = 0; i < strValue.length; i++) {
			  var retCode = strValue.charCodeAt(i);
			  var retChar = strValue.substr(i,1).toUpperCase();
			  retCode = parseInt(retCode);
			  
			  //입력받은 값중에 한글이 있으면 에러
			  if ( (retChar < "0" || retChar > "9") && (retChar < "A" || retChar > "Z") && ((retCode > 255) || (retCode < 0)) ) {
			   intErr = false;
			   break;
			  //입력받은 값중에 특수문자가 있으면 에러
			  }
			 }
			 
			 return intErr;
	}

	/*===============================================================
		입력키 특수문자 체크 (특수문자만 입력불가)
	===============================================================*/
	function fnCharCheck3(strValue){
			var intErr=true;		 
			 var retCode = 0;
			 var re = /[~!@\#$%<>^&*\()\-=+_\']/gi; //특수문자 정규식 변수 선언
			 
			 for (i = 0; i < strValue.length; i++) {
			  var retCode = strValue.charCodeAt(i);
			  var retChar = strValue.substr(i,1).toUpperCase();
			  retCode = parseInt(retCode);
			  
			  //입력받은 값중에 한글이 있으면 에러
			  if(re.test(strValue)) {
			   intErr = false;
			   break;
			  }
			 }
			 
			 return intErr;
	}
	

/*=======================================================================
전체 선택 삭제
=======================================================================*/
function fnCheckDel(){
		var frm=document.formList;
		chkObj = $("[name='table_records']:checked");
		if(!chkObj.length){
			alert("삭제하실 항목을 선택하여 주십시오");
			return;
		}

		if(confirm("선택하신 항목을 삭제하시겠습니까?")){
			frm.method="post";
			
			//--  path 도 같이 가져가기
			var p = document.createElement("input");
			p.type = "hidden";
			p.value = pgData;
			p.name = "pathStr";
			frm.appendChild(p);
			
			//-- 처리방식 지정
			var p = document.createElement("input");
			p.type = "hidden";
			p.value = "delete";
			p.name = "psMode";
			frm.appendChild(p);
			
			//-- 삭제할 레코드 지정
			len = chkObj.length;
			for(k=0;k<len;k++){
				var p = document.createElement("input");
				p.type = "hidden";
				p.value = chkObj.eq(k).val();
				p.name = "psObj[]";
				frm.appendChild(p)
			}
			frm.submit();
		}
}

/*=======================================================================
쿠키 체크 함수
=======================================================================*/
function fnGetCookie(name){
		var Found = false
		var start, end
		var i = 0
		while(i <= document.cookie.length) {
			start = i
			end = start + name.length
				if(document.cookie.substring(start, end) == name) {
					Found = true
					break;
				}
			i++
		}

		if(Found == true) {
			start = end + 1
			end = document.cookie.indexOf(";", start)
			if(end < start)
			end = document.cookie.length
			return document.cookie.substring(start, end)
		}
		return ""
}

/*=======================================================================
쿠키 체크 설정 함수
=======================================================================*/
function fnSetCookie(name, value, expiredays){
	var todayDate = new Date();
	todayDate.setDate( todayDate.getDate() + expiredays );
	document.cookie = name + "=" + escape( value ) + "; path=/; expires=" + todayDate.toGMTString() + ";"
	return true;
}

/*=======================================================================
연락처 양식 셋팅
=======================================================================*/
function fnTelSet(obj){
	v = obj.val();
	t = v.split("-");
	
	if(isNaN(v.replaceAll("-",""))){
		alert("잘못된 전화번호 형식입니다.");
		obj.val("");
		return;
	}

	if(t.length==1 && v.length>=9){
		v1 = "";
		v2 = "";
		v3 = "";
		if(v.length==9){
			//-- 가운데 3자리
			v1 = v.substr(0,2);
			v2 = v.substr(2,3);
			v3 = v.substr(5,4);
		}else if(v.length==10){
			//-- 가운데 3자리
			v1 = v.substr(0,3);
			v2 = v.substr(3,3);
			v3 = v.substr(6,4);
		}else if(v.length==11){
			//-- 가운데 4자리
			v1 = v.substr(0,3);
			v2 = v.substr(3,4);
			v3 = v.substr(7,4);
		}

		if(v1 && v2 && v3){
			obj.val(v1 + "-" + v2 + "-" + v3);
		}
	}
}

/*============================================
Data List 클릭시 수정 페이지로 이동 함수
============================================*/
function fnGoDataEdit(qIDX,addStr){
	if(!qIDX){
		alert("고유값 미설정오류");
		return;
	}
	if(!addStr)addStr="";
	exe = new Array(".asp",".php",".html");

	len = exe.length;
	nUrl = document.location.pathname.toString();

	for(k=0;k<len;k++)if(nUrl.indexOf(exe[k]))exeStr = exe[k];
	urlStr = nUrl.replace(exeStr,"") + "Edit" + exeStr;

	str = urlStr + "?pgData=" + pgData;
	if(qIDX)str+="&qIDX=" + qIDX;	
	if(addStr)str=str+"&"+addStr;
	
	//document.location=str;
	//-- IE 의 경우 location 으로 이동시 referrer 값이 없음 // 해당 현상 fix
	if((navigator.appName == 'Microsoft Internet Explorer') || ((navigator.appName == 'Netscape') && (new RegExp("Trident/.*rv:([0-9]{1,}[\.0-9]{0,})").exec(navigator.userAgent) != null))){
  	var referLink = document.createElement('a');
  	referLink.href = str;
  	document.body.appendChild(referLink);
  	referLink.click();
  }else{location.href = str;}
}

function fnGoDataView(qIDX,addStr){
	if(!qIDX){
		alert("고유값 미설정오류");
		return;
	}
	if(!addStr)addStr="";
	exe = new Array(".asp",".php",".html");

	len = exe.length;
	nUrl = document.location.pathname.toString();

	for(k=0;k<len;k++)if(nUrl.indexOf(exe[k]))exeStr = exe[k];
	urlStr = nUrl.replace(exeStr,"") + "View" + exeStr;

	str = urlStr + "?pgData=" + pgData;
	if(qIDX)str+="&qIDX=" + qIDX;	
	if(addStr)str=str+"&"+addStr;
	//document.location=str;
	//-- IE 의 경우 location 으로 이동시 referrer 값이 없음 // 해당 현상 fix
	if((navigator.appName == 'Microsoft Internet Explorer') || ((navigator.appName == 'Netscape') && (new RegExp("Trident/.*rv:([0-9]{1,}[\.0-9]{0,})").exec(navigator.userAgent) != null))){
  	var referLink = document.createElement('a');
  	referLink.href = str;
  	document.body.appendChild(referLink);
  	referLink.click();
  }else{location.href = str;}
  
}


function fnGoDataAdd(){
	exe = new Array(".asp",".php",".html");
	len = exe.length;
	nUrl = document.location.pathname.toString();
	for(k=0;k<len;k++)if(nUrl.indexOf(exe[k]))exeStr = exe[k];
	urlStr = nUrl.replace(exeStr,"") + "Edit" + exeStr;
	str = urlStr + "?pgData=" + pgData;
	//document.location=str;
	//-- IE 의 경우 location 으로 이동시 referrer 값이 없음 // 해당 현상 fix
	if((navigator.appName == 'Microsoft Internet Explorer') || ((navigator.appName == 'Netscape') && (new RegExp("Trident/.*rv:([0-9]{1,}[\.0-9]{0,})").exec(navigator.userAgent) != null))){
  	var referLink = document.createElement('a');
  	referLink.href = str;
  	document.body.appendChild(referLink);
  	referLink.click();
  }else{location.href = str;}
}

function fnGoDataList(){	
	exe = new Array(".asp",".php",".html");
	len = exe.length;
	nUrl = document.location.pathname.toString();
	for(k=0;k<len;k++)if(nUrl.indexOf(exe[k]))exeStr = exe[k];
	if(nUrl.indexOf("Edit.html")>=0||nUrl.indexOf("View.html")>=0||nUrl.indexOf("Ext.html")>=0){
		urlStr = nUrl.replace("Edit" + exeStr,"").replace("View" + exeStr,"").replace("Ext" + exeStr,"") + exeStr;		
	}
	
	urlStr = urlStr+"?pgData="+pgData;
	document.location=urlStr;
}

/*============================================
복사하기
============================================*/
function fnGoDataCopy(IDX){
	str = "<input type='text' name='cpIDX' value='"+IDX +"'>";
	str+= "<input type='text' name='psMode' value='copy'>";
	$("#formList").append(str);
	$("#formList").attr("method","post");
	$("#formList").submit();
	
}