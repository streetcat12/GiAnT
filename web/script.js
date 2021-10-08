/*
async function emojiTest() {
    let n = await eel.stupidTest()();
    document.getElementById('emoji').innerHTML = n;
}
emojiTest();
*/

var width = 1;

eel.expose(move);
function move(t,time) {
	console.log('test');
	if (t/20 == 0) {
	    document.getElementById('emoji').innerHTML = '😆';
	} else if (t/20 == 1) {
	    document.getElementById('emoji').innerHTML = '🙂';
	} else if (t/20 == 2) {
	    document.getElementById('emoji').innerHTML = '😑';
	} else if (t/20 == 3) {
	    document.getElementById('emoji').innerHTML = '😠';
	} else if (t/20 == 4) {
	    document.getElementById('emoji').innerHTML = '😡';
	} else if (t/20 == 5) {
	    move(0,285);
	    document.getElementById('emoji').innerHTML = '🤬';
	    document.getElementById('title').innerHTML = '잠시 마음을 토닥여 주세요<br><br>';
	    setTimeout(function() {document.getElementById('emoji').innerHTML = '😆'; document.getElementById('title').innerHTML = 'Mindful Keyboard<br><br>';},30000);
	    //document.getElementById('title').innerHTML = 'Mindful Keyboard<br><br><br><br><br><br>';
	}
	var elem = document.getElementById('progressbar');
	var id = setInterval(frame, time);
	function frame() {
		if (width <= t) {
			if (width >= t) {
				clearInterval(id);
			} else {
				width++;
				elem.style.width = width + '%';
			}
		} else {
			if (width <= t) {
				clearInterval(id);
			} else {
				width--;
				elem.style.width = width + '%';
			}
		}
	}
}

function openLog() {
    document.getElementsByClassName('barBody')[0].style.display='none';
    document.getElementsByClassName('logBody')[0].style.display='inline';
    document.getElementsByClassName('reportBody')[0].style.display='none';
}

function openMain() {
    document.getElementsByClassName('barBody')[0].style.display='inline';
    document.getElementsByClassName('logBody')[0].style.display='none';
    document.getElementsByClassName('reportBody')[0].style.display='none';
}

function openReport() {
    document.getElementsByClassName('barBody')[0].style.display='none';
    document.getElementsByClassName('logBody')[0].style.display='none';
    document.getElementsByClassName('reportBody')[0].style.display='inline';
}
openMain();

eel.expose(giveList);
function giveList(t) {
    document.getElementsByClassName('sentenceList')[0].innerHTML = t;
}

var btnLog = document.getElementById('openLog');
btnLog.addEventListener('click', openLog);
var btnMain = document.getElementById('openMain');
btnMain.addEventListener('click', openMain);
var btnMain2 = document.getElementById('openMain2');
btnMain2.addEventListener('click', openMain);
var btnReport = document.getElementById('openReport');
btnReport.addEventListener('click', openReport);