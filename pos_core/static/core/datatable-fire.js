
// Script for deleting data
function delete_data(id){
    var r = confirm("You are about to delete this data.. Click OK if you sure!!");
    if (r == true) {
    $.ajax({
        url: window.location.href,
        data: { id: id} ,
        type: 'DELETE',
        success: function(result) {
            location.reload();
        }
        });
    } else {

    }
    
}
// Script for editing data
function create_new(){
    var url = window.location.href+"form/"
    url = url.replace("#", "")
    url = url.replace("_=_", "")
    window.location.replace(url);
}
// Script for editing data
function edit_data(id){
    var url = window.location.href+"form/?edit="+id
    url = url.replace("#", "")
    url = url.replace("_=_", "")
    window.location.replace(url);
}
// Script to include csrf on post method
function csrfSafeMethod(method) {

    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
