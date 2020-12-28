# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################


from odoo import api, fields, models, _
from datetime import datetime, date, timedelta
from odoo.exceptions import Warning


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def change_delivery_date(self):
        select_order_line = self.order_line.filtered(lambda l:l.select_so_lines)
        if not select_order_line:
            raise Warning (_('Please select some order line for change delivery date.'))
        return {
            'name': 'Change Delivery Date',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model':'wizard.sale.dispatch.date',
            'view_id':self.env.ref('eq_sale_delivery_date.wizard_sale_dispatch_date_form_view').id,
            'target':'new',
            'context':{'default_sale_line_ids':[(6, 0, select_order_line.ids)]}
        }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    dispatch_date = fields.Date(string="Delivery Date")
    select_so_lines = fields.Boolean(string="Select", copy=False)

    @api.onchange('product_id')
    def product_id_change(self):
        domain = super(SaleOrderLine, self).product_id_change()
        self.dispatch_date = False
        if self.product_id:
            product_delivered_days = self.product_id.get_delivery_days()
            dispatch_date = date.today() + timedelta(days=product_delivered_days)
            self.dispatch_date = dispatch_date
        return domain

    @api.multi
    def _prepare_procurement_values(self, group_id=False):
        res = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        if self.dispatch_date:
            res.update({'date_planned':self.dispatch_date})
        return res

    @api.multi
    def write(self, values):
        lines = self.env['sale.order.line']
        res = super(SaleOrderLine, self).write(values)
        if 'dispatch_date' in values:
            lines = self
        if lines:
            previous_product_uom_qty = {line.id: line.product_uom_qty for line in lines}
            lines.with_context(previous_product_uom_qty=previous_product_uom_qty)._action_launch_stock_rule()
        return res


class stock_move(models.Model):
    _inherit = 'stock.move'

    def _search_picking_for_assignation(self):
        self.ensure_one()
        domain = [
                ('group_id', '=', self.group_id.id),
                ('location_id', '=', self.location_id.id),
                ('location_dest_id', '=', self.location_dest_id.id),
                ('picking_type_id', '=', self.picking_type_id.id),
                ('printed', '=', False),
                ('state', 'in', ['draft', 'confirmed', 'waiting', 'partially_available', 'assigned'])]
        if self.sale_line_id and self.sale_line_id.dispatch_date:
            domain += [('scheduled_date', '=', self.date_expected)]
        picking = self.env['stock.picking'].search(domain, limit=1)
        return picking


class wizard_sale_dispatch_date(models.TransientModel):
    _name = 'wizard.sale.dispatch.date'
    _description = "Wizard Sale Dispatch Date"

    date = fields.Date(string="Date", default=date.today())
    sale_line_ids = fields.Many2many('sale.order.line', 'wizard_change_date_sol_rel')

    @api.multi
    def do_change_date(self):
        for so_line in self.sale_line_ids:
            so_line.dispatch_date = self.date
            so_line.select_so_lines = False

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: