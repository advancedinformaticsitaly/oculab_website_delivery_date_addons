# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################

{
    'name' : 'Delivery Date on eCommerce',
    'category': 'Website/Website',
    'version': '12.0.1.0',
    'author': 'Equick ERP',
    'description': """
        * On eCommerce allows you to see that in how many days the product will be delivered based on days configure.
        * On Cart user can see the delivery date of product.
        * Generate delivery order based on the product delivery date.
    """,
    'summary': """product delivery days | product delivery date | delivery schedule date | picking schedule date | delivery schedule at date | Delivery Date Scheduler | order delivery date | Delivery day on eCommerce""",
    'depends' : ['sale_stock', 'website_sale', 'eq_sale_delivery_date','product_pricelist_brand_website_category','theme_clarico'],
    'price': 10,
    'currency': 'EUR',
    'license': 'OPL-1',
    'website': "",
    'data': [
        'views/templates.xml',
        'views/res_config_settings_views.xml',
        'views/product_brand_views.xml',
        'views/website_sale.xml',
    ],
    'demo': [],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: