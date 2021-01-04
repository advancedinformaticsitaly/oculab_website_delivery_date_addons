odoo.define('eq_tommaso_sale_delivery_date_website.product_display_delivery_days', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;

    $(document).ready(function (ev) {
        ajax.jsonRpc("/get_product_delivery_days", 'call', {'product_id':$('.product_id').val()})
            .then(function(data) {
                if (data){
                    $(".delivery_days").text(_t('Usually Delivered in ') + data + _t(' Days'));
                }
                else{
                    $(".delivery_days").text('');
                }

            });
        $('.product_id').on('change', function(){
            ajax.jsonRpc("/get_product_delivery_days", 'call', {'product_id':$('.product_id').val()})
            .then(function(data) {
                if (data){
                    $(".delivery_days").text(_t('Usually Delivered in ') + data + _t(' Days'));
                }
                else{
                    $(".delivery_days").text('');
                }

            });
        });
    })

})