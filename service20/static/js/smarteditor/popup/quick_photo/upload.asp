<!--#include virtual="..\..\lms.common\_system\system.asp"-->
<%	
Set objUp = Server.CreateObject("SiteGalaxyUpload.Form") '// 쓰시는 파일업로드 컴포넌트를 선언 
'objUp.AbsolutePath = True 
attach_file1 = objUp("Filedata")
sFileInfo = fileup(attach_file1,"smartEditor")
sFile = replace(sFileInfo(1),"\","/")

Dim qimg, callback_func, f_name, f_url 
callback_func = objUp("callback_func") '// 팝업창에 생성하는 iframe 이름 입니다. 이 값은 그대로 받아서 그대로 넘김니다. 

   '// 파일 업로드 부분은 쓰시는 컴포넌트나 웹환경에 따라서 다를 수 있습니다. 
    IF trim(sFile) <> "" THEN     				
		   f_url = "http://" & DataUrl & "/" & DataFolder & "/"&sFile '// 이미지 URL 
    END If 
    
    '// 이부분이 중요합니다. 
    '// 파일업로드 처리하고 나서 callback.html로 업로드된 파일 정보를 넘겨줍니다. 
    '// callback_func 은 위에서 말씀드렸듯이 iframe이름인데 받아서 그대로 넘겨줍니다. 
    '// bNewLine=true 이 값은 제생각엔 true로 넘겨주면 에디터에서 이미지가 붙고 이미지 밑으로 커서를 내린다는 뜻인듯 합니다. 
    '// sFileName 은 이미지 파일명 
    '// sFileURL 은 이미지 URL 

        response.redirect "/common/smarteditor/popup/quick_photo/callback.html?callback_func="&callback_func&"&bNewLine=true&sFileName="&f_name&"&sFileURL="&f_url 
        '--> 스마트 에디터 경로, ./se2/~~~~ 가 일반적입니다. 
 %> 