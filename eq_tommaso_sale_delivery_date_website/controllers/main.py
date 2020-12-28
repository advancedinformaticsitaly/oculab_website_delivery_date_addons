# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################

from odoo import http
from odoo.http import request


class product_display_delivery_days(http.Controller):

    @http.route('/get_product_delivery_days', type='json', auth='public')
    def get_product_delivery_days(self, **kw):
        product_delivered_days = 0
        if kw.get('product_id'):
            product_id = request.env['product.product'].sudo().browse(int(kw.get('product_id')))
            return product_id.get_delivery_days()
        return product_delivered_days

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: