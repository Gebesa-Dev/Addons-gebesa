# -*- coding: utf-8 -*-
# Copyright 2018, Esther Cisneros
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import timedelta

from openerp import _, api, fields, models


class SaleOrder(models.Model):

    _name = 'sale.order'
    _inherit = 'sale.order'

    order_replaced = fields.Many2one(
        'sale.order',
        string=_("Order that replaces"),
    )

    date_cancelled = fields.Date(
        string=_("Cancellation Date/Closed"),
    )

    @api.multi
    def action_cancel(self):
        for order in self:
            order.date_cancelled = fields.Date.today()
        super(SaleOrder, self).action_cancel()

    @api.multi
    def action_closed(self):
        for order in self:
            order.date_cancelled = fields.Date.today()
        super(SaleOrder, self).action_closed()

    @api.model
    def send_email_orders_canceled(self):
        lim_date = timedelta(days=1)
        date_today = fields.Date.today()
        ddd = fields.Datetime.from_string(date_today)
        date_cancel = ddd - lim_date
        order_ids = self.search([
            ('state', 'not in', ['done', 'draft', 'sent']),
            ('date_cancelled', '=', date_cancel)])
        table = ''
        remp_date = ''
        remp_ord = ''
        rel_seg = ''
        rel_seg_repla = ''
        for res in order_ids:
            if not res.date_cancelled:
                remp_date = '---'
            else:
                remp_date = res.date_cancelled
            if not res.order_replaced:
                remp_ord = '---'
            else:
                remp_ord = res.order_replaced.name
            if not res.related_segment:
                rel_seg = '---'
            else:
                rel_seg = res.related_segment
            if not res.order_replaced.related_segment:
                rel_seg_repla = '---'
            else:
                rel_seg_repla = res.order_replaced.related_segment
            table += """

            <div>
                <style type="text/css">
                    tr {
                    font-family: 'Arial';
                        color: #000000;
                    }
                    strong {
                        font-size: 14px;
                    }
                </style>
            </div>
                <tr align="center"><td style="border-bottom: 1px solid silver; font-size:12px;">%s</td>
                    <td style="border-bottom: 1px solid silver; font-size:12px;">%s</td>
                    <td style="border-bottom: 1px solid silver; font-size:12px;">%s</td>
                    <td style="border-bottom: 1px solid silver; font-size:12px;">%s</td>
                    <td style="border-bottom: 1px solid silver; font-size:12px;">%s</td>
                    <td align="center" style="border-bottom: 1px solid silver; font-size:12px;">
                    %s</td>
                </tr>
            """ % (remp_date, res.partner_id.name, res.name, rel_seg, remp_ord, rel_seg_repla)
        mail_obj = self.env['mail.mail']
        body_mail = u"""
            <div summary="o_mail_notification" style="padding:0px; width:100%%;
             margin:0 auto; background: #FFFFFF repeat top  /100%%; color:#77777
             7">
                <table cellspacing="0" cellpadding="0" style="width:900px;
                border-collapse:collapse; background:inherit; color:inherit">
                    <tbody><tr>
                        <td valign="center" width="400" style="padding:5px 10px
                         5px 5px;font-size: 18px">
                            <p>Los siguientes pedidos fueron Cancelados y/o
                            Cerrados</p>
                        </td>
                        <td valign="center" align="right" width="400"
                        style="padding:5px 15px 5px 10px; font-size: 12px;">
                            <p>
                            <strong>Sent by</strong>
                            <a href="http://erp.portalgebesa.com" style="text-
                            decoration:none; color: #a24689;">
                                <strong>%s</strong>
                            </a>
                            <strong>using</strong>
                            <a href="https://www.odoo.com" style="text-
                            decoration:none; color: #a24689;"><strong>Odoo
                            </strong></a>
                            </p>
                        </td>
                    </tr>
                </tbody></table>
            </div>
            <div style="padding:0px; width:900px; margin:0 auto; background:
            #FFFFFF repeat top /900%%; color:#777777">
                <table cellspacing="0" cellpadding="0" style="vertical-align:
                top; padding:0px; border-collapse:collapse; background:inherit;
                 color:inherit">
                    <tbody><tr>
                        <td valign="top" style="width:900px; padding:5px 10px
                        5px 5px; ">
                            <div>
                                <hr width="100%%" style="background-color:
                                rgb(204,204,204);border:medium none;clear:both;
                                display:block;font-size:0px;min-height:1px;
                                line-height:0;margin:15px auto;padding:0">
                            </div>
                        </td>
                    </tr></tbody>
                </table>
            </div>
            <div style="padding:0px; width:100%%; margin:0 auto; background:
            #FFFFFF repeat top /100%%;color:#777777">
                <table style="border-collapse:collapse; margin: 0 auto; width:
                1100px; background:inherit; color:inherit">
                    <tbody><tr>
                        <th width="10%%" style="padding:5px 10px 5px 5px;font-
                        size: 12px; border-bottom: 2px solid silver;"><strong>
                        Fecha de Cancelacion y/o Cerrado</strong></th>
                        <th width="40%%" style="padding:5px 10px 5px 5px;font-
                        size: 12px; border-bottom: 2px solid silver;"><strong>
                        Cliente</strong></th>
                        <th width="12%%" style="padding:5px 10px 5px 5px;font-
                        size: 12px; border-bottom: 2px solid silver;"><strong>
                        Pedido</strong></th>
                        <th width="20%%" style="padding:5px 10px 5px 5px;font-
                        size: 12px; border-bottom: 2px solid silver;"><strong>
                        Segmento(s) Relacionado(s)</strong></th>
                        <th width="12%%" style="padding:5px 10px 5px 5px;font-
                        size: 12px; border-bottom: 2px solid silver;"><strong>
                        Pedido que Sustituye</strong></th>
                        <th width="20%%" style="padding:5px 10px 5px 5px;font-
                        size: 12px; border-bottom: 2px solid silver;"><strong>
                        Seg. Rel. Pedido Sustituye</strong></th>
                    </tr>
                    %s
                    </tbody>
                </table>
            </div>
          """ % (self.env.user.company_id.name, table)
        mail = mail_obj.create({
            'subject': 'Pedidos Cancelados y/o Cerrados',
            'email_to': 'equipocompras@gebesa.com,sistemas@gebesa.com,brandon.ramirez@gebesa.com,miguel.martinez@gebesa.com,victor.campos@gebesa.com,elizabeth.valenzuela@gebesa.com,cristina.rodriguez@gebesa.com,julio.delarosa@gebesa.com',
            'headers': "{'Return-Path': u'odoo@gebesa.com'}",
            'body_html': body_mail,
            'auto_delete': True,
            'message_type': 'comment',
            'model': 'sale.order',
            'res_id': order_ids[0].id,
        })
        mail.send()
