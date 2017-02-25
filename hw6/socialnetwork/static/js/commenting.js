function showDown(postid) {
    var clist = $(".commentList" + postid);
    if (clist.height() > 150) {
        $("#goDown" + postid).append("<h3>More Comments</h3>");
    }
}

function getComments(event) {
    console.log("getting comments");
    var postid = $(this).attr('post-id');
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/get-comments/" + postid,
        success: function(resp) {
            $(".commentList" + postid).empty()
            $.each(resp, function() {
                var commentBlock = '<li>' +
                    '<div class="commenterImage">' +
                    '<img src="' + this["img"] + '"/>' +
                    '</div>' +
                    '<div class="commentText">' +
                    '<p>' + this["comment"] + '</p>' +
                    '<span class="date sub-text">' + this["created_at"] +
                    '</span>' +
                    '</div>' +
                    '</li>';
                $(".commentList" + postid).append(commentBlock);
            });
        },
        error: function(xhr, status, errorThrown) {
            console.log("There is a problem loading the comment.");
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        }
    });
}

function addComment(e) {
    e.preventDefault();
    console.log("adding comment");
    var postid = $(this).attr('post-id');
    var form = $("#commentForm" + postid);
    console.log($(".commentList" + postid).height());
    showDown(postid);
    $.ajax({
        url: "/add-comment/" + postid,
        type: "POST",
        dataType: "json",
        data: form.serialize(),
        success: function(resp) {
            console.log('in success');
            $(".commentList" + postid).empty()
            $.each(resp, function() {
                var commentBlock = '<li>' +
                    '<div class="commenterImage">' +
                    '<img src="' + this["img"] + '"/>' +
                    '</div>' +
                    '<div class="commentText">' +
                    '<p>' + this["comment"] + '</p>' +
                    '<span class="date sub-text">' + this["created_at"] +
                    '</span>' +
                    '</div>' +
                    '</li>';
                $(".commentList" + postid).append(commentBlock);
            });
            form.trigger("reset");
        },
        error: function(xhr, status, errorThrown) {
            console.log("There is a problem when adding the comment.");
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        }
    });
}

$(document).ready(function() {
    console.log("ready!");
    $(".addComment").on("click", addComment);
    $(".getComments").on("click", getComments);
});
