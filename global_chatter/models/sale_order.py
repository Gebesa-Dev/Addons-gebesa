# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'message.post.show.all']
