// FLOW Analytics Tracker — add to all pages
(function(){
  var uid = localStorage.getItem('flow_uid');
  if (!uid) { uid = Math.random().toString(36).substr(2,12); localStorage.setItem('flow_uid', uid); }
  // Detect user context
  var lang = localStorage.getItem('flow_lang') || navigator.language || 'unknown';
  var tz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
  function track(event, data) {
    var payload = {path: location.pathname, event: event, uid: uid, ref: document.referrer, data: data};
    // Attach lang/tz to pageview and duration
    if (event === 'pageview' || event === 'duration') {
      payload.data = Object.assign({lang: lang, tz: tz}, payload.data || {});
    }
    fetch('/api/event', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    }).catch(function(){});
  }
  // Pageview
  track('pageview');
  // Track time on page
  var startTime = Date.now();
  window.addEventListener('beforeunload', function() {
    var seconds = Math.round((Date.now() - startTime) / 1000);
    navigator.sendBeacon('/api/event', JSON.stringify({path: location.pathname, event: 'duration', uid: uid, data: {seconds: seconds, lang: lang, tz: tz}}));
  });
  // Expose for custom events
  window.flowTrack = track;
})();
