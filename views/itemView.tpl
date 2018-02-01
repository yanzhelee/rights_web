<!DOCTYPE html>
<html lang="zh-CN">
<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet" href="../static/css/bootstrap.css"/>
    <link rel="stylesheet" href="../static/css/bootstrap-theme.css"/>
    <script src="../static/js/jquery-2.1.1.js"></script>
    <script src="../static/js/bootstrap.js"></script>
    <script src="../static/js/bootstrap-paginator.min.js"></script>

    <title>权力清单页面</title>
</head>
<body class="container">
<input type="hidden" id="data" value='{{data}}'/>
<div class="row">
    <div class="col-md-4" style="padding:10px">
        <h3 id="title"></h3>
        <p id="content"></p>
    </div>
    <div class="col-md-4" style="padding:10px">
        <select id="leftSelect" class="form-control" style="width:80%" onchange="selectClick(this)">
            <option value="dabiao">打标数据</option>
        </select>
        <ul></ul>
    </div>
    <div class="col-md-4" style="padding:10px">
        <select id="rightSelect" class="form-control" style="width:80%" onchange="selectClick(this)">
            <option value="dabiao">打标数据</option>
        </select>
        <ul></ul>
    </div>
</div>
</body>
<script type="text/javascript">
 var data ={};
$(document).ready(function(){
    data = JSON.parse($("#data").val());
    $("#title").html(data.content.title)
    $("#content").html(data.content.content);

    for(var version in data.rights){
        $("#leftSelect").append('<option value="'+version+'">'+version+'</option>');
        $("#rightSelect").append('<option value="'+version+'">'+version+'</option>');
    }

    //加载左侧数据
    var leftSelect = $("#leftSelect")[0];
    selectClick(leftSelect)
});

function selectClick(obj_){
    var obj = $(obj_);
    var selectValue = obj.val();
    var rights = []
    if(selectValue == "dabiao"){
        rights = data.content.rights
    }else{
        rights = data.rights[selectValue].rights
    }
    var liStr = "";
    for(var i=0;i<rights.length;i++){
        if(selectValue == "dabiao"){
            liStr+= "<li><a href='http://172.16.4.22:8081/?server=db&username=root&db=jiancy&edit=rights&where%5BID%5D="+rights[i][0]+"' target='_black'>"+rights[i][2]+"</a></li>";
        }else{
            liStr+= "<li><a href='http://172.16.4.22:8081/?server=db&username=root&db=jiancy&edit=rights&where%5BID%5D="+rights[i][0]+"' target='_black'>"+rights[i][2]+"("+rights[i][4]+")"+"</a></li>";
        }

    }
    var ulObj = $(obj.parent()).find("ul");
    ulObj.html(liStr);
}

</script>
</html>