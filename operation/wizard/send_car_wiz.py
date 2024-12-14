from odoo import fields, models
from odoo.exceptions import ValidationError


class SendCarWizard(models.TransientModel):
    _name = "send.car.wizard"

    hall_id = fields.Many2one('operation.hall')
    business_entity = fields.Selection([
        ('vip', 'Vip'),
        ('green taxi', 'Green Taxi'),
    ], default='vip', required=True)
    vehicle_ids = fields.Many2many('fleet.vehicle', domain="["
                                                          "('business_entity','=',business_entity),"
                                                          "('status','=','with driver')"
                                                          "]", required=True)

    # Assign Cars to Hall
    def send_car(self):
        vehicle_vip_count = len(self.vehicle_ids.filtered(lambda v: v.business_entity == 'vip'))
        vehicle_green_taxi_count = len(self.vehicle_ids.filtered(lambda v: v.business_entity == 'green taxi'))
        if len(self.vehicle_ids) > self.hall_id.capacity:
            raise ValidationError(f"The Hall's capacity is {self.hall_id.capacity} vehicle(s), but the selected vehicles exceed this capacity")
        if vehicle_vip_count > self.hall_id.vip_no:
            raise ValidationError(f"The VIP vehicles capacity  in this Hall {self.hall_id.vip_no} vehicle(s)")
        if vehicle_green_taxi_count > self.hall_id.green_taxi_no:
            raise ValidationError(f"The Green Taxi capacity in this Hall {self.hall_id.green_taxi_no} vehicle(s)")
        self.hall_id.vehicle_ids = self.vehicle_ids
        for vehicle in self.hall_id.vehicle_ids:
            vehicle.hall_id = self.hall_id

