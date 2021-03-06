function addComment(comment) {
  var ul = document.getElementById("list-comments");
  var li = document.createElement("li");
  //var domString = '<div class="container"><span class="intro">Hello</span> <span id="name"> World!</span></div>';
  var domString = '<div>' + comment + '</div>';
  li.innerHTML =  domString;
  ul.appendChild(li);
}

function addCommentNew(comment) {
  var parent = document.getElementsByClassName("comments")[0];
  var username = document.getElementsByClassName("username")[0].textContent;
  var photo = document.getElementsByClassName("profile-photo")[0].textContent;
  var div = document.createElement("div");
  parent.prepend(div);

  //var domString = '<div class="container"><span class="intro">Hello</span> <span id="name"> World!</span></div>';
  var id = $('[id^=comment]').length + 1;
  var domString = commentDOM(username, comment, false, id, photo);
  div.outerHTML =  domString;
}

function addReplyComment(commentId, message) {
  var parent = document.getElementById("replies" + commentId);
  var username = document.getElementsByClassName("username")[0].textContent;
  var photo = document.getElementsByClassName("profile-photo")[0].textContent;

  var div = document.createElement("div");
//  div.className = "reply-comments";
  parent.appendChild(div);

  //var domString = '<div class="container"><span class="intro">Hello</span> <span id="name"> World!</span></div>';
  var domString = commentDOM(username, message, true, null, photo);
  div.outerHTML =  domString;
}

function commentDOM(username, message, isReply, id, photo){
    if ( !isReply){
        return '<div class="comment" id="comment' + id + '"> \
                <a class="avatar"> \
                    <img id="avatar-image" style="border-radius: 50%" src=' + photo + ' /> \
                </a> \
                <div class="content"> \
                    <a class="author">' + username + '</a> \
                    <div class="metadata"> \
                        <span class="date">Just now</span> \
                    </div> \
                    <div class="text">' + message + ' \
                    </div> \
                    <div class="actions"> \
                        <a class="reply" id="reply' + id + '">Reply</a> \
                    </div> \
                    <div class="comments" id="replies' + id + '"> </div> \
                </div> \
            </div>';
    }
    return '<div class="comment"> \
                <a class="avatar"> \
                    <img id="avatar-image" style="border-radius: 50%" src=' + photo + ' /> \
                </a> \
                <div class="content"> \
                    <a class="author">' + username + '</a> \
                    <div class="metadata"> \
                        <span class="date">Just now</span> \
                    </div> \
                    <div class="text">' + message + ' \
                    </div> \
                </div> \
            </div>';
}

$(function() {
    $('#form-comment').on('submit', function(e) {
        //var data = $("#form-comment :input").serialize();
        e.preventDefault();
        var time = document.getElementsByClassName('start-time1')[0].textContent
        var episodeId = document.getElementsByClassName('episode-id')[0].textContent
        var message = document.getElementById('input').value
        console.log(time)
        console.log(episodeId)
        $.ajax({
            type: "POST",
            url: "/comments",
            data: { message: message, episodeId: episodeId, episodeTime: time },
            success: function(data){
               console.log(data['commentId'])
               var idBack = data['commentId']
               var idCommentFront = $('[id^=comment]').length;
               createElementWithCommentId(idCommentFront, idBack)
            },
        });
        addCommentNew(message);
        var id = $('[id^=comment]').length;
        replyForm(id)
        incrementNumberOfComments()
        deleteContentNewCommentPlaceHolder()
    });
});

function createElementWithCommentId(i,j){
  var parent = $('.ui')[0]
  var div = document.createElement("div");
  parent.prepend(div);
  var domString = '<div id="comment-id-backend' + i + '" hidden>' + j + '</div>'
  div.outerHTML =  domString;
}


function initReply(num){
    for (let i = 1; i <= num; i++) {
        $("#reply" + i).click(function(){
        console.log('click')

        let z = document.createElement('div');
        let domString = '<form class="ui reply form" id="reply-form' + i +'"> \
            <div class="field"> \
              <input id="textarea' + i + '" type="text" name="comment" placeholder="Write a reply" class="input-new-comment"> \
              <button class="ui button" id="add-reply' + i +'" type="submit" value="Submit">Reply</button> \
            </div> \
          </form>';
        z.innerHTML =  domString;
        $('#comment' + i)[0].appendChild(z)

        addReplyButton(i)
    });
    }
}

function replyForm(i){
    $("#reply" + i).click(function(){
        console.log('click')

        let z = document.createElement('div');
        let domString = '<form class="ui reply form" id="reply-form' + i +'"> \
            <div class="field"> \
              <input id="textarea' + i + '" type="text" name="comment" placeholder="Write a reply" class="input-new-comment"> \
              <button class="ui button" id="add-reply' + i +'" type="submit" value="Submit">Reply</button> \
            </div> \
          </form>';
        z.innerHTML =  domString;
        $('#comment' + i)[0].appendChild(z)

        addReplyButton(i)
    })
}


function addReplyButton(commentId){
    $('#add-reply' + commentId).click(function() {
        let message = $('#textarea'+commentId)[0].value
        addReplyComment(commentId, message)
        document.getElementById("reply-form" + commentId).remove();
        let id = parseInt(document.getElementById("comment-id-backend" + commentId).textContent);
        console.log(id)
         $.ajax({
            type: "POST",
            url: "/reply",
            data: { message: message, commentId: id},
        });
        incrementNumberOfComments()

    });
};

function incrementNumberOfComments(){
    let commentNumber = parseInt($('#comment-number-value')[0].innerHTML);
    $('#comment-number-value')[0].innerHTML = commentNumber + 1;
}

function deleteContentNewCommentPlaceHolder(){
    $('.input-new-comment')[0].value = ""
}

function RetweetEpisode(userId, episodeId, hasAlreadyTweeted){

    if ( hasAlreadyTweeted == true || hasAlreadyTweeted == 'True'){
        $.post('/cancel_retweet', { 'episodeId': episodeId})
        .done(function(response) {
            console.log("it worked")
        }).fail(function() {
            console.log("error")
        });
//        $('#numberFollowers').text(parseInt(followers) - 1 + ' followers');
        let html = '<a href="javascript:RetweetEpisode('
                                + userId + ',' + episodeId + ', false' +
                            ");\" ><button class='btn btn-default'>Retweet</button></a>";
        $('#RetweetButton').html(html);
    }
    else{
        $.post('/retweet', { 'episodeId': episodeId})
        .done(function(response) {
            console.log("it worked")
        }).fail(function() {
            console.log("error")
        });
//        $('#numberFollowers').text(parseInt(followers) + 1 + ' followers');
        let html = '<a href="javascript:RetweetEpisode('
                                + userId + ',' + episodeId + ', true' +
                            ");\" ><button class='btn btn-default'>Cancel Retweet</button></a>";
        $('#RetweetButton').html(html);
    }
}
