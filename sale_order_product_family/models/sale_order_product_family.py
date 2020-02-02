# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class SaleOrderProductFamily(models.Model):
    _name = 'sale.order.product.family'

    sale_id = fields.Many2one(
        'sale.order',
        string=_('Sale Order'),
    )

    family_id = fields.Many2one(
        'product.family',
        string=_('Product Family'),
    )

    margin = fields.Float(
        string=_('Margin'),
    )

    _sql_constraints = [
        ('sale_family_uniq', 'unique (sale_id,family_id)', _('The sales order cannot have the same product family twice.')),
    ]
