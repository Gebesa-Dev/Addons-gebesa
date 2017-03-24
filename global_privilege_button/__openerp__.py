# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Global Privilege Button",
    "summary": "Creates a security group that limits the visibility of button",
    "version": "9.0.1.0.0",
    "category": "Uncategorized",
    "website": "https://odoo-community.org/",
    "author": "<Deysy Mascorro, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "product",
        "purchase",
    ],
    "data": [
        "security/security.xml",
        "views/product_template_view.xml",
        "views/purchase_order_view.xml",

    ],
    "demo": [

    ],
    "qweb": [

    ]
}
