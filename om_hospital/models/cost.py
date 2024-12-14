from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class Cost(models.Model):
    _name = 'cost.cost'
    _rec_name = 'cost_type_id'
    cost_type_id = fields.Many2one('cost.type', string='Cost Type')
    employee_ids = fields.Many2many('hr.employee', string='Employees')
    cost = fields.Integer(string='Cost')
    duration = fields.Integer(string='Duration')
    date_from = fields.Date(string='Date', default=fields.Date.today)
    status = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], default='draft')

    def set_draft(self):
        self.status = 'draft'

    def set_confirm(self):
        self.status = 'confirm'



