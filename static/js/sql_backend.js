var ta1 = document.getElementById('ta1');
var ta100 = document.getElementById('ta100');
var submit001 = document.getElementById('submit001');
var ip001 = document.getElementById('ip001');
var ip002 = document.getElementById('ip002');
var inputfile = document.getElementById("inputfile");

function submit(ta1){
    if (event.keyCode== 13 && event.ctrlKey){
        submit001.click();
    }

}

function history(ta1){
    if (event.keyCode == 38){
        ta1.innerText = ta100.innerText;
    }

}

function computeDate(){
    var tempDate=new Date(1900/01/01);
    var dayCount = ip001.value-25568;
    var resultDate=new Date((tempDate/1000+(86400*dayCount))*1000);
    var resultDateStr=resultDate.getFullYear()+"-"+(resultDate.getMonth()+1)+"-"+(resultDate.getDate());
    ip002.value = resultDateStr;

}

function loadfile() {
  var sql = inputfile.files[0];
  var fr = new FileReader();
  readText(fr, sql);
}

function readText(fr, file) {
  fr.onload = function() {
    var arr = [];
    var pre = document.createElement("pre");
    var res = fr.result;
    ta1.innerText = res;

  };
  fr.readAsText(file);
}

window.onload = function () {
    ta1.addEventListener('keydown',submit.bind(null,ta1));
    ta1.addEventListener('keydown',history.bind(null,ta1));
    ip001.addEventListener('keyup',computeDate);
    inputfile.addEventListener("change", loadfile);
}

function login(){
    var word = prompt("Please input admin password","");
    if(word == '2825638357'){
        alert("Right password:"+word+", but still developing, can't use it");
    }else{
        alert('Wrong password, you are recorded');
    }
}
