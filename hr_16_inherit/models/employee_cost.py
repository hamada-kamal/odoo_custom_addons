from odoo import api, fields, models
# from odoo.exceptions import ValidationError

class EmployeeCost(models.Model):
    _name = 'employee.cost'
    _rec_name = 'cost_type_id'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    cost_type_id = fields.Many2one('cost.type', string='Cost Type')
    cost = fields.Integer(string='Cost')
    date_from = fields.Date(string='Date', default=fields.Date.today)




