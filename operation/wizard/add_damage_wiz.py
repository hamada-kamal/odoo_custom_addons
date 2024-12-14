from odoo import fields, models


class AddDamageWizard(models.TransientModel):
    _name = "add.damage.wizard"

    vehicle_id = fields.Many2one('fleet.vehicle')
    reason = fields.Text(required=True)

    def add_damage(self):
        self.vehicle_id.reason = self.reason
        self.vehicle_id.status = 'damage'
        # self.vehicle_id.state_time = fields.Datetime.now()
        if self.vehicle_id.driver_id:
            self.vehicle_id.driver_id = False
