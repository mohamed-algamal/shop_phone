# -*- coding: utf-8 -*-
{
    'name': "shop phone management",
    'summary': "this is for shop phone management",
    'description': """
        this is shop phone for sale phone and all thing about phones
    """,
    'author': "Mohamed Algamal",
    'category': 'shop',
    'version': '1.0.0',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/menu_views.xml',
        'views/accessories_view.xml',
        'views/internal_view.xml',
        'views/electricity_view.xml',
        'views/mobiles.xml',
        'views/petrine_work.xml',
        'views/sales_view.xml',
        'views/maintenance.xml',
        'report/report.xml',
        'report/sales_cord_template_pdf.xml',
    ],
    'demo': [],
    'excludes': [''],
    'sequence': -100,
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
