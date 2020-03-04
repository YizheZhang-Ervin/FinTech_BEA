time001 = document.getElementById('time001');
animation001 = document.getElementById('animation001');
title001 = document.getElementById('title001');
diy001 = document.getElementById('diy001');
diychart = document.getElementById('diychart');

// set time trend plots
if(time001.src == 'data:image/png;base64,'){
    time001.style.display = 'none';
}else{
    time001.style.display = 'block';
}

// set animation plots
if(animation001.innerHTML == ''){
    animation001.style.display = 'none';
}else{
    animation001.style.display = 'block';
}

//set DIY plots
if(title001.innerHTML == 'Please select Date/Data which you need to analyze'){
    diy001.style.display = 'block';
}else{
    diy001.style.display = 'none';
}

if(diychart.src!='data:image/png;base64,'){
    diy001.style.display = 'block';
}