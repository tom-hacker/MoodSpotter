
const token = "BQB8F9OznjDMoaxedjG1NvX5yXMpu8eEjkPoKZOtUrCFhEm5a535BGCSsc94NmgoI3X7ExETXa2C79n_GNa5Ws1-mmAteL9JX3dawu8fWnn8LbZ2_7yxcIZ9ekpI3xluFuvZUEWfCsn0PAv5VLnGAyxnI4IJkjX_i8m4tRPJTQ"
globalDeviceId = "";
const track_uri = "spotify:track:7xGfFoTpQ2E7fRF5lN10tr"

function initPlayer() {
  window.onSpotifyWebPlaybackSDKReady = () => {
    const player = new Spotify.Player({
      name: 'MoodSpotter Player',
      getOAuthToken: cb => { cb(token); }
    });
    // Error handling
    player.addListener('initialization_error', ({ message }) => { console.error(message); });
    player.addListener('authentication_error', ({ message }) => { console.error(message); });
    player.addListener('account_error', ({ message }) => { console.error(message); });
    player.addListener('playback_error', ({ message }) => { console.error(message); });

    // Playback status updates
    player.addListener('player_state_changed', state => { console.log(state); });

    // Ready
    player.addListener('ready', ({ device_id }) => {
      console.log('Ready with Device ID', device_id);
      globalDeviceId = device_id;
      //playSong(device_id, token, 'spotify:track:7xGfFoTpQ2E7fRF5lN10tr');

    });

    // Not Ready
    player.addListener('not_ready', ({ device_id }) => {
      console.log('Device ID has gone offline', device_id);
    });

    // Connect to the player!
    player.connect();
  }
}



function playFirstSong(uri) {
  playSong(globalDeviceId, token, uri);
}



// Play a specified track on the Web Playback SDK's device ID
function playSong(device_id, _token, trackUri) {
  $.ajax({
    url: "https://api.spotify.com/v1/me/player/play?device_id=" + device_id,
    type: "PUT",
    data: '{"uris": ["' + trackUri + '"]}',
    beforeSend: function (xhr) { xhr.setRequestHeader('Authorization', 'Bearer ' + _token); },
    success: function (data) {
      console.log(data)
    }
  });
}
