function attack(){
    window.close();
    window.location="about:blank";
}

function click(e) {
    if (document.all) {
        if (event.button==2||event.button==3) {
            alert("Welcome here");
            οncοntextmenu='return false';
        }
    }
    if (document.layers) {
        if (e.which == 3) {
            οncοntextmenu='return false';
        }
    }
}

if (document.layers) {
    attack();
    document.captureEvents(Event.MOUSEDOWN);
}

document.οnmοusedοwn=click;
document.oncontextmenu = new Function("return false;")
document.onkeydown =document.onkeyup = document.οnkeypress=function(){
    if(window.event.keyCode == 123) {
        attack();
        window.event.returnValue=false;
        return(false);
    }
}