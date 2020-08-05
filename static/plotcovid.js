function plotcovid() {
　　　　　// Buid query parameter
    var param = {};
    param["startdate"] = document.getElementById("start").value;
    param["enddate"] = document.getElementById("end").value;
    countries=document.getElementsByName("country");
    param["country"]=""
    for ( var i=0 ; i<countries.length ; ++i ){
        if(!countries[i].checked)continue;
        if(i==0){param["country"]+=countries[i].value;}
        else{param["country"]+='.'+countries[i].value;}
    }
    columns=document.getElementsByName("columns");
    for ( var i=0 ; i<columns.length ; ++i ){
        if(columns[i].checked){
            param["column"]=columns[i].value;
            break;
        }
    }
    per_milion= document.getElementById("per_million");
    if(per_milion.checked)param["per_milion"]=per_milion.value;
    var query = jQuery.param(param);

    // Query with a new parameter 
    $.get("/CovidGraph/plot/covid" + "?" + query, function(data) {
        document.getElementById("plotimg").src = data;
    });
};
//
// Register Event handler
//
document.getElementById("plot").addEventListener("click", function(){
    plotcovid();
}, false);
document.getElementById("start").addEventListener("change",plotcovid,false);
document.getElementById("end").addEventListener("change",plotcovid,false);
args=document.getElementsByName("country");
for ( var i=0 ; i<args.length ; ++i ){
    args[i].addEventListener("change",plotcovid,false);
}
args=document.getElementsByName("columns");
for ( var i=0 ; i<args.length ; ++i ){
    args[i].addEventListener("change",plotcovid,false);
}
args=document.getElementById("per_million");
args.addEventListener("change",plotcovid,false);
//最初
$( document ).ready(plotcovid)
