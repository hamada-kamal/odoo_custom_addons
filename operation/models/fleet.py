from odoo import fields, models, api


class FleetInherit(models.Model):
    _inherit = 'fleet.vehicle'
    _description = "This is Fleet Inherit Model"

    business_entity = fields.Selection([
        ('vip', 'Vip'),
        ('green taxi', 'Green Taxi'),
        ('limousine', 'Limousine'),
    ])
    status = fields.Selection([
        ('available', 'Available'),
        ('checklist', 'Checklist'),
        ('with driver', 'With Driver'),
        ('damage', 'Damage'),
        ('none', 'None'),
    ], default='none', group_expand='_group_expand_states')
    product_id = fields.Many2one('product.product')
    hall_id = fields.Many2one('operation.hall')
    reason = fields.Text()
    state_time = fields.Datetime(compute='_set_state_time', store=True)
    total_time = fields.Char(compute='_total_time_on_state')
    branch = fields.Many2one('stock.warehouse')

    def _group_expand_states(self, states, domain, order):
        return [key for key, val in type(self).status.selection if key != 'none']

    def open_add_driver_wizard(self):
        return {
            'name': 'Adding driver to vehicle',
            'type': 'ir.actions.act_window',
            'res_model': 'add.driver.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_vehicle_id': self.id,
            },
        }

    def open_receive_vehicle_wizard(self):
        return {
            'name': 'Set Odometer Value \'K.M Out\'',
            'type': 'ir.actions.act_window',
            'res_model': 'receive.vehicle.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_vehicle_id': self.id,
            },
        }

    def open_add_damage_wizard(self):
        return {
            'name': 'Adding damage reason to vehicle',
            'type': 'ir.actions.act_window',
            'res_model': 'add.damage.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_vehicle_id': self.id,
            },
        }

    def open_request_maintenance_wizard(self):
        pass

    def open_return_to_available_wizard(self):
        return {
            'name': 'Return vehicle to available state.',
            'type': 'ir.actions.act_window',
            'res_model': 'return.available.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_vehicle_id': self.id,
            },
        }

    def return_to_available(self):
        self.status = 'available'

    @api.depends('status')
    def _set_state_time(self):
        self.state_time = fields.Datetime.now()

    @api.depends('state_time')
    def _total_time_on_state(self):
        for rec in self:
            if rec.state_time:
                rec.total_time = str(fields.Datetime.now() - rec.state_time)
            else:
                rec.total_time = ""

    @api.constrains('state_id', 'business_entity')
    def _check_vehicle_if_available(self):
        if self.state_id.type == 'Ready To Rent' and self.business_entity in ['vip', 'green taxi']:
            self.status = 'available'
        else:
            self.status = 'none'
