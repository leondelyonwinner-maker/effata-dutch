// Optional mic-to-text dictation for the Gesprek input field. Feature-detects
// SpeechRecognition (unsupported on iOS Safari as of iOS 26 -- see
// pronunciation.js for the same caveat) and hides the mic button entirely
// when unavailable, showing a one-line note instead. Typing always works
// regardless of browser support.
(function () {
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  var micBtn = document.getElementById("chat-mic-btn");
  var input = document.getElementById("chat-input");
  var unsupportedNote = document.getElementById("chat-mic-unsupported");
  if (!micBtn || !input) return;

  if (!SR) {
    if (unsupportedNote) unsupportedNote.hidden = false;
    return;
  }

  micBtn.hidden = false;

  var recognition = new SR();
  recognition.lang = "nl-NL";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;
  var listening = false;

  function reset() {
    listening = false;
    micBtn.classList.remove("chat-mic-listening");
  }

  recognition.onresult = function (event) {
    input.value = event.results[0][0].transcript;
    input.focus();
  };
  recognition.onend = reset;
  recognition.onerror = reset;

  micBtn.addEventListener("click", function () {
    if (listening) return;
    try {
      recognition.start();
      listening = true;
      micBtn.classList.add("chat-mic-listening");
    } catch (err) {
      reset();
    }
  });
})();
