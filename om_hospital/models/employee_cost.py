from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class EmployeeCost(models.Model):
    _name = 'employee.cost'
    _rec_name = 'cost_type_id'

    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    cost_type_id = fields.Many2one('cost.type', string='Cost Type')
    cost = fields.Integer(string='Cost')
    date_from = fields.Date(string='Date', default=fields.Date.today)




