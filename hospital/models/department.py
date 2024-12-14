from odoo import api, fields, models
from odoo.exceptions import ValidationError
class HospitalDepartment(models.Model):
    _name = "hospital.department"
    _rec_name = 'name'
    _description = "Hospital Department desc"

    def get_company_id(self):
        return self.env.user.company_id.id

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(default=True)

    company_id = fields.Many2one('res.company', default=get_company_id, readonly=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    cost = fields.Monetary(currency_field='currency_id')

    # cost = fields.Float(string="Cost")
