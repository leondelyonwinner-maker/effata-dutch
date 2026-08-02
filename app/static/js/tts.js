// Client-side Dutch text-to-speech ("Dengar" buttons). Uses the browser's
// SpeechSynthesis API which -- unlike SpeechRecognition -- works reliably
// on iOS Safari, so this is safe to wire up unconditionally on every page.
// Event delegation on document.body means HTMX-swapped-in buttons work
// automatically with no re-init step.
(function () {
  function speakDutch(text) {
    if (!("speechSynthesis" in window) || !text) return;
    // Coach messages carry English glosses/corrections in parentheses --
    // strip them so the nl-NL voice doesn't try to read English aloud.
    var clean = text.replace(/\([^)]*\)/g, "").trim();
    if (!clean) return;
    window.speechSynthesis.cancel();
    var utterance = new SpeechSynthesisUtterance(clean);
    utterance.lang = "nl-NL";
    utterance.rate = 0.9;
    window.speechSynthesis.speak(utterance);
  }

  document.body.addEventListener("click", function (event) {
    var btn = event.target.closest("[data-speak-nl]");
    if (!btn) return;
    speakDutch(btn.getAttribute("data-speak-nl"));
  });
})();
