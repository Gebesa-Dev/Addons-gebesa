# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import _, fields, models


class AccountAccount(models.Model):
    _name = 'account.account'
    _inherit = 'account.account'

    required_partner = fields.Boolean(
        string=_('Requiere partner'),
        default=False,
    )
