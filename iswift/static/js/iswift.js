var dragapproved=false
var minrestore=0  //该变量表示窗口目前的状态，0表示初始化状态，1表示最大化状态
var initialwidth,initialheight
//若Client浏览器为IE5.0以上版本的
var ie5=document.all&&document.getElementById
//若Client浏览器为NetsCape6。0版本以上的
var ns6=document.getElementById&&!document.all
function drag_drop(e){
   	 if (ie5&&dragapproved&&event.button==1){
   		 document.getElementById("msgDiv").style.left=tempx+event.clientX-offsetx+"px"
   		 document.getElementById("msgDiv").style.top=tempy+event.clientY-offsety+"px"
   	 }
   	 else if (ns6&&dragapproved){
   		 document.getElementById("msgDiv").style.left=tempx+e.clientX-offsetx+"px"
   		 document.getElementById("msgDiv").style.top=tempy+e.clientY-offsety+"px"
   	 	}
    }
function initializedrag(e){
     offsetx=ie5? event.clientX : e.clientX
   	 offsety=ie5? event.clientY : e.clientY
   	 //document.getElementById("dwindowcontent").style.display="none" //此句代码可不要
   	 tempx=parseInt(document.getElementById("msgDiv").style.left)
   	 tempy=parseInt(document.getElementById("msgDiv").style.top)

   	 dragapproved=true
   	 document.getElementById("msgDiv").onmousemove=drag_drop
   	 }
function stopdrag(){
dragapproved=false;
document.getElementById("msgDiv").onmousemove=null;
//document.getElementById("dwindowcontent").style.display="" //extra
}
function create_folder(str,submit_url){
/*
	var files_list = document.getElementById("file_list_ui");
	
	var bgObj=document.createElement("li");//背景遮罩层
	bgObj.setAttribute('id','create_li');
	bgObj.setAttribute('class','browse-file');
	files_list.insertBefore(bgObj,files_list.getElementsByTagName("li")[0]);
	
	var files_list_li = document.getElementById
*/
	var files_list = document.getElementById("file_list_ui")
	var bgObj=document.createElement("li");//背景遮罩层
	bgObj.setAttribute('id','create_li');
	bgObj.setAttribute('class','browse-file');
	var li_list = files_list.getElementsByTagName("li")
	if(li_list.length>0)
	{
		if(li_list[0].id=="create_li")
		{	
			alert("请填写文件名称！")
			return
		}
		files_list.insertBefore(bgObj,li_list[0]);
	}
	else
		files_list.appendChild(bgObj);
	
	var folder_img_div = document.createElement("div");//背景遮罩层
	folder_img_div.setAttribute('class','filename-col');
	bgObj.appendChild(folder_img_div);
	
	var folder_img = document.createElement("img");//背景遮罩层
	folder_img.setAttribute('class','icon page_icon_file_32 page_icon_file_np page_icon_folder_32');
	folder_img.setAttribute('height','20px');
	folder_img.setAttribute('width','26px');
	folder_img.setAttribute('src','/static/img/icon_spacer.gif');
	folder_img_div.appendChild(folder_img);
	
	var folder_form = document.createElement("form");//背景遮罩层
	folder_form.setAttribute("id","form_newfolder");
	folder_form.setAttribute("method","post");
	folder_form.setAttribute("action",submit_url);
	folder_img_div.appendChild(folder_form);
	
	var csrf_token=document.createElement("input");//$csrf_token
    csrf_token.setAttribute("id","csrf_token");
    csrf_token.setAttribute("type","hidden");
    csrf_token.setAttribute("name","csrfmiddlewaretoken");
    csrf_token.setAttribute("value","$csrf_token");
    folder_form.appendChild(csrf_token);

	var file_form_div = document.createElement("div");
	file_form_div.setAttribute("class","file_form_div");
	var div_name = document.createElement("div");
	div_name.setAttribute("class","div_name");
	var folder_name = document.createElement("input");//背景遮罩层
	folder_name.setAttribute("id","id_name");
	folder_name.setAttribute("name","id_name");
	folder_name.setAttribute("type","text");
	folder_name.setAttribute('class','form-control');
	folder_name.setAttribute("maxlength","255");
	folder_name.setAttribute("value","新建文件夹");
	folder_name.setAttribute("autofocus","autofocus");
	folder_name.onfocus=function(){if(this.value=='新建文件夹'){this.value=''}}
	folder_name.onblur=function(){if(this.value==''){this.value='新建文件夹'}}
	div_name.appendChild(folder_name)
	file_form_div.appendChild(div_name);
	
	var div_btn = document.createElement("div");
	div_btn.setAttribute("class","div_btn  btn-group");
	
	var div_create_btn = document.createElement("div");
	div_create_btn.setAttribute("class","div_create_btn");
	var folder_create_btn = document.createElement("input");//背景遮罩层
	folder_create_btn.setAttribute('type','submit');
	folder_create_btn.setAttribute('value','创建');
	folder_create_btn.setAttribute('class',"btn btn-small btn-primary");
	
	
	var div_create_cancle = document.createElement("div");
	div_create_cancle.setAttribute("class","div_create_btn");
	var folder_create_cancle = document.createElement("input");//背景遮罩层
	folder_create_cancle.setAttribute('type','button');
	folder_create_cancle.onclick=function(){
		files_list.removeChild(bgObj);
              }
	folder_create_cancle.setAttribute('class',"btn btn-small btn-primary");
	folder_create_cancle.setAttribute('value','取消');
	div_create_cancle.appendChild(folder_create_cancle);
	div_btn.appendChild(div_create_cancle);
	div_create_btn.appendChild(folder_create_btn);
	div_btn.appendChild(div_create_btn);
	
	file_form_div.appendChild(div_btn);
	
	folder_form.appendChild(file_form_div);
}
function delete_form(str,submit_url){
	var msgw,msgh,bordercolor;
    msgw=400;//提示窗口的宽度
    msgh=240;//提示窗口的高度
    titleheight=25 //提示窗口标题高度
    bordercolor="#EEEEEE";//提示窗口的边框颜色
    titlecolor="#99CCFF";//提示窗口的标题颜色

    var sWidth,sHeight;
    sWidth=document.body.offsetWidth;
    sHeight=screen.height;
    var bgObj=document.createElement("div");//背景遮罩层
    bgObj.setAttribute('id','bgDiv');
    bgObj.style.position="fixed";
    bgObj.style.top="0";
    bgObj.style.background="#777";
    bgObj.style.filter="progid:DXImageTransform.Microsoft.Alpha(style=3,opacity=25,finishOpacity=75";
    bgObj.style.opacity="0.6";
    bgObj.style.left="0";
    bgObj.style.width="100%";
    bgObj.style.height="100%";
    bgObj.style.zIndex = "10000";
    document.body.appendChild(bgObj);

    var msgObj=document.createElement("div") //dialog层
    msgObj.setAttribute("id","msgDiv");
    msgObj.setAttribute("align","center");
    msgObj.setAttribute("class","boderclass");
    msgObj.style.background="white";
    msgObj.style.border="1px solid " + bordercolor;
    msgObj.style.position = "fixed";
    msgObj.style.left = "50%";
    msgObj.style.top = "30%";
    msgObj.style.font="12px/1.6em Verdana, Geneva, Arial, Helvetica, sans-serif";
    msgObj.style.marginLeft = "-225px" ;
    msgObj.style.marginTop = -75+document.documentElement.scrollTop+"px";
    msgObj.style.width = msgw + "px";
    msgObj.style.height =msgh + "px";
    msgObj.style.textAlign = "center";
    msgObj.style.lineHeight ="25px";
    msgObj.style.zIndex = "10001";

    var title=document.createElement("h4");//标题
    title.setAttribute("id","msgTitle");
    title.setAttribute("align","right");
    title.style.margin="0";
    title.style.padding="3px";
    title.style.background=bordercolor;
    title.style.filter="progid:DXImageTransform.Microsoft.Alpha(startX=20, startY=20, finishX=100, finishY=100,style=1,opacity=75,finishOpacity=100);";
    title.style.opacity="0.75";
    title.style.border="1px solid " + bordercolor;
    title.style.height="18px";
    title.style.font="12px Verdana, Geneva, Arial, Helvetica, sans-serif";
    title.style.color="white";
    title.style.cursor="pointer";  
    document.body.appendChild(msgObj);
    msgObj.appendChild(title);
      
    var closea=document.createElement("a");//关闭按钮
    closea.setAttribute("id","closea");
    closea.setAttribute("href","#");
    closea.style.color="black";
    closea.innerHTML="<img src='/static/img/famfamfam/cancel.png'>";
    title.appendChild(closea);
    closea.onclick=function(){
          document.body.removeChild(bgObj);
                document.getElementById("msgDiv").removeChild(title);
                document.body.removeChild(msgObj);
    }
      
      
      var txt=document.createElement("h4");//对话框提示
      txt.style.margin="1em 0"
      txt.setAttribute("id","msgTxt");
      txt.innerHTML=str;
      msgObj.appendChild(txt);
      var txt_p=document.createElement("p");//对话框提示
      txt_p.innerHTML="您的文件不会被立即删除，" +
		"您可以在<a href='/deletedfiles'>回收站</a>查看您删除的文件，" +
		"并在那里恢复您删除的文件。"+
		"删除文件后你不做任何处理，您的文件默认保留一个月。<br>"+
		"<strong>注意：</strong>删除的文件依然占据您的存储空间，"+
		"您可以到<a href='/deletedfiles'>回收站</a>，"+
		"永久删除您要彻底删除的文件，那样会节省您的存储空间。";
      msgObj.appendChild(txt_p);

      var urls = submit_url;
      var folder_form = document.createElement("form");
      folder_form.setAttribute("id","delete_form");
      folder_form.setAttribute("method","post");
      folder_form.setAttribute("action",urls);
      msgObj.appendChild(folder_form);
      
      var txtdiv=document.createElement("div");//对话框内容层
      txtdiv.setAttribute("id","txtdiv");
      folder_form.appendChild(txtdiv);
      
      var foot_div=document.createElement("div");
      foot_div.setAttribute("class","modal-footer");
      folder_form.appendChild(foot_div);
      
      var input_cancle=document.createElement("input");//提交按钮
      input_cancle.setAttribute("id","cancle-btn");
      input_cancle.setAttribute("type","button");
      input_cancle.setAttribute("value","取消");
      input_cancle.setAttribute("class","btn");
      input_cancle.style.margin="0 5px 0 0 ";
      input_cancle.onclick=function(){
          document.body.removeChild(bgObj);
                document.getElementById("msgDiv").removeChild(title);
                document.body.removeChild(msgObj);
      }
      foot_div.appendChild(input_cancle);
      
      var input_submit=document.createElement("input");//提交按钮
      input_submit.setAttribute("id","fat-btn");
      input_submit.setAttribute("type","submit");
      input_submit.setAttribute("value","删除");
      input_submit.setAttribute("class","btn btn-danger");
      input_submit.setAttribute("data-loading-text","Loading...");
      foot_div.appendChild(input_submit);
}
function dialog_form(str,submit_url){
	    

       var msgw,msgh,bordercolor;
       msgw=400;//提示窗口的宽度
       msgh=186;//提示窗口的高度
       titleheight=25 //提示窗口标题高度
       bordercolor="#EEEEEE";//提示窗口的边框颜色
       titlecolor="#99CCFF";//提示窗口的标题颜色
   
       var sWidth,sHeight;
       sWidth=document.body.offsetWidth;
       sHeight=screen.height;
       var bgObj=document.createElement("div");//背景遮罩层
       bgObj.setAttribute('id','bgDiv');
       bgObj.style.position="fixed";
       bgObj.style.top="0";
       bgObj.style.background="#777";
       bgObj.style.filter="progid:DXImageTransform.Microsoft.Alpha(style=3,opacity=25,finishOpacity=75";
       bgObj.style.opacity="0.6";
       bgObj.style.left="0";
       //bgObj.style.width=sWidth + "px";
       //bgObj.style.height=sHeight + "px";
       bgObj.style.width="100%";
       bgObj.style.height="100%";
       bgObj.style.zIndex = "10000";
       document.body.appendChild(bgObj);
   
       var msgObj=document.createElement("div") //dialog层
       msgObj.setAttribute("id","msgDiv");
       msgObj.setAttribute("align","center");
       msgObj.setAttribute("class","boderclass");
       msgObj.style.background="white";
       msgObj.style.border="1px solid " + bordercolor;
       msgObj.style.position = "fixed";
       msgObj.style.left = "50%";
       msgObj.style.top = "30%";
       msgObj.style.font="12px/1.6em Verdana, Geneva, Arial, Helvetica, sans-serif";
       msgObj.style.marginLeft = "-225px" ;
       msgObj.style.marginTop = -75+document.documentElement.scrollTop+"px";
       msgObj.style.width = msgw + "px";
       msgObj.style.height =msgh + "px";
       msgObj.style.textAlign = "center";
       msgObj.style.lineHeight ="25px";
       msgObj.style.zIndex = "10001";
   
         var title=document.createElement("h4");//标题
         title.setAttribute("id","msgTitle");
         title.setAttribute("align","right");
         title.style.margin="0";
         title.style.padding="3px";
         title.style.background=bordercolor;
         title.style.filter="progid:DXImageTransform.Microsoft.Alpha(startX=20, startY=20, finishX=100, finishY=100,style=1,opacity=75,finishOpacity=100);";
         title.style.opacity="0.75";
         title.style.border="1px solid " + bordercolor;
         title.style.height="18px";
         title.style.font="12px Verdana, Geneva, Arial, Helvetica, sans-serif";
         title.style.color="white";
         title.style.cursor="pointer";
         //title.innerHTML="关闭";
         //title.setAttribute("onMousedown","initializedrag(event)");
         //title.setAttribute("onMouseup","stopdrag()");
         //title.setAttribute("onSelectStart","return false");     
         document.body.appendChild(msgObj);
         document.getElementById("msgDiv").appendChild(title);
         
         
         
  
         
         var closea=document.createElement("a");//关闭按钮
         closea.setAttribute("id","closea");
         closea.setAttribute("href","#");
         closea.style.color="black";
         closea.innerHTML="<img src='/static/img/famfamfam/cancel.png'>";
         document.getElementById("msgTitle").appendChild(closea);
         closea.onclick=function(){
             document.body.removeChild(bgObj);
                   document.getElementById("msgDiv").removeChild(title);
                   document.body.removeChild(msgObj);
                   }
         
         
         var txt=document.createElement("p");//对话框提示
         txt.style.margin="1em 0"
         txt.setAttribute("id","msgTxt");
         txt.innerHTML=str;
         document.getElementById("msgDiv").appendChild(txt);
         
 
         var form_test=document.createElement("form");//表单
         form_test.setAttribute("id","form_test");
         form_test.setAttribute("method","post");
         form_test.setAttribute("enctype","multipart/form-data")
         form_test.setAttribute("action",submit_url);
         document.getElementById("msgDiv").appendChild(form_test);
         
         var txtdiv=document.createElement("div");//对话框内容层
         txtdiv.setAttribute("id","txtdiv");
         form_test.appendChild(txtdiv);
         
         var csrf_token=document.createElement("input");//$csrf_token
         csrf_token.setAttribute("id","csrf_token");
         csrf_token.setAttribute("type","hidden");
         csrf_token.setAttribute("name","csrfmiddlewaretoken");
         csrf_token.setAttribute("value","$csrf_token");
         document.getElementById("txtdiv").appendChild(csrf_token);
         
         //var input_object_name=document.createElement("input");//本用来确定上传点object名字
         //input_object_name.setAttribute("id","input_object_name");
         //input_object_name.setAttribute("name","input_object_name");
         //input_object_name.setAttribute("type","text");
         //document.getElementById("form_test").appendChild(input_test);
         
         var id_fieldset=document.createElement("fieldset");//feildset标签
         id_fieldset.setAttribute("id","id_fieldset");
         form_test.appendChild(id_fieldset);
 
         var id_name=document.createElement("input");//container name ,object name 等
         id_name.setAttribute("id","id_name");
         id_name.setAttribute("name","id_name");
         id_name.setAttribute("type","text");
         id_name.setAttribute("maxlength","255");
         document.getElementById("id_fieldset").appendChild(id_name);         
         
         var id_name=document.createElement("input");//method?上传object
         id_name.setAttribute("id","id_method");
         id_name.setAttribute("name","method");
         id_name.setAttribute("type","hidden");
         id_name.setAttribute("value","UploadObject");
         document.getElementById("id_fieldset").appendChild(id_name);  
         var id_name=document.createElement("input");//method?上传到哪个container
         id_name.setAttribute("id","id_container_name");
         id_name.setAttribute("name","container_name");
         id_name.setAttribute("type","hidden");
         id_name.setAttribute("value","TEST1");
         document.getElementById("id_fieldset").appendChild(id_name);
         
         var id_object_file=document.createElement("input");//文件标签
         id_object_file.setAttribute("id","id_object_file");
         id_object_file.setAttribute("name","id_object_file");
         id_object_file.setAttribute("type","file");
         document.getElementById("id_fieldset").appendChild(id_object_file);
         
         var foot_div=document.createElement("div");
         foot_div.setAttribute("class","modal-footer");
         form_test.appendChild(foot_div);
         
         var input_submit=document.createElement("input");//提交按钮
         input_submit.setAttribute("id","fat-btn");
         input_submit.setAttribute("type","submit");
         input_submit.setAttribute("value","提交");
         input_submit.setAttribute("class","btn btn-primary");
         input_submit.setAttribute("data-loading-text","Loading...");
         foot_div.appendChild(input_submit);
         
         var input_cancle=document.createElement("input");//提交按钮
         input_cancle.setAttribute("id","cancle-btn");
         input_cancle.setAttribute("type","button");
         input_cancle.setAttribute("value","取消");
         input_cancle.setAttribute("class","btn");
         input_cancle.style.margin="0 0 0 5px ";
         input_cancle.onclick=function(){
        	 document.body.removeChild(bgObj);
             document.getElementById("msgDiv").removeChild(title);
             document.body.removeChild(msgObj);
         }
         foot_div.appendChild(input_cancle);
}