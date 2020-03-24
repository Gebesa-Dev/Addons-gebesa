# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
import logging

_logger = logging.getLogger(__name__)

class MrpBomLineMassiveReplacement(models.TransientModel):
    _name = "mrp.bom.line.massive.replacement"

    product_id = fields.Many2one(
        'product.product',
        string='Product origin',
    )
    new_product_id = fields.Many2one(
        'product.product',
        string='New product',
    )
    limit = fields.Integer(
        string='Limite',
    )

    @api.multi
    def process(self):
        bom_line_obj = self.env['mrp.bom.line']
        for replacement in self:
            if replacement.limit > 0:
                bom_line = bom_line_obj.search(
                    [('product_id', '=', replacement.product_id.id)],
                    limit=replacement.limit)
            else:
                bom_line = bom_line_obj.search(
                    [('product_id', '=', replacement.product_id.id)])
            done_ids = []
            for line in bom_line:
                line.product_id = replacement.new_product_id.id

                if replacement.product_id.standard_price == replacement.new_product_id.standard_price:
                    continue

                if line.bom_id.id in done_ids:
                    continue

                done_ids.append(line.bom_id.id)

            # Revaluacion
            for bom in done_ids:
                self.env['mrp.bom'].browse(bom).action_reval()
