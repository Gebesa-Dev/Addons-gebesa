# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class MrpShipmentSaleOrder(models.TransientModel):
    _name = 'mrp.shipment.sale.order'

    sale_ids = fields.Many2many(
        'sale.order',
        string=_('Sale Order'),
    )

    @api.multi
    def add_sale_order(self):
        shipment_obj = self.env['mrp.shipment']
        shipment_line_obj = self.env['mrp.shipment.line']
        ship_sale_obj = self.env['mrp.shipment.sale']
        active_ids = self._context.get('active_ids', []) or []
        shipment = shipment_obj.browse(active_ids)
        order_line_id = []
        sale_id = []
        for sale in shipment.sale_ids:
            sale_id.append(sale.sale_id.id)
        for lines in shipment.line_ids:
            order_line_id.append(lines.order_line_id.id)
        for shipment_sale in self:
            for sale in shipment_sale.sale_ids:
                if sale.state in ("done", "sale"):
                    for line in sale.order_line:
                        if line.id not in order_line_id:
                            if line.missing_quantity > 0:
                                # miss_seg = line.segment_qty
                                # miss_seg = miss_seg - line.quantity_shipped
                                # if miss_seg > 0:
                                if sale.id not in sale_id:
                                    ship_sale = ship_sale_obj.create({
                                        'sale_id': sale.id,
                                        'shipment_id': shipment.id,
                                        'partner_id': sale.partner_id.id,
                                        'partner_shipping_id': sale.partner_shipping_id.id,
                                        'country_id': sale.partner_shipping_id.country_id.id,
                                        'state_id': sale.partner_shipping_id.state_id.id,
                                        'city': sale.partner_shipping_id.city
                                    })
                                    sale_id.append(sale.id)
                                else:
                                    ship_sale = ship_sale_obj.search([
                                        ('sale_id', '=', sale.id),
                                        ('shipment_id', '=', shipment.id)
                                    ])
                                shipment_line_obj.create({
                                    'shipment_id': shipment.id,
                                    'shipment_sale_id': ship_sale.id,
                                    'partner_id': line.order_partner_id.id,
                                    'sale_order_id': sale.id,
                                    'order_line_id': line.id,
                                    'product_id': line.product_id.id,
                                    'price_unit': line.price_unit,
                                    'quantity': line.missing_quantity,
                                    'quantity_shipped': line.missing_quantity,
                                    'partner_id': sale.partner_id.id,
                                    'partner_shipping_id': sale.partner_shipping_id.id,
                                    'country_id': sale.partner_shipping_id.country_id.id,
                                    'state_id': sale.partner_shipping_id.state_id.id,
                                    'city': sale.partner_shipping_id.city,
                                    'street': sale.partner_shipping_id.street,
                                    'street2': sale.partner_shipping_id.street2,
                                    'product_name': line.product_id.name,
                                    'product_code': line.product_id.default_code,
                                    'standard_cost': line.product_id.standard_price
                                    # 'quantity': miss_seg,
                                    # 'quantity_shipped': miss_seg,
                                })
