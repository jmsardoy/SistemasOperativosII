$(document).ready(function(){
	$("#cargarModulo").click(function(){
		$("#fileFormDiv").fadeIn("slow");
		$("#removeFormDiv").hide();
	});
	$("#removerModulo").click(function(){
		$("#fileFormDiv").hide();
		$("#removeFormDiv").fadeIn("slow");
	});
	$("#file").on("change",function(){
		$("#choose").html($(this).val());
	});
});