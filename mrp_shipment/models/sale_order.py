# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    shiptment_status = fields.Selection(
        [('no_shipment', _('No shipment')),
         ('partial_shipment', _('Partial shipment')),
         ('total_shipment', _(u'Total shipment'))],
        string=_("Shiptment statu"),
        store=True,
        select=True,
        default='no_shipment',
        compute='_compuete_shiptment_status'
    )

    folio_shipped = fields.Char(
        string='Folio shipped',
        compute='_compuete_folio_shipped'
    )

    date_shipped = fields.Char(
        string='Date shipped',
        compute='_compuete_folio_shipped'
    )
    shipped_departure_date = fields.Char(
        string='shipped Departure Date',
        compute='_compuete_folio_shipped'
    )

    @api.depends('order_line.shipment_line_ids')
    def _compuete_folio_shipped(self):
        for sale in self:
            fol = date = ''
            date2 = ''
            folio = []
            for line in sale.order_line:
                for shipment_line in line.shipment_line_ids:
                    shipment = shipment_line.shipment_id
                    if shipment.folio not in folio:
                        folio.append(shipment.folio)
                        date = date + ' ' + shipment.date + ','
                        date2 = date2 + ' ' + shipment.departure_date + ','
                        fol = fol + ' ' + shipment.folio + ','
            sale.folio_shipped = fol[1:-1]
            sale.date_shipped = date[1:-1]
            # se asigna la var y se le un arreglo, quit la pos ini y pos fin
            sale.shipped_departure_date = date2[1:-1]

    @api.depends('order_line.quantity_shipped', 'order_line.product_uom_qty')
    def _compuete_shiptment_status(self):
        for sale in self:
            ship_qty = 0
            pro_qty = 0
            for line in sale.order_line:
                ship_qty += line.quantity_shipped
                pro_qty += line.product_uom_qty
            if ship_qty == 0:
                sale.shiptment_status = 'no_shipment'
            elif ship_qty == pro_qty:
                sale.shiptment_status = 'total_shipment'
            else:
                sale.shiptment_status = 'partial_shipment'
