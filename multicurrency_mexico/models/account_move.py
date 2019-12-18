# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    move_exchange_id = fields.Many2one(
        'account.move',
        string='Movement that generated the exchange difference',
    )
    move_exchange_difference_ids = fields.One2many(
        'account.move',
        'move_exchange_id',
        string='Exchange difference',
    )
