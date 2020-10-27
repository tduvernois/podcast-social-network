function FollowUser(userIdToFollow, followers, isAlreadyFollowing){

    if ( isAlreadyFollowing == true || isAlreadyFollowing == 'True'){
        $.post('/unfollow_user/' + userIdToFollow, null)
        .done(function(response) {
            console.log("it worked")
        }).fail(function() {
            console.log("error")
        });
//        $('#numberFollowers').text(parseInt(followers) - 1 + ' followers');
        let html = '<a href="javascript:FollowUser('
                                + userIdToFollow + ',' + userIdToFollow + ', false' +
                            ");\" ><button class='btn btn-default'>Follow</button></a>";
        $('#FollowButton').html(html);
    }
    else{
        $.post('/follow_user/' + userIdToFollow, null)
        .done(function(response) {
            console.log("it worked")
        }).fail(function() {
            console.log("error")
        });
//        $('#numberFollowers').text(parseInt(followers) + 1 + ' followers');
        let html = '<a href="javascript:FollowUser('
                                + userIdToFollow + ',' + userIdToFollow + ', true' +
                            ");\" ><button class='btn btn-default'>Unfollow</button></a>";
        $('#FollowButton').html(html);
    }
}