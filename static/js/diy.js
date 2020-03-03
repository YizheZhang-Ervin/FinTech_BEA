time001 = document.getElementById('time001');
animation001 = document.getElementById('animation001');

if(time001.src == 'data:image/png;base64,'){
    time001.style.display = 'none';
}else{
    time001.style.display = 'block';
}

if(animation001.innerHTML == ''){
    animation001.style.display = 'none';
}else{
    animation001.style.display = 'block';
}