
var inputElement = document.getElementById("username");
var username = inputElement.value;
// Set a cookie
setCookie( "username", username, 1);

function setCookie(name, value, days) {
    var expires = "";
    if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + encodeURIComponent(value) + expires + "; path=/";
  }
  
  function getCookie(name) {
    var cookieName = name + "=";
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.indexOf(cookieName) === 0) {
        return decodeURIComponent(cookie.substring(cookieName.length));
      }
    }
    return null;
  }
  function setUsername(){
    var inputElement = document.getElementById("username");
    var username = inputElement.value;
    // Set a cookie
    setCookie( "username", username, 1);
  }
