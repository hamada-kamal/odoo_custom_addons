from odoo import fields, models, api


class Hall(models.Model):
    _name = 'operation.hall'
    _inherit = ['mail.thread']
    _description = "This Is Hall Model"

    name = fields.Char()
    center_id = fields.Many2one('operation.operational.center', string='Name', tracking=True)
    green_taxi_no = fields.Integer(default=0, tracking=True)
    vip_no = fields.Integer(default=0, tracking=True)
    capacity = fields.Integer(compute='_calc_hall_capacity', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
    ], default='draft', tracking=True)
    vehicle_ids = fields.Many2many('fleet.vehicle')

    @api.depends('green_taxi_no', 'vip_no')
    def _calc_hall_capacity(self):
        for hall in self:
            hall.capacity = hall.green_taxi_no + hall.vip_no

    def set_confirm(self):
        self.state = 'confirm'

    def open_send_car_wizard(self):
        return {
            'name': 'Send Vehicles To Hall',
            'type': 'ir.actions.act_window',
            'res_model': 'send.car.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_hall_id': self.id,
            },
        }

    def replace_car(self):
        pass

    def show_orders(self):
        invoices = (self.env['operation.counter']
                    .search([('hall_id', '=', self.id)])
                    .mapped('invoice_id.id'))
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', invoices)],
            'target': 'current',
        }

    def show_vehicles_in_hall(self):
        tree_id = self.env.ref('operation.dashboard_tree').id
        form_id = self.env.ref('operation.dashboard_form').id
        return {
            'name': 'Dashboard',
            'type': 'ir.actions.act_window',
            'res_model': 'fleet.vehicle',
            'view_mode': 'tree,form',
            'views': [(tree_id, 'tree'), (form_id, 'form')],
            'domain': [('hall_id', '=', self.id)],
        }

    def show_dashboard(self):
        tree_id = self.env.ref('operation.dashboard_tree').id
        form_id = self.env.ref('operation.dashboard_form').id
        return {
            'name': 'Dashboard',
            'type': 'ir.actions.act_window',
            'res_model': 'fleet.vehicle',
            'view_mode': 'tree,form',
            'views': [(tree_id, 'tree'), (form_id, 'form')],
        }
