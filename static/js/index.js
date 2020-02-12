//详细地列举我所遇到的问题，以及别人给我的提示。
//在此，我感谢王慧老师对我的启发和帮助。下面的报告中，我还会具体地提到
//他们在各个方法对我的帮助。
//我的程序里中凡是引用到其他程序或文档之处，
//例如教材、课堂笔记、网上的源代码以及其他参考书上的代码段,
//我都已经在程序的注释里很清楚地注明了引用的出处。
//
//我从未没抄袭过别人的程序，也没有盗用别人的程序，
//不管是修改式的抄袭还是原封不动的抄袭。
//我编写这个程序，从来没有想过要去破坏或妨碍其他计算机系统的正常运转。
//<何玮>
function getXk(){
	var ml=$('#ml option:selected').val();
	$.ajax({
		url:"http://127.0.0.1:8000/getXk/",
		type:'POST',
		dataType:'json',
		async : false,
		data:{'mldm':ml},
		success:function(data){
			var len=data.xk.length;
			var html="<option>--选择学科--</option>";
			$.each(data.xk,function(i){
				html=html+'<option value='+this.dm+' >('+this.dm+')'+this.mc+'</option>';
				if(i==len-1)
				{
					$('#xk').html(html);
				}
			});
		},
		fail:function(){
			console.log("fail");
		}
	})
}

function getZy(){
	var xk=$('#xk option:selected').val();
	$.ajax({
		url:"http://127.0.0.1:8000/getZy/",
		type:'POST',
		dataType:'json',
		async : false,
		data:{'q':xk},
		success:function(data){
			var len=data.zy.length;
			var html="<option>--选择专业--</option>";
			$.each(data.zy,function(i){
				html=html+'<option value='+this+' >'+this+'</option>';
				if(i==len-1)
				{
					$('#zy').html(html);
				}
			});
		},
		fail:function(){
			console.log("fail");
		}
	})
}

function check(){
	var choice=0;
	if ($('#ssdm').val()!='--选择省市--') {
		choice++;
	}
	if ($('#dwmc').val()!='') {
		choice++;
	}
	if ($('#ml').val()!='--选择门类--') {
		choice++;
	}
	if ($('#zy').val()!='--选择专业--') {
		choice++;
	}
	if ($('#xxfs').val()!='') {
		choice++;
	}
	if ($('#xk').val()=='--选择学科--') {
		alert("请选择学科！");
		return false;
	}
	else if (choice<1) {
		alert("学科外必须再选择一项！");
		return false;
	}
	else{
		return true;
	}
}