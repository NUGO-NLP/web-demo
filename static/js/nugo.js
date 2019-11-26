var radio_gs_btn = document.getElementById('gyeongsang');
var radio_jl_btn = document.getElementById('jeolla');
var recognition_btn = document.getElementById('recognition');
var translate_btn = document.getElementById('translate');
var synthesis_btn = document.getElementById('synthesis');
var standard_sent = document.getElementById('standard');
var dialect_sent = document.getElementById('dialect');

var mobile = (/iphone|ipad|ipod|android/i.test(navigator.userAgent.toLowerCase()));

standard_sent.textContent = '안녕하세요 NUGO 입니다.'
dialect_sent.textContent = '안녕하십니꺼 NUGO 입니더'

if(!mobile) {
    var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition
    var recognition = new SpeechRecognition();
}
var synthesis = window.speechSynthesis;
var voices = synthesis.getVoices();
var utterance = new SpeechSynthesisUtterance('');

for(i = 0; i < voices.length ; i++) {
    if(voices[i].name === 'Google 한국의') {
        utterance.voice = voices[i];
        break;
    }
}

if(!mobile) {
    recognition.interimResults = true;
    recognition.lang = 'ko-KR';
    recognition.maxAlternatives = 1;

    var startRecognition = function(stream) {
        recognition.onend = function() {
            console.log('recognition done.');
        }
        recognition.onresult = function(event_object_list) {
            var event_last_idx = event_object_list.results.length - 1;
            var transcript = event_object_list.results[event_last_idx][0].transcript;
            if(transcript == null) {
                return;
            }
            if(event_object_list.results[event_last_idx].isFinal == true) {
                standard_sent.textContent = transcript;
                standard_sent.style.color = '#000000';
                recognition.stop();
            }
            else {
                var transcript = '';
                for (var i = event_object_list.resultIndex; i < event_object_list.results.length; ++i) {
                    transcript += event_object_list.results[i][0].transcript;
                }
                standard_sent.textContent = transcript;
                standard_sent.style.color = '#666666';
            }
        };
        recognition.start();
    }

    recognition_btn.onclick = function() {
        navigator.mediaDevices.getUserMedia({ audio: true, video: false }).then(startRecognition);
    };
}
else {
    recognition_btn.onclick = function() {
        alert('Not available on mobile.');
    };
}

translate_btn.onclick = function() {
    var standard_text = standard_sent.value;
    var data = {
        'version':1,
        'action':{
            'parameters':{
                'sentence':{
                    'value':standard_text
                }
            }
        }
    }

    var xhr = new XMLHttpRequest();
    if(radio_gs_btn.checked == true) {
        xhr.open('POST', '/convertIntoGyeongsang');
    }
    else {
        xhr.open('POST', '/convertIntoJeolla');
    }
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(data));
    xhr.onload = function() {
        var dialect_text = JSON.parse(xhr.responseText)['output']['dialect_sentence'];
        dialect_sent.textContent = dialect_text;
    };
};

synthesis_btn.onclick = function() {
    utterance.text = dialect_sent.textContent;
    utterance.rate = 0.9;
    synthesis.speak(utterance);
}