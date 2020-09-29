function calculateTotalValue(length) {
  var minutes = Math.floor(length / 60),
    seconds_int = length - minutes * 60,
    seconds_str = seconds_int.toString(),
    seconds = seconds_str.substr(0, 2),
    time = minutes + ':' + seconds

  return time;
}

function calculateCurrentValue(currentTime) {
  var current_hour = parseInt(currentTime / 3600) % 24,
    current_minute = parseInt(currentTime / 60) % 60,
    current_seconds_long = currentTime % 60,
    current_seconds = current_seconds_long.toFixed(),
    current_time = (current_minute < 10 ? "0" + current_minute : current_minute) + ":" + (current_seconds < 10 ? "0" + current_seconds : current_seconds);

  return current_time;
}

function initProgressBar(i) {
  var player = document.getElementById('player'+ i);
  var length = player.duration
  var current_time = player.currentTime;

  // calculate total length of value
  var totalLength = calculateTotalValue(length)
  jQuery(".end-time" + i).html(totalLength);

  // calculate current value time
  var currentTime = calculateCurrentValue(current_time);
  jQuery(".start-time" + i).html(currentTime);

  var progressbar = document.getElementById('seekObj' + i);
  progressbar.value = (player.currentTime / player.duration);
  progressbar.addEventListener("click", seek);

  if (player.currentTime == player.duration) {
    $('#play-btn'+ i).removeClass('pause');
  }

  function seek(evt) {
    var percent = evt.offsetX / this.offsetWidth;
    player.currentTime = percent * player.duration;
    progressbar.value = percent / 100;
  }
};

function initPlayers(num) {

  for (var i = 1; i <= num; i++) {
    let j = i;
    (function() {

      // Variables
      // ----------------------------------------------------------
      // audio embed object
      var playerContainer = document.getElementById('player-container' + i),
        player = document.getElementById('player' + i),
        isPlaying = false,
        playBtn = document.getElementById('play-btn' + i);



      // Controls Listeners
      // ----------------------------------------------------------
      if (playBtn != null) {
        playBtn.addEventListener('click', function() {
            togglePlay()
        });
      }



      // Controls & Sounds Methods
      // ----------------------------------------------------------
      function togglePlay(evt) {
                  console.log(j);

        if (player.paused === false) {
          player.pause();
          isPlaying = false;
          $('#play-btn' + j).removeClass('pause');

            $('#play-btn' + j).css({
            'background-image': 'url("http://www.lukeduncan.me/images/play-button.png")'
           });

        } else {
          player.play();
          $('#play-btn' + j).addClass('pause');
            $('#play-btn' + j).css({
            'background-image': 'url("http://www.lukeduncan.me/images/pause-button.png")'
           });
          isPlaying = true;
        }
      }
    }());
  }
}

function userListenEpisode(userId, episodeId){
    $.post('/listen', {
        userId: userId,
        episodeId: episodeId
    }).done(function(response) {
        console.log("it worked")
    }).fail(function() {
        console.log("error")
    });
}

function userFollowPodcast(podcastId, followers, isAlreadyFollowing){

    if ( isAlreadyFollowing == true ){
        $.post('/unfollow/' + podcastId, null)
        .done(function(response) {
            console.log("it worked")
        }).fail(function() {
            console.log("error")
        });
        $('#numberFollowers').text(parseInt(followers) - 1 + ' followers');
        let html = '<a href="javascript:userFollowPodcast('
                                + podcastId + ',' + (parseInt(followers) - 1) + ', false' +
                            ");\" ><button class='btn btn-default'>Follow</button></a>";
        $('#FollowButton').html(html);
    }
    else{
        $.post('/follow/' + podcastId, null)
        .done(function(response) {
            console.log("it worked")
        }).fail(function() {
            console.log("error")
        });
        $('#numberFollowers').text(parseInt(followers) + 1 + ' followers');
        let html = '<a href="javascript:userFollowPodcast('
                                + podcastId + ',' + (parseInt(followers) + 1) + ', true' +
                            ");\" ><button class='btn btn-default'>Unfollow</button></a>";
        $('#FollowButton').html(html);
    }
}



