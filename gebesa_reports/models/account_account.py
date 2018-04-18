# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, fields, models


class AccountAccount(models.Model):
    _inherit = 'account.account'

    income_statement = fields.Selection(
        [(1, _(u'Ventas Nacionales')),
         (2, _(u'Ventas Exportacion')),
         (3, _(u'Devoluciones sobre ventas nacionales')),
         (4, _(u'Devoluciones sobre ventas exportacion')),
         (5, _(u'Descuento sobre ventas nacionales')),
         (6, _(u'Descuento sobre ventas exportacion')),
         (7, _(u'Costo de ventas estandar')),
         (8, _(u'Desviacion en consumo de materia')),
         (9, _(u'Desviacion en precio compra de materia')),
         (10, _(u'Flete nacional')),
         (11, _(u'Flete exportacion')),
         (12, _(u'Instalacion')),
         (13, _(u'Mano de obra')),
         (14, _(u'Gastos de fabricacion')),
         (15, _(u'Gastos de ventas')),
         (16, _(u'Gastos de administracion')),
         (17, _(u'Depreciacion')),
         (18, _(u'Intereses Bancarios')),
         (19, _(u'Gastos financieros')),
         (20, _(u'Producto financiero')),
         (21, _(u'Perdida tipo de cambio')),
         (22, _(u'Utilidad cambiaria')),
         (23, _(u'Otros ingresos')),
         (24, _(u'ISR y PTU')),
         (25, _(u'Otras Ventas'))],
        string=_(u"Estado de resultados"),
    )

    trial_balance = fields.Selection(
        [(1, _(u'Caja y Banco')),
         (2, _(u'Inversiones')),
         (3, _(u'Clientes')),
         (4, _(u'Deudores Diversos')),
         (5, _(u'Impuestos a Favor')),
         (6, _(u'Otras Cuentas por Cobrar')),
         (7, _(u'Inventarios')),
         (8, _(u'IVA Acreditar')),
         (9, _(u'Anticipo a Proveedores y Acreedores')),
         (10, _(u'Depositos por Itentificar')),
         (11, _(u'Acciones')),
         (12, _(u'Terrenos')),
         (13, _(u'Edificios')),
         (14, _(u'Maquinaria y Equipo')),
         (15, _(u'Herramientas')),
         (16, _(u'Equipo de Transporte')),
         (17, _(u'Muebles y Enseres')),
         (18, _(u'Equipo de Computo')),
         (19, _(u'Construcciones')),
         (20, _(u'Equipo de Comunicacion')),
         (21, _(u'Equipo de Seguriad')),
         (41, _(u'Supertavit por Actualizacion Activo')
         (22, _(u'Depreciacion')),
         (23, _(u'Deposito de Garantia')),
         (24, _(u'Gastos Diferidos')),
         (25, _(u'Prestamos Bancarios a Corto Plazo')),
         (26, _(u'Proveedores')),
         (27, _(u'Acreedores')),
         (28, _(u'Acreedores de Nomina')),
         (29, _(u'Impuestos a Pagar')),
         (30, _(u'Anticipos de Clientes')),
         (31, _(u'Otros Anticipos de Clientes')),
         (32, _(u'IVA Repercutido')),
         (33, _(u'Pasivo a Largo Plazo')),
         (34, _(u'Prestamos Bancarios a Largo Plazo')),
         (35, _(u'Capital Social')),
         (36, _(u'Reserva Legal')),
         (37, _(u'Resultado de Ejercicios Anteriores')),
         (38, _(u'Supertavit por Actualizacion Capital')),
         (39, _(u'Otras Aportaciones')),
         (40, _(u'Reexpresion de capital por reev. de activos'))],
        string=_(u"Balance General"),
    )
