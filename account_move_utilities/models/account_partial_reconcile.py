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
            field_account = 'property_account_customer_advance_id'
        elif (res.credit_move_id.invoice_id.type == 'in_invoice' and
                res.debit_move_id.invoice_id.type == 'in_refund'):
            invoice = res.credit_move_id.invoice_id
            move = res.debit_move_id.move_id
            field_account = 'property_account_supplier_advance_id'
        if invoice and move and self._context.get('extend_reconcile', True):
            # if invoice.currency_id.id != invoice.company_id.currency_id.id:
            #     if invoice.date_invoice != move.date:
            #         raise ValidationError("No Implementado")
            product = res.credit_move_id.invoice_id.invoice_line_ids[
                0].product_id.id
            deposit = self.pool['ir.values'].get_default(
                self._cr, self._uid, 'sale.config.settings',
                'deposit_product_id_setting') or False
            account = invoice.account_id
            if product == deposit:
                account_deposit = invoice.partner_id.mapped(field_account)
                line_base = move.line_ids.filtered(
                    lambda l: l.account_id == account_deposit)
                line_reconcile = invoice.advance_ids.mapped('advance_id').mapped(
                    'move_id').mapped('line_ids').filtered(
                    lambda l: l.account_id == account_deposit)
                if line_base and line_reconcile:
                    for line in line_reconcile:
                        if line.account_id.reconcile:
                            (line_base + line).with_context(
                                create_tax=False,
                                extend_reconcile=False).reconcile()

                line_base = move.line_ids.filtered(
                    lambda l: l.account_id != account)
                line_reconcile = invoice.move_id.mapped('line_ids').filtered(
                    lambda l: l.account_id != account)
                if line_base and line_reconcile:
                    for line_r in line_reconcile:
                        for line_b in line_base:
                            if line_r.account_id.id == line_b.account_id.id:
                                if line_r.account_id.reconcile:
                                    (line_b + line_r).with_context(
                                        create_tax=False,
                                        extend_reconcile=False).reconcile()

            else:
                line_base = move.line_ids.filtered(
                    lambda l: l.account_id != account)
                line_reconcile = invoice.move_id.mapped('line_ids').filtered(
                    lambda l: l.account_id != account)
                if line_base and line_reconcile:
                    for line_r in line_reconcile:
                        for line_b in line_base:
                            if line_r.account_id.id == line_b.account_id.id:
                                if line_r.account_id.reconcile:
                                    (line_b + line_r).with_context(
                                        create_tax=False,
                                        extend_reconcile=False).reconcile()

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
                field_account = 'property_account_customer_advance_id'
            elif (reconcile.credit_move_id.invoice_id.type == 'in_invoice' and
                    reconcile.debit_move_id.invoice_id.type == 'in_refund'):
                invoice = reconcile.credit_move_id.invoice_id
                move = reconcile.debit_move_id.move_id
                field_account = 'property_account_supplier_advance_id'
            if invoice and move:
                product = reconcile.credit_move_id.invoice_id.invoice_line_ids[
                    0].product_id.id
                deposit = self.pool['ir.values'].get_default(
                    self._cr, self._uid, 'sale.config.settings',
                    'deposit_product_id_setting') or False
                account = invoice.account_id
                if product == deposit:
                    account_deposit = invoice.partner_id.mapped(field_account)
                    line_base = move.line_ids.filtered(
                        lambda l: l.account_id == account_deposit)
                    if line_base.debit > line_base.credit:
                        pos_base = 'debit_move_id'
                        pos_line = 'credit_move_id'
                    else:
                        pos_base = 'credit_move_id'
                        pos_line = 'debit_move_id'
                    line_reconcile = invoice.advance_ids.mapped(
                        'advance_id').mapped('move_id').mapped(
                        'line_ids').filtered(
                        lambda l: l.account_id == account_deposit)
                    if line_base and line_reconcile:
                        for line in line_reconcile:
                            if line.account_id.reconcile:
                                self.search([
                                    (pos_base, '=', line_base.id),
                                    (pos_line, '=', line.id)]).unlink()
                    line_base = move.line_ids.filtered(
                        lambda l: l.account_id != account)
                    line_reconcile = invoice.move_id.mapped('line_ids').filtered(
                        lambda l: l.account_id != account)
                    if line_base and line_reconcile:
                        for line_r in line_reconcile:
                            for line_b in line_base:
                                if line_r.account_id.id == line_b.account_id.id:
                                    if line_r.account_id.reconcile:
                                        if line_b.debit > line_b.credit:
                                            pos_base = 'debit_move_id'
                                            pos_line = 'credit_move_id'
                                        else:
                                            pos_base = 'credit_move_id'
                                            pos_line = 'debit_move_id'
                                        self.search([
                                            (pos_base, '=', line_b.id),
                                            (pos_line, '=', line_r.id)]).unlink()
                else:
                    line_base = move.line_ids.filtered(
                        lambda l: l.account_id != account)
                    line_reconcile = invoice.move_id.mapped('line_ids').filtered(
                        lambda l: l.account_id != account)
                    if line_base and line_reconcile:
                        for line_r in line_reconcile:
                            for line_b in line_base:
                                if line_r.account_id.id == line_b.account_id.id:
                                    if line_r.account_id.reconcile:
                                        if line_b.debit > line_b.credit:
                                            pos_base = 'debit_move_id'
                                            pos_line = 'credit_move_id'
                                        else:
                                            pos_base = 'credit_move_id'
                                            pos_line = 'debit_move_id'
                                        self.search([
                                            (pos_base, '=', line_b.id),
                                            (pos_line, '=', line_r.id)]).unlink()
        return super(AccountPartialReconcile, self).unlink()
