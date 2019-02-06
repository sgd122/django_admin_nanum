/*======================================================================
관리자모드 > 사이트관리 > 배너관리
=======================================================================*/
$(document).ready(function(){
	fnSiteBannerInit();
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
	if(!v1)return;
	param="mode=template&inSIIDX="+v1+"&inBNcode=all";
	$.ajax({
		url:'./json/banner.html',
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
	if(!v1 || !v2){
		alert("오류가 발생하였습니다. (47)");
		$('#bannerModal').modal('hide');
		return;
	}

  param="mode=list&inSIIDX="+v1+"&inBNcode="+v2;
	$.ajax({
		url:'./json/banner.html',
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
						str+="<td class='txtC'>"+obj["BNtitle"]+"</td>";
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
		
		param="mode=info&inSIIDX="+v1+"&inBNcode="+v2+"&inBNIDX="+IDX;
		$.ajax({
			url:'./json/banner.html',
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
					$("#inBNstate").val(data["data"]["BNstate"]);
					$("#inBNlink").val(data["data"]["BNlink"]);
					$("#inBNtarget").val(data["data"]["BNtarget"]);
					
					$("#bannerEditModal").modal('show');
					
				}else{
					alert("오류가 발생하였습니다. (137)");
				}
			}
		});
	}else{
		$("#bannerEditModal").modal('show');
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
});


//-- 추가/수정 저장
function fnSiteBannerEditSave(){
	v1 = $("#inSIIDX").val();
	v2 = $("#inBNcode").val();

	if(!v1 || !v2 || v2==0){
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

	var form = $('#formBanner')[0];
	var formData = new FormData(form);
	formData.append("inSIIDX", v1);
	formData.append("inBNcode", v2);

	$.ajax({
	  url: './json/banner.html',
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
		url:'./json/banner.html',
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