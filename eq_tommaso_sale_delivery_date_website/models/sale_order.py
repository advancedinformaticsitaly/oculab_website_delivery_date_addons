# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################

from odoo import models,fields,api,_
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _cart_update(self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs):
        res = super(SaleOrder, self)._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)
        if res.get('line_id') and res.get('quantity') > 0:
            line_id = self.env['sale.order.line'].sudo().browse(res['line_id'])
            line_id.product_id_change()
        return res


class res_config_settings(models.TransientModel):
    _inherit = "res.config.settings"

    product_delivered_days = fields.Integer(string='Product Delivered Days',config_parameter='eq_tommaso_sale_delivery_date_website.product_delivered_days')

    @api.constrains('product_delivered_days')
    def check_product_delivered_days(self):
        for each in self:
            if each.product_delivered_days < 0:
                raise UserError(_('Please enter correct product delivered days.'))


class product_brand_ept(models.Model):
    _inherit = 'product.brand.ept'

    product_delivered_days = fields.Integer(string='Product Delivered Days')

    @api.constrains('product_delivered_days')
    def check_product_delivered_days(self):
        for each in self:
            if each.product_delivered_days < 0:
                raise UserError(_('Please enter correct product delivered days.'))


class product_product(models.Model):
    _inherit = 'product.product'

    def get_delivery_days(self):
        for product in self:
            product_delivered_days = 0
            qty_available = product.qty_available
            if qty_available:
                product_delivered_days = int(self.env["ir.config_parameter"].sudo().get_param("eq_tommaso_sale_delivery_date_website.product_delivered_days"))
            else:
                product_delivered_days = product.product_brand_ept_id.product_delivered_days
        return product_delivered_days

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: