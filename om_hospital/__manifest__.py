{
    'name': 'hospital Management System',
    'author': 'Kimo Kamal',
    'depends': ['mail','sale'],

    'assets': {
        'web.assets_backend': [
            'om_hospital/static/src/js/script.js',
        ],
    },

    'data': [

        'security/security.xml',
        'security/ir.model.access.csv',

        'data/sequence.xml',
        'data/cron.xml',

        'wizard/get_doctor.xml',
        'wizard/create_appointment.xml',

        # 'views/assets.xml',
        'views/menu.xml',
        'views/patient.xml',
        'views/appointment.xml',
        'views/doctor.xml',
        'views/sale_order.xml',
        'views/invoice_lines.xml',
        'views/employee_inherit.xml',
        'views/cost_type.xml',
        'views/employee_cost.xml',
        'views/cost.xml',
        'views/crm_inherit.xml',
        'views/purchase_inherit.xml',


        'reports/hospital_reports.xml',
        'reports/patient_card_template.xml',
        'reports/sale_order_reports_inherit.xml',
        'reports/doctor_patients_template.xml',


    ],


}
