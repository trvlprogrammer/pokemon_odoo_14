# -*- coding: utf-8 -*-
{
    'name': "Pokemon",

    'summary': """
        Pokemon""",

    'description': """
        Pokemon
    """,

    'author': "Alfatih Ridho NT",
    'website': "alfatihridhont@gmail.com",
    'category': 'Pokemon',
    'version': '14.0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'security/access_rule.xml',
        'views/pokemon.xml',
        'data/schedulers.xml',
        'wizard/wizard.xml',
    ],
    'qweb': [
        
    ],
}
