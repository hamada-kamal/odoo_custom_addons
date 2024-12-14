from odoo import fields, models


class AddDriverWizard(models.TransientModel):
    _name = "add.driver.wizard"

    vehicle_id = fields.Many2one('fleet.vehicle')
    vehicle_business_entity = fields.Selection(related='vehicle_id.business_entity')
    driver_id = fields.Many2one('res.partner', domain="[('business_entity','=',vehicle_business_entity)]", required=True)

    def add_driver(self):
        self.vehicle_id.driver_id = self.driver_id.id
        if self.vehicle_id.driver_id:
            self.vehicle_id.status = 'checklist'
            self.vehicle_id.state_time = fields.Datetime.now()


