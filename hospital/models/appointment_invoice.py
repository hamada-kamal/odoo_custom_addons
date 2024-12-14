from odoo import api,fields,models


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    def _get_company_id(self):
        return self.env.user.company_id.id

    appointment_id = fields.Many2one('hospital.appointment',string="Appointment")
    patient_id = fields.Many2one('hospital.patient', string="Patient")
    department_id = fields.Many2one('hospital.department', string="Department")
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    state = fields.Selection([('cancel', 'Cancelled'), ('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done')], default='draft',
                             string="State")
    note = fields.Text(string='Note')
    company_id = fields.Many2one('res.company', default=_get_company_id)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    cost = fields.Monetary(string="Total Cost", currency_field='currency_id', related='department_id.cost')