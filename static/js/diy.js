time001 = document.getElementById('time001');
animation001 = document.getElementById('animation001');

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
