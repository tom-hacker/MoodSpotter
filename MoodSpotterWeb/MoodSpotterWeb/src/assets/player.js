
const token = "BQDpeC5gbDZWVG3D_1yYD6R6YnIqYQeLIHWdV6o2rba-2PIDlVlH3E65rzWEaKaOof_JJ7FX-2nRnTPd7uBou_k4QUMK1f_6tdDNaPKF6vdoX0zq6vIk7XuITbR5-sh8UaThYDb2R8Fs9HgA9SZHTfuXbRn--tqWjznYb99P4Q";
moodSpotterDevicdId = "";

currTrack = "";
currArtist = "";
currAlbumImg = ""

function initPlayer() {
  window.onSpotifyWebPlaybackSDKReady = () => {
    const player = new Spotify.Player({
      name: 'MoodSpotter Player',
      getOAuthToken: cb => { cb(token); }
    });

    //error handling
    player.addListener('initialization_error', ({ message }) => { console.error(message); });
    player.addListener('authentication_error', ({ message }) => { console.error(message); });
    player.addListener('account_error', ({ message }) => { console.error(message); });
    player.addListener('playback_error', ({ message }) => { console.error(message); });

    //get status updates
    player.addListener('player_state_changed', state => { console.log(state); this.parseTrack(state); });

    //player not ready
    player.addListener('ready', ({ device_id }) => {
      console.log('Ready with Device ID', device_id);
      moodSpotterDevicdId = device_id;
    });

    //player not ready
    player.addListener('not_ready', ({ device_id }) => {
      console.log('Device ID has gone offline', device_id);
    });

    //player connected
    player.connect();
  }
}

//for external call
function playSong(uri) {
  playSongInternal(moodSpotterDevicdId, token, uri);
}


function parseTrack(uri) {
  if (uri != null) {
    this.currTrack = uri.track_window.current_track.name;
    this.currArtist = uri.track_window.current_track.artists[0].name;
    this.currAlbumImg = uri.track_window.current_track.album.images[0].url;
  }
}

function getTrackName() {
  return this.currTrack;
}

function getArtist() {
  return this.currArtist;
}

function getAlbumImg() {
  return this.currAlbumImg;
}

//play song with MoodSpotterPlayer
function playSongInternal(device_id, _token, trackUri) {
  $.ajax({
    url: "https://api.spotify.com/v1/me/player/play?device_id=" + device_id,
    type: "PUT",
    data: '{"uris": ["' + trackUri + '"]}',
    beforeSend: function (xhr) { xhr.setRequestHeader('Authorization', 'Bearer ' + _token); },
    success: function (data) {
    }
  });
}
