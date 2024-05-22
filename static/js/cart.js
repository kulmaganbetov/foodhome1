function calculate_cart(_this, decrement=false, quantity=1){
   var id = _this.data('id')
   var url = _this.data('url')
   var quantity_show = '#' + 'quantity-show-' + id
   $.ajax({
      url: url,
      type: 'POST',
      data:{
         quantity: quantity,
         decrement: decrement
      },
      error: function(jqXHR, textStatus, errorThrown) {
         alert(jqXHR.responseText)
         console.log(jqXHR.responseText)
      },
      success:function (data) {
         if(data.status){
            total_items = data.total_items
            $('#output-total-items').html(total_items)
            $('#output-price-sum').html(data.total_price)
            var quantity_content = $(quantity_show).html(data.quantity).closest('.quantity-content')
            if(data.quantity > 0){
               quantity_content.removeClass('hidden')
               _this.closest('.in-cart').addClass('hidden')
               _this.closest('.fotter-product').find(
                  '.product-quanity-content').removeClass('hidden')
            }
            else{
               quantity_content.addClass('hidden')
               _this.closest('.product-quanity-content').addClass('hidden')
               _this.closest('.fotter-product').find(
                  '.in-cart').removeClass('hidden')
            }
            if(total_items>0){
               $('.float-cart').removeClass('hidden')
            }
            else{
               $('.float-cart').addClass('hidden')
               
            }
            
         }       
      }
   })
}

$(document).on("click", ".add-to-cart", function(e) {
   calculate_cart($(this))
})

$(document).on("click", ".remove-to-cart", function(e) {
   calculate_cart($(this), true, 1)
})

$(document).on("click", ".in-cart", function(e) {
   calculate_cart($(this))
   
})