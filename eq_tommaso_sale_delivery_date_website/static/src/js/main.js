odoo.define('eq_tommaso_sale_delivery_date_website.product_display_delivery_days', function (require) {
    "use strict";

    var ajax = require('web.ajax');

    $(document).ready(function (ev) {
        ajax.jsonRpc("/get_product_delivery_days", 'call', {'product_id':$('.product_id').val()})
            .then(function(data) {
                if (data){
                    $(".delivery_days").text('Usually Delivered in ' + data + ' Days');
                }
                else{
                    $(".delivery_days").text('');
                }

            });
        $('.product_id').on('change', function(){
            ajax.jsonRpc("/get_product_delivery_days", 'call', {'product_id':$('.product_id').val()})
            .then(function(data) {
                if (data){
                    $(".delivery_days").text('Usually Delivered in ' + data + ' Days');
                }
                else{
                    $(".delivery_days").text('');
                }

            });
        });
    })

})