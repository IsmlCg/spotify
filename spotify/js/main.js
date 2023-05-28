URL = "spotify/mp3/";
function playSong( songUrl ) {
  var audioPlayer = document.getElementById('audioPlayer');
  var play = document.getElementById('play');
  play.src = get_mp3_url( songUrl );
  audioPlayer.load();
  audioPlayer.play();
}

function get_mp3_url( songUrl ){
  return URL + songUrl;
}

var playData =null;
create_Playlist( true )
function create_Playlist( start = false ) {
  var data = {
    start: start
  };

  fetch('/createplaylist', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(  data => {
    if (typeof data.error === 'undefined') {
      console.log( data);
      playData = data;
      addPlaylists( data['number'] )
      
      getSonds();
    }else{
      redirectToPage(); 
    }
    // Handle the response data
  })
  .catch(error => {
    console.error('Error:', error);
    redirectToPage(); 
    // Handle the error
  });
}

function addPlaylists( number ) {
  var container = document.getElementById("all-play-lists");
  html = "";
  // Clear the container
  container.innerHTML = "";
  for (let i = number; i >0 ; i--) {
     html += " <div class='list' id='list-"+i+"' onclick='setPlayListsSongs( "+i+" ); '> My Playlist # " + i +"</div>"
  }
  container.insertAdjacentHTML("beforeend",  html );
}

function playlistSonds( number ) {
  var data = {
    number : number
  };

  fetch('/playlistsonds', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(  data => {
    if (typeof data.error === 'undefined') {
      console.log( data);    
      data = Array.from(Object.values(data));
      loadPlayListSongs( data )
    }else{
      redirectToPage(); 
    }
    
    // playData = data;
    // Handle the response data
  })
  .catch(error => {
    console.error('Error:', error);
    redirectToPage();
    // Handle the error
  });
}





// -------------------------------------
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




function setPlayListsSongs( number ){
  // Set a cookie
  var container = document.getElementById("play-list-tittle");
  html = "My Playlist # " + number;
  // Clear the container
  container.innerHTML = "";
  document.getElementById("play-song-template").innerHTML=""; 
  container.insertAdjacentHTML("beforeend",  html );

  setCookie( "number", number, 1);
  playlistSonds( number )
}

function loadPlayListSongs( data ){
  var myTemplate = $.templates("#playSongTmpl");
    app = {
      data: data
    };  
  var html = myTemplate.render(app);
  $("#play-song-template").html(html);
}

function loadSongs( data ){
  var myTemplate = $.templates("#songListTmpl");
    app = {
      data: data
    };  
  var html = myTemplate.render(app);
  $("#songs-list").html(html);
}

function getSonds() {
  var data = {
    data : 'null'
  };
  fetch('/songs', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(  data => {
    if (typeof data.error === 'undefined') {
      console.log( data);
      loadSongs( data );
    }else{
      redirectToPage(); 
    }
    
    // playData = data;
    // Handle the response data
  })
  .catch(error => {
    console.error('Error:', error);
    redirectToPage();
    // Handle the error
  });
}

function addSongs( name, filename, description ){
  var data = {
    description: description,
    filename: filename,
    name: name
  };
  fetch('/addsong', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(  data => {
    if (typeof data.error === 'undefined') {
      console.log( data);
      data = Array.from(Object.values(data));
      loadPlayListSongs( data );
    }else{
      redirectToPage(); 
    }
    
  })
  .catch(error => {
    console.error('Error:', error);
    redirectToPage();
    // Handle the error
  });
}

function findSongs(){
  var data = {
    find_song: document.getElementById('find-song').value
  };
  fetch('/findsongs', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(  data => {
    
    if (typeof data.error === 'undefined') {
      console.log( data);
      loadSongs( data );
    }else{
      redirectToPage(); 
    }
  })
  .catch(error => {
    console.error('Error:', error);
    redirectToPage();
    // Handle the error
  });
}

function redirectToPage() {
  alert('Token has expired')
  window.location.href = "index";
}