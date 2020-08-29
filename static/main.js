// part of script inspired by https://github.com/addpipe/simple-recorderjs-demo
var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext; //audio context to help us record
const resultNode = document.getElementById('result');
const actionButton = document.getElementById('action');

function resultProcess(data) {
    resultNode.textContent = `Довжина тексту: ${data.length} \n
        Текст: ${data}
    `;
    actionButton.textContent = "Почати запис (3 сек)";
    actionButton.disabled = false;
}

function exportWAV(blob) {
    actionButton.textContent = "Обробляється..."
    var data = new FormData()
    data.append('file', blob);
    fetch(`./recognize`, { method: "POST", body: data })
        .then(response => response.text())
        .then(resultProcess);
}
function record() {

    var constraints = { audio: true, video: false }
    navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
        actionButton.textContent = "Запис..."
        actionButton.disabled = true;
        /*
            create an audio context after getUserMedia is called
            sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
            the sampleRate defaults to the one set in your OS for your playback device
        */
        audioContext = new AudioContext();

        /*  assign to gumStream for later use  */
        gumStream = stream;

        /* use the stream */
        input = audioContext.createMediaStreamSource(stream);

        /* 
            Create the Recorder object and configure to record mono sound (1 channel)
            Recording 2 channels  will double the file size
        */
        rec = new Recorder(input, { numChannels: 1 })

        //start the recording process
        rec.record()
        sleep(3000).then(stop);
    })
}


function stop() {
    rec.stop();

    //stop microphone access
    gumStream.getAudioTracks()[0].stop();

    //create the wav blob and pass it on to createDownloadLink
    rec.exportWAV(exportWAV);
}


const sleep = time => new Promise(resolve => setTimeout(resolve, time));

async function handleAction() {
    record();
}