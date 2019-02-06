/*======================================================================
관리자모드 > 제품관리 > 오픈마켓관리 > 요금제관리
=======================================================================*/

$(document).ready(function(){
	$("#priceTable tbody tr td.editable").click(function(){
		fnMarketPriceEdit($(this));
	});
	
	$("#priceTable").mouseleave(function(){
		$("#priceTable tbody tr td.focused").removeClass("focused");
	});
	fnMarketTableFocusInit();
});

$(document).on("click",function(ev) { 
	//if($(e.target).parents("셀렉트박스").size() == 0) { //셀렉트박스 닫기, $(document).off("click"); //이벤트해제 } 
	//if(ev.target.nodeName!="TD" && ev.target.nodeName!="INPUT")fnMarketPriceEditCancel();
	if(ev.target.nodeName!="TD" && ev.target.nodeName!="INPUT"){
		len = $("#priceTable tbody tr td.editable input").length;
		if(len)fnMarketPriceEditSave($("#priceTable tbody tr td.editable input"),"",0);
	}
	
}); 
isCtrl = false;
$(window).on("keydown",function(ev){
	if(ev.keyCode==17)isCtrl=true;
});

$(window).on("keyup",function(ev){
	if(ev.keyCode==17)isCtrl=false;
});

MPTtemp=0;
infoTdCount=4;	//-- 추가한 지원 외 정보필드
//-- 취소를 위한 임시값 할당
function fnMarketPriceTemp(obj){
	MPTtemp = obj.val();
}

//-- 요금제 선택 / 저장
function fnMarketPriceSet(obj){
	objID = obj.attr("id");
	objNum = objID.replace("inPriceType","");		
	
	if(obj.val()){
		//-- 일반 요금 선택
		//-- 이전 요금제 검사
		
		preObjNum=0;
		if(objNum!=1){
			preObjNum = parseInt(objNum)-1;
		}
		
		if(preObjNum>0){
			preObj = $("#inPriceType"+preObjNum);
			if(!preObj.val()){
				alert("요금제는 순서대로 선택해주세요.");
				preObj.focus();
				obj.val('');
				return;
			}	
		}
		
		//-- 중복검사
		objVal = obj.val();
		for(k=1;k<=20;k++){
			if(k==objNum)continue;
			chkObj = $("#inPriceType"+k);
			if(chkObj.val()==objVal){
				alert(k + "번째 요금제에서 이미 지정한 요금제입니다.");
				obj.val(MPTtemp);
				return;
			}
		}
		fnMarketPriceTypeupdate(objNum,objVal);
	}else{
		//-- 사용안함 선택시
		if(!confirm("삭제하시겠습니까?\n\n삭제시 요금제" + objNum + " 이후 요금제들이 하나씩 앞으로 이동합니다.")){
			obj.val(MPTtemp);
			return;
		}
						
		//-- 요금제 재정렬
		for(k=parseInt(objNum);k<=20;k++){
			chkObj = $("#inPriceType"+k);
			v = $("#inPriceType"+(k+1)).val();
			chkObj.val(v);
			if(!v)break;
		}
		
		//-- 데이터 처리
		param="PTIDX=" + $("#inPTIDX").val() + "&mode=delMPT&inMPTnum="+objNum;
		$.ajax({
			url:'./json/priceInfo.html',
			method : 'post',
			cache:false,
			data : param,
			dataType:"json",
			success:function(data){
				if(data["result"]=="OK"){
					//-- 다음 작업 진행
					fnMarketPriceTypeupdate(objNum,0);
				}else{
					alert("오류가 발생했습니다.");
					return;
				}
			}
		});
		
	}
}

//-- 요금제 정보 업데이트
function fnMarketPriceTypeupdate(objNum,objVal){	
	//-- 업데이트할 값 준비
	MPT="";
	for(k=1;k<=20;k++){
		obj = $("#inPriceType"+k);
		if(obj.val()){
			if(MPT)MPT+="#";
			MPT+=obj.val();
		}else{
			break;
		}
	}
	
	if(!$("#inPTIDX").val()){
		alert("오류!");
		return;
	}	
	
	param="PTIDX=" + $("#inPTIDX").val() + "&mode=updateMPT&inMPT="+MPT;
	$.ajax({
		url:'./json/priceInfo.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				//-- 테이블 정리
				if(objVal)fnMarketPriceAdd(objNum);
				else fnMarketPriceDel(objNum);
			}else{
				alert("오류가 발생했습니다.");
				return;
			}
		}
	});
}

//-- 요금제 정보 추가(테이블 정리)
MPPtemp = "";
function fnMarketPriceAdd(num){
	tbl = $("#priceTable");
	td = tbl.find("thead tr").eq(0).find("th");
	tdLen = td.length;
	if(parseInt(num)+(infoTdCount+1)<=tdLen)return;
	str = '<th class="column-title w100px">지원금'+num+'</th>';
	tbl.find("thead tr").append(str);
	str = '<td class="editable">0</td>';
	tbl.find("tbody tr").append(str);
	
	tbl.find("tbody tr td.editable").unbind("click");
	tbl.find("tbody tr td.editable").click(function(){		
		fnMarketPriceEdit($(this));
	});
	fnMarketTableFocusInit();	//-- 포커스 액션 초기화
}

//-- 요금제 정보 삭제(테이블 정리)
function fnMarketPriceDel(num){
	tbl = $("#priceTable");
	num = parseInt(num);
	tbl.find("thead tr th").eq(num+infoTdCount).remove();	
	th = tbl.find("thead tr th");
	len = th.length;
	for(k=num+infoTdCount;k<len;k++){
		th.eq(k).html("지원금"+(k-infoTdCount));
	}
	tr = tbl.find("tbody tr");
	len = tr.length;
	for(k=0;k<len;k++){
		tr.eq(k).find("td").eq(num+(infoTdCount-1)).remove();
	}
}

//-- 정보 수정
function fnMarketPriceEdit(obj){
	v = obj.html();
	if(v.indexOf("input")>=0)return;
	//fnMarketPriceEditCancel();
	len = $("#priceTable tbody tr td.editable input").length;
	if(len)fnMarketPriceEditSave($("#priceTable tbody tr td.editable input"),"",0);

	MPPtemp = v;
	v = v.replaceAll(",","");
	str = "<input type='text' class='form-control input-sm' value='"+v+"' onkeydown='fnMarketPriceEditKeyAction(event.keyCode,$(this))'>";
	obj.html(str);
	$("#priceTable tbody tr td.editable input").focus();
}

//-- 정보 수정시 특수키 액션
function fnMarketPriceEditKeyAction(code,obj){
	//-- isCtrl 변수는 해당 페이지에서 제어
	if(code==27){fnMarketPriceEditCancel();}
	else if(code==13){fnMarketPriceEditSave(obj,"",0);}
	else if(code==9){fnMarketPriceEditSave(obj,"cell",1);}
	else if(code==37 && isCtrl){fnMarketPriceEditSave(obj,"cell",-1);}	//-- 왼쪽
	else if(code==38 && isCtrl){fnMarketPriceEditSave(obj,"row",-1);}	//-- 위쪽
	else if(code==39 && isCtrl){fnMarketPriceEditSave(obj,"cell",1);}	//-- 오른쪽
	else if(code==40 && isCtrl){fnMarketPriceEditSave(obj,"row",1);}	//-- 아래쪽
}

//-- 정보 수정완료/저장
function fnMarketPriceEditSave(obj,mv,dis){
	//-- 지원금 수정 저장
	objTd = obj.parent();
	objTr = objTd.parent();
	rowTd = objTr.find("td");
	objNum = rowTd.index(objTd);
	objIDX = rowTd.eq(0).find("input").val();
	objVal = obj.val();
	
	if(MPPtemp.replaceAll(",","") == objVal){		
		//-- 수정전과 값이 같음. 업데이트 안함
		fnMarketPriceEditCancel();
		fnMarketPriceEditMove(objTd,mv,dis);
	}else{
		//-- 값이 다름. 업데이트!
		param="PTIDX=" + $("#inPTIDX").val() + "&PIIDX=" + objIDX;
		param+="&mode=modelEdit";
		param+="&fieldNum="+objNum;
		param+="&fieldVal="+objVal;
		
		$.ajax({
			url:'./json/priceInfo.html',
			method : 'post',
			cache:false,
			data : param,
			dataType:"json",
			success:function(data){
				if(data["result"]=="OK"){
					
					//-- 업데이트 날짜 수정
					obj.parent().parent().find("td").eq(1).html(data["update"]);
					
					//-- 값 수정
					v = obj.val();
					if(!isNaN(v.replaceAll(",","")))v = fnCommify(v);
					obj.parent().html(v);
					
					if(mv){
						fnMarketPriceEditMove(objTd,mv,dis);
					}
					
				}else{
					alert("오류!");
					fnMarketPriceEditCancel();
				}
			}
		});
	}
}

//-- 정보 수정 칸 이동
firstEditable=2;	//-- 첫 수정 가능칸
function fnMarketPriceEditMove(objTd,mv,dis){
	
	objTr = objTd.parent();
	rowTd = objTr.find("td");
	objNum = rowTd.index(objTd);
	
	if(mv=="cell"){
		
		if(dis>0){
			//-- 오른쪽 이동
			if(rowTd.length-1>objNum){
				fnMarketPriceEdit(rowTd.eq(objNum+1));
			}else if(rowTd.length-1==objNum){
				//-- 다음줄 첫번째칸 이동
				objTbl = objTr.parent();
				trNum = objTbl.find("tr").index(objTr);
				if(trNum<objTbl.find("tr").length-1){
					targetTd = objTbl.find("tr").eq(trNum+1).find("td").eq(firstEditable);
					fnMarketPriceEdit(targetTd);
				}
			}
		}else if(dis<0){
			//-- 왼쪽이동
			if(objNum>firstEditable){
				fnMarketPriceEdit(rowTd.eq(objNum-1));
			}else if(firstEditable==objNum){
				//-- 윗줄 첫번째칸 이동
				objTbl = objTr.parent();
				trNum = objTbl.find("tr").index(objTr);
				if(trNum>0){
					targetTd = objTbl.find("tr").eq(trNum-1).find("td").eq(objTbl.find("tr").eq(trNum-1).find("td").length-1);
					fnMarketPriceEdit(targetTd);
				}
			}
		}
		
	}else if(mv=="row"){
		objTbl = objTr.parent();
		trNum = objTbl.find("tr").index(objTr);
		if(dis>0){			
			//-- 아랫쪽으로 이동			
			if(trNum<objTbl.find("tr").length-1){
				targetTd = objTbl.find("tr").eq(trNum+1).find("td").eq(objNum);
				fnMarketPriceEdit(targetTd);
			}
		}else if(dis<0){
			//-- 윗쪽으로 이동
			if(trNum>0){
				targetTd = objTbl.find("tr").eq(trNum-1).find("td").eq(objNum);
				fnMarketPriceEdit(targetTd);
			}
		}
	}
}

//-- 정보 수정 취소
function fnMarketPriceEditCancel(){
	//-- 지원금 수정 취소
	inputObj = $("#priceTable tbody tr td.editable input");
	inputTd = inputObj.parent();
	inputTd.html(MPPtemp);
	MPPtemp="";
}

//-- 모델 추가
function fnMarketModelAdd(){
	param="PTIDX=" + $("#inPTIDX").val() + "&mode=modelAdd";
	$.ajax({
		url:'./json/priceInfo.html',
		method : 'post',
		cache:false,
		data : param,
		dataType:"json",
		success:function(data){
			if(data["result"]=="OK"){
				//-- TR추가
				IDX = data["IDX"];
				tdLen = $("#priceTable tbody tr").eq(0).find("td").length;
				
				str='<tr class="even pointer">';
        str+='  <td class="a-center"><input type="checkbox" class="flat newTr" name="table_records" value="'+IDX+'"></td>';
        str+='  <td></td>';
        str+='  <td class="editable"></td>';
        str+='  <td class="editable">0</td>';
        for(k=1;k<=tdLen-infoTdCount;k++){
        	str+='	<td class="editable">0</td>';
      	}
        str+='</tr>';
				$("#priceTable tbody").append(str);
				fnTopFrameResize();
				
				$('input.flat.newTr').iCheck({
            checkboxClass: 'icheckbox_flat-green',
            radioClass: 'iradio_flat-green'
        });
        
        $("#priceTable tbody tr td.editable").unbind("click");
        $("#priceTable tbody tr td.editable").click(function(){		
					fnMarketPriceEdit($(this));
				});
        
			}else{
				alert("오류가 발생했습니다.");
				return;
			}
		}
	});
}

function fnMarketTableFocusInit(){
	$("#priceTable tbody tr td").unbind("mouseover");
	$("#priceTable tbody tr td").mouseover(function(){
		$("#priceTable tbody tr td.focused").removeClass("focused");
		objTd = $(this);
		objTr = objTd.parent();
		rowTd = objTr.find("td");
		objNum = rowTd.index(objTd);
		
		totRow = objTr.parent().find("tr");
		trLen = totRow.length;
		
		for(k=0;k<trLen;k++){
			trObj = totRow.eq(k);
			trObj.find("td").eq(objNum).addClass("focused");
		}
		
		rowTd.addClass("focused");
		
	});
}