function getPosts() {
    var recentPostId = $(".posts").first().attr("id");
    $.ajax({
        url: '/update-post/' + recentPostId,
        type: "POST",
        dataType: "html",
        success: function(resp) {
            $(".postList").prepend(resp);
            console.log("updated posts: success");
        },
        error: function(xhr, status, errorThrown) {
            console.log("There is a problem when refreshing posts.");
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        }
    });
}

$(document).ready(function() {
    if ($(".posts").length > 0) {
        window.setInterval(function() {getPosts(); }, 5000);
    }
});
