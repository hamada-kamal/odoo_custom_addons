{
    'name': 'Customize Hr Module',
    'author': 'Hamada Kamal',
    'depends': ['hr'],
    'data': [

        'security/ir.model.access.csv',

        'data/cron.xml',

        'views/menu.xml',
        'views/employee_inherit.xml',
        'views/cost_type.xml',
        'views/employee_cost.xml',

        # 'report/crm_reports.xml',
        # 'report/customer_contact_info_template.xml',
    ]
}
