/*======================================================================
관리자모드 > 사이트관리 > 배너관리
=======================================================================*/
$(document).ready(function(){
	fnSiteBannerInit();
	$("#subTitle").html($("#s2 option:selected").text());
});

//-- 배너 기능 초기화
function fnSiteBannerInit(){
	$("#template .x_panel.editable").click(function(){
		$(this).addClass("active");
		v = $(this).attr("id").replace("bn","");
		$("#inBNcode").val(v);
		$('#bannerModal').modal('show');
	});
	fnSiteTemplateLoad();
}

//-- 템플릿에 배너 갯수 블러오기
function fnSiteTemplateLoad(){
	v1 = $("#inSIIDX").val();
	v3 = $("#inCTIDX").val();
	
	if(!v1)return;
	param="mode=template&inSIIDX="+v1+"&inCTIDX=" + v3 + "&inBNcode=all";
	$.ajax({
		url:'./json/cateMainBanner.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				bnObj = $(".x_panel.editable");
				bnLength = bnObj.length;
				for(k=0;k<bnLength;k++){
					obj = bnObj.eq(k);
					num = obj.attr("id").replace("bn","");
					bCount = 0;
					try{
						if(data["BNcount"][num])bCount=data["BNcount"][num];
						str = "<span class='badge bg-green'>배너"+(k+1)+"<br>"+bCount+"개</span>";
					}catch(E){
						str = "<span class='badge bg-green'>배너"+(k+1)+"<br>0개</span>";
					}
					obj.html(str);
				}
			}else{
				alert("오류가 발생하였습니다. (35)");
			}
		}
	});
}

//-- 리스트 로드
function fnSiteBannerList(){
	v1 = $("#inSIIDX").val();
	v2 = $("#inBNcode").val();
	v3 = $("#inCTIDX").val();
	
	if(!v1 || !v2){
		alert("오류가 발생하였습니다. (47)");
		$('#bannerModal').modal('hide');
		return;
	}

  param="mode=list&inSIIDX="+v1+"&inCTIDX=" + v3 + "&inBNcode="+v2;
  
	$.ajax({
		url:'./json/cateMainBanner.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				len = data["length"];
				str="";
				if(len>0){
					for(k=0;k<len;k++){
						obj = data["data"][k];
						str+="<tr>";
						str+="<td class='txtC'>"+obj["BNsort"]+"</td>";
						str+="<td class='txtC'><img src='/_Data/Banner/"+obj["BNimage1"]+"' style='height:50px;'></td>";
						str+="<td class='txtC'>"+obj["BNtitle"]
						if(obj["BNsubTitle"])str+="<br><font color='gray'>"+obj["BNsubTitle"]+"</font>";
						str+="</td>";
						str+="<td class='txtC'>"+obj["BNlink"]+"</td>";
						str+="<td class='txtC'>"+obj["BNstate"]+"</td>";
						str+="<td class='txtC'><button type='button' class='btn btn-info btn-xs' onclick='fnSiteBannerEdit(" + obj["IDX"] + ")'>수정</button></td>";
						str+="<td class='txtC'><button type='button' class='btn btn-danger btn-xs' onclick='fnSiteBannerDel(" + obj["IDX"] + ")'>삭제</button></td>";
						str+="</tr>";
					}
				}else{
					str = "<tr><td colspan=6 class='txtC'>-등록된 정보가 없습니다.-</td></tr>";
				}
				$("#bannerList").html(str);
			}else{
				alert("오류가 발생하였습니다. (80)");
			}
		}
	});
}

//-- 팝업 로드시
$('#bannerModal').on('show.bs.modal', function (e) {
	fnSiteBannerList();
});

//-- 팝업 아웃
$('#bannerModal').on('hidden.bs.modal', function (e) {
	$("#inBNcode").val(0);
	$("#bannerList").html("");
	$("#imgInfo1").html("");
	$("#imgInfo2").html("");
  $("#template .x_panel.active").removeClass("active");
});

//-- 추가/수정
function fnSiteBannerEdit(IDX){
	$("#formBanner #inBNIDX").val(IDX);
	
	//-- 수정시 기존 정보 로드/셋팅하기
	if(IDX){
		v1 = $("#inSIIDX").val();
		v2 = $("#inBNcode").val();	
		v3 = $("#inCTIDX").val();
		
		param="mode=info&inSIIDX="+v1+"&inCTIDX=" + v3 + "&inBNcode="+v2+"&inBNIDX="+IDX;
		$.ajax({
			url:'./json/cateMainBanner.html',
			method : 'post',
			cache:false,
			data : param,
			dataType:"json",
			success:function(data){
				if(data["result"]=="OK"){
					if(data["data"]["BNimage1"]){
						$("#imgInfo1").html("현재파일 : " + data["data"]["BNimage1"]);
						$("#inBNimage1Old").val(data["data"]["BNimage1"]);
					}
					
					if(data["data"]["BNimage2"]){
						$("#imgInfo2").html("현재파일 : " + data["data"]["BNimage2"]);
						$("#inBNimage2Old").val(data["data"]["BNimage2"]);
					}
					
					$("#inBNtitle").val(data["data"]["BNtitle"]);
					$("#inBNsubTitle").val(data["data"]["BNsubTitle"]);
					$("#inBNstate").val(data["data"]["BNstate"]);
					$("#inBNlink").val(data["data"]["BNlink"]);
					$("#inBNtarget").val(data["data"]["BNtarget"]);
					$("#inBNPEIDX").val(data["data"]["BNPEIDX"]);					
					
					$("#bannerEditModal").modal('show');
					fnSiteBannerPrdLoad();
					
				}else{
					alert("오류가 발생하였습니다. (137)");
				}
			}
		});
	}else{
		$("#bannerEditModal").modal('show');
		
		/*테스트 코드 //5034,5037,5040 */
		//$("#inBNPEIDX").val("5034,5037,5040,5007,4942,4945");
		fnSiteBannerPrdLoad();
		
	}
}




//-- 추가/수정 취소시 form reset
$('#bannerEditModal').on('hidden.bs.modal', function (e) {
  document.getElementById("formBanner").reset();
  $("#imgInfo1").html("");
  $("#imgInfo2").html("");
  //-- form.reset() 으로는 file 객체가 reset 되지않아서 input file 객체를 다시 생성해준다.
	$("#inputFile1").html('<input type="file" class="form-control" placeholder="이미지" name="inBNimage1" id="inBNimage1" value="">');
	$("#inputFile2").html('<input type="file" class="form-control" placeholder="이미지" name="inBNimage2" id="inBNimage2" value="">');
	$("#prdList").html("");
	
	
	$(this).find("input[type='hidden']").val("");
	
});


//-- 추가/수정 저장
function fnSiteBannerEditSave(){
	v1 = $("#inSIIDX").val();
	v2 = $("#inBNcode").val();
	v3 = $("#inCTIDX").val();

	if(!v1 || !v2 || v2==0 || !v3){
		alert("오류가 발생하였습니다.");
		return;
	}

	//-- 신규 추가시 이미지 첨부 필수
	if($("#inBNIDX").val()==0){
		if(!$("#inBNimage1").val()){
			alert("이미지를 등록해주세요");
			return;
		}
	}

	$('#formBanner').find("[name='mode']").val("edit");

	var form = $('#formBanner')[0];
	var formData = new FormData(form);
	formData.append("inSIIDX", v1);
	formData.append("inBNcode", v2);
	formData.append("inCTIDX", v3);
	

	$.ajax({
	  url: './json/cateMainBanner.html',
	  processData: false,
	  contentType: false,
	  data: formData,
	  type: 'POST',
	  dataType:'json',
	  success: function(result){
	  	fnSiteBannerList();
	  	fnSiteTemplateLoad();
	  	$("#bannerEditModal").modal('hide');
	  }
	});
}

//-- 삭제
function fnSiteBannerDel(IDX){
	if(!confirm("정말로 삭제하시겠습니까?"))return;

	v1 = $("#inSIIDX").val();
	v2 = $("#inBNcode").val();
	if(!v1 || !v2){
		alert("오류가 발생하였습니다. (23)");
		$('#bannerModal').modal('hide');
		return;
	}	
	
	param="mode=del&inSIIDX="+v1+"&inBNcode="+v2+"&inBNIDX="+IDX;
	$.ajax({
		url:'./json/cateMainBanner.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				fnSiteBannerList();
				fnSiteTemplateLoad();
			}else{
				alert("오류가 발생하였습니다. (137)");
			}
		}
	});
}



//-- 제품 검색 준비
function fnSiteBannerFindPrd(){
	$("#findPrdModal").modal("show");
}


//-- 제품 검색창 닫을시 속성 잡기
$('#findPrdModal').on('hidden.bs.modal', function (e) {
  if(!$("body").hasClass("modal-open"))$("body").addClass("modal-open");
});


//-- 제품 검색 Go
function fnSiteBannerFindPrdGo(){
	v1 = $("#inSIIDX").val();
	v2 = $("#inBNcode").val();
	v3 = $("#inCTIDX").val();
	
	v = $("#findPrdModal #inFindPrdKey").val();
	if(!v){
		alert("검색어를 입력해주세요");
		$("#findPrdModal #inFindPrdKey").focus();
		return;
	}
	
	prdList = $("#findPrdModal #findPrdList");
	
	str = "<center> 제품을 불러옵니다.. </center>";
	prdList.html(str);

	param="mode=findPrd&inSIIDX="+v1+"&inBNcode="+v2+"&inCTIDX="+v3+"&inFindKey="+v;
	
	$.ajax({
		url:'./json/cateMainBanner.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				len = data["length"];
				prdList.html("");	
				if(len==0){
					str = "<center> 등록된 제품이 없습니다. </center>";
					prdList.html(str);
				}else{
					for(k=0;k<len;k++){

						d = data["data"][k];
						str='';
						img = "<img src='" + d["Pimage"] + "' alt='"+d["Pname"]+"' title='"+d["Pname"]+"'>";

						str ='<div class="col-sm-3 col-xs-4 prdBox choicePrd">';
        		str+='	<div class="x_panel">';
						str+='		<div class="x_content">';
						str+='			<div class="prdImg">'+img+'</div>';
						str+='			<div class="prdName" alt="'+d["Pname"]+'" title="'+d["Pname"]+'">'+d["Pname"]+'</div>';
						str+='			<div class="prdPrice">'+d["Pprice"]+' 원</div>';
        		str+='		</div>';
        		str+='		<div class="prdCover txtC">';
        		str+='			<button type="button" class="btn btn-primary" onclick="fnSiteBannerFindPrdAdd('+d["PEIDX"]+')">추가하기</button>';
        		str+='		</div>';
        		str+='	</div>';
        		str+='</div>';

						prdList.append(str);
					}
				}
			}else{
				new PNotify({title: '처리실패',text: '오류가 발생하여 처리에 실패하였습니다.',type: 'danger',delay:1000});
			}
		}
	});
}

//-- 제품 추가
function fnSiteBannerFindPrdAdd(PEIDX){
	
	v = $("#inBNPEIDX").val();
	
	tmp = v.split(",");
	len = tmp.length;
	for(k=0;k<len;k++){
		if(tmp[k]==PEIDX){
			alert("이미 추가된 상품입니다.");
			return;
		}
	}
	
	if(v)v+=",";
	v+=PEIDX;
	
	$("#inBNPEIDX").val(v);
	fnSiteBannerPrdLoad();
	alert("추가되었습니다.\n\n저장 후 반영됩니다.");
	
	/*
	v1 = $("#inSIIDX").val();
	v2 = $("#inBNcode").val();
	v3 = $("#inCTIDX").val();
	
	param="mode=catePrdAdd&inSIIDX="+v1+"&inBNcode="+v2+"&inCTIDX="+v3+"&PEIDX="+PEIDX;
	
	$.ajax({
		url:'./json/cateMainBanner.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				alert("OK");
			}else{
				new PNotify({title: '처리실패',text: '오류가 발생하여 처리에 실패하였습니다.',type: 'danger',delay:1000});
			}
		}
	});
	*/
}

function fnSiteBannerPrdLoad(){
	v1 = $("#inSIIDX").val();
	v2 = $("#inBNcode").val();
	v3 = $("#inCTIDX").val();
	
	v = $("#inBNPEIDX").val();
	if(!v)return;
	
	prdList = $("#bannerEditModal #prdList");
	
	param="mode=prdList&inSIIDX="+v1+"&inBNcode="+v2+"&inPEIDX="+v;
	
	
	$.ajax({
		url:'./json/cateMainBanner.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				
				len = data["length"];
				prdList.html("");	
				if(len==0){
					str = "<center> 등록된 제품이 없습니다. </center>";
					prdList.html(str);
				}else{
					for(k=0;k<len;k++){
						d = data["data"][k];
						str='';
						img = "<img src='" + d["Pimage"] + "' alt='"+d["Pname"]+"' title='"+d["Pname"]+"'>";

						str ='<div class="col-sm-3 col-xs-4 prdBox choicePrd" id="BNprd'+d["PEIDX"]+'">';
        		str+='	<div class="x_panel">';
						str+='		<div class="x_content">';
						str+='			<div class="prdImg">'+img+'</div>';
						str+='			<div class="prdName" alt="'+d["Pname"]+'" title="'+d["Pname"]+'">'+d["Pname"]+'</div>';
						str+='			<div class="prdPrice">'+d["Pprice"]+' 원</div>';
        		str+='		</div>';
        		str+='		<div class="prdCover txtC">';
        		str+='			<button type="button" class="btn btn-primary btn-sm" onclick="fnSiteBannerFindPrdDel('+d["PEIDX"]+')">삭제</button>';
        		str+='		</div>';
        		str+='	</div>';
        		str+='</div>'; 

						prdList.append(str);
					}
					//$("#bannerEditModal").css("overflow-y","auto !important");					
					//$("#bannerEditModal .modal-backdrop").css("overflow","hidden !important");
				}
				
				
			}else{
				new PNotify({title: '처리실패',text: '오류가 발생하여 처리에 실패하였습니다.',type: 'danger',delay:1000});
			}
			
			if(!$("body").hasClass("modal-open"))$("body").addClass("modal-open");
		}
	});
}


//-- 제품 삭제
function fnSiteBannerFindPrdDel(PEIDX){
	v = $("#inBNPEIDX").val();
	tmp = v.split(",");
	len = tmp.length;
	
	newV = "";
	for(k=0;k<len;k++){		
		if(tmp[k]==PEIDX)continue;
		if(newV!="")newV+=",";
		newV+=tmp[k];
	}
	
	$("#inBNPEIDX").val(newV);
	
	$("#BNprd"+PEIDX).remove();
	
	alert("삭제되었습니다.\n\n저장 후 반영됩니다.");
}

$('#findPrdModal').on('hidden.bs.modal', function (e) {
	$("#findPrdModal #inFindPrdKey").val("");
	$("#findPrdModal #findPrdList").html("<center>제품명 혹은 제품코드를 입력하시고 검색을 해주세요</center>");
});