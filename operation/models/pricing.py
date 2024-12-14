from odoo import fields, models, api


class Pricing(models.Model):
    _name = 'operation.pricing'
    _description = "This Is Pricing Model"

    name = fields.Char(tracking=True, required=True)
    operational_center_id = fields.Many2one('operation.operational.center', required=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
    ], default='draft', tracking=True)
    business_entity = fields.Selection([
        ('vip', 'Vip'),
        ('green taxi', 'Green Taxi'),
        ('limousine', 'Limousine'),
    ])
    start_date = fields.Date(default=fields.Date.today, required=True)
    end_date = fields.Date(default=fields.Date.today, required=True)
    branch_ids = fields.Many2many('stock.warehouse', string='Branches')
    trip_ids = fields.One2many('operation.trip', 'pricing_id', string='Trips')

    def set_draft(self):
        self.state = 'draft'

    def set_confirm(self):
        self.state = 'confirm'

