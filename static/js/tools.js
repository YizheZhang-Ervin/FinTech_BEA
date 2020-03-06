//invoke camera
let video = document.getElementById("video");
    function getMedia() {
        let constraints = {
            video: {width: 350, height: 350},
            audio: true
        };
        if(navigator.mediaDevices.getUserMedia(constraints)=='undefined'){
            alert("can't use media devices!");
        }else{
            var promise = navigator.mediaDevices.getUserMedia(constraints);
        }
        promise.then(function (MediaStream) {
            video.srcObject = MediaStream;
            video.play();
        }).catch(function (PermissionDeniedError) {
            console.log(PermissionDeniedError);
        })
    }
    function takePhoto() {
        let canvas = document.getElementById("canvas");
        let ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, 350, 350);
    }

// system parameters
function showParameters(){
var textarea = document.getElementById('ta001');
var w=window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
var h=window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
var aw = screen.availWidth;
var ah = screen.availHeight;
var host = location.hostname;
var path = location.pathname;
var port = location.port;
var protocol = location.protocol;
var browsernum = navigator.appCodeName;
var browsername = navigator.appName;
var browserversion = navigator.appVersion;
var hardware = navigator.platform;
var useragent = navigator.userAgent;
var language = navigator.systemLanguage;
var data=
'> port: '+port+'&#10;'
+'> host: '+host+'&#10;'
+'> protocol: '+protocol+'&#10;'
+'> path: '+path+'&#10;'
+'> screen width: '+w + '&#10;'
+'> screen height: '+h+'&#10;'
+'> screen available width: '+aw+'&#10;'
+'> screen available height: '+ah+'&#10;'
+'> browser number: '+browsernum+'&#10;'
+'> browser name: '+browsername+'&#10;'
+'> hardware platform: '+hardware+'&#10;'
+'> language: '+language+'&#10;'
+'> browser version/user agent: '+'&#10;&nbsp;&nbsp;&nbsp;'+browserversion+'&#10;';
textarea.innerHTML = data;
}