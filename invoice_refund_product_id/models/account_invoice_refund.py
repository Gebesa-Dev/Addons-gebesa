# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models, netsvc
from openerp.addons import decimal_precision as dp
from openerp.exceptions import ValidationError


class AccountInvoiceRefund(models.Model):
    _inherit = 'account.invoice.refund'

    @api.model
    def _get_domain_product_id(self):
        acc = []
        product_acc = 'property_account_income_id'
        for inv in self.env['account.invoice'].browse(
                self._context.get('active_ids')):
            if type not in ('out_invoice', 'out_refund'):
                product_acc = 'property_account_expense_id'
            for account in inv.move_id.line_ids.mapped('account_id'):
                acc.append(account.id)

        return [
            ('active', '=', True),
            (product_acc, 'not in', acc),
            (product_acc, '!=', False)]

    product_id = fields.Many2one(
        'product.product',
        string=_(u'Product'),
        ondelete='set null',
        select=True,
        domain=_get_domain_product_id
    )

    amount = fields.Float(
        _(u'Amount'),
        digits_compute=dp.get_precision('Account'),
    )

    @api.multi
    def compute_refund(self, mode='refund'):
        ctx = self._context.copy()

        invoice_obj = self.env['account.invoice']
        account_m_line = self.env['account.move.line']
        wf_service = netsvc.LocalService('workflow')

        for ref in self:
            product_id = ref.product_id.id
            amount = ref.amount
            filter_refund = ref.filter_refund
            for inv in invoice_obj.browse(self._context.get('active_ids')):
                # journal_id = inv.journal_id.id
                if mode != 'refund':
                    if inv.amount_total != inv.residual:
                        raise ValidationError(_(u"Invalid operation, the bill \
                                              already has payments"))
                if amount > inv.residual:
                    raise ValidationError(_(u"Invalid operation, the balance \
                                          of the invoice is less than the \
                                          amount payable"))
                ctx.update({'type': inv.type})
                if inv.partner_shipping_id:
                    ctx.update({
                        'default_partner_shipping_id': inv.partner_shipping_id.id})
                if inv.sales_channel_id:
                    ctx.update({
                        'default_sales_channel_id': inv.sales_channel_id.id})

        ctx.update({'product_id': product_id})
        ctx.update({'mode': mode})
        ctx.update({'default_mode': mode})
        ctx.update({'amount': amount})
        # Se cambia el estatus para cuando sea tipo saldar o modificar, evitar la validacion de aprovar
        # if mode in ('cancel', 'modify'):
        #     mode = 'refund'
        res = super(AccountInvoiceRefund, self.with_context(
                    ctx)).compute_refund('refund')
        refund_id = res['domain'][1][2][0]
        # import pdb; pdb.set_trace()
        refund = invoice_obj.browse(refund_id)
        if refund and filter_refund == 'cancel':
            refund.write({'cfdi_uuid': '00000000-0000-0000-0000-000000000000'})
        if refund.type == 'in_refund':
            wf_service.trg_validate(self._uid, 'account.invoice', refund_id,
                                    'invoice_open', self._cr)

        if mode == 'refund':
            for line in refund.invoice_line_ids:
                fpos = line.invoice_id.fiscal_position_id
                company = line.invoice_id.company_id
                type = line.invoice_id.type
                account = line.get_invoice_line_account(type, line.product_id, fpos, company)
                if account:
                    line.account_id = account.id
                line._set_taxes()
                line.price_unit = amount

            refund.compute_taxes()

        for form in self:
            for invoice in invoice_obj.browse(self._context.get('active_ids')):
                if mode == 'refund':
                    to_reconcile_ids = {}
                    refund = invoice_obj.browse(refund_id)
                    for tmp_line in refund.move_id.line_ids:
                        if tmp_line.account_id.id == inv.account_id.id:
                            to_reconcile_ids[tmp_line.account_id.id] = [
                                tmp_line.id]
                    for account in to_reconcile_ids:
                        invoice.register_payment(account_m_line.browse(
                            to_reconcile_ids[account]))
        return res
