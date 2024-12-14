from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalCheck(models.Model):
    _name = "hospital.check"
    _rec_name = 'name'
    _description = "Hospital Doctor desc"

    _sql_constraints = [('model_check_unique_name_constrains', 'UNIQUE(name)', 'The check name already used!')]

    def get_company_id(self):
        return self.env.user.company_id.id

    name = fields.Char(string='Check Name', required=True)
    department_id = fields.Many2one('hospital.department', string="Department", required=True,
                                    domain="[('active','=', True)]")
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor",
                                domain="[('department_id','=', department_id)]")

    company_id = fields.Many2one('res.company', default=get_company_id)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    cost = fields.Monetary(currency_field='currency_id')

    @api.onchange('department_id')
    def onchange_department(self):
        self.doctor_id = False