function whatsapp_send_message(phone_number, whatsapp_text){
  	whatsapp_href = `https://wa.me/${phone_number}?text=${whatsapp_text}`
  	window.location.href = whatsapp_href
}

$(document).on("click", ".go-whatsapp", function(e) {
  	event.preventDefault()
  	var url = $(this).data('url')
  	phone_cookie = $(this).data('cookie')
  	whatsapp_text = $(this).data('message')
  	if(!whatsapp_text|| whatsapp_text=='None'){
    	whatsapp_text = ''
  	}
  	if(Cookies.get(phone_cookie)){
    	whatsapp_send_message( Cookies.get(phone_cookie), whatsapp_text)
  	}
  	else{
    	var id = $(this).data('id')
    	$.ajax({
      		url: url,
      		type: 'GET',
      		data:{},
      		error: function(jqXHR, textStatus, errorThrown) {
            var err = JSON.parse(jqXHR.responseText);
        		alert(err)
            console.log(err)
      		},
      		success:function (data) {
        		if(data.status){
          			phone_number = data.phone_number
          			Cookies.set(phone_cookie, phone_number, { expires: 1 })
          			whatsapp_send_message(phone_number, whatsapp_text)
        		}
        		else{
          			alert(data)
                console.log(data)
        		}
      		}
    	})
  	}
})