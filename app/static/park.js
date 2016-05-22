function getTicketOptions(car_type){
    $.ajax({
        type: "GET",
        url: "/ticket_list?car_type="+car_type,
        dataType: "json",
        success: function(data, textStatus){
            var TicketSelect = document.getElementById("id_ticket");
            for(var i=TicketSelect.options.length-1; i>-1; i--){
                TicketSelect[i] = null;}
            if(data.length>0){
                $("#id_ticket").show();
                for(i=0;i<data.length;i++){
                    TicketSelect.options[i] = new Option();
                    TicketSelect.options[i].text = data[i].label;
                    TicketSelect.options[i].value = data[i].label;}
            }else{
                    $("#id_ticket").hide();}
          }
        })
  }
