let chunks = [];
let mediaRecorder;

navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.onstart = function() {
      chunks = [];
    }

    mediaRecorder.ondataavailable = function(e) {
      chunks.push(e.data);
    }

    mediaRecorder.onstop = function() {
      let blob = new Blob(chunks, { 'type' : 'audio/ogg; codecs=opus' });
      let url = URL.createObjectURL(blob);
      let a = document.createElement("a");
      document.body.appendChild(a);
      a.style = "display: none";
      a.href = url;
      a.download = 'sample.ogg';
      a.click();
      window.URL.revokeObjectURL(url);
    }

    document.querySelector('#start').onclick = function() {
      mediaRecorder.start();
      this.disabled = true;
      document.querySelector('#stop').disabled = false;
    }

    document.querySelector('#stop').onclick = function() {
      mediaRecorder.stop();
      this.disabled = true;
      document.querySelector('#start').disabled = false;
    }
  })
  .catch(err => console.log('Uh oh... ' + err));
