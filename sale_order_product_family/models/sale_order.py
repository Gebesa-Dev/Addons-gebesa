# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_order_product_family_id = fields.One2many(
        'sale.order.product.family',
        'sale_id',
        string=_('Product Family'),
    )

    @api.constrains('sale_order_product_family_id')
    def _check_margin(self):
        for product_family in self.sale_order_product_family_id:
            if product_family.margin > 100 or product_family.margin < 0:
                raise ValidationError(_('The family margin cannot be negative or greater than one hundred'))
