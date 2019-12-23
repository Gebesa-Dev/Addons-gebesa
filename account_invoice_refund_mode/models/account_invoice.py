# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    invoice_refund_id = fields.Many2one(
        'account.invoice',
        string=_('Create From'),
    )

    mode = fields.Text(
        string=_('Mode'),
        help=_('Indicates the selected type for credit note'),
    )

    @api.multi
    def action_move_create(self):
        for inv in self:
            if inv.type == 'out_refund' and inv.mode == 'cancel':
                invoice_origin = self.search([('number', '=', inv.origin)])
                if invoice_origin:
                    ctx = dict(self._context, lang=inv.partner_id.lang)
                    journal = inv.journal_id.with_context(ctx)
                    ctx.update({'create_tax': False})
                    reverse = invoice_origin.move_id.with_context(ctx).reverse_moves(
                        date=None, journal_id=journal)
                    for rev in self.env['account.move'].browse(reverse):
                        rev.date = inv.date_invoice
                        inv.move_id = rev.id
                    return True
        return super(AccountInvoice, self).action_move_create()

    @api.model
    def _prepare_refund(
            self, invoice, date_invoice=None, date=None,
            description=None, journal_id=None):
        values = super(AccountInvoice, self)._prepare_refund(
            invoice, date_invoice=date_invoice, date=date,
            description=description, journal_id=journal_id)
        invoice_origin = self.env['account.invoice'].browse(
            self._context.get('active_id', False))
        values['invoice_refund_id'] = invoice_origin.id
        values['mode'] = invoice_origin.mode

        return values
