# -*- coding: utf-8 -*-
# © <2016> Cesar barron
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import UserError


class MrpBom(models.Model):
    _name = "mrp.bom"
    _inherit = "mrp.bom"

    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string=_('Warehouse'),
        required=True)

    @api.multi
    def unlink(self):
        for bom in self:
            if bom.bom_line_ids:
                raise UserError(_('This BOM has detail'))
        return super(MrpBom, self).unlink()

    # @api.multi
    # def write(self, values):
    #     # te traes el producto anterior
    #     # val = self.product_tmpl_id
    #     for rec in self:

    #         template = self.env['product.template']
    #         if 'type' in values.keys():
    #             types = values['type']
    #         else:
    #             types = rec.type
    #         if 'warehouse_id' in values.keys():
    #             ware_obj = self.env['stock.warehouse']
    #             ware = ware_obj.browse(values['warehouse_id'])
    #         else:
    #             ware = rec.warehouse_id
    #         if 'routing_id' in values.keys():
    #             routing_obj = self.env['mrp.routing']
    #             routing = routing_obj.browse(values['routing_id'])
    #         else:
    #             routing = rec.routing_id
    #         if types == 'normal':
    #             if ware.id != routing.location_id.stock_warehouse_id.id:
    #                 raise UserError(_('The production route must'
    #                                   ' be in the same warehouse than the bom'))
    #             if rec.product_tmpl_id:
    #                     rec.product_tmpl_id.invoice_policy = 'delivery'
    #         if types == 'phantom':
    #             if routing.id != 0:
    #                 raise UserError(_('Kit products should not have route production'))
    #             if rec.product_tmpl_id:
    #                     rec.product_tmpl_id.invoice_policy = 'order'
    #         route_ids = []
    #         manuf_ids = [29, 30, 31, 32]
    #         if 'product_tmpl_id' in values.keys():
    #             # te traes el objeto vacio
    #             template = self.env['product.template']
    #             # se construye el objeto, y los busca por medio del values
    #             val = template.browse(values['product_tmpl_id'])
    #             # condicion para la busquedan
    #             route_ids = val.mapped('route_ids').mapped('id')
    #             if not any(x in manuf_ids for x in route_ids):
    #                 if 6 in route_ids:
    #                     raise UserError(_('This product is raw material'))

    #             # for route in val.route_ids:
    #             #     if route.id == 6:
    #             #         raise UserError(_('This product is raw material'))
    #         else:
    #             val = rec.product_tmpl_id

    #         if 'product_id' in values.keys():
    #             producto_obj = self.env['product.product']
    #             product = producto_obj.browse(values['product_id'])

    #         else:
    #             product = rec.product_id

    #         if val.id != product.product_tmpl_id.id:
    #             raise UserError(_('Product and template it does not match'))
    #     return super(MrpBom, self).write(values)

    @api.multi
    def write(self, values):
        # te traes el producto anterior
        # val = self.product_tmpl_id
        template = self.env['product.template']
        if 'type' in values.keys():
            types = values['type']
        else:
            types = self.type
        if 'warehouse_id' in values.keys():
            ware_obj = self.env['stock.warehouse']
            ware = ware_obj.browse(values['warehouse_id'])
        else:
            ware = self.warehouse_id
        if 'routing_id' in values.keys():
            routing_obj = self.env['mrp.routing']
            routing = routing_obj.browse(values['routing_id'])
        else:
            routing = self.routing_id
        if types == 'normal':
            if ware.id != routing.location_id.stock_warehouse_id.id:
                raise UserError(_('The production route must'
                                  ' be in the same warehouse than the bom'))
            if self.product_tmpl_id:
                    self.product_tmpl_id.invoice_policy = 'delivery'
        if types == 'phantom':
            if routing.id != 0:
                raise UserError(_('Kit products should not have route production'))
            if self.product_tmpl_id:
                    self.product_tmpl_id.invoice_policy = 'order'
        route_ids = []
        manuf_ids = [29, 30, 31, 32]
        if 'product_tmpl_id' in values.keys():
            # te traes el objeto vacio
            template = self.env['product.template']
            # se construye el objeto, y los busca por medio del values
            val = template.browse(values['product_tmpl_id'])
            # condicion para la busquedan
            route_ids = val.mapped('route_ids').mapped('id')
            if not any(x in manuf_ids for x in route_ids):
                if 6 in route_ids:
                    raise UserError(_('This product is raw material'))

            # for route in val.route_ids:
            #     if route.id == 6:
            #         raise UserError(_('This product is raw material'))
        else:
            val = self.product_tmpl_id

        if 'product_id' in values.keys():
            producto_obj = self.env['product.product']
            product = producto_obj.browse(values['product_id'])

        else:
            product = self.product_id

        if val.id != product.product_tmpl_id.id:
            raise UserError(_('Product and template it does not match'))
        return super(MrpBom, self).write(values)

    @api.model
    def create(self, vals):
        # objeto para no guardar variantes ya existentes
        # bom_obj = self.env['mrp.bom']
        ware_obj = self.env['stock.warehouse']
        routing_obj = self.env['mrp.routing']
        producto_obj = self.env['product.product']
        template = self.env['product.template']
        val = template.browse(vals['product_tmpl_id'])
        ware = ware_obj.browse(vals['warehouse_id'])
        routing = routing_obj.browse(vals['routing_id'])
        route_ids = []
        manuf_ids = [29, 30, 31, 32]
        if 'product_id' in vals.keys():
            product = producto_obj.browse(vals['product_id'])
            if val.id != product.product_tmpl_id.id:
                raise UserError(_('Product and template it does not match'))
        # objeto de busqueda para ver si ya existe
        # bom_id = bom_obj.search([('product_id', "=", vals['product_id']),
        #                         ('active', '=', True)])
        # if len(bom_id) > 0:
        #    raise UserError(_('This product is already exists'))
        if vals['type'] == 'normal':
            if ware.id != routing.location_id.stock_warehouse_id.id:
                raise UserError(_('The production route must'
                                  'be in the same warehouse than the bom'))
        if vals['type'] == 'phantom':
            if routing.id != 0:
                raise UserError(_('Kit products should not have route production'))

        route_ids = val.mapped('route_ids').mapped('id')
        if not any(x in manuf_ids for x in route_ids):
            if 6 in route_ids:
                raise UserError(_('This product is raw material'))
        # for route in val.route_ids:
        #     if route.id == 6:
        #         raise UserError(_('This product is raw material'))

        return super(MrpBom, self).create(vals)


class MrpBomLine(models.Model):
    _name = "mrp.bom.line"
    _inherit = "mrp.bom.line"

    location_id = fields.Many2one(
        'stock.location',
        string=_('Location'),
        required=True)

    @api.model
    def create(self, values):
        bom_obj = self.env['mrp.bom']
        product_obj = self.env['product.product']
        location_obj = self.env['stock.location']
        # warehouse_obj = self.env['stock.warehouse']
        if 'bom_id' in values.keys():
            bom = bom_obj.browse([values['bom_id']])
            product = product_obj.browse([values['product_id']])
            location = location_obj.browse([values['location_id']])
            # buscamos BoM del articulo (detalle) a agregar
            product_bom = bom_obj.search([
                ('product_id', '=', values['product_id'])])
            if bom.type == 'phantom':
                # No se pueden agregar productos sin detalle a los Kits
                if not product_bom:
                    raise UserError(_('You can not add a product that \
                        has no BOM: %s') % (product.name,))
            else:
                if location.type_stock_loc == 'fp':
                    raise UserError(_('You can not add a PT detail if this is not a Kit: %s')
                                    % (product.name,))
            if product.standard_price == 0.000000:
                raise UserError(_('You can not add a product with cost 0: %s')
                                % (product.name,))
            if location.type_stock_loc == 'rm' and product_bom and product_bom.warehouse_id.id == bom.warehouse_id.id:
                raise UserError(_('You can not add a MP detail with this product, it is made in this warehouse: %s')
                                % (product.name,))
            if location.type_stock_loc == 'wip' and (not product_bom or product_bom.warehouse_id.id != bom.warehouse_id.id):
                raise UserError(_('You can not add a product without BoM in this location: %s')
                                % (product.name,))

            if product.id == bom.product_id.id:
                raise UserError(_('One product cannot be detail of itself'))
            for line in bom.bom_line_ids:
                if line.product_id.id == product.id:
                    raise UserError(_('This product is already in this Bom'))
        return super(MrpBomLine, self).create(values)

    @api.multi
    def write(self, values):
        # if 'bom_id' in values.keys() and self._uid in (1, 37, 38, 86, 107):
        #     return
        bom_obj = self.env['mrp.bom']
        product_obj = self.env['product.product']
        location_obj = self.env['stock.location']

        if 'product_id' or 'location_id' in values.keys():
            if 'product_id' in values.keys():
                product = product_obj.browse([values['product_id']])
            else:
                product = product_obj.browse([self.product_id.id])

            if 'location_id' in values.keys():
                location = location_obj.browse([values['location_id']])
            else:
                location = location_obj.browse([self.location_id.id])

            if 'bom_id' in values.keys():
                bom = bom_obj.browse([values['bom_id']])
            else:
                bom = bom_obj.browse([self.bom_id.id])

            product_bom = bom_obj.search([
                ('product_id', '=', product.id),
                ('active', '=', True)], limit=1)
            if bom.type == 'phantom':
                # No se pueden agregar productos sin detalle a los Kits
                if not product_bom:
                    raise UserError(_('You can not add a product that \
                        has no BOM: %s') % (product.name,))
            else:
                if location.type_stock_loc == 'fp':
                    raise UserError(_('You can not add a PT detail if this is not a Kit: %s')
                                    % (product.name,))
            if product.standard_price == 0.000000:
                raise UserError(_('You can not add a product with cost 0: %s')
                                % (product.name,))
            if location.type_stock_loc == 'rm' and product_bom and product_bom.warehouse_id.id == bom.warehouse_id.id:
                raise UserError(_('You can not add a MP detail with this product, it is made in this warehouse: %s')
                                % (product.name,))
            if location.type_stock_loc == 'wip' and (not product_bom or product_bom.warehouse_id.id != bom.warehouse_id.id):
                raise UserError(_('You can not add a product without BoM in this location: %s')
                                % (product.name,))

            if product.id == bom.product_id.id:
                raise UserError(_('One product cannot be detail of itself'))

            bom_dynamic = False
            if self._context and self._context.get('bom_dynamic'):
                bom_dynamic = self._context['bom_dynamic']
            for line in bom.bom_line_ids:
                if not bom_dynamic:
                    if line.product_id.id == product.id and line.id != self.id:
                        raise UserError(_('This product is already in this Bom'))

        return super(MrpBomLine, self).write(values)
