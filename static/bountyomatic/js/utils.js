function getUrlParameter(sParam) {
  var sPageURL = window.location.search.substring(1);
  var sURLVariables = sPageURL.split('&');
  for (var i = 0; i < sURLVariables.length; i++) {
    var sParameterName = sURLVariables[i].split('=');
    if (sParameterName[0] == sParam) {
      return decodeURIComponent(sParameterName[1]) || true;
    }
  }
}
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
  // test that a given url is a same-origin URL
  // url could be relative or scheme relative or absolute
  var host = document.location.host; // host + port
  var protocol = document.location.protocol;
  var sr_origin = '//' + host;
  var origin = protocol + sr_origin;
  // Allow absolute or scheme relative URLs to same origin
  return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
    (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
    // or any other URL that isn't scheme relative or absolute i.e relative.
    !(/^(\/\/|http:|https:).*/.test(url));
}
$(function() {
  $.xhrPool = [];
  $.xhrPool.abortAll = function() {
    $(this).each(function(i, jqXHR) {   //  cycle through list of recorded connection
      jqXHR.abort();  //  aborts connection
      $.xhrPool.splice(i, 1); //  removes from list by index
    });
  };
  $.ajaxSetup({
    beforeSend: function(jqXHR, settings) {
      $.xhrPool.push(jqXHR);
      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        // Send the token to same-origin, relative URLs only.
        // Send the token only if the method warrants CSRF protection
        // Using the CSRFToken value acquired earlier
        var csrftoken = $.cookie('csrftoken');
        jqXHR.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
    complete: function(jqXHR) {
      var i = $.xhrPool.indexOf(jqXHR);   //  get index for current connection completed
      if (i > -1) $.xhrPool.splice(i, 1); //  removes from list by index
  }
  });

  $(window).on('location', function(e) {
    $.xhrPool.abortAll();
  });
});