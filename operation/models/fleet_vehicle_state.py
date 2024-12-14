from odoo import fields, models


class FleetVehicleStateInherit(models.Model):
    _inherit = 'fleet.vehicle.state'
    _description = "This is Fleet Vehicle State Inherit Model"

    type = fields.Char()
