function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    return [year, month, day].join('-');
}

function addLoadIcon(){
    var episodes = $('.episodes')[0]
    var icon = document.createElement("div");
    var domString = `<div class="ui segment" style="margin-top: 50px;border: unset"> \
                      <div class="ui active inverted dimmer"> \
                        <div class="ui text loader">Loading</div> \
                      </div> \
                      <p></p> \
                    </div>`
    icon.innerHTML =  domString;
    icon.setAttribute("id", "icon-loading");
    episodes.appendChild(icon);
}

function addEpisode(r, c) {
  var comment = 'test'
  var episodes = $('.episodes')[0]
  var episode = document.createElement("div");
  var domString = episodeHtml(r, c)
  episode.innerHTML =  domString;
  episodes.appendChild(episode);
}

function episodeHtml(r, c){
        return `<img class="album-image" style="background-image: url(${ r.image })"></img> \
            <div class="episode"> \
            <div class="episode-date">${ formatDate(r.timestamp) }</div> \
            <p class="episode-name" style="margin-bottom: 5px"><a style="color: gray" href="podcast/${ r.podcast_id }">${ r.podcast_title  }</a></b></p> \
            <p class="episode-name"><a style="color: black" href="episode/${ r.episode_id }">${ r.episode_title}</a></b></p> \
            <div class="episode-description">${ r.description }</div> \
            <div class="audio-player"> \
                 <a href="javascript:userListenEpisode(
                    '${ r.user.id}',
                    '${ r.episode_id }'
                );">
                    <div id="play-btn${c}"></div> \
                </a> \
                <div class="audio-wrapper" id="player-container${c}"> \
                    <audio id="player${c}" ontimeupdate="initProgressBar(${c})"> \
                        <source src="${r.audio_link}" type="audio/mp3"> \
                    </audio> \
                </div> \
                <div class="player-controls scrubber"> \
                    <span id="seekObjContainer"> \
                          <progress id="seekObj${c}" value="0" max="1"></progress> \
                      </span> \
                    <br> \
                    <small style="float: left; position: relative; left: 15px;" class="start-time${c}"></small> \
                    <small style="float: right; position: relative; right: 20px;" class="end-time${c}"></small> \
                </div> \
            </div> \
        </div>`
}


$(window).scroll(function() {

   let paginationSize = 5

   if($(window).scrollTop() + $(window).height() >= $(document).height() - 100) {
            let currentLength = $('.episode').length
            if ( currentLength % paginationSize == 0 ){
                var currentPage = currentLength / paginationSize
                let nextPage = currentPage + 1
                let c = currentLength
                addLoadIcon()
                $.get('/my_feed?page=' + nextPage)
                .done(function(response) {
                    if ( response.length >= 0){
                        response.forEach( r =>
                            {
                                c = c + 1
                                addEpisode(r, c)
                            }
                        )
                    initPlayers(c)
                    }
                document.getElementById("icon-loading").remove();
                }).fail(function() {
                    console.log("error")
                });
            }
       }

});