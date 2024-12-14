from odoo import fields, models


class ReceiveVehicleWizard(models.TransientModel):
    _name = "receive.vehicle.wizard"

    vehicle_id = fields.Many2one('fleet.vehicle')
    odometer = fields.Float(String='Last Odometer', required=True)

    def set_odometer_out(self):
        self.vehicle_id.odometer = self.odometer
        self.vehicle_id.status = 'with driver'
        # self.vehicle_id.state_time = fields.Datetime.now()


