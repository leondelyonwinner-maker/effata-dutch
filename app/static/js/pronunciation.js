// "Ucapkan kata ini" pronunciation-practice widgets. Feature-detects the Web
// Speech API's SpeechRecognition (speech-to-text) -- as of iOS 26, Safari
// does not reliably support this (WebKit's engine restriction), so on
// unsupported browsers the mic button is hidden and a short explanatory
// note takes its place. This is a proxy-scoring feature, not a hard
// requirement: text-to-speech ("Dengar", see tts.js) works everywhere.
//
// The audio itself never leaves the device -- only the browser's own
// transcript is POSTed to /pronunciation/score for similarity scoring.
(function () {
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;

  function submitAttempt(widget, transcript) {
    var resultEl = widget.querySelector(".pron-result");
    if (!resultEl || typeof htmx === "undefined") return;
    htmx.ajax("POST", "/pronunciation/score", {
      target: resultEl,
      swap: "innerHTML",
      values: {
        target_text: widget.getAttribute("data-target-text") || "",
        transcript: transcript,
        csrf_token: widget.getAttribute("data-csrf") || "",
      },
    });
  }

  function initWidget(widget) {
    if (widget.dataset.pronInitialized) return;
    widget.dataset.pronInitialized = "true";

    var micBtn = widget.querySelector("[data-pron-mic]");
    var unsupportedNote = widget.querySelector(".pron-unsupported");
    if (!micBtn) return;

    if (!SR) {
      micBtn.hidden = true;
      if (unsupportedNote) unsupportedNote.hidden = false;
      return;
    }

    var recognition = new SR();
    recognition.lang = "nl-NL";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    var listening = false;
    var label = micBtn.querySelector(".pron-mic-label");

    function reset() {
      listening = false;
      micBtn.classList.remove("pron-mic-listening");
      if (label) label.textContent = "Ucapkan kata ini";
    }

    recognition.onresult = function (event) {
      var transcript = event.results[0][0].transcript;
      submitAttempt(widget, transcript);
    };
    recognition.onend = reset;
    recognition.onerror = reset;

    micBtn.addEventListener("click", function () {
      if (listening) return;
      try {
        recognition.start();
        listening = true;
        micBtn.classList.add("pron-mic-listening");
        if (label) label.textContent = "Mendengarkan...";
      } catch (err) {
        reset();
      }
    });
  }

  function initAll(root) {
    root.querySelectorAll(".pron-widget").forEach(initWidget);
  }

  document.addEventListener("DOMContentLoaded", function () {
    initAll(document);
  });
  document.body.addEventListener("htmx:afterSwap", function (event) {
    if (event.target) initAll(event.target);
  });
})();
