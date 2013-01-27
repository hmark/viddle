$(document).ready(function(){
    var term = getUrlVars()["term"];
    
    if (term != "")
        $(".searchfield").val(term);

    $('.video').hide();
    $('.button').click(toggleVideo);

    decodeSearchString();
});

function getUrlVars(){
    var vars = [], hash;
    var hashes = decodeURI(window.location.href).slice(window.location.href.indexOf('?') + 1).split('&');
    
    for(var i = 0; i < hashes.length; i++){
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    
    return vars;
}

function toggleVideo(){
    video = $(this).siblings("div.video");

   if (video.is(":visible")){
        $(this).text("SHOW VIDEO")
    }
    else{
        $(this).text("HIDE VIDEO")
    }

    video.slideToggle("slow")
}

function decodeSearchString(){
    var field = $(".searchfield");
    var encoded = field.val();
    field.val(decodeURIComponent(encoded.replace(/\+/g,  " ")));

     console.log("test", field, encoded, field.text)
}
