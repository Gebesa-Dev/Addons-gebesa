# -*- coding: utf-8 -*-
# Copyright 2018, Esther Cisneros
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api,exceptions, _, fields, models

class AccountInvoice(models.Model):
    # _name = 'account.payment'
    _inherit = 'account.invoice'

    evidence_status = fields.Selection(
        [('received', _('Received')),
         ('not_received', _('Not Received'))],
        string=_('Evidencia Galbo'),
        default='not_received'
    )
    @api.multi
    def button_invoice_evidence (self):
        for rec in self:
            rec.write({'evidence_status': 'received'})
        return True
