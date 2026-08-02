// External script (not an inline hx-on attribute) so it works under a strict
// Content-Security-Policy with no 'unsafe-eval'/'unsafe-inline' script-src.
document.addEventListener("htmx:afterRequest", function (event) {
  if (event.target && event.target.id === "chat-form") {
    event.target.reset();
    var log = document.getElementById("chat-log");
    if (log) {
      log.scrollTop = log.scrollHeight;
    }
  }
});
