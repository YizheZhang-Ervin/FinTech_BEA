function execjs(event){
    if (event.keyCode==13){
        let input1 = document.getElementById("input001");
        let output1 = document.getElementById("output001");
        let result1 = eval(input1.value);
        console.log(result1);
        output1.innerHTML = result1;
    }
}

function choose(name){
    let d1 = document.getElementById("div001")
    let d2 = document.getElementById("div002")
    if(name=="PythonShell"){
        d2.style.display="none";
        d1.style.display="block";
    }
    else if(name=="JavaScriptShell"){
        d1.style.display="none";
        d2.style.display="block";
    }
}