<?require_once   $_SERVER["DOCUMENT_ROOT"] . "/_system/init.inc";

//기본 리다이렉트
echo $_REQUEST["htImageInfo"];


//-- callback 변수 재조절
//echo $_REQUEST["callback"];
$callback = str_replace("http://","",$_REQUEST["callback"]);
$callback = substr($callback,1);
$callback = substr($callback,strpos($callback,"/"));
//echo $callback;
//exit();

$url = $callback .'?callback_func='. $_REQUEST["callback_func"];
$bSuccessUpload = is_uploaded_file($_FILES['Filedata']['tmp_name']);
if ($bSuccessUpload) { //성공 시 파일 사이즈와 URL 전송
	
	$tmp_name = $_FILES['Filedata']['tmp_name'];
	$name = $_FILES['Filedata']['name'];
	
	
	$upPath = $_SERVER["DOCUMENT_ROOT"] . "/_DATA/Editor/" . $_SESSION["photoFolder"] . "/";
		
	if(!file_exists($upPath)){
		mkdir($upPath,0777);
		chmod($upPath,0777);
	}
	
	//저장되는 파일 이름 변형(중복 방지)
	$exe = explode(".",$name);
	$len = sizeof($exe);
	$exe = $exe[$len-1];
	$nweFile = date(time()) . "." . $exe;
	// 파일 중복 체크
	$cnt=0;
	while(file_exists($upPath .  $nweFile)){
		$cnt++;
		$nweFile = date(time()) . "(" . $cnt .")." . $exe;
	}
	
	$new_path = $upPath . $nweFile;
	
	//@move_uploaded_file($tmp_name, $new_path);
	fnImgResizeGD($tmp_name, $new_path,800,800);
		
	
	$url .= "&bNewLine=true";
	$url .= "&sFileName=".$nweFile;
	//$url .= "&size=". $_FILES['Filedata']['size'];
	//아래 URL을 변경하시면 됩니다.
	//$url .= "&sFileURL=/home15/_DATA/" . $_SESSION["photoFolder"] . "/". urlencode(urlencode($name);
	$url .= "&sFileURL=/_DATA/Editor/" . $_SESSION["photoFolder"] . "/". urlencode($nweFile);
	
} else { //실패시 errstr=error 전송
	$url .= '&errstr=error';
}
header('Location: '. $url);
?>