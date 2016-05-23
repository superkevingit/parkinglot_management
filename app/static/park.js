function getTicketOptions(car_type){
    $.ajax({
        type: "GET",
        url: "/ticket_list?car_type="+car_type,
        dataType: "json",
        success: function(data, textStatus){
            var TicketSelect = document.getElementById("id_tickettype");
            if(data.length>0){
                $("#id_tickettype").show();
                for(i=0;i<data.length;i++){
                    TicketSelect.options[i] = new Option();
                    TicketSelect.options[i].text = data[i].label;
                    TicketSelect.options[i].value = data[i].text;
                }
            }else
                $("#id_tickettype").hide();
          }
        })
  }
