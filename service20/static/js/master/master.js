/*=======================================================================
기본 INIT
=======================================================================*/
p = document.location.pathname.split("/");
pathChk = p.length;

$(document).ready(function(){
	$("a").focus(function(){$(this).blur();});

	//-- 메세지 수신 처리 --//
	var cnt = 10; //$("#custom_notifications ul.notifications li").length + 1;
	TabbedNotification = function (options) {
	    var message = "<div id='ntf" + cnt + "' class='text alert-" + options.type + "' style='display:none'><h2>";
	    message+= "<input type='hidden' name='inMSGFLAG[]' value='" + options.flag + "'>";
	    message+= "<input type='hidden' name='inMSGIDX[]' value='" + options.IDX + "'>";
	    message+= "<i class='fa fa-bell'></i> " + options.title + "</h2><div class='close'><a href='javascript:;' class='notification_close'><i class='fa fa-close'></i></a></div><p>" + options.text + "</p></div>";
	    if (document.getElementById('custom_notifications') == null) {
	        alert('doesnt exists');
	    } else {
	        $('#custom_notifications ul.notifications').append("<li><a id='ntlink" + cnt + "' class='alert-" + options.type + "' href='#ntf" + cnt + "'><i class='fa fa-bell animated shake'></i></a></li>");
	        $('#custom_notifications #notif-group').append(message);
	        cnt++;
	        CustomTabs(options);
	    }
	}

	CustomTabs = function (options) {
	    $('.tabbed_notifications > div').hide();
	    $('.tabbed_notifications > div:first-of-type').show();
	    $('#custom_notifications').removeClass('dsp_none');
	    $('.notifications a').click(function (e) {
	        e.preventDefault();
	        var $this = $(this),
	            tabbed_notifications = '#' + $this.parents('.notifications').data('tabbed_notifications'),
	            others = $this.closest('li').siblings().children('a'),
	            target = $this.attr('href');
	        others.removeClass('active');
	        $this.addClass('active');
	        $(tabbed_notifications).children('div').hide();
	        $(target).show();
	    });
	}
	CustomTabs();

	var tabid = idname = '';
	$(document).on('click', '.notification_close', function (e) {
			p = $(this).parent().parent();
	    idname = p.attr("id");
			MSGFLAG = p.find("[name='inMSGFLAG[]']").val();
			if(MSGFLAG=="project"){	//== 프로젝트 메세지일경우 읽음 처리
		    MSGIDX = p.find("[name='inMSGIDX[]']").val();
		    if(MSGIDX){	//-- 단순 메세지 / MSGIDX 가 있을경우 처리	/ 기타 MSGIDX 가 없을경우 그냥 일반 알람.
			    //-- 메세지 확인 처리
			    param="mode=checkMsg&IDX="+MSGIDX;
					$.ajax({
						url:'/inc/messageCheck.html',
						method : 'post',
						cache:false,
						data : param,
						dataType:"json",
						success:function(data){
							if(data["result"]=="ERROR"){
								//-- 오류발생
							}
						}
					});
				}
			}
	
	    tabid = idname.substr(-2);
	    $('#ntf' + tabid).remove();
	    $('#ntlink' + tabid).parent().remove();
	    $('.notifications a').first().addClass('active');
	    $('#notif-group div').first().css('display','block');
	});

	/* 메세지 띄우기 형식 샘플
	new TabbedNotification({
	    title: 'Tabbed Notificat',
	    text: 'Custom Info... Raw denim you probably haven\'t heard of them jean shorts Austin. Nesciunt tofu stumptown aliqua, retro synth master cleanse. Mustache cliche tempor, williamsburg carles vegan helvetica.',
	    type: 'danger',
	    sound: false
	});
	*/

	fnCheckMessage();
	

  //-- FORM 에서 EnterKey 입력시 Submit 되는 현상 방지
  $('#formObject input[type="text"]').bind('keydown', function(e) {
	    if (e.keyCode == 13){
        e.preventDefault();
	    }
	});
	
	//-- fancyBox Start
	$("a#single_image").fancybox();
	
	//-- modal 창 좌표잡기 일괄 제어
	modalPop = $(".modal-dialog");
	modalLen = modalPop.length;
	for(k=0;k<modalLen;k++){
		obj = modalPop.eq(k);
		modalObj = obj.parent();
		modalObj.on('show.bs.modal', function (e) {
			//-- 박스 좌표 다시 잡기
			scrTop = top.document.documentElement.scrollTop;
		  if(scrTop<1)scrTop=50;		  
		  $(this).find(".modal-dialog").css("margin-top",scrTop);
		});
	}
	
	//-- 검색영역에서 TEXT input 에서 엔터키 입력시 검색 실행
	  $('#formSearch input[type="text"]').bind('keydown', function(e) {
	    if (e.keyCode == 13){
        fnAdminSearch();
	    }
	});
	
	top.scrollTo(0,0);
	
	$("form").validate();
	fnInfoSortInit();
});

//-- end of document ready

//$(function(){$("form").validate();})

//-- 프레임 리사이즈
$(document).ready(function(){
	if(pathChk<=2)return;	//-- 서브페이지에서만 작동
	fnTopFrameResize();
});

$(window).resize(function(){
	if(pathChk<=2)return;	//-- 서브페이지에서만 작동
	fnTopFrameResize();
});

function fnTopFrameResize(){
	try{top.fnFrameResize($(".container.body").height());}catch(E){}
}


/*=======================================================================
F5 막기 & 뒤로가기(백스페이스) 막기
=======================================================================*/
$(document).keydown(function (e) {
    // F5, ctrl + F5, ctrl + r 새로고침 막기
    var allowPageList   = new Array('/a.php', '/b.php');
    var bBlockF5Key     = true;
    for (number in allowPageList) {
        var regExp = new RegExp('^' + allowPageList[number] + '.*', 'i');
        if (regExp.test(document.location.pathname)) {
            bBlockF5Key = false;
            break;
        }
    }

    if (bBlockF5Key) {
        if (e.which === 116) {
            if (typeof event == "object") {
                event.keyCode = 0;
            }
            top.fnTabRefresh();
            return false;
        } else if (e.which === 82 && e.ctrlKey) {
        		top.fnTabRefresh();
            return false;
        } else if (e.which==8){
        	if(e.target.nodeName!="INPUT" && e.target.nodeName!="TEXTAREA"){
        		fnTabBack();
        		return false;
        	}
        }
    }
});


/*=======================================================================
택 기능 구현
=======================================================================*/
//-- 탭 추가
function fnTabAdd(tabID,tabTTL,urlStr){
	if($("#tabArea #tab"+tabID).length){
		document.getElementById("frame" + tabID).contentWindow.location=urlStr;
		fnTabFocus(tabID);

	}else{
		str = "<div class='tabItem' id='tab"+tabID+"' onclick='fnTabFocus($(this).attr(\"id\"))'><span class='ttl'>"+tabTTL+"</span><span class='close glyphicon glyphicon-remove' onclick='fnTabDel($(this).parent().attr(\"id\"))'></span></div>";
		$("#tabArea").append(str);

		str = "<iframe src='"+urlStr+"' id='frame"+tabID+"' class='active' frameborder=0></iframe>";
		$("#tabFrame").append(str);

		obj = $("#frame"+tabID);
		body = obj.find("document");

		tabCnt = $("#tabArea .tabItem").length;
		if(tabCnt>9){
			w = Math.floor(100/tabCnt);
		}else{
			w = "10";
		}
		$("#tabArea .tabItem").css("width",w+"%");
		fnTabFocus(tabID);
		fnTabSort();
	}
}

//-- 프레임 리사이즈
function fnFrameResize(h){
	$("#tabFrame .active").height(h);
}

//-- 탭 포커스
function fnTabFocus(tabID){
	tabID = tabID.replace("tab","");
	$("#tabArea .active").removeClass("active");
	$("#tabArea #tab"+tabID).addClass("active");

	$("#tabFrame .active").removeClass("active");
	$("#tabFrame #frame"+tabID).addClass("active");
}

//-- 탭 삭제
function fnTabDel(tabID){

	len = $("#tabArea .tabItem").length;
	if(len<=1)return;	//-- 1개일때는 삭제안됨

	tabID = tabID.replace("tab","");
	$("#tabArea #tab"+tabID).html("");
	$("#tabArea #tab"+tabID).animate({width:"0px"},300,function(){$("#tabArea #tab"+tabID).remove();
		fnTabFocus($("#tabArea .tabItem").eq(0).attr("id"));
	});
	$("#tabFrame #frame"+tabID).fadeOut(300,function(){$("#tabFrame #frame"+tabID).remove();});
}

//-- 탭 드래그
function fnTabSort(){
	$('#tabArea').sortable({
      placeholderClass: 'tabItem tabItemDrag'
  });
}

//-- 탭 새로고침
function fnTabRefresh(){
	try{
		tabID = $("#tabArea .active").attr("id").replace("tab","");
		document.getElementById("frame" + tabID).contentWindow.location.reload();
	}catch(E){}
}

//-- 탭 뒤로가기
function fnTabBack(){
	try{
		tabID = $("#tabArea .active").attr("id").replace("tab","");
		document.getElementById("frame"+tabID).contentWindow.fnTabBack();
	}catch(E){
		//alert(document.location.pathname + " \n\n " + document.referrer);
		//-- 로그인 페이지로 빠져나가지 않도록 처리
		if(document.referrer.indexOf("index")==-1 && document.referrer.indexOf("login")==-1){
			history.back();
		}
	}
	return false;
}

/*=======================================================================
메세지 검사 & 알람검사 & 실시간 접수 검사
=======================================================================*/
function fnCheckMessage(){
	if(pathChk>2)return;
	param="mode=list";
	$.ajax({
		url:'/inc/messageCheck.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			
			//-- 프로젝트 수정/추가 관련 메세지
			msgLen = data["msgLnegth"];
			for(k=0;k<msgLen;k++){
				obj = data["msgData"][k];
				fnMakeMessage(obj["IDX"],obj["MSGtitle"],obj["MSGcontent"],"info","project");
			}
			
			//-- 알람
			arLen = data["alarmLength"];
			for(k=0;k<arLen;k++){
				obj = data["alarmData"][k];
				fnMakeMessage(obj["IDX"],obj["MSGtitle"],obj["MSGcontent"],"success","alram");
			}
		}
	});

	//-- 1분에 한번 메세지 검사
	setTimeout("fnCheckMessage()",60000);
}

//== 메세지 박스 생성
function fnMakeMessage(IDX,TTL,TXT,TYP,FLG){

	if(IDX){
		//-- 중복메세지 검사
		MSGF = $("[name='inMSGFLAG[]']");
		MSGS = $("[name='inMSGIDX[]']");
		len = MSGS.length;
		for(k=0;k<len;k++){
			v = MSGS.eq(k).val();
			f = MSGF.eq(k).val();
			if(v==IDX && f==FLG)return;
		}
	}
	
	if(FLG=="alram"){
		alert("통화알람이 있습니다!");
	}

	new TabbedNotification({
	    title: TTL,
	    text: TXT,
	    type: TYP,
	    flag:FLG,
	    IDX: IDX,
	    sound: false
	});
	$(window).focus();
}

/*=============================================
	Editor Form에서 서브밋 전에 처리기능
=============================================*/
$("form").submit(function(){

	if($("#submitBtnDiv")){
		if (typeof(oEditors) !== 'undefined') {
			len = oEditors.length;
			for(k=0;k<len;k++){
				oEditors[k].exec("UPDATE_CONTENTS_FIELD", []);
			}
		}
		/*
			$("#submitBtnDiv").css("display","none");
			$("#submitBtnDiv").after('<div class="col-md-12 col-sm-12 col-xs-12 txtC" id="submitLoadingDiv">처리중입니다... <input type="button" class="btn btn-xs btn-danger" onclick="fnFormLoadingCancel()" value="취소"></div>');
		*/
	}
});

function fnFormLoadingCancel(){
	$("#submitBtnDiv").css("display","block");
	$("#submitLoadingDiv").remove();
}

/*=======================================================================
관리자모드 수정 페이지로 가기
=======================================================================*/
function fnGoPageMode(m,qIDX,addStr){
	if(!m)return;

	exe = new Array(".asp",".php",".html");
	len = exe.length;
	nUrl = document.location.pathname.toString();

	for(k=0;k<len;k++)if(nUrl.indexOf(exe[k]))exeStr = exe[k];

	str="";
	if(m=="list"){
		if(nUrl.indexOf("Edit.html")>=0||nUrl.indexOf("View.html")>=0){
			urlStr = nUrl.replace("Edit" + exeStr,"").replace("View" + exeStr,"") + exeStr;
		}
	}else if(m=="add"){
		urlStr = nUrl.replace(exeStr,"") + "Edit" + exeStr;
	}else if(m=="edit"){
		urlStr = nUrl.replace(exeStr,"") + "Edit" + exeStr;
		str = "&qIDX=" + qIDX;
	}
	if(addStr)str=str+"&"+addStr;
	urlStr = urlStr+"?pgData="+pgData+str;
	document.location=urlStr;
}

/*=============================================
	검색처리
=============================================*/
function fnAdminSearch(){

	p = document.location.pathname;
	
	var params = jQuery("#searchForm").serializeArray();
	str = "";
    jQuery.each( params, function( i, field ) {

     	if(field.value==""){

     	}else{
     		str = str + field.name + "=" + field.value + "&"
     	}
    });
	//var fields = $( ":input" ).serializeArray();

	pgData = "";
	searchStr = "pgData=" + pgData + "&page=1";
	for(k=1;k<=15;k++){
		obj = $("#s" + k);
		objType = obj.prop("tagName");
		t = obj.prop("type");
		sVal="";
		if(objType=="INPUT" || objType=="SELECT" || objType=="RADIO"){
			/*
				select : select-one
				text   : text
				radio  : radio
				checkbox : checkbox
			*/
			if(t == "radio"){
				sVal = $("#s" + k + ":checked").val();
			}else if(t == "checkbox"){
				if($("#s" + k).prop("checked"))sVal = $("#s" + k).val();
			}else{
				//-- 일반 텍스트
				sVal = obj.val();
			}
			sVal = sVal.replaceAll("'","");
			sVal = sVal.replaceAll('"',"");
			//sVal = escape(sVal);

			searchStr+= "&s" + k + "=" + sVal;
		}
	}//-- end For

	
	//document.location="/admin/service20/msch" + "?" + "yr=2018";
	///admin/service20/msch/?pgData=&page=1&s1=2019&s2=&s3=10
	//alert(p + "?" + searchStr);
	//document.location=p + "?" + searchStr;
	document.location="?" + str;


}

/*=======================================================================
리스트에서 테이블 정렬기능
=======================================================================*/

function fnInfoSortInit(){
	
	th = $("#formList thead tr th");
	len = th.length;
	
	for(k=0;k<len;k++){		
		obj = th.eq(k);
		
		v = obj.attr("order");
		
		if(v){
			str = obj.html();
			str = "<a href='javascript:fnInfoSort(\""+v+"\");'>" +str;
			if(nOrder1==v){
				if(nOrder2=="asc"){
					str+="▲";
				}else{
					str+="▼";
				}
			}
			str+="</a>";
			obj.html(str);
		}
	}
}

function fnInfoSort(f){	//-- 정렬필드 확인 및 링크작동. 1번 클릭 asc, 2번 클릭 desc, 3번클릭하면 정렬해제한다.
	nUrl = document.location.pathname.toString();
	o2="";
	if(nOrder1==f){
		if(nOrder2==""){
			o2="asc";
		}else if(nOrder2=="asc"){
			o2="desc";
		}else if(nOrder2=="desc"){
			f="";
			o2="";
		}
	}
	
	str=nUrl+"?pgData="+pgData;
	str+="&order1="+f;
	str+="&order2="+o2;
	document.location = str;
	
}


/*=============================================
	카테고리 트리액션 (grp 값은 테이블 선택 인자값. 빈값 = categoryInfo / EX = categoryExternal
=============================================*/
//-- 하위 카테고리 추가
function fnCateAdd(qIDX){
	if(!$("#inSubCTname").val()){
		alert("추가할 분류명을 입력해주세요");
		$("#inSubCTname").focus();
		return;
	}		

	CTname = $("#inSubCTname").val();
	param="mode=add&qIDX="+qIDX+"&CTname="+CTname+"&grp="+$("#grp").val();

	$.ajax({
		url:'./json/categoryProc.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				nIDX = data["nIDX"];

				if(nIDX){
					obj = $("#cateObj"+qIDX);
					if(obj.has("ul").length){
						ulObj = obj.find("ul").eq(0);
						str = "<li id=\"cateObj" + nIDX + "\"><a href=\"javascript:fnCateView("+nIDX+")\">" + CTname + "</li>";
						ulObj.append(str);
					}else{
						str = "<ul>";
						str+= "<li id=\"cateObj" + nIDX + "\"><a href=\"javascript:fnCateView("+nIDX+")\">" + CTname + "</li>";
						str+="</ul>";
						obj.append(str);
					}
					$("#divCateDetail").html("");
					$("#tree1").find(".active").removeClass("active");
				}else{
					alert("오류가 발생하였습니다. (423)");
				}

			}else{
				alert("오류가 발생하였습니다. (427)");
			}
		}
	});
}

//-- 선택 카테고리 삭제
function fnCateDel(qIDX){
	alert("삭제는 관리자에게 문의해주세요");
	//if(!confirm("해당 카테고리를 삭제하시겠습니까?"))return;
	//$("#cateObj"+qIDX).remove();
}

//-- 선택 카테고리 수정
function fnCateEdit(){
	obj1 = $("#divNowCTname");
	obj2 = $("#divNewCTname");

	if(obj2.hasClass("hiddenObj")){
		//-- 일반 > 수정하기
		$("#inNewCTname").val($("#nowCTname").html());
		obj1.removeClass("hiddenObj");
		obj2.removeClass("hiddenObj");
		obj1.addClass("hiddenObj");
	}else{
		//-- 수정하기 > 일반
		obj1.removeClass("hiddenObj");
		obj2.removeClass("hiddenObj");
		obj2.addClass("hiddenObj");
	}

}

//-- 선택 카테고리 수정 취소
function fnCateEditCancel(){
	obj1 = $("#divNowCTname");
	obj2 = $("#divNewCTname");

	obj1.removeClass("hiddenObj");
	obj2.removeClass("hiddenObj");
	obj2.addClass("hiddenObj");
}

//-- 선택 카테고리 수정 저장 (실제반영)
function fnCateEditSave(qIDX){
	if(!$("#inNewCTname").val()){
		alert("변경할 새로운 분류명을 입력해주세요");
		$("#inNewCTname").focus();
		return;
	}

	CTname = $("#inNewCTname").val();
	param="mode=edit&qIDX="+qIDX+"&CTname="+CTname+"&grp="+$("#grp").val();

	$.ajax({
		url:'./json/categoryProc.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				obj = $("#cateObj"+qIDX);
				obj.find("a").eq(0).html(CTname);
				$("#divCateDetail").html("");
				$("#tree1").find(".active").removeClass("active");
			}else{
				alert("오류가 발생하였습니다. (494)");
			}
		}
	});
}

function fnCateView(qIDX){
	$("#tree1").find(".active").removeClass("active");
	$("#cateObj"+qIDX).addClass("active");
	
	if(qIDX){
		param="mode=view&qIDX="+qIDX+"&grp="+$("#grp").val();
		
		$.ajax({
			url:'./json/categoryProc.html',
			method : 'post',
			cache:false,
			data : param,
			dataType:"json",
			success:function(data){
				if(data["result"]=="OK"){

					str = '<div class="x_panel" id="divCateDetail">';
					str+= '	<div class="page-header"><h5 id="container">분류 정보</h5></div>';

					str+= '	<div class="form-group">';
				  str+= '    <label class="control-label col-md-3 col-sm-3 col-xs-12">고유번호</label>';
				  str+= '    <div class="col-md-9 col-sm-9 col-xs-12">'+ data['IDX'] +'</div>';
				  str+= '  </div>';

				  str+= '	<div class="form-group">';
				  str+= '    <label class="control-label col-md-3 col-sm-3 col-xs-12">고유코드</label>';
				  str+= '    <div class="col-md-9 col-sm-9 col-xs-12">'+ data['CTcode'] +'</div>';
				  str+= '  </div>';

				  str+= '  <div class="form-group" id="divNowCTname">';
				  str+= '    <label class="control-label col-md-3 col-sm-3 col-xs-12">선택한분류</label>';
				  str+= '    <div class="col-md-6 col-sm-6 col-xs-12" id="nowCTname">'+ data['CTname'] +'</div>';
				  str+= '    <div class="col-md-3 col-sm-3 col-xs-12">';
				  str+= '    	<button class="btn btn-primary btn-sm" onclick="fnCateEdit()">분류명수정</button>';
				  str+= '    </div>';
				  str+= '  </div>';

				  str+= '  <div class="form-group hiddenObj" id="divNewCTname">';
				  str+= '    <label class="control-label col-md-3 col-sm-3 col-xs-12">새로운분류명</label>';
				  str+= '    <div class="col-md-6 col-sm-6 col-xs-12">';
				  str+= '    	<input type="text" class="form-control" required="required" placeholder="새로운분류명" name="inNewCTname" id="inNewCTname" value="" onkeydown="if(event.keyCode==13)fnCateEditSave(\'' + qIDX + '\')">';
				  str+= '    </div>';
				  str+= '    <div class="col-md-3 col-sm-3 col-xs-12">';
				  str+= '    	<button class="btn btn-primary btn-sm" onclick="fnCateEditSave(\'' + qIDX + '\')">V</button><button class="btn btn-danger btn-sm" onclick="fnCateEditCancel()">X</button>';
				  str+= '    </div>';
				  str+= '  </div>';


				  if(data["CTlevel"]<5){
					  str+= '  <div class="form-group">';
					  str+= '    <label class="control-label col-md-3 col-sm-3 col-xs-12">하위분류 추가</label>';
					  str+= '    <div class="col-md-6 col-sm-6 col-xs-12">';
					  str+= '    	<input type="text" class="form-control" required="required" placeholder="분류명" name="inSubCTname" id="inSubCTname" value="" onkeydown="if(event.keyCode==13)fnCateAdd(\'' + qIDX + '\')">';
					  str+= '    </div>';
					  str+= '    <div class="col-md-3 col-sm-3 col-xs-12">';
					  str+= '    	<button class="btn btn-primary btn-sm" onclick="fnCateAdd(\'' + qIDX + '\')">하위추가</button>';
					  str+= '    </div>';
					  str+= '  </div>';
					}

				  if(qIDX>0){
					  str+= '  <div class="form-group txtC">';
					  str+=	'	 <button class="btn btn-danger btn-sm" onclick="fnCateDel(\'' + qIDX + '\')">삭제하기</button>';
					  str+= '  </div>';
					}
					str+= '</div>';
					
					$("#divCateDetail").html(str);
					
					fnTopFrameResize();

				}else{
					alert("오류가 발생하였습니다. (571)");
				}
			}
		});

	}else{

		str = '<div class="x_panel" id="divCateDetail">';
		str+= '	<div class="page-header"><h5 id="container">분류 정보</h5></div>';
		str+= '분류를 선택해주세요.';
		str+= '</div>';		
		$("#divCateDetail").html(str);
		fnTopFrameResize();
	}
}

/*=============================================
	관리자모드 > 제품관리 > 리스트에서 가중치 변경하기
=============================================*/
tmpPweight=0;
function fnPweightMemory(v){
	tmpPweight=v;
}

function fnPweightUpdate(obj,PIDX){
	if(isNaN(obj.val()) || obj.val()=="" || obj.val()<0){
		if(!tmpPweight)tmpPweight=0;
		obj.val(tmpPweight);
		return;
	}
	
	if(tmpPweight==obj.val()){	//-- 값 변화 없으면 처리 안함
		return;
	}
	
	param="mode=Pweight&PIDX="+PIDX+"&Pweight="+obj.val();

	$.ajax({
		url:'./json/prdWeightUpdate.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				new PNotify({title: '가중치 변경 성공',text: '가중치 변경에 성공하였습니다.',type: 'success',delay:1000});
			}else{
				alert("오류가 발생하였습니다. (659)");
			}
		}
	});
	
}

/*=============================================
	관리자모드 > 제품관리 > 제조사 선택에 따른 브랜드 정보 셋팅하기
=============================================*/
function fnUpdateBrand(CIobjID,BRobjID,nBRIDX){
	CIobj = $("#"+CIobjID);
	BRobj = $("#"+BRobjID);

	BRobj.find("option").remove();
	BRobj.append("<option value=''>브랜드선택</option>");

	nCI = CIobj.val();
	param="CIIDX="+nCI;

	if(!nCI)return;

	$.ajax({
		url:'./json/brandList.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				len = data["length"];
				for(k=0;k<len;k++){
					d = data["data"][k];
					s="";
					if(nBRIDX==d["IDX"])s="selected";

					BRobj.append("<option value='" + d["IDX"] + "' " + s + ">" + d["name"] + "</option>");
				}

			}else{
				alert("오류가 발생하였습니다. (620)");
			}
		}
	});
}

/*=============================================
	관리자모드 > 제품관리 > 제품분류 순차 선택하기
=============================================*/
nCategoryDivObj = "";
function fnSetCategoryStep(lv){

	obj = nCategoryDivObj;

	//-- 선택된 카테고리 문자열 생성
	str="";
	for(k=1;k<=lv;k++){
		txt = obj.find("#inCATE"+k+" option:selected").text();
		if(txt){
			if(str)str+=" &gt; ";
			str+=txt;
		}
	}

	obj.find("#divCATEstr").html(str);

	if(lv>=5)return;

	//-- 이후 select 객체 날리기
	for(k=lv+1;k<=5;k++){
		obj.find("#inCATE"+k+" option").remove();
	}

	v="";
	if(lv>0)v = obj.find("#inCATE"+lv).val();
	
	grp = obj.find("#grp").val();

	param="mode=step&CTlevel="+lv+"&grp="+grp;
	if(v)param+="&CTIDX="+v;

	$.ajax({
		url:'/Product/json/categoryStep.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				len = data["length"];

				str = "";
				for(k=0;k<len;k++){
					d = data["data"][k];
					s="";
					str+="<option value='" + d["IDX"] + "'>" + d["name"] + "</option>";
				}

				tObj = obj.find("#inCATE"+(lv+1));


				tObj.find("option").remove();
				tObj.append(str);

			}else{
				alert("오류가 발생하였습니다. (683)");
			}
		}
	});
}


/*=============================================
	관리자모드 > 제품관리 > 제품분류 순차 초기화
=============================================*/
CateSelectObj1 = "";	//-- IDX 넣는 객체
CateSelectObj2 = "";	//-- 문자열 넣는 객체
function fnSetCategoryStepInit(modalWin,obj1,obj2,grp){
	CateSelectObj1 = $("#"+obj1);
	CateSelectObj2 = $("#"+obj2);
		
	CTIDX = CateSelectObj1.val();

	nCategoryDivObj	= $("#"+modalWin);
		
	obj = nCategoryDivObj;

	//-- INPUT 박스 제거 // 제품 검색결과 클리어
		obj.find("input[type='text']").val("");
		if(!grp || grp=="undefiled")grp="";
		nCategoryDivObj.find("#grp").val(grp);
	
		$("#prdSearchResult").html("<center>- 분류를 선택하거나 검색어를 입력하세요 -</center>");

	if(CTIDX && CTIDX>0){
		//-- 전체 select 객체 날리기
		for(k=1;k<=5;k++){
			obj.find("#inCATE"+k+" option").remove();
		}

		param="mode=all&CTIDX="+CTIDX+"&grp="+grp;

		$.ajax({
			url:'/Product/json/categoryStep.html',
			method : 'post',
			cache:false,
			data : param,
			dataType:"json",
			success:function(data){
				if(data["result"]=="OK"){

					for(k=0;k<5;k++){
						d = data["data"][k];
						len = d["length"];
						str="";
						for(j=0;j<len;j++){
							d2 = d["data"][j];
							s = "";
							if(d2["selected"])s="selected";
							str+="<option value='" + d2["IDX"] + "' " + s + ">" + d2["name"] + "</option>";
						}
						tObj = obj.find("#inCATE"+(k+1));
						tObj.find("option").remove();
						tObj.append(str);
					}

						//-- 선택된 카테고리 문자열 생성
						str="";
						for(k=1;k<=5;k++){
							txt = obj.find("#inCATE"+k+" option:selected").text();
							if(txt){
								if(str)str+=" &gt; ";
								str+=txt;
							}
						}
						obj.find("#divCATEstr").html(str);

				}else{
					alert("오류가 발생하였습니다. (748)");
				}
			}
		});
	}else{
		//-- 기본 호출
		fnSetCategoryStep(0);
	}
}

/*=============================================
	관리자모드 > 제품관리 > 제품분류 순차 선택완료
=============================================*/
function fnSetCategoryStepEnd(){
	obj = nCategoryDivObj;

	v = "";
	for(k=1;k<=5;k++){
		if(obj.find("#inCATE"+k+" option:selected").val()){
			v = obj.find("#inCATE"+k+" option:selected").val();
		}else{
			if(obj.find("#inCATE"+k+" option").length>0){
				//alert("마지막 분류까지 선택해주세요");
				//return;
			}
			break;
		}
	}

	if(v){
		CateSelectObj1.val(v);
		CateSelectObj2.val(obj.find("#divCATEstr").html().replaceAll("&gt;",">"));
	}else{
		CateSelectObj1.val("");
		CateSelectObj2.html("");
	}
	obj.find("#modalClose").click();
}

/*=============================================
	관리자모드 > 제품관리 > 옵션관리 기능
=============================================*/
//-- 옵션값 추가/수정 초기화
function fnOPTeditInit(){
	$("#inOPTname1").val("");
	$("#inOPTname2").val("");
	
	$("#optItemList tr").remove();
	$("#inOPTIDX").val("");
	fnOPTaddItem();	
	$('#optionModal').modal('show');
	
	//-- 단일형으로 기본 셋팅
	$("[name='inOPTtype']").eq(0).attr("checked",true);
	fnOPTsetType();
}

//-- 옵션 형태 선택
function fnOPTsetType(){		
	opType = $("[name='inOPTtype']:checked").val();
	opt2 = $(".opt2");
	if(opType==1){
		opt2.css("display","none");
		$(".opt2 input[type='text']").val("");
	}else{
		opt2.css("display","table-cell");
	}
}

//-- 옵션값 추가
function fnOPTaddItem(){
	opType = $("[name='inOPTtype']:checked").val();
	addStyle="";
	if(opType==1){
		addStyle="style='display:none;'";
	}
	str ='<tr>';
	str+='	<td><input type="text" class="form-control input-sm" placeholder="선택1" name="inOPTitem1" value=""></td>';
	str+='	<td class="opt2" ' + addStyle + '><input type="text" class="form-control input-sm" placeholder="선택2" name="inOPTitem2" value=""></td>';
	str+='	<td><input type="text" class="form-control input-sm" placeholder="추가금" name="inOPTprice" value=""></td>';
	str+='	<td class="txtC"><input type="button" class="btn btn-danger btn-xs" value="-" onclick="fnOPTdelItem($(this))" /></td>';
	str+='</tr>';
	$("#optItemList").append(str);
}

//-- 옵션값 삭제
function fnOPTdelItem(obj){
	obj.parent().parent().remove();
	len = $("#optItemList tr").length;
	if(!len)fnOPTaddItem();
}

//-- 옵션값 적용
function fnOPTset(){
	/*
	//-- 작성할 문자열
	단일선택시 
	{"opType":"1","name1":"","name2":"","opList":[{"name":"opName","item":[{"name":"",price:""},{"name":"",price:""},{"name":"",price:""}]}]}
	
	조합선택시
	{"opType":"2","name1":"","name2":"","opList":[{"name":"opName","item":[{"name":"","item":[{"name":"",price:""},{"name":"",price:""}]},{"name":"opName","item":[{"name":"","item":[{"name":"",price:""},{"name":"",price:""}]}]}	
	*/
			
	opType = $("[name='inOPTtype']:checked").val();
	
	opName1 = $("#inOPTname1").val();
	opName2 = $("#inOPTname2").val();
	if(!opName1){
		alert("옵션명1 을 입력해 주세요");
		$("#inOPTname1").focus();
		return;
	}
	
	if(opType==2 && !opName2){
		alert("옵션명2 를 입력해 주세요");
		$("#inOPTname2").focus();
		return;
	}	
	
	tr = $("#optItemList tr");
	len = tr.length;
	opInfo = new Array();	//-- Json 문자열 만들기 위한 배열
	itemViewStr = "";	//-- 보여주기 위한 문자열
	for(k=0;k<len;k++){	
		opRow = tr.eq(k);
		opText = opRow.find("td input[type='text']");
		
		opItem1 = opText.eq(0).val();
		opItem2 = opText.eq(1).val();
		opPrice = opText.eq(2).val();
		
		len1 = opInfo.length;
				
		
		//-- 추가금 미입력시 초기값 입력
		if(!opPrice){
			opPrice=0;
			opText.eq(2).val(0);
		}
		
		if(opType==1){
			//-- 단일선택형
			if(!opItem1){
				alert("선택항목을 입력해주세요.");
				opText.eq(0).focus();
				return;
			}
			
			/*
			opInfo[len1] = new Array();
			opInfo[len1]["name"] = opItem1;
			opInfo[len1]["price"] = opPrice;
			*/
			opInfo[len1] = {name:opItem1,price:opPrice}
			
			if(itemViewStr)itemViewStr+="\n";
			itemViewStr+=opItem1+"("+opPrice+")";
			
		}else if(opType==2){
			//-- 조합선택형
			if(!opItem1){
				alert("선택항목1 을 입력해주세요.");
				opText.eq(0).focus();
				return;
			}
			
			if(!opItem2){
				alert("선택항목2 을 입력해주세요.");
				opText.eq(1).focus();
				return;
			}
			
			//-- 기존 객체 찾기
			idx1 = -1;
			for(j=0;j<len1;j++){				
				if(opInfo[j]["name"]==opItem1){
					idx1 = j;
					break;
				}
			}
			
			if(idx1<0){
				//-- 새로운 그룹 추가
				idx1 = opInfo.length;
				opInfo[idx1] = new Array();
				opInfo[idx1] = {name:opItem1};
				opInfo[idx1]["item"] = new Array();
				opInfo[idx1]["item"][0] = {name:opItem2,price:opPrice}				
			}else{
				//-- 기존 그룹체 추가
				idx2 = opInfo[idx1]["item"].length;
				opInfo[idx1]["item"][idx2] = {name:opItem2,price:opPrice}
				itemViewStr+=opItem1+"("+opPrice+")";
			}
			
			if(itemViewStr)itemViewStr+="\n";
			itemViewStr+=opItem1+" / "+opItem2+"("+opPrice+")";
		}		
	}
	//-- 배열화 끝
	
	jsonStr = JSON.stringify(opInfo);
	
	//-- 옵션 방식, 옵션 명 붙이기
	jsonStr = '{"opType":"'+opType+'","name1":"'+opName1+'","name2":"'+opName2+'","item":'+jsonStr+'}';
	
	/*
	//-- 테스트
	t = JSON.parse(jsonStr);	
	alert(t["opType"]);
	*/
	
	IDX = $("#inOPTIDX").val();
	if(IDX){
		//-- 수정시
		obj = $("#optInfo .form-group").eq(IDX);
		if(opType==2)obj.find(".control-label").html(opName1 + "/" + opName2);
		else obj.find(".control-label").html(opName1);
		
		
		obj.find("[name='inPoptionStr[]']").val(itemViewStr);
		obj.find("[name='inPoption[]']").val(jsonStr);

	}else{
		//-- 신규 입력시
		str='		<div class="form-group">';
		str+='		<label class="control-label col-md-3 col-sm-3 col-xs-12">'+opName1;
		if(opType==2)str+='/'+opName2;
		str+='		</label>';
	  str+='  	<div class="col-md-6 col-sm-6 col-xs-12">';
	  str+='  		<textarea type="text" class="form-control h100px" placeholder="정보값" name="inPoptionStr[]" readonly>'+itemViewStr+'</textarea>';
	  str+='  		<input type="hidden" name="inPoption[]" value=\''+jsonStr+'\' readonly>';
	  str+='  	</div>';
	  str+='  	<div class="col-md-3 col-sm-3 col-xs-12">';
	  str+='    	<input type="button" value="수정" class="btn btn-primary btn-xs" onclick="fnOPTedit($(this))">';
	  str+='    	<input type="button" value="삭제" class="btn btn-danger btn-xs" onclick="fnOPTdelItem($(this))">';
	  str+='  	</div>';
	  str+='  </div>';
	  $("#optInfo").append(str);
	}
  $('#optionModal').modal('hide');
}

//-- Json 문자열로 옵션 객체 다시 셋팅
function fnOPTsetJson(jsonStr){
	
	//-- 작성할 문자열
	//{"name":"opName","item":[{"name":"",price:""},{"name":"",price:""},{"name":"",price:""}]}
	if(!jsonStr)return;
	
	t = JSON.parse(jsonStr);
	opGroup = t["option"];
	
	len1 = opGroup.length;
	
	//-- option 그룹만큼 for
	for(k=0;k<len1;k++){
		
		opInfo = opGroup[k];
		
		jsonStr = JSON.stringify(opInfo);
		
		opName1 = opInfo["name1"];
		opName2 = opInfo["name2"];
		opType	= opInfo["opType"];
		len2 = opInfo["item"].length;
		itemViewStr="";
		//-- 옵션 아이템 만큼 for
		for(j=0;j<len2;j++){
			
			opItem = opInfo["item"][j];
			
			
			if(opType != 2){
				opItem1 = opItem["name"];
				opPrice = opItem["price"];
				
				//-- 단일 선택형 셋팅
				if(itemViewStr)itemViewStr+="\n";
				itemViewStr+=opItem1+"("+opPrice+")";
			}else if(opType == 2){
				//-- 조합형 선택형 셋팅
				opItem1 = opItem["name"];				
				len3 = opItem["item"].length;
				
				
				for(i=0;i<len3;i++){
					opItem2 = opInfo["item"][j]["item"][i]["name"];
					opPrice = opInfo["item"][j]["item"][i]["price"];
					
					if(itemViewStr)itemViewStr+="\n";
					itemViewStr+=opItem1+" / "+opItem2+"("+opPrice+")";
				}				
			}	//-- end else if
		}//-- end for len2
		
		
		str='		<div class="form-group">';
		str+='		<label class="control-label col-md-3 col-sm-3 col-xs-12">'+opName1;
		if(opType==2)str+='/'+opName2;
		str+='</label>';
	  str+='  	<div class="col-md-6 col-sm-6 col-xs-12">';
	  str+='  		<textarea type="text" class="form-control h100px" placeholder="정보값" name="inPoptionStr[]" readonly>'+itemViewStr+'</textarea>';
	  str+='  		<input type="hidden" name="inPoption[]" value=\''+jsonStr+'\' readonly>';
	  str+='  	</div>';
	  str+='  	<div class="col-md-3 col-sm-3 col-xs-12">';
	  str+='    	<input type="button" value="수정" class="btn btn-primary btn-xs" onclick="fnOPTedit($(this))">';
	  str+='    	<input type="button" value="삭제" class="btn btn-danger btn-xs" onclick="fnOPTdelItem($(this))">';
	  str+='  	</div>';
	  str+='  </div>';
	  $("#optInfo").append(str);
		
		
		
	}//-- end for len1
}

//-- 옵션값 수정을 위해 다시 셋팅
function fnOPTedit(obj){
	
	p = obj.parent().parent();
	jsonStr = p.find("[name='inPoption[]']").val();
	fnOPTeditInit();

	//-- 옵션 IDX 구하기
	IDX = $("#optInfo .form-group").index(p);

	$("#inOPTIDX").val(IDX);
	
	opInfo = JSON.parse(jsonStr);
	
	//-- 모든 줄 삭제
	$("#optItemList tr").remove();
		
	if(opInfo["opType"] != 2){
		//-- 단일 선택형 셋팅
		$("[name='inOPTtype']").eq(0).attr("checked",true);
		fnOPTsetType();
		$("#inOPTname1").val(opInfo["name1"]);
		
		len1 = opInfo["item"].length;
		for(k=0;k<len1;k++){
			info = opInfo["item"][k];
			str ='<tr>';
			str+='	<td><input type="text" class="form-control input-sm" placeholder="선택1" name="inOPTitem1" value="' + info["name"] + '"></td>';
			str+='	<td class="opt2" style="display:none;"><input type="text" class="form-control input-sm" placeholder="선택2" name="inOPTitem2" value=""></td>';
			str+='	<td><input type="text" class="form-control input-sm" placeholder="추가금" name="inOPTprice" value="' + info["price"] + '"></td>';
			str+='	<td class="txtC"><input type="button" class="btn btn-danger btn-xs" value="-" onclick="fnOPTdelItem($(this))" /></td>';
			str+='</tr>';
			$("#optItemList").append(str);
		}
		
		
	}else if(opInfo["opType"] == 2){
		//-- 조합형 선택형 셋팅
		$("[name='inOPTtype']").eq(1).attr("checked",true);
		fnOPTsetType();
		$("#inOPTname1").val(opInfo["name1"]);		
		$("#inOPTname2").val(opInfo["name2"]);
		
		len1 = opInfo["item"].length;
		
		for(k=0;k<len1;k++){
			info = opInfo["item"][k];
			name1 = info["name"];
			len2 = info["item"].length;
			
			for(j=0;j<len2;j++){
				info2 = info["item"][j];
				name2 = info2["name"];
				price = info2["price"];
				
				str ='<tr>';
				str+='	<td><input type="text" class="form-control input-sm" placeholder="선택1" name="inOPTitem1" value="' + name1 + '"></td>';
				str+='	<td class="opt2"><input type="text" class="form-control input-sm" placeholder="선택2" name="inOPTitem2" value="' + name2 + '"></td>';
				str+='	<td><input type="text" class="form-control input-sm" placeholder="추가금" name="inOPTprice" value="' + price + '"></td>';
				str+='	<td class="txtC"><input type="button" class="btn btn-danger btn-xs" value="-" onclick="fnOPTdelItem($(this))" /></td>';
				str+='</tr>';
				$("#optItemList").append(str);
			}//-- end for
		}//-- end for
		
	}	//-- end else if
}




/* 기존 옵션 기능 임시 삭제
//-- 옵션값 추가
function fnOPTaddItem(){	
	str ='<div class="form-group">';
 	str+='	<div class="control-label col-md-3 col-sm-3 col-xs-12">옵션값 <input type="button"class="btn btn-danger btn-xs" value="-" onclick="fnOPTdelItem($(this))" tabindex=-1 /> </div>';
  str+='  <div class="col-md-5 col-sm-5 col-xs-6">';
  str+='      <input type="text" class="form-control" placeholder="옵션값" name="inOPTitem" value="">';
  str+='  </div>';
  str+='  <div class="col-md-4 col-sm-4 col-xs-6">';
  str+='  	<div class="input-group">';
	str+='		  <input type="text" class="form-control" placeholder="추가금" name="inOPTprice" value="">';
	str+='		  <span class="input-group-addon" id="sizing-addon2">원</span>';
	str+='		</div>';
  str+='  </div>';
  str+='</div>';
	$("#OPTgroup").append(str);
}

//-- 옵션값 삭제
function fnOPTdelItem(obj){
	obj.parent().parent().remove();
	len = $("#OPTgroup .form-group").length;
	if(!len)fnOPTaddItem();
}

//-- 옵션값 적용
function fnOPTset(){
	//-- 작성할 문자열
	//{"name":"opName","item":[{"name":"",price:""},{"name":"",price:""},{"name":"",price:""}]}

	optName = $("#inOPTname").val();
	if(!optName){
		alert("옵션명을 입력해주세요");
		$("#inOPTname").focus();
		return;
	}

	optItems = $("#OPTgroup .form-group");
	len = optItems.length;

	itemJsonStr = "";
	itemViewStr = "";
	for(k=0;k<len;k++){
		opt = optItems.eq(k);

		v1 = opt.find("[name='inOPTitem']").val();
		v2 = opt.find("[name='inOPTprice']").val();

		if(!v1){
			alert("옵션값을 입력해주세요");
			opt.find("[name='inOPTitem']").focus();
			return;
		}
		if(!v2)v2=0;

		//-- Json Data 처리용
		if(itemJsonStr)itemJsonStr+=",";
		itemJsonStr+='{"name":"'+v1+'","price":"'+v2+'"}';

		//-- 보여주기용
		if(itemViewStr)itemViewStr+=",";
		itemViewStr+=v1+"("+v2+")";
	}

	jsonStr = '{"name":"'+optName+'","item":[' + itemJsonStr + ']}';

	IDX = $("#inOPTIDX").val();
	if(IDX){
		obj = $("#optInfo .form-group").eq(IDX);

		obj.find(".control-label").html(optName);
		obj.find("[name='inPoptionStr[]']").val(itemViewStr);
		obj.find("[name='inPoption[]']").val(jsonStr);

	}else{
		str='		<div class="form-group">';
		str+='		<label class="control-label col-md-3 col-sm-3 col-xs-12">'+optName+'</label>';
	  str+='  	<div class="col-md-6 col-sm-6 col-xs-12">';
	  str+='  		<input type="text" class="form-control" placeholder="정보값" name="inPoptionStr[]" value="'+itemViewStr+'" readonly>';
	  str+='  		<input type="hidden" name="inPoption[]" value=\''+jsonStr+'\' readonly>';
	  str+='  	</div>';
	  str+='  	<div class="col-md-3 col-sm-3 col-xs-12">';
	  str+='    	<input type="button" value="수정" class="btn btn-primary btn-xs" onclick="fnOPTedit($(this))">';
	  str+='    	<input type="button" value="삭제" class="btn btn-danger btn-xs" onclick="fnOPTdelItem($(this))">';
	  str+='  	</div>';
	  str+='  </div>';
	  $("#optInfo").append(str);
	}
  $('#optionModal').modal('hide');
}

//-- Json 문자열로 옵션 객체 셋팅
function fnOPTsetJson(jsonStr){
	//-- 작성할 문자열
	//{"name":"opName","item":[{"name":"",price:""},{"name":"",price:""},{"name":"",price:""}]}
	if(!jsonStr)return;

	t = JSON.parse(jsonStr);
	opInfo = t["option"];
	len = opInfo.length;
	for(k=0;k<len;k++){
		d = opInfo[k];

		optName = d["name"];

		itemLen = d["item"].length;

		itemJsonStr = "";
		itemViewStr = "";
		for(j=0;j<itemLen;j++){
			itm = d["item"][j];
			v1 = itm["name"];
			v2 = itm["price"];
			if(!v2)v2=0;
			//-- Json Data 처리용
			if(itemJsonStr)itemJsonStr+=",";
			itemJsonStr+='{"name":"'+v1+'","price":"'+v2+'"}';

			//-- 보여주기용
			if(itemViewStr)itemViewStr+="\n";
			itemViewStr+=v1+"("+v2+")";
		}

		jsonStr = '{"name":"'+optName+'","item":[' + itemJsonStr + ']}';
		str='		<div class="form-group">';
		str+='		<label class="control-label col-md-3 col-sm-3 col-xs-12">'+optName+'</label>';
	  str+='  	<div class="col-md-6 col-sm-6 col-xs-12">';
	  str+='  		<textarea type="text" class="form-control h100px" placeholder="정보값" name="inPoptionStr[]" readonly>'+itemViewStr+'</textarea>';
	  str+='  		<input type="hidden" name="inPoption[]" value=\''+jsonStr+'\' readonly>';
	  str+='  	</div>';
	  str+='  	<div class="col-md-3 col-sm-3 col-xs-12">';
	  str+='    	<input type="button" value="수정" class="btn btn-primary btn-xs" onclick="fnOPTedit($(this))">';
	  str+='    	<input type="button" value="삭제" class="btn btn-danger btn-xs" onclick="fnOPTdelItem($(this))">';
	  str+='  	</div>';
	  str+='  </div>';
	  $("#optInfo").append(str);
	}
}

//-- 옵션값 수정을 위해 다시 셋팅
function fnOPTedit(obj){
	p = obj.parent().parent();
	jsonStr = p.find("[name='inPoption[]']").val();
	fnOPTeditInit();

	//-- 옵션 IDX 구하기
	IDX = $("#optInfo .form-group").index(p);

	$("#inOPTIDX").val(IDX);

	opInfo = JSON.parse(jsonStr);

	$("#inOPTname").val(opInfo["name"]);

	opItem = opInfo["item"];
	opLen = opItem.length;

	$("#OPTgroup .form-group").remove();

	for(k=0;k<opLen;k++){
		op = opItem[k];
		str ='<div class="form-group">';
	 	str+='	<div class="control-label col-md-3 col-sm-3 col-xs-12">옵션값 <button type="button" class="btn btn-danger btn-xs" value="-" onclick="fnOPTdelItem($(this))">-</button></div>';
	  str+='  <div class="col-md-5 col-sm-5 col-xs-6">';
	  str+='      <input type="text" class="form-control" placeholder="옵션값" name="inOPTitem" value="' + op["name"] + '">';
	  str+='  </div>';
	  str+='  <div class="col-md-4 col-sm-4 col-xs-6">';
	  str+='  	<div class="input-group">';
		str+='		  <input type="text" class="form-control" placeholder="추가금" name="inOPTprice" value="' + op["price"] + '">';
		str+='		  <span class="input-group-addon" id="sizing-addon2">원</span>';
		str+='		</div>';
	  str+='  </div>';
	  str+='</div>';
		$("#OPTgroup").append(str);
	}
}
*/

/*=============================================
	관리자모드 > 제품관리 > 휴드폰 요금제 정보
=============================================*/
tempPT="";
function fnPhoneTelecomSave(){
	tempPT = $("#inPTIDX").val();	
}

function fnPhonePayListLoad(){
	
	//-- 기존 요금제 설정 검사
	tr = $("#TBLphonePayList tr");
	if(tr.length>0){
		if(!confirm("기존 설정한 요금제가 존재합니다.\n\n통신사 변경시 기설정 요금제는 초기화됩니다.\n\n진행하시겠습니까?")){
			$("#inPTIDX").val(tempPT);
			return;
		}
	}
	$("#TBLphonePayList").html("");
	
	PT = $("#inPTIDX");	
	opObj = $("#inPphonePayList");
	opObj.find("option").remove();
	opObj.html("<option value=''>요금제선택</option>");
	if(!PT.val()){
		return;
	}
	
	//-- 해당 통신사의 요금제 가져오기
	param="PTIDX="+PT.val();
	$.ajax({
		url:'./json/telecomPayList.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				len = data["length"];
				str="";
				for(k=0;k<len;k++){
					d = data["data"][k];
					str+="<option value='"+d["IDX"]+"##"+d["PPname"]+"##"+d["PPprice"]+"'>" + d["PPname"] + "</option>";
				}
				opObj.append(str);
			}else{
				alert("요금제를 불러오는데 실패하였습니다.");
			}
		}
	});
}

//-- 추가하기 버튼 클릭시 모달창 초기화
function fnPhonePayInit(){
	PT = $("#inPTIDX");
	if(!PT.val()){
		alert("통신사를 선택해주세요");
		PT.focus();
		return;
	}
	
	$("#inPPIDX").val("");
	$("#inPphonePayList").val("");
	$("#inPphonePaySupport").val(0);
	$("#inPphonePayPrice").html("");
	
	$("#phonePayModal").modal("show");
}

//-- 모달창에서 셀렉트 버튼 선택시
function fnPhonePaySelect(){
	$("#inPphonePayPrice").html("");
	if(!$("#inPphonePayList").val())return;
	v = $("#inPphonePayList").val().split("##");	
	$("#inPphonePayPrice").html("월 " + fnCommify(v[2]) + " 원");	
}

//-- 모달창에서 적용하기 클릭시
function fnPhonePaySet(){
	v1 = $("#inPphonePayList").val();
	v2 = $("#inPphonePaySupport").val();
	
	if(!v1){
		alert("요금제를 선택해주세요");
		$("#inPphonePayList").focus();
		return;
	}
	
	if(v2=="")v2=0;
	
	v1 = v1.split("##");
	
	jsonStr = '{"PPIDX":"'+v1[0]+'","name":"'+v1[1]+'","price":"'+v1[2]+'","support":"'+v2+'"}';
	
	IDX = $("#inPPIDX").val();			
	
	tbl = $("#TBLphonePayList");
	tr = tbl.find("tr");
	len = tr.length;
	
	//-- 중복검사
	for(k=0;k<len;k++){
		if(IDX!="" && k==IDX)continue;
		row = tr.eq(k);
		PPIDX = row.find("span").html();
		if(PPIDX == v[0]){
			alert("이미 등록된 요금제입니다.");
			return;
		}
	}

	if(IDX){
		//-- 수정
		td = tr.eq(IDX).find("td");
		td.eq(0).html(v1[1]);
		td.eq(1).html(fnCommify(v1[2]));
		td.eq(2).html(fnCommify(v2));
		td.eq(3).find("span").html(v1[0]);
		td.eq(3).find("input[type='hidden']").val(jsonStr);
	}else{
		//-- 추가
		str ='<tr>';
		str+='	<td>'+v1[1]+'</td>';
		str+='	<td>'+fnCommify(v1[2])+'</td>';
		str+='	<td>'+fnCommify(v2)+'</td>';
		str+='	<td>';
		str+='		<input type="button" value="수정" class="btn btn-primary btn-xs" onclick="fnPhonePayEdit($(this))">';
	  str+='  	<input type="button" value="삭제" class="btn btn-danger btn-xs" onclick="fnPhonePaydelItem($(this))">';
	  str+='  	<span class="hiddenObj">'+v1[0]+'</span>';
	  str+='  	<input type="hidden" name="inPphonePayInfo[]" value=\''+jsonStr+'\' />';
		str+='	</td>';
		str+='</tr>';
		tbl.append(str);
	}
	
	$("#phonePayModal").modal("hide");
	fnTopFrameResize();
}

//-- 요금제 수정
function fnPhonePayEdit(obj){
	tr = obj.parent().parent();
		
	jsonStr = tr.find("input[type='hidden']").val();
	//-- 옵션 IDX 구하기
	IDX = $("#TBLphonePayList tr").index(tr);
	$("#inPPIDX").val(IDX);
	
	pInfo = JSON.parse(jsonStr);
	
	$("#inPphonePayList").val(pInfo["PPIDX"]+"##"+pInfo["name"]+"##"+pInfo["price"]);
	$("#inPphonePayPrice").html("월 " + fnCommify(pInfo["price"]) + " 원");	
	$("#inPphonePaySupport").val(pInfo["support"]);
	$("#phonePayModal").modal("show");
}

//-- 요금제 삭제
function fnPhonePaydelItem(obj){	
	obj.parent().parent().remove();
}

//-- 요금제 다시 셋팅
function fnPhonePaySetJson(jsonStr){
	if(!jsonStr)return;

	t = JSON.parse(jsonStr);
	opInfo = t["priceType"];
	len = opInfo.length;
	
	tbl = $("#TBLphonePayList");	
	for(k=0;k<len;k++){
		d = opInfo[k];
		jsonStr = '{"PPIDX":"'+d["PPIDX"]+'","name":"'+d["name"]+'","price":"'+d["price"]+'","support":"'+d["support"]+'"}';
		str ='<tr>';
		str+='	<td>'+d["name"]+'</td>';
		str+='	<td>'+fnCommify(d["price"])+'</td>';
		str+='	<td>'+fnCommify(d["support"])+'</td>';
		str+='	<td>';
		str+='		<input type="button" value="수정" class="btn btn-primary btn-xs" onclick="fnPhonePayEdit($(this))">';
	  str+='  	<input type="button" value="삭제" class="btn btn-danger btn-xs" onclick="fnPhonePaydelItem($(this))">';
	  str+='  	<span class="hiddenObj">'+d["PPIDX"]+'</span>';
	  str+='  	<input type="hidden" name="inPphonePayInfo[]" value=\''+jsonStr+'\' />';
		str+='	</td>';
		str+='</tr>';
		tbl.append(str);
	}
	fnTopFrameResize();
}

/*=============================================
	관리자모드 > 제품관리 > 추가정보 기본세트 설정하기
=============================================*/
function fnPrdAddInfoSet(m){
	
	//-- 기존 값이 있는지 체크
	addInfo = $("#addInfoWrap input[type='text']");
	len = addInfo.length;
	
	for(k=0;k<len;k++){
		v = addInfo.eq(k).val();
		if(v)break;
	}
	
	if(v){
		if(!confirm("이미 입력된 내용이 존재합니다.\n\n계속 진행시 기존 내용은 삭제됩니다.\n\n계속 진행하시겠습니까?")){
			return;
		}
	}
	
	for(k=0;k<len;k++){addInfo.eq(k).val("");}

	if(m=="1"){	//-- 정수기
		addInfo.eq(0).val("정수방식");
		addInfo.eq(2).val("필터");
		addInfo.eq(4).val("용량");
		addInfo.eq(6).val("사이즈");
		addInfo.eq(8).val("색상");
		addInfo.eq(10).val("기능");
		addInfo.eq(12).val("방문주기");
		addInfo.eq(14).val("정수기 형태");
		addInfo.eq(16).val("");
		addInfo.eq(18).val("");
	}else if(m=="2"){	//--	공기청정기
		addInfo.eq(0).val("사용면적");
		addInfo.eq(2).val("정화단계");
		addInfo.eq(4).val("필터");
		addInfo.eq(6).val("기능");
		addInfo.eq(8).val("색상");
		addInfo.eq(10).val("사이즈");
		addInfo.eq(12).val("소비전력");
		addInfo.eq(14).val("에너지소비효율등급");
		addInfo.eq(16).val("");
		addInfo.eq(18).val("");
	}else if(m=="3"){	//-- 비데
		addInfo.eq(0).val("제품 크기");
		addInfo.eq(2).val("제품 중량");
		addInfo.eq(4).val("정수방식");
		addInfo.eq(6).val("색상");
		addInfo.eq(8).val("기능");
		addInfo.eq(10).val("정격전압");
		addInfo.eq(12).val("소비전력");
		addInfo.eq(14).val("방문주기");
		addInfo.eq(16).val("");
		addInfo.eq(18).val("");
	}else if(m=="4"){	//-- 안마의자
		addInfo.eq(0).val("제품 크기");
		addInfo.eq(2).val("제품 중량");
		addInfo.eq(4).val("정격전압");
		addInfo.eq(6).val("소비전력");
		addInfo.eq(8).val("기능");
		addInfo.eq(10).val("색상");
		addInfo.eq(12).val("제품외피");
		addInfo.eq(14).val("");
		addInfo.eq(16).val("");
		addInfo.eq(18).val("");
	}else if(m=="9"){	//-- 기본
		addInfo.eq(0).val("제품 크기");
		addInfo.eq(2).val("제품 중량");
		addInfo.eq(4).val("색상");
		addInfo.eq(6).val("기능");
		addInfo.eq(8).val("");
		addInfo.eq(10).val("");
		addInfo.eq(12).val("");
		addInfo.eq(14).val("");
		addInfo.eq(16).val("");
		addInfo.eq(18).val("");
	}
}


/*=============================================
	관리자모드 > 제품관리 > 제품관리 > 상태업데이트
=============================================*/
function fnPrdStateUpdate(PIDX,ST){
	param="mode=Pstate&PIDX="+PIDX+"&inPstate="+ST;
	$.ajax({
		url:'./json/prdStateUpdate.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				new PNotify({title: '데이터 저장 성공',text: '데이터 저장에 성공하였습니다.',type: 'success',delay:1000});
			}else{
				new PNotify({title: '처리실패',text: '오류가 발생하여 처리에 실패하였습니다. (1035)',type: 'danger',delay:1000});
			}
		}
	});
}


/*=============================================
	관리자모드 > 제품관리 > 제품관리 > 상세페이지 형식에 따른 추가 정보 보이고/숨기기
=============================================*/
function fnPrdSetViewType(v){
	info1 = $("#phoneInfo1");
	info2 = $("#phoneInfo2");
	
	btn = $("#viewTypeBtn .btn");
	btn.removeClass("btn-default").removeClass("btn-info");
	
	if(v=="CM"){
		info1.slideUp(500,function(){fnTopFrameResize();});
		info2.slideUp(500);
		
		btn.eq(0).addClass("btn-info");
		btn.eq(1).addClass("btn-default");
		
	}else if(v=="PH"){
		info1.slideDown(500,function(){fnTopFrameResize();});
		info2.slideDown(500);
		
		btn.eq(0).addClass("btn-default");
		btn.eq(1).addClass("btn-info");
	}
	
}

/*=============================================
	관리자모드 > 제품관리 > 외부연동 > 사이트 연동에 따른 효과 처리
=============================================*/
function fnPrdExSiteSet(){
	obj = $("#siteCheck input[type='checkbox']");
	len = obj.length;
	for(k=0;k<len;k++){
		chk = obj.eq(k).attr("checked");
		v = obj.eq(k).val();
		infoBox = $("#info"+v+" .x_content");
		if(chk=="checked"){
			infoBox.slideDown(500,function(){fnTopFrameResize()});
		}else{
			infoBox.slideUp(500,function(){fnTopFrameResize()});
			
			//-- 내용 초기화
			infoBox.find("input[type='checkbox']").eq(2).attr("checked","checked");
			infoBox.find("input[type='text']").val("");
			
		}
	}
}

/*=============================================
	관리자모드 > 제품관리 > 사이트연동 / 외부연동 > 상태업데이트
=============================================*/
function fnPrdExStateUpdate(PEIDX,ST){
	param="mode=PEstate&PEIDX="+PEIDX+"&inPEstate="+ST;
	$.ajax({
		url:'./json/prdStateUpdate.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				new PNotify({title: '데이터 저장 성공',text: '데이터 저장에 성공하였습니다.',type: 'success',delay:1000});
			}else{
				new PNotify({title: '처리실패',text: '오류가 발생하여 처리에 실패하였습니다. (1035)',type: 'danger',delay:1000});
			}
		}
	});
}


/*=============================================
	관리자모드 > 제품관리 > 제품관리 > 제품상세 > 제품 순위 체크
=============================================*/
function fnPrdNaverShopRefresh(PIDX){

	if(!$("#inPnaverPrdCode").val()){
		alert("지식쇼핑 상품코드가 없습니다.");
		return;
	}

	$("#updateBtn").css("display","none");
	$("#updateStr").css("display","inline");
	urlPath = "http://tools.rcommall.com/Shop/shop.html";
	param="PIDX="+PIDX+"&PnaverPrdCode="+$("#inPnaverPrdCode").val();

	$("#NrankList div").html("확인중");

	$.ajax({
			url:urlPath,
			type:"POST",
			cache:false,
			cookies:false,
			crossDomain: true,
			data : param,
			dataType:"jsonp",
			jsonp : "fnPrdNaverShopRefreshCallBack"
		});
}

function fnPrdNaverShopRefreshCallBack(obj){
	//resultTxt = JSON.stringify(obj);

	if(obj["result"]=="OK"){
		len = obj["length"];
		$("#NrankList div").html("순위권밖");
		for(k=0;k<len;k++){
			d = obj["data"][k];
			if(d["rank"]>0)$("#Nrank"+d["SIIDX"]).html("<font color=blue>" + d["rank"] + " 위</font>");
		}

	}else if(obj["result"]=="PIDXEMPTY"){
		alert("제품 고유번호가 존재하지 않습니다.");
		$("#NrankList div").html("<font color=red>오류</font>");
	}

	$("#updateBtn").css("display","inline");
	$("#updateStr").css("display","none");
}

/*=============================================
	관리자모드 > 제품관리 > 제품관리 > 제품상세 > 지식쇼핑 바로가기
=============================================*/
function fnPrdNaverShopGo(){
	v = $("#inPnaverPrdCode").val();
	if(!v){
		alert("지식쇼핑 상품코드가 없습니다.");
		return;
	}
	window.open("http://shopping.naver.com/detail/detail.nhn?nv_mid="+v,"_blank");
}


/*=============================================
	관리자모드 > 제품관리 > 외부연동 > 관리번호 재발급
=============================================*/
function fnPrdNumRemake(flag1,flag2,SIIDX){
		
	if(flag1=="N")siteName = "네이버";
	else if(flag1=="D")siteName = "다음";
	else{
		alert("오류!");
		return;
	}
	
	IDXS="";
	if(flag2=="select"){
		chkObj = $("[name='table_records']:checked");
		if(!chkObj.length){
			alert("재발급할 항목을 선택하여 주십시오");
			return;
		}
		//-- 문자열 생성
		len = chkObj.length;
		
		for(k=0;k<len;k++){
			if(IDXS)IDXS+=",";
			IDXS+=chkObj.eq(k).val();
		}
		
		lenStr = len+"개";
	}else{
		IDXS="all";
		lenStr = "현재사이트 전체";
	}
	
	if(!confirm("관리번호를 재발급받으시겠습니까?\n\n대상사이트 : " + siteName + "\n\n대상정보 : " + lenStr)){
		return;	
	}

	param="PEIDX="+IDXS + "&SIIDX="+SIIDX+"&flag1="+flag1+"&flag2="+flag2;

	$.ajax({
		url:'./json/prdNumRemake.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				document.location.reload();
			}else{
				new PNotify({title: '처리실패',text: '오류가 발생하여 처리에 실패하였습니다. (1070)',type: 'danger',delay:1000});
			}
		}
	});
}

/*=============================================
	관리자모드 > 제품관리 > 외부연동 > 지식쇼핑 바로가기
=============================================*/
function fnPrdNaverShopGoDirect(code){
	if(!code){
		alert("지식쇼핑 상품코드가 없습니다.");
		return;
	}
	window.open("http://shopping.naver.com/detail/detail.nhn?nv_mid="+code,"_blank");
}

/*=============================================
	관리자모드 > 제품관리 > 외부연동 > 단일 제품순위 확인
=============================================*/
function fnPrdNaverShopRefreshList(PIDX,NprdCode){
	if(!PIDX){
		alert("고유번호를 확인해주세요.");
		return;
	}
	
	if(!NprdCode){
		alert("네이버쇼핑 제품 코드가 존재하지 않습니다.");
		return;
	}
	
	urlPath = "http://tools.rcommall.com/Shop/shop.html";
	param="PIDX="+PIDX+"&mode=List&PnaverPrdCode="+NprdCode;
	$("#tdPERrankTime"+PIDX).html("확인중");
	$(".btnRefresh").attr("disabled",true);
	
	$.ajax({
			url:urlPath,
			type:"POST",
			cache:false,
			cookies:false,
			crossDomain: true,
			data : param,
			dataType:"jsonp",
			jsonp : "fnPrdNaverShopRefreshCallBackList"
		});
}

function fnPrdNaverShopRefreshCallBackList(obj){
	//resultTxt = JSON.stringify(obj);
	if(obj["result"]=="OK"){
		len = obj["length"];		
		for(k=0;k<len;k++){
			d = obj["data"][k];
			if($("#inSIIDX").val()==d["SIIDX"]){
				rank = d["rank"];
				chkTime = obj["chkItme"];
				PIDX  = obj["PIDX"];
				
				if(rank==0)rank="<font color=red>없음</font>";
				$("#tdPERrank"+PIDX).html(rank);
				$("#tdPERrankTime"+PIDX).html(chkTime);
				$(".btnRefresh").attr("disabled",false);
				return;
			}
		}
		
		alert("업데이트에 실패하였습니다.(1)");
		$("#tdPERrankTime"+PIDX).html('업데이트 실패');
		$(".btnRefresh").attr("disabled",false);

	}else if(obj["result"]=="PIDXEMPTY"){
		alert("제품 고유번호가 존재하지 않습니다.");
		$("#tdPERrankTime"+PIDX).html('업데이트 실패');
		$(".btnRefresh").attr("disabled",false);
	}else{
		
		alert("업데이트에 실패하였습니다.(2)\n" + obj["result"]);
		$("#tdPERrankTime"+PIDX).html('업데이트 실패');
		$(".btnRefresh").attr("disabled",false);
	}
	
}

/*=============================================
	관리자모드 > 제품관리 > 외부연동 > 단일 관리번호 재발급
=============================================*/
function fnPrdNumRemakeList(PEIDX,flag1,SIIDX){
	if(!PEIDX){
		alert("고유번호를 확인해주세요.");
		return;
	}
	
	if(flag1=="N")siteName = "네이버";
	else if(flag1=="D")siteName = "다음";
	else{
		alert("오류!");
		return;
	}
	
	if(!confirm("관리번호를 재발급받으시겠습니까?\n\n대상사이트 : " + siteName)){
		return;	
	}
	
	param="PEIDX="+PEIDX + "&SIIDX="+SIIDX+"&flag1="+flag1;
	$.ajax({
		url:'./json/prdNumRemake.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				document.location.reload();
			}else{
				new PNotify({title: '처리실패',text: '오류가 발생하여 처리에 실패하였습니다. (1070)',type: 'danger',delay:1000});
			}
		}
	});
}

/*=============================================
	관리자모드 > 주문관리 > 상담요청 > 상태업데이트
=============================================*/
function fnPrdReqUpdate(PQIDX,ST){
	param="PQIDX="+PQIDX+"&inPQstate="+ST;
	$.ajax({
		url:'./json/prdReqUpdate.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				new PNotify({title: '데이터 저장 성공',text: '데이터 저장에 성공하였습니다.',type: 'success',delay:1000});
			}else{
				new PNotify({title: '처리실패',text: '오류가 발생하여 처리에 실패하였습니다. (1147)',type: 'danger',delay:1000});
			}
		}
	});
}

/*=============================================
	전화번호 입력양식 검사 및 하이폰 셋팅
=============================================*/
function fnTelSet(obj){
	v = obj.val();
	t = v.split("-");

	if(isNaN(v.replaceAll("-",""))){
		alert("잘못된 전화번호 형식입니다.");
		obj.val("");
		return false;
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
	return true;
}

/*=============================================
	아이디 중복 체크
=============================================*/
var MIDchk=false;
function fnMIDcheck(){
	MIDchk=false;
	rsObj = $("#idCheckResult");
	v = $("#inMID").val();
	if(!v){
		rsObj.html("<font color=red>아이디를 입력해주세요</font>");
		return;
	}

	if(v.indexOf(" ")>=0){
		rsObj.html("<font color=red>공백은 사용하실 수 없습니다.</font>");
		return;
	}

	param="inMID="+v;
	$.ajax({
		url:'/inc/MIDcheck.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				MIDchk=true;
				rsObj.html("<font color=blue>사용가능한 아이디입니다.</font>");
			}else if(data["result"]=="LENGTH"){
				rsObj.html("<font color=red>4자~12자 사이로 입력해주세요.</font>");
			}else if(data["result"]=="CHAR"){
				rsObj.html("<font color=red>영문소문자 및 숫자만 이용하실 수 있습니다.</font>");
			}else if(data["result"]=="FIRSTCHAR"){
				rsObj.html("<font color=red>첫글자는 반드시 영문자여야합니다.</font>");
			}else if(data["result"]=="USED"){
				rsObj.html("<font color=red>이미 사용된 아이디 입니다.</font>");
			}

			if(MIDchk==true){
				$("button[type='submit']").attr("disabled",false);
				$("button[type='submit']").html("저장");
			}else{
				$("button[type='submit']").attr("disabled",true);
				$("button[type='submit']").html("아이디검사 필요");
			}

		}
	});
}

function fnMIDcheckReset(){
	MIDchk=false;
	rsObj = $("#idCheckResult");
	rsObj.html("중복검사를 해주세요");
	$("button[type='submit']").attr("disabled",true);
	$("button[type='submit']").html("아이디검사 필요");
}



/*=======================================================================
	우편번호 검색 (다음 API 연동)
=======================================================================*/
	 function fnPostcodeFind(objCode){

		obj1 = $("#"+objCode+"post");
		obj2 = $("#"+objCode+"addr1");
		obj3 = $("#"+objCode+"addr2");

		p = obj1.parent();
		if(!$("#" + objCode + "postWrap").html()){
			str = '<div id="' + objCode + 'postWrap" style="display:none;border:1px solid;z-index:999;width:100%;max-width:400px;height:460px;margin:10px 0px;overflow:hidden;-webkit-overflow-scrolling:touch;background-color:#fff;">';
			str+='<img src="//i1.daumcdn.net/localimg/localimages/07/postcode/320/close.png" id="btnCloseLayer" style="cursor:pointer;position:relative;float:right;right:-3px;top:-3px;z-index:1;" onclick="$(\'#' + objCode + 'postWrap\').remove();fnTopFrameResize();"  alt="닫기 버튼">';
			str+='</div>';
			p.parent().append(str);
		}

		postWin = document.getElementById(objCode + 'postWrap');

		var currentScroll = Math.max(document.body.scrollTop, document.documentElement.scrollTop);
		new daum.Postcode({
           oncomplete: function(data) {
               // 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분.

               // 각 주소의 노출 규칙에 따라 주소를 조합한다.
               // 내려오는 변수가 값이 없는 경우엔 공백('')값을 가지므로, 이를 참고하여 분기 한다.
               var fullAddr = data.address; // 최종 주소 변수
               var extraAddr = ''; // 조합형 주소 변수

               // 기본 주소가 도로명 타입일때 조합한다.
               if(data.addressType === 'R'){
                   //법정동명이 있을 경우 추가한다.
                   if(data.bname !== ''){
                       extraAddr += data.bname;
                   }
                   // 건물명이 있을 경우 추가한다.
                   if(data.buildingName !== ''){
                       extraAddr += (extraAddr !== '' ? ', ' + data.buildingName : data.buildingName);
                   }
                   // 조합형주소의 유무에 따라 양쪽에 괄호를 추가하여 최종 주소를 만든다.
                   fullAddr += (extraAddr !== '' ? ' ('+ extraAddr +')' : '');
               }

               obj1 = $("#"+objCode+"post");
							 obj2 = $("#"+objCode+"addr1");
							 obj3 = $("#"+objCode+"addr2");

               // 우편번호와 주소 및 영문주소 정보를 해당 필드에 넣는다.
               //obj1.val(data.postcode1+"-"+data.postcode2);
               obj1.val(data.zonecode);
               obj2.val(fullAddr);

               // iframe을 넣은 element를 안보이게 한다.
               postWin.style.display = 'none';
               //$("#inOcomCode").focus();

               // 우편번호 찾기 화면이 보이기 이전으로 scroll 위치를 되돌린다.
               //document.body.scrollTop = currentScroll;
               $("#inOcomCode").focus();
               setTimeout("obj3.focus()",100);
               fnTopFrameResize();
               
               //alert(data.sido+" "+data.sigungu+" "+data.bname+"\n\n"+data.jibunAddress+"\n\n"+data.postcode);
           },
           // 우편번호 찾기 화면 크기가 조정되었을때 실행할 코드를 작성하는 부분. iframe을 넣은 element의 높이값을 조정한다.
           onresize : function(size) {
          	h= size.height;
          	if(h>600)h=600;
           	postWin.style.height = (h+30)+"px";
						

           },
           width : '100%',
           height : '100%'
       }).embed(postWin);
       postWin.style.display = 'block';
       fnTopFrameResize();
 	}

/*=============================================
	관리자모드 > 상담관리 > 제품검색
=============================================*/
function fnCallFindPrd(){
	CTIDX = v;
	val = 0;
	for(k=1;k<=5;k++){
		v = $("#inCATE"+k+" option:selected").val();
		if(v)val=v;
		else break;
	}

	$("#prdSearchResult").html("검색중..");

	s1 = $("#inFindPrdSearch").val();
	param="CTIDX="+val+"&s1="+s1;
	$.ajax({
		url:'/CS/json/callProductSearch.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			//$("#prdSearchResult").html(data["data"]);
			if(data["result"]=="OK"){
				$("#prdSearchResult").html("");

				len = data["length"];
				for(k=0;k<len;k++){
					d = data["data"][k];
					str = "<div class='col-lg-2 col-md-3 col-sm-4 col-xs-6 prdBox' onclick='fnCallFindPrdSet($(this))'>";
					str+= "	<div class='x_panel'>";
          str+= "   <div class='x_content'>";
					str+= "			<div class='prdImg'><img src='" +d["Pimage"] + "' style='width:100%;'></div>";
					str+= "			<div class='prdName'>" + d["Pname"] + "</div>";
					str+= "			<div class='prdPrice'>" + d["Ppirce"] + "원</div>";
					str+= "			<div class='hiddenObj'>" + d["IDX"] + "</div>";
					str+= "			<div class='hiddenObj'>" + d["Pcode"] + "</div>";
					str+= "			<div class='hiddenObj'>" + d["BRname"] + "</div>";
					str+= "		</div>"
					str+= "	</div>"
					str+= "</div>"
					$("#prdSearchResult").append(str);
				}
			}else if(data["result"]=="NULL"){
				$("#prdSearchResult").html("<center>- 분류를 선택하거나 검색어를 입력하세요 -</center>");
			}else{
				alert("오류가 발생하였습니다. (1369)");
			}
		}
	});
}

function fnCallFindPrdSet(obj){
	IDX = obj.find(".hiddenObj").eq(0).html();
	img = obj.find(".prdImg").html();
	prdName = obj.find(".prdName").html();
	prdPrice = obj.find(".prdPrice").html();
	prdCode = obj.find(".hiddenObj").eq(1).html();
	BRname = obj.find(".hiddenObj").eq(2).html();

	tObj = $("#CAprd");
	tObj.find(".prdImg").html(img);
	tObj.find(".prdName").html(prdName);
	tObj.find(".prdPrice").html(prdPrice);
	tObj.find("#inPIDX").val(IDX);

	$('#findPrdModal').modal('hide');

	/*-- 브랜드 / 제품명 / 제품코드 입력 불가처리 --*/
	$("#inCAprdBrand").val(BRname);
	$("#inCAprdName").val(prdName);
	$("#inCAprdCode").val(prdCode);

	fnCallPrdEditable();
	fnTopFrameResize();
}

function fnCallFindPrdUnset(){
	tObj = $("#CAprd");
	tObj.find(".prdImg").html("");
	tObj.find(".prdName").html("<center>-미지정-</center>");
	tObj.find(".prdPrice").html("");
	tObj.find("#inPIDX").val("");
	fnCallPrdEditable();
	fnTopFrameResize();
}

function fnCallPrdEditable(){
	v = $("#inPIDX").val();
	if(v){
		$("#inCAprdBrand").attr("readonly",true);
		$("#inCAprdName").attr("readonly",true);
		$("#inCAprdCode").attr("readonly",true);
	}else{
		$("#inCAprdBrand").attr("readonly",false);
		$("#inCAprdName").attr("readonly",false);
		$("#inCAprdCode").attr("readonly",false);
	}
}

/*=============================================
	관리자모드 > 상담관리 > 댓글기능
=============================================*/
function fnCACMTlist(p){
	if(!CAIDX)return;
	if(!p)p=1;
	param="mode=list&CAIDX="+CAIDX+"&page="+p;
	$.ajax({
		url:'./json/callComment.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				$("#CACMTBOX").html("");
				len = data["length"];
				for(k=0;k<len;k++){
					d = data["data"][k];
					str = "				<li>";
				  str+= "          <a>";
				  str+=	"							<span class='image'><img src='" + d["Mphoto"] + "' class='Mphoto'></span>";
				  str+= "             <span><span>" + d["Mname"] + "</span>";
				  str+= "           	<span class='time'>" + d["CACregDate"] + "</span></span>";
				  str+= "           	<span class='message'>"+d["CACcontent"]+"</span>";
					str+= "					</a>";
				  str+= "   	    </li>";
				  $("#CACMTBOX").append(str);
				}

			}else{
				alert("오류가 발생하였습니다. (1454)");
			}
		}
	});
}

//-- 댓글 저장
function fnCACMTsave(){
	if(!$("#inCACcontent").val()){
		alert("내용을 입력하세요");
		$("#inCACcontent").focus();
		return;
	}

	param="mode=save&CAIDX="+CAIDX;
	param+="&CACcontent="+$("#inCACcontent").val();

	$.ajax({
		url:'./json/callComment.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				$("#inPJCcontent").val("");
				fnCACMTlist(1);
			}else{
				alert("오류가 발생하였습니다. (1482)");
			}
		}
	});
}

/*=============================================
	관리자모드 > 상담관리 > SMS 리스팅 및 발송
=============================================*/
function fnCallSMSlist(){
	if(!CAIDX)return;
	param ="mode=list&CAIDX="+CAIDX;
	box = $("#CASMSBOX");
	box.html("데이터를 불러오는 중...");
	$.ajax({
		url:'/CS/json/callSMS.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				box.html("");
				len = data["length"];
				if(!len){
					str = "<li style='display:block;'><center>발송내역이 없습니다.</center></li>";
					box.append(str);
				}else{
					for(k=0;k<len;k++){
						d = data["data"][k];
						str = "<li>";
	        	str+= "	<a>";
	        	str+= "		<span><span>" + d["SMSLrTel"] + "</span>";
	        	str+= "		<span class='time'>" + d["SMSLsendDate"] + "</span></span>";
	        	str+= "		<span class='message'>" + d["SMSLmsg"] + "</span>";
	        	str+= "	</a>";
	        	str+= "</li>";
	          box.append(str);
					}
				}
			}else if(data["result"]=="ERROR"){
				alert("SMS리스트를 불러오는 중 오류가 발생하였습니다. (1520)");
			}
		}
	});
}

function fnCallSMS(m){
	$("#inCASMSrTel option").remove();
	str="";

	if(m=="call"){	//-- 상담정보에서 연락처 가져오기
		for(k=1;k<=3;k++){
			tel = $("#inCAtel"+k).val();
			telName = $("#inCAtel"+k+"name").val();
	
			if(tel){
				str+= "<option value='" + tel + "'>";
				if(telName)str+=telName + " : ";
				str+=tel + "</option>";
			}
		}
		
		if(!str){
			alert("입력된 연락처가 없습니다.\n\n고객정보에서 연락처를 입력해 주세요.");
			return;
		}
		
	}else if(m=="as"){	//-- AS 관리에서 연락처 정보 가져오기
		
	}

	$("#inCASMSrTel").append(str);
	$("#inCASMScontent").val("");
	$("#divCASMSbyte").html("0/80byte");
	$("#smsModal").modal("show");
}



function fnCallSMSsend(){
	tel = $("#inCASMSrTel").val();
	con = $("#inCASMScontent").val();
	if(!tel){
		alert("SMS를 수신할 연락처가 없습니다.");
		return;
	}

	if(!con){
		alert("내용을 입력해주세요");
		return;
	}

	if(con.indexOf("O")>=0){
		if(!confirm("임시로 작성된 'O' 문자가 존재합니다.\n\n그대로 발송하시겠습니까?"))return;
	}

	if(!confirm("SMS발송 후 취소가 불가합니다.\n\n발송하시겠습니까?"))return;

	param ="mode=send&CAIDX="+CAIDX;
	param+="&inCASMSsTel="+$("#inCASMSsTel").val();
	param+="&inCASMSrTel="+tel;
	param+="&inCASMScon="+con;
	param+="&inCASMStype=call";


	$.ajax({
		url:'/CS/json/callSMS.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				new PNotify({title: 'SMS발송 성공',text: 'SMS가 성공적으로 발송되었습니다.',type: 'success'});
				fnCallSMSlist();
				$("#smsModal").modal("hide");
			}else if(data["result"]=="ERROR"){
				alert("오류가 발생하였습니다. (1585)");
			}
		}
	});
}

//-- SMS 바이트 체크
function fnSMSbyteChk(con,byteObj){
		smsObj = $("#"+con);
    var temp_str = smsObj.val();
    var remain = $("#"+byteObj);
    nByte = fnSMSgetByte(temp_str);

    remain.html(nByte + " byte");
    /*
    if(nByte > 80){
	    alert(80 + "Bytes를 초과할 수 없습니다.");
	    while(nByte > 80){
		    temp_str = temp_str.substring(0, temp_str.length-1);
		    smsObj.val(temp_str);
		    nByte = fnSMSgetByte(temp_str);
    		remain.html(nByte + "/80byte");
	    }
	    smsObj.focus();
    }
    */
}

//-- SMS 바이트 체크
function fnSMSgetByte(str){
    var resultSize = 0;
    if(str == null)return 0;

    for(var i=0; i<str.length; i++){
	    var c = escape(str.charAt(i));
	    if(c.length == 1)//기본 아스키코드
	    {resultSize ++;}
	    else if(c.indexOf("%u") != -1)//한글 혹은 기타
	    {resultSize += 2;}
	    else resultSize ++;
    }
    return resultSize;
}

//-- 예약어 선택시 내용 셋팅하기
function fnSMSsetReserved(v,con,byteObj){
	conObj = $("#"+con);
	conObj.val(SMSreserved[v]);
	fnSMSbyteChk(con,byteObj);
}

/*=============================================
	관리자모드 > 상담관리 > 정보복사
=============================================*/
function fnCallCopyInfo(){
	$("#inCAbenefitBank").val($("#inCAbank").val());
	$("#inCAbenefitBankCode").val($("#inCAbankCode").val());
	$("#inCAbenefitBankUser").val($("#inCAname").val());
	
}

/*=============================================
	관리자모드 > 상담관리 > 댓글미리보기
=============================================*/
function fnCallCMTpreview(IDX){
	CAIDX = IDX;
	fnCACMTlist(1);
	$("#cmtModal").modal("show");
}

/*=============================================
	관리자모드 > 상담관리 > SMS발송내역 미리보기
=============================================*/
function fnCallSMSpreview(IDX){
	CAIDX = IDX;
	fnCallSMSlist(1);
	$("#smsModal").modal("show");
}

/*=============================================
	관리자모드 > 상담관리 > 설치점 정보 가져오기(사용안함)
=============================================
function fnCallSetupInfo(){
	param+= "&CAIDX="+CAIDX+"&mode=setupInfo";
	$.ajax({
	  type: "POST",
	  url: "./json/callAS.html",
	  data: param,  
	  dataType: "json",
	  success: function(data){
	  	if(data["result"]=="OK"){
	  		
	  	}else{
	  		
	  	}
	  }
	});
}
*/

/*=============================================
	관리자모드 > 상담관리 > AS내역 가져오기
=============================================*/
function fnCallASinfo(){
	
	tbody = $("#asList");
	tbody.html("<tr><td colspan=5><center>AS내역을 불러옵니다.</center></td></tr>");
	
	param = "&CAIDX="+CAIDX+"&mode=list";
	$.ajax({
	  type: "POST",
	  url: "./json/callAS.html",
	  data: param,  
	  dataType: "json",
	  success: function(data){
	  	if(data["result"]=="OK"){
	  		len = data["length"];
	  		tbody.html("");
	  		if(len<1){
	  			tbody.html("<tr><td colspan=5><center>AS내역이 없습니다.</center></td></tr>");
	  		}else{
		  		for(k=0;k<len;k++){
		  			d = data["data"][k];
		  			str = "<tr>";
		  			str+= "<td>" + d["AStype"] + "</td>";
		  			str+= "<td>" + d["SMname"] + "</td>";
		  			str+= "<td>" + d["ASstate"] + "</td>";
		  			str+= "<td>" + d["ASendDate"] + "</td>";
		  			str+= "<td><button type='button' class='btn btn-primary btn-xs' onclick='fnCallEditAs("+d["IDX"]+")'>보기</button></td>";
		  			
		  			str+= "</tr>";
		  			tbody.append(str);
		  		}
		  	}
	  	}else{
	  		
	  	}
	  }
	});	
}

/*=============================================
	관리자모드 > 상담관리 > AS추가
=============================================*/
function fnCallAddAS(){	
	$("#findASModal").modal("show");
}

//-- hide 액션에서는 자식 modal 창의 hide 액션과 충돌이 일어남.
$('#findASModal').on('hidden.bs.modal', function (e) {
	if($('#findASModal').css("display")=="block")return;	//-- 자식 modal 과 충돌 방지

	$("#formAS .iradio_flat-green").removeClass("checked");
	$("#formAS [name='inAStype']").removeAttr("checked");
	$("#formAS [name='inAStype']").eq(0).attr("checked","checked").parent().addClass("checked");
	
	$("#formAS [name='inASpriceType']").removeAttr("checked");
	$("#formAS [name='inASpriceType']").eq(0).attr("checked","checked").parent().addClass("checked");
	
	$("#formAS [name='inASprdSendState']").removeAttr("checked");
	$("#formAS [name='inASprdSendState']").eq(0).attr("checked","checked").parent().addClass("checked");
	
	$("#formAS [name='inASstate']").removeAttr("checked");
	$("#formAS [name='inASstate']").eq(0).attr("checked","checked").parent().addClass("checked");
	
	$("#inSMIDX").val("");
	
	$("#SMname").html("");
	$("#SMtel").html("");
	$("#SMemail").html("");
	$("#SMaddr1").html("");
	$("#SMaddr2").html("");
	
	$("#formAS")[0].reset();	
		
});

/*=============================================
	관리자모드 > 상담관리 > AS수정
=============================================*/
function fnCallEditAs(IDX){
	frm = $("#formAS");
	//-- 값 셋팅
	
	param+= "&CAIDX="+CAIDX+"&inASIDX="+IDX+"&mode=edit";
	$.ajax({
	  type: "POST",
	  url: "./json/callAS.html",
	  data: param,  
	  dataType: "json",
	  success: function(data){
	  	if(data["result"]=="OK"){
	  		frm.find("#inASIDX").val(IDX);

	  		//-- 작업자 정보 셋팅
	  		frm.find("#SMname").html(data["SMname"]);
	  		frm.find("#SMtel").html(data["SMtel"]);
	  		frm.find("#SMemail").html(data["SMemail"]);
	  		frm.find("#SMaddr1").html(data["SMaddr1"]);
	  		frm.find("#SMaddr2").html(data["SMaddr2"]);

	  		frm.find("#inASprdSendDate").val(data["ASprdSendDate"]);
	  		frm.find("#inASprdSendCom").val(data["ASprdSendCom"]);
	  		frm.find("#inASprdSendCode").val(data["ASprdSendCode"]);
	  		frm.find("#inASserial").val(data["ASserial"]);
	  		frm.find("#inASplanDate").val(data["ASplanDate"]);
	  		frm.find("#inASendDate").val(data["ASendDate"]);

	  		frm.find("#inASworkComment").val(data["ASworkComment"]);
	
	  		$("#findASModal").modal("show");
	  	}else{
	  		alert("데이터를 불러오는데 실패하였습니다.");
	  	}
	  },
	  error:function(){
	  	alert("데이터를 불러오는데 실패하였습니다.");
	  }
	});
	
	
	
}

/*=============================================
	관리자모드 > 상담관리 > AS저장
=============================================*/
function fnCallASsave(){
	param = $("#formAS").serialize();
	param+= "&CAIDX="+CAIDX+"&mode=save";
	$.ajax({
	  type: "POST",
	  url: "./json/callAS.html",
	  data: param,  
	  dataType: "json",
	  success: function(data){
	  	if(data["result"]=="OK"){
	  		new PNotify({title: '데이터 저장 성공',text: '데이터 저장에 성공하였습니다.',type: 'success',delay:1000});
	  		$("#findASModal").modal("hide");
	  		fnCallASinfo();//-- AS내역 가져오기
	  	}else{
	  		alert("저장 중 오류가 발생하였습니다.");
	  	}
	  },
	  error:function(){
	  	alert("저장 중 오류가 발생하였습니다.");
	  }
	});
	
}


/*=============================================
	관리자모드 > 상담관리 > 상담녹취관리
=============================================*/
//-- 녹취 듣기
function fnRecordingPlay(IDX){

	param ="mode=play&RCIDX="+IDX;
	$.ajax({
		url:'./json/recording.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				d = data["data"];
				$("#recordingModal #divRCsTel").html(d["RCsTel"]);
				$("#recordingModal #divRCrTel").html(d["RCrTel"]);
				$("#recordingModal #divRCsTel").html(d["divRCsTel"]);
				$("#recordingModal #divRCtelDate").html(d["RCtelDate"] + " " + d["RCtelTime"]);
				$("#recordingModal #divRCtelTerm").html(d["RCtelTerm"]);
				$("#recordingModal #divRCplay").html("파일서버에서 음성파일을 다운로드합니다.<br>다운로드가 완료되면 자동 재생됩니다.<br>파일용량 : " + d["RCfileSize"]);
				$("#recordingModal #divRCdown").html('<button type="button" class="btn btn-sm btn-primary" onclick="fnRecordingDown(\'' + IDX + '\');">다운로드</button>');

				fnFileFtpDown(IDX);

				$("#recordingModal").modal("show");
			}else if(data["result"]=="ERROR"){
				alert("오류가 발생하였습니다. (1682)");
			}
		}
	});
}

function fnFileFtpDown(IDX){
		param ="mode=ftpDown&RCIDX="+IDX;
		$.ajax({
			url:'./json/recording.html',
			type : 'POST',
			cache:false,
			data : param,
			dataType:"json",
			success:function(data){

				if(data["result"]=="OK"){
					str='<object width="275" height="100" id="mPlayer" classid="clsid:22D6F312-B0F6-11D0-94AB-0080C74C7E95" style="left: 0px; top: 0px;">';
					str+='<param name="AutoSize" value="0"/>';
					str+='<param name="AutoStart" value="1"/>';
					str+='<param name="Volume" value="-100"/>';
					str+='<param name="Filename" value="http://tools.rcommall.com/Recording/playfile/'+d["RCfile"] + '"/>';
					str+='<param name="CanSeek" value="1"/>';
					str+='<param name="CanSeekToMarkers" value="1"/>';
					str+='<param name="ShowPositionControls" value="0"/>';
					str+='<param name="ShowCaptioning" value="0"/>';
					str+='<param name="ShowStatusBar" value="1"/>';
					str+='</object>';

					$("#recordingModal #divRCplay").html(str);

				}else{
					if(confirm("파일 다운로드에 오류가 발생하였습니다. (1714)\n\n다시 시도하시겠습니까?")){
						document.location.reload();
					}
				}

			}
		});

	}

function fnRecordingDown(IDX){
	$("#downframe").attr("src","./json/recording.html?RCIDX="+IDX+"&mode=down");
}

function fnRecordingClose(){	//-- 창닫을때 재생한 미디어 플레이어 멈추기
	$("#recordingModal #divRCsTel").html("");
	$("#recordingModal #divRCrTel").html("");
	$("#recordingModal #divRCsTel").html("");
	$("#recordingModal #divRCtelDate").html("");
	$("#recordingModal #divRCtelTerm").html("");
	document.getElementById("mPlayer").stop();
	$("#recordingModal #divRCplay").html("");
	$("#recordingModal #divRCdown").html("");
}

/*=============================================
	관리자모드 > 통합 댓글기능
=============================================*/
function fnCMTlist(TID,TIDX,p){
	if(!TIDX)return;
	if(!p)p=1;
	param="mode=list&TID="+TID+"&TIDX="+TIDX+"&page="+p;
	$.ajax({
		url:'/inc/comment.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				$("#CMTBOX").html("");
				len = data["length"];
				for(k=0;k<len;k++){
					d = data["data"][k];
					str = "				<li>";
				  str+= "          <a>";
				  str+=	"								<span class='image'><img src='" + d["Mphoto"] + "' class='Mphoto'></span>";
				  str+= "             	<span><span>" + d["Mname"] + "</span>";
				  str+= "            					<span class='time'>" + d["CMTregDate"] + "</span></span>";
				  str+= "            <span class='message'>"+d["CMTcontent"]+"</span>";
					str+= "					</a>";
				  str+= "   	    </li>";
				  $("#CMTBOX").append(str);
				}
				fnTopFrameResize();
			}else{
				alert("오류가 발생하였습니다. (1769)");
			}
		}
	});
}

//-- 댓글 저장
function fnCMTsave(TID,TIDX){
	if(!$("#inCMTcontent").val()){
		alert("내용을 입력하세요");
		$("#inCMTcontent").focus();
		return;
	}

	param="mode=save&TID="+TID+"&TIDX="+TIDX;
	param+="&CMTcontent="+$("#inCMTcontent").val();

	$.ajax({
		url:'/inc/comment.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				$("#inCMTcontent").val("");
				fnCMTlist(TID,TIDX,1);
			}else{
				alert("오류가 발생하였습니다. (1796)");
			}
		}
	});
}

/*=============================================
	관리자모드 > 상담관리 > SMS발송하기
=============================================*/
//-- 번호 추가
function fnSMSreadyAddTel(){
	if(!fnTelSet($("#inSMSnewNum")))return;

	tel = $("#inSMSnewNum").val();

	//-- 중복검사
	listObj = $("#smsReadyList");
	listTr = listObj.find("tr");
	len = listTr.length;
	for(k=0;k<len;k++){
		tdObj = listTr.eq(k).find("td");
		if(tdObj.eq(0).html()==tel){
			alert("이미 등록된 번호입니다.");
			return;
		}
	}

	str = '<tr>';
	str+= '	<td  class="txtC w80per">'+tel+'</td>';
	str+= '	<td  class="txtC"><input class="btn btn-danger btn-xs" onclick="$(this).parent().parent().remove()" type="button" value="삭제"></td>';
	str+= '</tr>';
	listObj.append(str);
	$("#inSMSnewNum").val("");
}



function fnSMSreadySend(){
	listObj = $("#smsReadyList");
	listTr = listObj.find("tr");
	len = listTr.length;

	if(!len){
		alert("수신자가 없습니다.");
		return;
	}

	telNums = "";
	for(k=0;k<len;k++){
		tdObj = listTr.eq(k).find("td");
		if(telNums)telNums+=",";
		telNums+=tdObj.eq(0).html() + "##0";	//-- 구분자 ## 으로 주문번호 붙여주기
	}

	SMScontent = $("#inSMScontent").val();
	if(!SMScontent){
		alert("발송할 내용이 없습니다.");
		return;
	}

	if(SMScontent.indexOf("O")>=0){
		if(!confirm("임시로 작성된 'O' 문자가 존재합니다.\n\n그대로 발송하시겠습니까?"))return;
	}

	if(!confirm("SMS발송 후 취소가 불가합니다.\n\n발송하시겠습니까?"))return;

	param ="mode=send";
	param+="&inSMSsTel="+$("#inSMSsTel").val();
	param+="&inSMSrTel="+telNums;
	param+="&inSMStitle="+$("#inSMStitle").val();
	param+="&inSMScon="+SMScontent;
	param+="&inSMStype=common";

	$.ajax({
		url:'/inc/smsSend.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				new PNotify({title: 'SMS발송 성공',text: 'SMS가 성공적으로 발송되었습니다.',type: 'success'});
				$("#smsModal").modal("hide");
			}else if(data["result"]=="ERROR"){
				alert("오류가 발생하였습니다. (1881)");
			}
		}
	});
}

/*=============================================
	셀러 트리액션
=============================================*/
//-- 하위 그룹 추가
function fnSellerGroupAdd(qIDX){
	if(!$("#inSubSGname").val()){
		alert("추가할 그룹명을 입력해주세요");
		$("#inSubSGname").focus();
		return;
	}

	SGname = $("#inNewSGname").val();

	//-- 체크형식일 경우 체크값을, hidden 형식일경우(부모로부터 내려받을경우) 일반 val() 값을 잡아내기
	if($("#inSubSGallowSell").prop("type")=="hidden"){
		SGallowSell = $("#inSubSGallowSell").val();
		SGallowSetup = $("#inSubSGallowSetup").val();
		SGallowAS = $("#inSubSGallowAS").val();
	}else{
		SGallowSell = $("#inSubSGallowSell:checked").val();
		SGallowSetup = $("#inSubSGallowSetup:checked").val();
		SGallowAS = $("#inSubSGallowAS:checked").val();
	}

	if(!SGallowSell)SGallowSell="N";
	if(!SGallowSetup)SGallowSetup="N";
	if(!SGallowAS)SGallowAS="N";

	SGname = $("#inSubSGname").val();
	param="mode=add&qIDX="+qIDX+"&SGname="+SGname;
	param+="&SGallowSell="+SGallowSell;
	param+="&SGallowSetup="+SGallowSetup;
	param+="&SGallowAS="+SGallowAS;

	$.ajax({
		url:'./json/groupProc.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				nIDX = data["nIDX"];

				if(nIDX){
					obj = $("#cateObj"+qIDX);
					if(obj.has("ul").length){
						ulObj = obj.find("ul").eq(0);
						str = "<li id=\"cateObj" + nIDX + "\"><a href=\"javascript:fnSellerGroupView("+nIDX+")\">" + SGname + "</li>";
						ulObj.append(str);
					}else{
						str = "<ul>";
						str+= "<li id=\"cateObj" + nIDX + "\"><a href=\"javascript:fnCateView("+nIDX+")\">" + SGname + "</li>";
						str+="</ul>";
						obj.append(str);
					}
					$("#divCateDetail").html("");
					$("#tree1").find(".active").removeClass("active");
				}else{
					alert("오류가 발생하였습니다. (1946)");
				}
				
				fnTopFrameResize();

			}else{
				alert("오류가 발생하였습니다. (1950)");
			}
		}
	});
}

//-- 선택 그룹 삭제
function fnSellerGroupDel(qIDX){
	alert("삭제는 관리자에게 문의해주세요");
	//if(!confirm("해당 카테고리를 삭제하시겠습니까?"))return;
	//$("#cateObj"+qIDX).remove();
}

//-- 선택 그룹 수정
function fnSellerGroupEdit(){
	obj1 = $("#divNowSGname");
	obj2 = $("#divNowSGallow");
	obj3 = $("#divNewSGname");
	obj4 = $("#divNewSGallow");

	btn1 = $("#btnEditSave");
	btn2 = $("#btnEdit");

	if(obj3.hasClass("hiddenObj")){
		//-- 일반 > 수정하기
		$("#inNewSGname").val($("#nowSGname").html());
		obj1.removeClass("hiddenObj");
		obj2.removeClass("hiddenObj");
		obj3.removeClass("hiddenObj");
		obj4.removeClass("hiddenObj");

		btn1.removeClass("hiddenObj");

		obj1.addClass("hiddenObj");
		obj2.addClass("hiddenObj");
		btn2.html("취소");

	}else{
		//-- 수정하기 > 일반
		obj1.removeClass("hiddenObj");
		obj2.removeClass("hiddenObj");
		obj3.removeClass("hiddenObj");
		obj4.removeClass("hiddenObj");

		btn1.removeClass("hiddenObj");

		obj3.addClass("hiddenObj");
		obj4.addClass("hiddenObj");
		btn1.addClass("hiddenObj");

		btn2.html("수정");
	}
}

//-- 선택 그룹 수정 취소
function fnSellerGroupEditCancel(){
	obj1 = $("#divNowSGname");
	obj2 = $("#divNewSGname");
	obj3 = $("#divNewSGallow");

	btn1 = $("#btnEditSave");
	btn2 = $("#btnEdit");

	obj1.removeClass("hiddenObj");
	obj2.removeClass("hiddenObj");
	obj2.addClass("hiddenObj");
	obj3.addClass("hiddenObj");
}

//-- 선택 그룹 수정 저장 (실제반영)
function fnSellerGroupEditSave(qIDX){
	if(!$("#inNewSGname").val()){
		alert("변경할 새로운 그룹명을 입력해주세요");
		$("#inNewSGname").focus();
		return;
	}

	SGname = $("#inNewSGname").val();

	//-- 체크형식일 경우 체크값을, hidden 형식일경우(부모로부터 내려받을경우) 일반 val() 값을 잡아내기
	if($("#inNewSGallowSell").prop("type")=="hidden"){
		SGallowSell = $("#inNewSGallowSell").val();
		SGallowSetup = $("#inNewSGallowSetup").val();
		SGallowAS = $("#inNewSGallowAS").val();
	}else{
		SGallowSell = $("#inNewSGallowSell:checked").val();
		SGallowSetup = $("#inNewSGallowSetup:checked").val();
		SGallowAS = $("#inNewSGallowAS:checked").val();
	}

	if(!SGallowSell)SGallowSell="N";
	if(!SGallowSetup)SGallowSetup="N";
	if(!SGallowAS)SGallowAS="N";


	param="mode=edit&qIDX="+qIDX+"&SGname="+SGname;
	param+="&SGallowSell="+SGallowSell;
	param+="&SGallowSetup="+SGallowSetup;
	param+="&SGallowAS="+SGallowAS;

	$.ajax({
		url:'./json/groupProc.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				obj = $("#cateObj"+qIDX);
				obj.find("a").eq(0).html(SGname);
				$("#divCateDetail").html("");
				$("#tree1").find(".active").removeClass("active");				
			}else{
				alert("오류가 발생하였습니다. (2063)");
			}
			fnTopFrameResize();
		}
	});
}

function fnSellerGroupView(qIDX){

	$("#tree1").find(".active").removeClass("active");
	$("#cateObj"+qIDX).addClass("active");
	param="mode=view&qIDX="+qIDX;

	$.ajax({
		url:'./json/groupProc.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){

				if(!data["SGlevel"])data["SGlevel"]=0;

				str = '<div class="x_panel" id="divCateDetail">';
				str+= '	<div class="page-header"><h5 id="container">그룹 정보</h5></div>';

				if(qIDX){
					str+= '	<div class="form-group">';
				  str+= '    <label class="control-label col-md-3 col-sm-3 col-xs-12">고유번호</label>';
				  str+= '    <div class="col-md-9 col-sm-9 col-xs-12">'+ data['IDX'] +'</div>';
				  str+= '  </div>';

				  str+= '	<div class="form-group">';
				  str+= '    <label class="control-label col-md-3 col-sm-3 col-xs-12">고유코드</label>';
				  str+= '    <div class="col-md-9 col-sm-9 col-xs-12">'+ data['SGcode'] +'</div>';
				  str+= '  </div>';

				  str+= '  <div class="form-group" id="divNowSGname">';
				  str+= '    <label class="control-label col-md-3 col-sm-3 col-xs-12">선택한그룹</label>';
				  str+= '    <div class="col-md-9 col-sm-9 col-xs-12" id="nowSGname">'+ data['SGname'] +'</div>';
				  str+= '  </div>';
				  str+= '  <div class="form-group" id="divNowSGallow">';
				  str+= '    <label class="control-label col-md-3 col-sm-3 col-xs-12">권한</label>';
				  str+= '    <div class="col-md-9 col-sm-9 col-xs-12" id="nowSGallow">';
				  if(data["SGallowSell"]=="Y")str+=	'		   <label class="label label-success padding5px"><span class="glyphicon glyphicon-usd"></span> 판매</label>';
				  if(data["SGallowSetup"]=="Y")str+=	'		   <label class="label label-success padding5px"><span class="glyphicon glyphicon-wrench"></span> 설치</label>';
				  if(data["SGallowAS"]=="Y")str+=	'		   <label class="label label-success padding5px"><span class="glyphicon glyphicon-retweet"></span> AS</label>';
				  str+=	'		 </div>';
				  str+= '	 </div>';
				}

			  str+= '  <div class="form-group hiddenObj" id="divNewSGname">';
			  str+= '    <label class="control-label col-md-3 col-sm-3 col-xs-12">새로운그룹명</label>';
			  str+= '    <div class="col-md-9 col-sm-9 col-xs-12">';
			  str+= '    	<input type="text" class="form-control" required="required" placeholder="새로운그룹명" name="inNewSGname" id="inNewSGname" value="" onkeydown="if(event.keyCode==13)fnSellerGroupEditSave(\'' + qIDX + '\')">';
			  str+= '    </div>';
			  str+= '  </div>';

			  if(data["SGlevel"]==1){	//-- 최고레벨의 그룹만이 판매/설치/AS 권한 수정가능
				  checked1=checked2=checked3="";
				  if(data["SGallowSell"]=="Y")checked1="checked";
				  if(data["SGallowSetup"]=="Y")checked2="checked";
				  if(data["SGallowAS"]=="Y")checked3="checked";
				  str+= '  <div class="form-group hiddenObj" id="divNewSGallow">';
				  str+= '    <label class="control-label col-md-3 col-sm-3 col-xs-12">새로운권한</label>';
				  str+= '    <div class="col-md-9 col-sm-9 col-xs-12">';
				  str+= '    	<label><input type="checkbox" value="Y" '+ checked1 + ' name="inNewSGallowSell"	id="inNewSGallowSell"> 판매</label>&nbsp;&nbsp;&nbsp;&nbsp;';
				  str+= '    	<label><input type="checkbox" value="Y" '+ checked2 + ' name="inNewSGallowSetup" id="inNewSGallowSetup"> 설치</label>&nbsp;&nbsp;&nbsp;&nbsp;';
				  str+= '    	<label><input type="checkbox" value="Y" '+ checked3 + ' name="inNewSGallowAS"		id="inNewSGallowAS"> AS</label>';
				  str+= '    </div>';
				  str+= '  </div>';
				}else{	//-- 하위 레벨들은 그대로 현상 유지
					str+=	'<input type="hidden" value="'+data["SGallowSell"]+'" name="inNewSGallowSell"	id="inNewSGallowSell">';
					str+=	'<input type="hidden" value="'+data["SGallowSetup"]+'" name="inNewSGallowSetup"	id="inNewSGallowSetup">';
					str+=	'<input type="hidden" value="'+data["SGallowAS"]+'" name="inNewSGallowAS"	id="inNewSGallowAS">';
				}

			  if(qIDX>0){	// IDX 값이 있을때에만 수정/삭제 가능
				  str+= '  <div class="form-group txtC">';
				  str+=	'	 <button class="btn btn-info btn-sm hiddenObj" onclick="fnSellerGroupEditSave(\'' + qIDX + '\')" id="btnEditSave">저장</button>&nbsp;&nbsp;';
				  str+=	'	 <button class="btn btn-primary btn-sm" onclick="fnSellerGroupEdit(\'' + qIDX + '\')" id="btnEdit">수정</button>&nbsp;&nbsp;&nbsp;&nbsp;<button class="btn btn-danger btn-sm" onclick="fnSellerGroupDel(\'' + qIDX + '\')">삭제하기</button>';
				  str+= '  </div>';
				}


			  if(data["SGlevel"]<5){	// 5단계까지만 추가가능
			  	str+= '	<div class="page-header"><h5 id="container">하위그룹 추가</h5></div>';
				  str+= '  <div class="form-group">';
				  str+= '    <label class="control-label col-md-3 col-sm-3 col-xs-12">하위그룹명</label>';
				  str+= '    <div class="col-md-6 col-sm-6 col-xs-12">';
				  str+= '    	<input type="text" class="form-control" required="required" placeholder="그룹명" name="inSubSGname" id="inSubSGname" value="" onkeydown="if(event.keyCode==13)fnSellerGroupAdd(\'' + qIDX + '\')">';
				  str+= '    </div>';
				  str+= '  </div>';

				  if(!qIDX){	// 최상위 추가시에만 권한 설정 가능
					  str+= '  <div class="form-group">';
					  str+= '    <label class="control-label col-md-3 col-sm-3 col-xs-12">권한</label>';
					  str+= '    <div class="col-md-6 col-sm-6 col-xs-12">';
					  str+= '    	<label><input type="checkbox" value="Y" name="inSubSGallowSell"	id="inSubSGallowSell"> 판매</label>&nbsp;&nbsp;&nbsp;&nbsp;';
					  str+= '    	<label><input type="checkbox" value="Y" name="inSubSGallowSetup" id="inSubSGallowSetup"> 설치</label>&nbsp;&nbsp;&nbsp;&nbsp;';
					  str+= '    	<label><input type="checkbox" value="Y" name="inSubSGallowAS"		id="inSubSGallowAS"> AS</label>';
					  str+= '    </div>';
					  str+= '  </div>';
					}else{	//-- 최상위가 아닐경우 부모의 상태 물려받기
						str+=	'<input type="hidden" value="'+data["SGallowSell"]+'" name="inSubSGallowSell"	id="inSubSGallowSell">';
						str+=	'<input type="hidden" value="'+data["SGallowSetup"]+'" name="inSubSGallowSetup"	id="inSubSGallowSetup">';
						str+=	'<input type="hidden" value="'+data["SGallowAS"]+'" name="inSubSGallowAS"	id="inSubSGallowAS">';
					}

				  str+= '  <div class="form-group txtC">';
				  str+=	'	 <button class="btn btn-primary btn-sm" onclick="fnSellerGroupAdd(\'' + qIDX + '\')">하위추가</button>';
				  str+= '  </div>';
				}


				str+= '</div>';
				$("#divCateDetail").html(str);
				fnTopFrameResize();

			}else{
				alert("오류가 발생하였습니다. (2183)");
			}
		}
	});
}

/*=============================================
	첨부파일 다운받기
=============================================*/
function fnFileDownload(str){
	document.location='/inc/fileDown.html?fInfo='+str;
}

/*=============================================
	알람예약 시간더하기
=============================================*/
function fnCRtimeAdd(v){
	if(!$("#inCRdate").val()){
		var nd = new Date();
		dm = (nd.getMonth()+1);
		dd = nd.getDate();
		if(dm<10)dm="0"+dm;
		if(dd<10)dd="0"+dd;
		$("#inCRdate").val(nd.getFullYear() + "-"+dm+"-"+dd);
	}

	if(!$("#inCRtime").val())$("#inCRtime").val("00:00");

	//str = $("#inCRdate").val() + " " + $("#inCAtime").val() + ":00";
	d = $("#inCRdate").val().split("-");
	t = $("#inCRtime").val().split(":");

	var nd = new Date();
	nd.setYear(d[0]);
	nd.setMonth(d[1]-1);
	nd.setDate(d[2]);

	nd.setHours(t[0]);
	nd.setMinutes(t[1]);
	nd.setSeconds(0);

	//-- 새로운 날짜/시간 객체 구하기
	var newd = new Date(Date.parse(nd) + ((v*1000) * 60));
	dm = (newd.getMonth()+1);
	dd = newd.getDate();
	if(dm<10)dm="0"+dm;
	if(dd<10)dd="0"+dd;

	th =  newd.getHours();
	tm = newd.getMinutes();

	if(th<10)th="0"+th;
	if(tm<10)tm="0"+tm;

	$("#inCRdate").val(newd.getFullYear() + "-"+dm+"-"+dd);
	$("#inCRtime").val(th + ":" + tm);
}
	
/*======================================================================
관리자모드 > 발주관리 > 상담건검색
=======================================================================*/
function fnPrdOrderFindOrderInit(){
	$("#CAfindResult").html("<tr><td colspan=6 class='txtC'>상담고객을 검색해주세요.</td></tr>");
	$("#inCAname").focus();
}

function fnPrdOrderFindOrder(pp){		
	//-- pp 인자값을 구분으로 팝업에서 정보 출력할지 일반 정보창 출력할지 체크
	if(pp==1){	//-- 팝업 검색용
		tObj = $("#CAfindResult");
		v = $("#inCAname").val();
		if(!v){
			alert("상담고객명을 입력해주세요");
			$("#inCAname").focus();
		}
		param="inCAname="+v;
		
	}else{	//-- 정보 입력창 내용 출력용
		tObj = $("#CAinfo");
		v = $("#inCAIDX").val();
		if(!v)return;
		param="inCAIDX="+v;
	}
	
	param+="&mode=call";
	
	tObj.html("<tr><td colspan=6 class='txtC'>검색중입니다.</td></tr>");
	$.ajax({
		url:'./json/prdOrderFind.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				len = data["length"];
				tObj.html("");
				if(len>0){
					for(k=0;k<len;k++){
						d = data["data"][k];
						str = "<tr>";
			      str+= "	<td>" + d["CAname"] + "</td>";
			      str+= "	<td>" + d["CAtel"] + "</td>";
			      str+= " <td>" + d["CAaddr1"] + "</td>";
			      str+= " <td>" + d["CAprdName"] + "</td>";
			      str+= " <td>" + d["CAregDate"] + "</td>";
			      if(pp)str+= " <td><button class='btn btn-info btn-xs' type='button' onclick='fnPrdOrderFindOrderSet("+d["IDX"]+")'>선택</button></td>";
			      str+= "</tr>";
			      tObj.append(str);
					}
				}else{
					tObj.html("<tr><td colspan=6 class='txtC'>검색 결과가 없습니다.</td></tr>");
				}
			}else{
				//-- 오류발생
			}
		}
	});	
}

function fnPrdOrderFindOrderSet(IDX){
	$("#inCAIDX").val(IDX);
	fnPrdOrderFindOrder(0);
	$("#orderFindModal").modal("hide");
}

function fnPrdOrderViewCAdetail(){
	IDX = $("#inCAIDX").val();
	if(!IDX){
		alert("선택된 상담건이 없습니다.\n\n상담건을 검색해주세요");
		return;
	}
	top.fnTabAdd('cs2','상담관리','/CS/callEdit.html?qIDX='+IDX);
}

/*======================================================================
관리자모드 > 발주관리 > 수령자검색(셀러)
=======================================================================*/
function fnPrdOrderFindSellerInit(){
	$("#SMfindResult").html("<tr><td colspan=6 class='txtC'>셀러명을 검색해주세요.</td></tr>");
	$("#inSMname").focus();
}

function fnPrdOrderFindSeller(pp){
	//-- pp 인자값을 구분으로 팝업에서 정보 출력할지 일반 정보창 출력할지 체크
	if(pp==1){	//-- 팝업 검색용
		slObj = $("#SMfindResult");
		v = $("#inSMname").val();
		if(!v){
			alert("상담고객명을 입력해주세요");
			$("#inSMname").focus();
		}
		param="inSMname="+v;
		
	}else{	//-- 정보 입력창 내용 출력용
		slObj = $("#SMinfo");
		v = $("#inSMID").val();
		if(!v)return;
		param="inSMID="+v;
	}
	param+="&mode=seller";
	
	slObj.html("<tr><td colspan=6 class='txtC'>검색중입니다.</td></tr>");
	$.ajax({
		url:'./json/prdOrderFind.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				len = data["length"];
				slObj.html("");
				if(len>0){
					for(k=0;k<len;k++){
						d = data["data"][k];
						str = "<tr>";
			      str+= "	<td>" + d["SMname"] + "</td>";
			      str+= "	<td>" + d["SMID"] + "</td>";
			      str+= "	<td>" + d["SMtel"] + "</td>";
			      str+= " <td>" + d["SMaddr1"] + "</td>";
			      if(pp)str+= " <td><button class='btn btn-info btn-xs' type='button' onclick='fnPrdOrderFindSellerSet(\""+d["SMID"]+"\")'>선택</button></td>";
			      str+= "</tr>";
			      slObj.append(str);
					}
				}else{
					slObj.html("<tr><td colspan=6 class='txtC'>검색 결과가 없습니다.</td></tr>");
				}
			}else{
				//-- 오류발생
			}
		}
	});	
}

function fnPrdOrderFindSellerSet(SMID){
	$("#inSMID").val(SMID);
	fnPrdOrderFindSeller(0);
	$("#sellerFindModal").modal("hide");
}

/*======================================================================
관리자모드 > 게시판관리 > 게시판 열람
=======================================================================*/
function fnBoardView(Bname,BIIDX){
	top.fnTabAdd('board99',Bname,'/Board/boardView.html?BIIDX='+BIIDX);
}

/*======================================================================
관리자모드 > 게시판관리 > 게시판 글작성시 랜덤 이름/비밀번호 만들기
=======================================================================*/
function fnMakeBoardWriter(){
	
	//-- 입력 객체 확인
	tr = $("#trBDname");
	if(!tr.find("input").length){
		tr.find("td").eq(0).html("<input type='text' name='inBDname' id='inBDname' value=''>");
		str ="<tr>";
		str+="	<th>비밀번호</th>";
		str+="	<td><input type='password' name='inBDpass' id='inBDpass'></td>";
		str+="</tr>";
		tr.after(str);
		fnTopFrameResize();
	}
	
	$.ajax({
		url:'/Board/json/mkWriter.html',
		method : 'post',
		cache:false,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				
				$("#inBDname").val(data["writer"]);
				$("#inBDpass").val(data["pass"]);
				
			}else if(data["result"]=="ERROR"){
				alert("오류가 발생했네요... 개발팀에 이야기해주세요 ㅠㅠ");
				return;
			}
		}
	});
}

/*======================================================================
관리자모드 > 제품관리 > 오픈마켓관리 > 추천제품 관리
=======================================================================*/
//-- 배너 기능 초기화
function fnMarketQuickInit(){
	fnMarketQuickLoad();
	$(".marketQuick .x_panel.editable").click(function(){
		$(this).addClass("active");
		v = $(this).attr("id").split("_");
		$("#inMQgroup1").val(v[0]);
		$("#inMQgroup2").val(v[1]);
		$("#inMQNUM").val(v[2]);
	  fnMarketQuickEdit();	  
		$('#marketQuickEditModal').modal('show');
	});
}

//-- 팝업 아웃
$('#marketQuickEditModal').on('hidden.bs.modal', function (e) {
	$(this).find("input[type='text']").val("");
	$(this).find("#inMQgroup1").val(0);
	$(this).find("#inMQgroup2").val(0);
	$(this).find("#inMQNUM").val(0);
  $(".marketQuick .x_panel.active").removeClass("active");
});

//-- 배너 정보 저장
function fnMarketQuickSave(){
	p = $("#marketQuickEditModal");
	img = p.find("#inMQimage");
	if(!img.val()){
		img.focus();
		alert("이미지 URL 을 입력해주세요");
		return;
	}

	var form = $('#formBanner')[0];
	var formData = new FormData(form);

	$.ajax({
	  url: './json/quick.html',
	  processData: false,
	  contentType: false,
	  data: formData,
	  type: 'POST',
	  dataType:'json',
	  success: function(result){
	  	fnMarketQuickLoad();
	  	$("#marketQuickEditModal").modal('hide');
	  }
	});
}

//-- 배너 정보 가져오기
function fnMarketQuickEdit(){
	p = $("#marketQuickEditModal");
	v1 = p.find("#inMQgroup1").val();
	v2 = p.find("#inMQgroup2").val();
	v3 = p.find("#inMQNUM").val();
	
	param = "mode=info&inMQgroup1="+v1;
	param+="&inMQgroup2="+v2;
	param+="&inMQNUM="+v3;
	
	$.ajax({
	  url: './json/quick.html',
	  data: param,
	  type: 'POST',
	  dataType:'json',
	  success: function(data){
	  	p.find("#inMQimage").val(data["MQimage"]);
	  	p.find("#inMQurl11").val(data["MQurl11"]);
	  	p.find("#inMQurlA").val(data["MQurlA"]);
	  	p.find("#inMQurlG").val(data["MQurlG"]);
	  }
	});
}

//-- 등록된 배너 블러와서 보여주기
function fnMarketQuickLoad(){
	$(".editable").html("");
	param = "mode=list";	
	$.ajax({
	  url: './json/quick.html',
	  data: param,
	  type: 'POST',
	  dataType:'json',
	  success: function(data){
	  	len = data["length"];
	  	for(k=0;k<len;k++){
	  		d = data["data"][k];
	  		
	  		grp1 = d["MPQgroup1"];
	  		grp2 = d["MPQgroup2"];	  		
	  		num = d["MPQnum"];
	  		img = d["MPQimage"];
	  		$("#"+grp1+"_"+grp2+"_"+num).html("<img src='"+img+"'>");
	  	}
	  }
	});
}

//-- 등록된 URL 로 바로가기
function fnMarketQuickGo(flag){
	v = $("#marketQuickEditModal #inMQurl"+flag).val();
	if(!v){
		alert("입력된 URL 이 없습니다.");
		return;
	}
	window.open(v,"_blank");
}

/*======================================================================
관리자모드 > A/S관리 > 고객검색
=======================================================================*/
function fnFindCall(){
	$("#findCallModal").modal("show");
}

$('#findCallModal').on('hidden.bs.modal', function (e) {
	$(this).find("input[type='text']").val("");
  $("#findCallResult").html("<tr><td colspan=5><center>고객명 입력 후 검색 버튼을 클릭해주세요.</center></td></tr>");
});

//-- 검색 찾기
function fnFindCallGo(){
	v = $("#findCallModal #inCAname").val();
	if(!v){
		alert("고객명을 입력해주세요.");
		$("#inCAname").focus();
		return;
	}
	param = "mode=list&s1="+v;
	tbody = $("#findCallResult");	
	tbody.html("<tr><td colspan=5><center>검색중입니다.</center></td></tr>");
	$.ajax({
	  url: './json/findCall.html',
	  data: param,
	  type: 'POST',
	  dataType:'json',
	  success: function(data){
	  	if(data["result"]=="OK"){
		  	len = data["length"];
		  	tbody.html("");
		  	if(!len){
		  		tbody.html("<tr><td colspan=5><center>- 검색결과가 존재하지 않습니다. -</center></td></tr>");
		  	}else{
			  	for(k=0;k<len;k++){
			  		d = data["data"][k];
			  		str ="<tr>";
			  		str+="<td id='CAname"+d["IDX"]+"'>"+d["CAname"]+"</td>";
			  		str+="<td id='CAtel"+d["IDX"]+"'>"+d["CAtel"]+"</td>";
			  		str+="<td id='CAprdName"+d["IDX"]+"'>"+d["CAprdName"]+"</td>";
			  		str+="<td>"+d["CAstate"]+"</td>";
			  		str+="<td><button class='btn btn-xs btn-info' onclick='fnFindCallSet("+d["IDX"]+")'>선택</button>";
			  		
			  		//-- 기타정보 숨김처리
			  		str+="<span class='hiddenObj' id='CApost"+d["IDX"]+"'>"+d["CApost"]+"</span>";
			  		str+="<span class='hiddenObj' id='CAaddr1"+d["IDX"]+"'>"+d["CAaddr1"]+"</span>";
			  		str+="<span class='hiddenObj' id='CAaddr2"+d["IDX"]+"'>"+d["CAaddr2"]+"</span>";
			  		str+="<span class='hiddenObj' id='CAprdCode"+d["IDX"]+"'>"+d["CAprdCode"]+"</span>";
			  		
			  		str+="<span class='hiddenObj' id='PIDX"+d["IDX"]+"'>"+d["PIDX"]+"</span>";
			  		str+="<span class='hiddenObj' id='Pimg"+d["IDX"]+"'>"+d["Pimg"]+"</span>";
			  		str+="<span class='hiddenObj' id='Pname"+d["IDX"]+"'>"+d["Pname"]+"</span>";
			  		str+="<span class='hiddenObj' id='Pprice"+d["IDX"]+"'>"+d["Pprice"]+"</span>";
			  		
			  		str+="</td>";
			  		str+="</tr>";
			  		
			  		tbody.append(str);
			  	}
			  }
		  }else{
		  	alert("오류가 발생했습니다");
		  }
	  }
	});
}

//-- 고객 선택
function fnFindCallSet(IDX){
	$("#inCAIDX").val(IDX);
	$("#inASname").val($("#CAname"+IDX).html());
	$("#inAStel").val($("#CAtel"+IDX).html());
	$("#inASpost").val($("#CApost"+IDX).html());
	$("#inASaddr1").val($("#CAaddr1"+IDX).html());
	$("#inASaddr2").val($("#CAaddr2"+IDX).html());
	$("#inCAprdName").val($("#CAprdName"+IDX).html());
	$("#inCAprdCode").val($("#CAprdCode"+IDX).html());
	
	$("#inPIDX").val($("#PIDX"+IDX).html());
	$(".prdImg").html("<img src='"+$("#Pimg"+IDX).html()+"'>");
	$(".prdName").html($("#Pname"+IDX).html());
	$(".prdPrice").html(fnCommify($("#Pprice"+IDX).html())+"원");
	$("#findCallModal").modal("hide");	
	fnASeditAble();
}

//-- 선택된 고객이 있을 경우 일부 정보 수정 불가
function fnASeditAble(){
	v = $("#inCAIDX").val();
	if(v){
		//-- 고객정보가 있을 경우		
		$("#inASname").attr("readonly",true);
		$("#inAStel").attr("readonly",true);
		$("#inASpost").attr("readonly",true);
		$("#inASaddr1").attr("readonly",true);
		$("#inASaddr2").attr("readonly",true);
		
		$("#btnPrdSet").css("display","none");
		$("#btnPrdClear").css("display","none");
		$("#btnFindCall").css("display","none");
		$("#btnFindCallAddr").css("display","none");
	}
	fnCallPrdEditable();
}

/*======================================================================
관리자모드 > A/S관리 > 작업자 선택
=======================================================================*/
function fnFindWorker(){	
	$("#findWorkerModal").modal("show");
}

$('#findWorkerModal').on('hidden.bs.modal', function (e) {
	$(this).find("input[type='text']").val("");
  $("#findWorkerResult").html("<tr><td colspan=5><center>검색하실 작업자의 이름 혹은 지역을 입력 후 검색 버튼을 클릭해주세요.</center></td></tr>");
});

function fnFindWorkerClose(){
	$("#findWorkerModal").modal("hide");
}

function fnFindWorkerGo(){
	v1 = $("#findWorkerModal #inSMname").val();
	v2 = $("#findWorkerModal #inSMarea").val();
	if(!v1 && !v2){
		alert("작업자명 혹은 지역을 입력해주세요");
		return;
	}
	
	param = "mode=list&s1="+v1+"&s2="+v2;
	tbody = $("#findWorkerResult");
	tbody.html("<tr><td colspan=5><center>검색중입니다.</center></td></tr>");
	$.ajax({
	  url: './json/findWorker.html',
	  data: param,
	  type: 'POST',
	  dataType:'json',
	  success: function(data){
	  	if(data["result"]=="OK"){
		  	len = data["length"];
		  	tbody.html("");
		  	if(!len){
		  		tbody.html("<tr><td colspan=5><center>- 검색결과가 존재하지 않습니다. -</center></td></tr>");
		  	}else{
			  	for(k=0;k<len;k++){
			  		d = data["data"][k];
			  		str ="<tr>";
			  		str+="<td id='SMname"+d["IDX"]+"'>"+d["SMname"]+"</td>";
			  		str+="<td id='SMtel"+d["IDX"]+"'>"+d["SMtel"]+"</td>";
			  		str+="<td id='SMarea"+d["IDX"]+"'>"+d["SMarea"]+"</td>";
			  		str+="<td><input type='button' class='btn btn-xs btn-info' onclick='fnFindWorkerSet("+d["IDX"]+")' value='선택' />";
			  		
			  		//-- 기타정보 숨김처리
			  		str+="<span class='hiddenObj' id='SMaddr1"+d["IDX"]+"'>"+d["SMaddr1"]+"</span>";
			  		str+="<span class='hiddenObj' id='SMaddr2"+d["IDX"]+"'>"+d["SMaddr2"]+"</span>";
			  		str+="<span class='hiddenObj' id='SMemail"+d["IDX"]+"'>"+d["SMemail"]+"</span>";
			  		
			  		str+="</td>";
			  		str+="</tr>";
			  		
			  		tbody.append(str);
			  	}
			  }
		  }else{
		  	alert("오류가 발생했습니다");
		  }
	  }
	});
}

function fnFindWorkerSet(IDX){
	$("#inSMIDX").val(IDX);
	
	$("#SMname").html($("#SMname"+IDX).html());
	$("#SMtel").html($("#SMtel"+IDX).html());
	$("#SMemail").html($("#SMemail"+IDX).html());
	$("#SMaddr1").html($("#SMaddr1"+IDX).html());
	$("#SMaddr2").html($("#SMaddr2"+IDX).html());
	
	fnFindWorkerClose();
}

function fnFindWorkerDetail(){
	v = $("#inSMIDX").val();
	if(!v)return;
	param = "mode=detail&s1="+v;
	
	$.ajax({
	  url: './json/findWorker.html',
	  data: param,
	  type: 'POST',
	  dataType:'json',
	  success: function(data){
	  	if(data["result"]=="OK"){	  		
	  		d = data["data"];
	  		$("#SMname").html(d["SMname"]);
				$("#SMtel").html(d["SMtel"]);
				$("#SMemail").html(d["SMemail"]);
				$("#SMaddr1").html(d["SMaddr1"]);
				$("#SMaddr2").html(d["SMaddr2"]);
	
	  	}else{
	  	}
	  }
	});
}

