# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models
from openerp.exceptions import ValidationError


class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"

    @api.model
    def create(self, vals):
        res = super(AccountPartialReconcile, self).create(vals)
        invoice = False
        move = False
        if (res.credit_move_id.invoice_id.type == 'out_refund' and
                res.debit_move_id.invoice_id.type == 'out_invoice'):
            invoice = res.debit_move_id.invoice_id
            move = res.credit_move_id.move_id
            account = 'property_account_customer_advance_id'
        elif (res.credit_move_id.invoice_id.type == 'in_invoice' and
                res.debit_move_id.invoice_id.type == 'in_refund'):
            invoice = res.credit_move_id.invoice_id
            move = res.debit_move_id.move_id
            account = 'property_account_supplier_advance_id'
        if invoice and move:
            if invoice.currency_id.id != invoice.company_id.currency_id.id:
                if invoice.date_invoice != move.date:
                    raise ValidationError("No Implementado")
            account = invoice.partner_id.mapped(account)
            line_base = move.line_ids.filtered(
                lambda l: l.account_id == account)
            line_reconcile = invoice.advance_ids.mapped('advance_id').mapped(
                'move_id').mapped('line_ids').filtered(
                lambda l: l.account_id == account)
            if line_base and line_reconcile:
                for line in line_reconcile:
                    (line_base + line).reconcile()
        return res

    @api.multi
    def unlink(self):
        for reconcile in self:
            invoice = False
            move = False
            if (reconcile.credit_move_id.invoice_id.type == 'out_refund' and
                    reconcile.debit_move_id.invoice_id.type == 'out_invoice'):
                invoice = reconcile.debit_move_id.invoice_id
                move = reconcile.credit_move_id.move_id
                account = 'property_account_customer_advance_id'
            elif (reconcile.credit_move_id.invoice_id.type == 'in_invoice' and
                    reconcile.debit_move_id.invoice_id.type == 'in_refund'):
                invoice = reconcile.credit_move_id.invoice_id
                move = reconcile.debit_move_id.move_id
                account = 'property_account_supplier_advance_id'
            if invoice and move:
                account = invoice.partner_id.mapped(account)
                line_base = move.line_ids.filtered(
                    lambda l: l.account_id == account)
                if line_base.debit > line_base.credit:
                    pos_base = 'debit_move_id'
                    pos_line = 'credit_move_id'
                else:
                    pos_base = 'credit_move_id'
                    pos_line = 'debit_move_id'
                line_reconcile = invoice.advance_ids.mapped('advance_id').mapped(
                    'move_id').mapped('line_ids').filtered(
                    lambda l: l.account_id == account)
                if line_base and line_reconcile:
                    for line in line_reconcile:
                        self.search([
                            (pos_base, '=', line_base.id),
                            (pos_line, '=', line.id)]).unlink()
        return super(AccountPartialReconcile, self).unlink()
