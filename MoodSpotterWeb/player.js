
const token = "BQCAxv-lWJxA4FlfJiI6o54Ohqw4hJK8v4v0eLqmVQS3EJ1VfhKjOalqbbA0nAYPhVI9RkD2_WZllmxCWGV0UYzNii7-m1_7iKEmGzaT4LslTl-RWV0h4nUaA-eP10Pol8EtfdtqFF7lStA1ZNbCJ5Xow-BUyq4abzMlLsHLUg"
globalDeviceId = "";
const track_uri = "spotify:track:7xGfFoTpQ2E7fRF5lN10tr"



window.onSpotifyWebPlaybackSDKReady = () => {
  const token = 'BQCAxv-lWJxA4FlfJiI6o54Ohqw4hJK8v4v0eLqmVQS3EJ1VfhKjOalqbbA0nAYPhVI9RkD2_WZllmxCWGV0UYzNii7-m1_7iKEmGzaT4LslTl-RWV0h4nUaA-eP10Pol8EtfdtqFF7lStA1ZNbCJ5Xow-BUyq4abzMlLsHLUg';
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


function playFirstSong() {
  playSong(globalDeviceId, token, track_uri);
}

function playSecondSong() {
  playSong(globalDeviceId, token, "spotify:track:0mjAU3yKR1QnXnHtjGJqTM")
}



function rabbitMQ() {

  var moduleName = 'node_modules/amqplib/callback_api';
  require([moduleName], function(rabbitmqModule){
      // do something with fooModule


  })


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
