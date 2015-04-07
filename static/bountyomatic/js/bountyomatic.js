//
// Utils
//
function setProgressBar(text) {
  var battletag = $("div.battletag");
  battletag.text(text);
  battletag.addClass("active");
  battletag.addClass("progress-bar-striped");
  battletag.addClass("progress-bar-warning");
}
function unsetProgressBar(text) {
  var battletag = $("div.battletag");
  battletag.text(text);
  battletag.removeClass("active");
  battletag.removeClass("progress-bar-striped");
  battletag.addClass("progress-bar");
  battletag.removeClass("progress-bar-warning");
}
//
// API
//
function getPlayerBattletag(callback) {
	$.ajax({
    url: "/api/player-battletag",
    dataType: 'json',
    success: function(data) {
      if (callback)
        callback(data);
      unsetProgressBar(data.battletag);
    },
    error: function(xhr, status, err) {
      console.error("/api/player-battletag", status, err.toString());
    },
  });
}
function getRegions(callback) {
  $.ajax({
    url: "/api/regions",
    dataType: 'json',
    success: function(data) {
      if (callback)
        callback(data);
    },
    error: function(xhr, status, err) {
      console.error("/api/regions", status, err.toString());
    }
  }); 
}
function getRealms(region, callback) {
  $.ajax({
    url: "/api/realms?region=" + region,
    dataType: 'json',
    success: function(data) {
      if (callback)
        callback(data);
    },
    error: function(xhr, status, err) {
      console.error("/api/realms?region=" + region, status, err.toString());
    }
  }); 
}
function getPlayerCharacters(callback) {
  $.ajax({
    url: "/api/player-characters",
    dataType: 'json',
    success: function(data) {
      if (callback)
        callback(data);
    },
    error: function(xhr, status, err) {
      console.error("/api/player-characters", status, err.toString());
    }
  });  
}