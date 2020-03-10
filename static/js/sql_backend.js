var ta1 = document.getElementById('ta1');
var submit001 = document.getElementById('submit001');

function submit(event){
    if (event.keyCode== 13 && event.ctrlKey){
        submit001.click();
    }

}

window.onload = function () {
    ta1.addEventListener('keydown',submit)

}