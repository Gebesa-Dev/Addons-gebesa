# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Sale Order Product Family",
    "summary": "Sale Order Product Family",
    "version": "9.0.1.0.0",
    "category": "Sale",
    "website": "https://odoo-community.org/",
    "author": "<Armando Robledo>, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base", "sale",
        "product_structure_gebesa",
    ],
    "data": [
        "views/sale_order_view.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
