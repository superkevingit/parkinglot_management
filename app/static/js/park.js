$(document).ready(function(){
    $("#license").keyup(function(){
        var license = $("#license").val();
        $.get("/FindByLicense",{'license':license}, function(data){
            for(val i = data.length-1; i>=0; i--){
                $('#license-result').append(data[i])
            };
        })
    });

    $("#license").keydown(function(){
        $('#license-result').empty();
    })

    $("#license").blur(function(){
        $('#license-result').empty();
    })
});


$('#license').keyup(function(){
    var query;
    query = $(this).val();
    $.get('/FindByTicket', {license: query}, function(data){
        $('#license').html(data);
    })
})
