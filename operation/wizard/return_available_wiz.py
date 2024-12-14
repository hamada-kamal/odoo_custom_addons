from odoo import fields, models


class ReturnAvailableWizard(models.TransientModel):
    _name = "return.available.wizard"

    vehicle_id = fields.Many2one('fleet.vehicle')
    odometer = fields.Float(String='Last Odometer', required=True)

    def set_odometer_in(self):
        self.vehicle_id.odometer = self.odometer
        self.vehicle_id.status = 'available'
        # self.vehicle_id.state_time = fields.Datetime.now()
        if self.vehicle_id.driver_id:
            self.vehicle_id.driver_id = False

