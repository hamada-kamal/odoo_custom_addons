{
    'name': "hospital",
    'description': "this is the hospital description",
    'author': "Hamada Kamal",
    'sequence': 1,
    'license': 'LGPL-3',
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '16.0.0.1',
    'depends': ['mail', 'account'],
    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'data/sequence.xml',
        'data/cron.xml',

        'views/menus.xml',
        'views/patient.xml',
        'views/female_patient.xml',
        'views/doctor.xml',
        'views/appointment.xml',
        'views/department.xml',
        'views/inherit_invoice.xml',
        'views/check.xml',

        'wizard/cancel_appointment_wiz.xml',
        'wizard/test_excel_report_wiz.xml',

        'report/patient_appointments_report.xml'
    ],
}
# -*- coding: utf-8 -*-
